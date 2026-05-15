// IS1 dashboard build dispatcher.
//
// Cloudflare Workers Cron Triggers fire this Worker on the schedules defined
// in wrangler.toml. The Worker POSTs to GitHub's workflow_dispatch API to
// trigger the corresponding workflow. This bypasses GitHub Actions'
// `schedule:` event, which is documented as best-effort and has been
// observed dropping or delaying runs multi-hour on this repo.
//
// The original GHA `schedule:` blocks in both workflows are kept as a
// redundant backup — concurrency:group=daily in both YAMLs prevents
// double-runs.
//
// Required secrets (set via `wrangler secret put`):
//   GITHUB_TOKEN              fine-grained PAT with Actions:write on this repo
//
// Optional secrets:
//   HEALTHCHECK_URL_DAILY      healthchecks.io URL for the 09:50 BKK fire
//   HEALTHCHECK_URL_DISCLOSURE healthchecks.io URL for the 14:00 + 18:00 BKK fires
//   MANUAL_TRIGGER_TOKEN       random string; required to use the POST endpoint

const MAX_ATTEMPTS = 3;
const BACKOFF_MS = [0, 2000, 6000];

// Maps each cron expression in wrangler.toml [triggers] to the workflow
// filename it should dispatch. Adding a new cron means adding both an entry
// here and the corresponding line in wrangler.toml.
const CRON_TO_WORKFLOW = {
  "15 2 * * 1-5": "daily.yml",              // 09:15 BKK — full pipeline
  "0 7 * * 1-5":  "disclosure-refresh.yml", // 14:00 BKK — afternoon catch-up
  "0 11 * * 1-5": "disclosure-refresh.yml", // 18:00 BKK — end-of-day sweep
};

// Maps each workflow to its healthcheck URL secret name. Lets daily.yml and
// disclosure-refresh.yml report to separate healthchecks.io checks so a
// missed daily fire emails immediately and isn't drowned by disclosure noise.
const WORKFLOW_HEALTHCHECK = {
  "daily.yml":              "HEALTHCHECK_URL_DAILY",
  "disclosure-refresh.yml": "HEALTHCHECK_URL_DISCLOSURE",
};

async function dispatchWorkflow(env, workflowFile) {
  const url = `https://api.github.com/repos/${env.GITHUB_OWNER}/${env.GITHUB_REPO}/actions/workflows/${workflowFile}/dispatches`;
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Accept": "application/vnd.github+json",
      "Authorization": `Bearer ${env.GITHUB_TOKEN}`,
      "X-GitHub-Api-Version": "2022-11-28",
      "User-Agent": "is1-coverage-dispatcher",
    },
    body: JSON.stringify({ ref: env.GITHUB_REF ?? "main" }),
  });

  if (response.status !== 204) {
    const body = await response.text();
    throw new Error(`GitHub API ${response.status}: ${body.slice(0, 300)}`);
  }
}

async function pingHealthcheck(url, suffix = "") {
  if (!url) return;
  try {
    await fetch(`${url}${suffix}`, { method: "GET" });
  } catch (e) {
    console.warn(`Healthcheck ping (${suffix || "ok"}) failed: ${e.message}`);
  }
}

export default {
  async scheduled(event, env, ctx) {
    const workflow = CRON_TO_WORKFLOW[event.cron];
    if (!workflow) {
      throw new Error(`No workflow mapped for cron "${event.cron}". Update CRON_TO_WORKFLOW in worker.js.`);
    }
    const healthcheckUrl = env[WORKFLOW_HEALTHCHECK[workflow]];
    let lastError = null;

    for (let attempt = 1; attempt <= MAX_ATTEMPTS; attempt++) {
      try {
        if (BACKOFF_MS[attempt - 1] > 0) {
          await new Promise((r) => setTimeout(r, BACKOFF_MS[attempt - 1]));
        }
        await dispatchWorkflow(env, workflow);
        console.log(`Dispatch succeeded on attempt ${attempt}: cron="${event.cron}" → ${workflow}`);
        ctx.waitUntil(pingHealthcheck(healthcheckUrl));
        return;
      } catch (error) {
        lastError = error;
        console.error(`Attempt ${attempt}/${MAX_ATTEMPTS} for ${workflow} failed: ${error.message}`);
      }
    }

    ctx.waitUntil(pingHealthcheck(healthcheckUrl, "/fail"));
    throw lastError;
  },

  // Manual smoke-test endpoint. POST with `?workflow=<file>` to force a
  // dispatch without waiting for cron. Defaults to daily.yml.
  //   POST /                            → daily.yml
  //   POST /?workflow=disclosure-refresh.yml → disclosure-refresh.yml
  async fetch(request, env, ctx) {
    if (request.method !== "POST") {
      return new Response("POST to dispatch. Optional ?workflow=<filename>.", { status: 405 });
    }
    const auth = request.headers.get("authorization");
    if (auth !== `Bearer ${env.MANUAL_TRIGGER_TOKEN}`) {
      return new Response("unauthorized", { status: 401 });
    }
    const url = new URL(request.url);
    const workflow = url.searchParams.get("workflow") ?? "daily.yml";
    if (!WORKFLOW_HEALTHCHECK[workflow]) {
      return new Response(`unknown workflow: ${workflow}`, { status: 400 });
    }
    try {
      await dispatchWorkflow(env, workflow);
      return new Response(null, { status: 204 });
    } catch (e) {
      return new Response(e.message, { status: 502 });
    }
  },
};
