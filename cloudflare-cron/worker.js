// IS1 dashboard daily-build dispatcher.
//
// Cloudflare Workers Cron Trigger fires this Worker on the schedule defined
// in wrangler.toml. The Worker POSTs to GitHub's workflow_dispatch API to
// trigger .github/workflows/daily.yml, which runs the existing surveillance +
// build pipeline. This bypasses GitHub Actions' unreliable `schedule:` event
// (observed dropping or delaying runs by hours on this repo).
//
// The original GHA `schedule:` cron is intentionally kept in daily.yml as a
// redundant backup — concurrency:group=daily prevents double-runs.
//
// Required secrets (set via `wrangler secret put`):
//   GITHUB_TOKEN       fine-grained PAT with Actions:write on this repo
//
// Optional secrets:
//   HEALTHCHECK_URL    healthchecks.io check URL (no trailing slash). The
//                      Worker hits <url> on success and <url>/fail on
//                      exhausted retries, so a missed daily dispatch
//                      surfaces as an email from healthchecks.io.

const MAX_ATTEMPTS = 3;
const BACKOFF_MS = [0, 2000, 6000];

async function dispatchWorkflow(env) {
  const url = `https://api.github.com/repos/${env.GITHUB_OWNER}/${env.GITHUB_REPO}/actions/workflows/${env.GITHUB_WORKFLOW}/dispatches`;
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
    let lastError = null;

    for (let attempt = 1; attempt <= MAX_ATTEMPTS; attempt++) {
      try {
        if (BACKOFF_MS[attempt - 1] > 0) {
          await new Promise((r) => setTimeout(r, BACKOFF_MS[attempt - 1]));
        }
        await dispatchWorkflow(env);
        console.log(`Dispatch succeeded on attempt ${attempt} for cron ${event.cron}`);
        ctx.waitUntil(pingHealthcheck(env.HEALTHCHECK_URL));
        return;
      } catch (error) {
        lastError = error;
        console.error(`Attempt ${attempt}/${MAX_ATTEMPTS} failed: ${error.message}`);
      }
    }

    ctx.waitUntil(pingHealthcheck(env.HEALTHCHECK_URL, "/fail"));
    throw lastError;
  },

  // Manual smoke-test endpoint. Hit https://<worker>.workers.dev/ to force a
  // dispatch without waiting for the cron. Returns 204 on success.
  async fetch(request, env, ctx) {
    if (request.method !== "POST") {
      return new Response("POST to dispatch", { status: 405 });
    }
    const auth = request.headers.get("authorization");
    if (auth !== `Bearer ${env.MANUAL_TRIGGER_TOKEN}`) {
      return new Response("unauthorized", { status: 401 });
    }
    try {
      await dispatchWorkflow(env);
      return new Response(null, { status: 204 });
    } catch (e) {
      return new Response(e.message, { status: 502 });
    }
  },
};
