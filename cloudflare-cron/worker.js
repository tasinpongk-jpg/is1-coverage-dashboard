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
// The account is on the Workers Free plan (5 cron triggers total).
// whoop-health-desk holds 2, so this worker keeps the 3 weekday crons in
// wrangler.toml. The four filing-deadline prompts (16 Aug, 16 Nov, 1 Mar,
// 16 May, formerly their own 02:30 UTC crons) are folded into the 02:15 UTC
// Monday-Friday run below.
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
const BANGKOK_TZ = "Asia/Bangkok";

// Cloudflare weekdays run 1=Sunday .. 7=Saturday, so 1-5 is Sunday-Thursday
// and skips Friday. Names and the numeric form 2-6 are the same Monday-Friday
// range. event.cron is matched after folding those names to numbers, so a
// MON-FRI expression and a 2-6 expression hit the same entry.
const DAY_NUM = { SUN: "1", MON: "2", TUE: "3", WED: "4", THU: "5", FRI: "6", SAT: "7" };

// Canonical form of the 02:15 UTC / 09:15 Bangkok Monday-Friday trigger.
const MORNING_CRON = "15 2 * * 2-6";

export function canonicalCron(expr) {
  const parts = String(expr || "").trim().toUpperCase().split(/\s+/);
  if (parts.length !== 5) return parts.join(" ");
  parts[4] = parts[4].replace(/[A-Z]{3}/g, (name) => DAY_NUM[name] || name);
  return parts.join(" ");
}

// Maps each cron expression in wrangler.toml [triggers] to the workflow
// filename it should dispatch. Keys are canonical (weekday names folded).
// Adding a new cron means adding both an entry here and the corresponding
// line in wrangler.toml, and only when the account still has a free cron slot.
const CRON_TO_WORKFLOW = {
  "15 2 * * 2-6": "daily.yml",              // 09:15 BKK Mon-Fri — full pipeline
  "0 7 * * 2-6":  "disclosure-refresh.yml", // 14:00 BKK Mon-Fri — afternoon catch-up
  "0 11 * * 2-6": "disclosure-refresh.yml", // 18:00 BKK Mon-Fri — end-of-day sweep
};

// One-shot filing-deadline prompts. These used to be annual crons at 02:30 UTC
// (09:30 Bangkok) with day-of-week *. The active date is the UTC calendar day
// that cron fired, which is the same civil date in Asia/Bangkok at 02:15 UTC
// (09:15 Bangkok). Inputs match the old workflow_dispatch payloads.
export const FILING_PROMPTS = [
  {
    workflow: "quarterly-filing-refresh.yml",
    inputs: { filing_period: "2026Q2_H1", filing_deadline: "2026-08-16" },
    activeDate: "2026-08-16",
  },
  {
    workflow: "quarterly-filing-refresh.yml",
    inputs: { filing_period: "2026Q3", filing_deadline: "2026-11-16" },
    activeDate: "2026-11-16",
  },
  {
    workflow: "quarterly-filing-refresh.yml",
    inputs: { filing_period: "2026FY_DEC", filing_deadline: "2027-03-01" },
    activeDate: "2027-03-01",
  },
  {
    workflow: "quarterly-filing-refresh.yml",
    inputs: { filing_period: "2027Q1", filing_deadline: "2027-05-16" },
    activeDate: "2027-05-16",
  },
];

// Maps each workflow to its healthcheck URL secret name. Lets daily.yml and
// disclosure-refresh.yml report to separate healthchecks.io checks so a
// missed daily fire emails immediately and isn't drowned by disclosure noise.
const WORKFLOW_HEALTHCHECK = {
  "daily.yml":              "HEALTHCHECK_URL_DAILY",
  "disclosure-refresh.yml": "HEALTHCHECK_URL_DISCLOSURE",
  "quarterly-filing-refresh.yml": null,
};

function datePart(parts, type) {
  const found = parts.find((part) => part.type === type);
  if (!found) throw new Error(`missing ${type} in Asia/Bangkok date`);
  return found.value;
}

// Civil date of a cron instant in Asia/Bangkok, taken from scheduledTime
// rather than the wall clock. 02:15 UTC and the old 02:30 UTC fire share
// this date: both are still the same UTC day, and Bangkok is UTC+7.
export function bangkokCivilDate(scheduledTime) {
  const instant = new Date(scheduledTime);
  if (Number.isNaN(instant.getTime())) {
    throw new Error("scheduledTime is not a valid timestamp");
  }
  const parts = new Intl.DateTimeFormat("en-US", {
    timeZone: BANGKOK_TZ,
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  }).formatToParts(instant);
  const year = datePart(parts, "year");
  const month = datePart(parts, "month");
  const day = datePart(parts, "day");
  const ymd = `${year}-${month}-${day}`;
  // Weekday of that civil date. 0 = Sunday ... 6 = Saturday.
  const weekday = new Date(Date.UTC(Number(year), Number(month) - 1, Number(day))).getUTCDay();
  return { ymd, weekday };
}

function addCivilDays(ymd, days) {
  const [year, month, day] = ymd.split("-").map(Number);
  const utc = new Date(Date.UTC(year, month - 1, day));
  utc.setUTCDate(utc.getUTCDate() + days);
  const y = utc.getUTCFullYear();
  const m = String(utc.getUTCMonth() + 1).padStart(2, "0");
  const d = String(utc.getUTCDate()).padStart(2, "0");
  return `${y}-${m}-${d}`;
}

function dispatchIdentity(job) {
  if (!job.inputs) return job.workflow;
  const keys = Object.keys(job.inputs).sort();
  return `${job.workflow}\n${JSON.stringify(keys.map((key) => [key, job.inputs[key]]))}`;
}

export function dedupeDispatches(jobs) {
  const seen = new Set();
  const unique = [];
  for (const job of jobs) {
    const identity = dispatchIdentity(job);
    if (seen.has(identity)) continue;
    seen.add(identity);
    unique.push({ workflow: job.workflow, ...(job.inputs ? { inputs: job.inputs } : {}) });
  }
  return unique;
}

// Prompts whose active date is the Bangkok civil date of this run.
// The 02:15 cron is MON-FRI, so it does not fire on Saturday or Sunday.
// A filing date on Saturday or Sunday is dispatched on the next Monday,
// the first 02:15 run after that date. A Monday that is itself a filing
// date is included once, not also as a weekend catch-up. A Saturday and
// Sunday pair that resolves to the same workflow inputs is included once;
// distinct prompts are each included once.
export function filingPromptsDue(scheduledTime, prompts = FILING_PROMPTS) {
  const { ymd, weekday } = bangkokCivilDate(scheduledTime);
  const dates = new Set([ymd]);
  if (weekday === 1) {
    dates.add(addCivilDays(ymd, -1));
    dates.add(addCivilDays(ymd, -2));
  }
  const jobs = [];
  for (const prompt of prompts) {
    if (!dates.has(prompt.activeDate)) continue;
    jobs.push({ workflow: prompt.workflow, inputs: prompt.inputs });
  }
  return dedupeDispatches(jobs);
}

// Workflows for one cron fire. The morning run always includes daily.yml
// and, on a due filing date, the filing prompt. The set is deduped so each
// workflow-plus-inputs pair is dispatched once per run. 07:00 and 11:00
// stay a single disclosure-refresh dispatch.
export function dispatchesForCron(expr, scheduledTime, prompts = FILING_PROMPTS) {
  const canonical = canonicalCron(expr);
  const workflow = CRON_TO_WORKFLOW[canonical];
  if (!workflow) return null;
  const jobs = [{ workflow }];
  if (canonical === MORNING_CRON && scheduledTime != null) {
    jobs.push(...filingPromptsDue(scheduledTime, prompts));
  }
  return dedupeDispatches(jobs);
}

export function workflowForCron(expr) {
  return CRON_TO_WORKFLOW[canonicalCron(expr)];
}

async function dispatchWorkflow(env, workflowFile, inputs = undefined) {
  const url = `https://api.github.com/repos/${env.GITHUB_OWNER}/${env.GITHUB_REPO}/actions/workflows/${workflowFile}/dispatches`;
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Accept": "application/vnd.github+json",
      "Authorization": `Bearer ${env.GITHUB_TOKEN}`,
      "X-GitHub-Api-Version": "2022-11-28",
      "User-Agent": "is1-coverage-dispatcher",
    },
    body: JSON.stringify({ ref: env.GITHUB_REF ?? "main", ...(inputs ? { inputs } : {}) }),
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

async function dispatchOne(env, ctx, event, job) {
  const healthcheckName = WORKFLOW_HEALTHCHECK[job.workflow];
  const healthcheckUrl = healthcheckName ? env[healthcheckName] : undefined;
  let lastError = null;

  for (let attempt = 1; attempt <= MAX_ATTEMPTS; attempt++) {
    try {
      if (BACKOFF_MS[attempt - 1] > 0) {
        await new Promise((r) => setTimeout(r, BACKOFF_MS[attempt - 1]));
      }
      await dispatchWorkflow(env, job.workflow, job.inputs);
      console.log(`Dispatch succeeded on attempt ${attempt}: cron="${event.cron}" → ${job.workflow}`);
      ctx.waitUntil(pingHealthcheck(healthcheckUrl));
      return;
    } catch (error) {
      lastError = error;
      console.error(`Attempt ${attempt}/${MAX_ATTEMPTS} for ${job.workflow} failed: ${error.message}`);
    }
  }

  ctx.waitUntil(pingHealthcheck(healthcheckUrl, "/fail"));
  throw lastError;
}

export default {
  async scheduled(event, env, ctx) {
    const jobs = dispatchesForCron(event.cron, event.scheduledTime);
    if (!jobs) {
      throw new Error(`No workflow mapped for cron "${event.cron}". Update CRON_TO_WORKFLOW in worker.js.`);
    }
    const errors = [];
    for (const job of jobs) {
      try {
        await dispatchOne(env, ctx, event, job);
      } catch (error) {
        errors.push(error);
      }
    }
    if (errors.length === 1) throw errors[0];
    if (errors.length > 1) {
      throw new Error(errors.map((error) => error.message).join("; "));
    }
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
    if (!(workflow in WORKFLOW_HEALTHCHECK)) {
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
