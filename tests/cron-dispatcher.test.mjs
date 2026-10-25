import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";

import worker, {
  bangkokCivilDate,
  canonicalCron,
  dispatchesForCron,
  FILING_PROMPTS,
  filingPromptsDue,
  workflowForCron,
} from "../cloudflare-cron/worker.js";

test("Cloudflare weekday names and 2-6 both mean Monday-Friday", () => {
  assert.equal(canonicalCron("15 2 * * MON-FRI"), "15 2 * * 2-6");
  assert.equal(canonicalCron("15 2 * * mon-fri"), "15 2 * * 2-6");
  assert.equal(canonicalCron("15 2 * * 2-6"), "15 2 * * 2-6");
  assert.equal(workflowForCron("15 2 * * MON-FRI"), "daily.yml");
  assert.equal(workflowForCron("15 2 * * 2-6"), "daily.yml");
  assert.equal(workflowForCron("0 7 * * MON-FRI"), "disclosure-refresh.yml");
  assert.equal(workflowForCron("0 11 * * 2-6"), "disclosure-refresh.yml");
});

test("1-5 is Sunday-Thursday on Cloudflare and is not a weekday dispatch", () => {
  assert.equal(canonicalCron("15 2 * * 1-5"), "15 2 * * 1-5");
  assert.equal(workflowForCron("15 2 * * 1-5"), undefined);
  assert.equal(dispatchesForCron("15 2 * * 1-5", Date.parse("2026-11-13T02:15:00.000Z")), null);
});

function cronsFromToml(text) {
  const triggers = text.split(/^\[triggers\]/m)[1]?.split(/^\[/m)[0] ?? "";
  const array = triggers.match(/crons\s*=\s*\[([\s\S]*?)\]/);
  assert.ok(array, "wrangler.toml [triggers] has a crons array");
  return [...array[1].matchAll(/"([^"]+)"/g)].map((match) => match[1]);
}

test("wrangler.toml keeps exactly three MON-FRI crons and never a bare 1-5 range", () => {
  const text = readFileSync(new URL("../cloudflare-cron/wrangler.toml", import.meta.url), "utf8");
  const crons = cronsFromToml(text);
  assert.deepEqual(crons, [
    "15 2 * * MON-FRI",
    "0 7 * * MON-FRI",
    "0 11 * * MON-FRI",
  ]);
  assert.equal(crons.length, 3);
  for (const cron of crons) {
    const day = cron.split(/\s+/)[4];
    assert.equal(day, "MON-FRI");
    assert.notEqual(day, "1-5");
    assert.equal(canonicalCron(cron).split(/\s+/)[4], "2-6");
    assert.equal(canonicalCron(cron).endsWith("6"), true);
    assert.notEqual(workflowForCron(cron), undefined);
  }
});

// Weekday of a civil date in Asia/Bangkok. Probe at 12:00 Bangkok (05:00 UTC)
// so the result is the Gregorian weekday of that date, computed here rather
// than copied from a list.
function weekdayName(iso) {
  const [year, month, day] = iso.split("-").map(Number);
  const noonBangkok = new Date(Date.UTC(year, month - 1, day, 5, 0, 0));
  return new Intl.DateTimeFormat("en-US", {
    timeZone: "Asia/Bangkok",
    weekday: "long",
  }).format(noonBangkok);
}

test("filing-date weekdays come from the calendar, not a hardcoded list", () => {
  assert.equal(weekdayName("2026-11-16"), "Monday");
  assert.equal(weekdayName("2027-05-16"), "Sunday");
  assert.equal(weekdayName("2026-03-01"), "Sunday");
  assert.equal(weekdayName("2026-08-16"), "Sunday");
  assert.equal(weekdayName("2027-03-01"), "Monday");
  assert.equal(weekdayName("2026-05-16"), "Saturday");
  assert.equal(weekdayName("2026-08-17"), "Monday");
  assert.equal(weekdayName("2027-05-17"), "Monday");
  assert.equal(weekdayName("2026-05-18"), "Monday");
  assert.equal(weekdayName("2026-11-13"), "Friday");
  assert.equal(weekdayName("2026-08-19"), "Wednesday");
});

test("02:15 UTC and the old 02:30 UTC fire share one Bangkok civil date", () => {
  for (const day of ["2026-08-16", "2026-11-16", "2027-03-01", "2027-05-16"]) {
    const at0215 = Date.parse(`${day}T02:15:00.000Z`);
    const at0230 = Date.parse(`${day}T02:30:00.000Z`);
    const morning = bangkokCivilDate(at0215);
    const oldFire = bangkokCivilDate(at0230);
    assert.equal(morning.ymd, day);
    assert.equal(oldFire.ymd, day);
    assert.equal(morning.ymd, new Date(at0215).toISOString().slice(0, 10));
    assert.equal(morning.weekday, oldFire.weekday);
  }
});

function promptJobs(scheduledTime, prompts = FILING_PROMPTS) {
  return filingPromptsDue(scheduledTime, prompts).map((job) => job.inputs.filing_period);
}

test("each active filing date dispatches once on its weekday or the next Monday", () => {
  assert.deepEqual(
    FILING_PROMPTS.map((prompt) => prompt.activeDate),
    ["2026-08-16", "2026-11-16", "2027-03-01", "2027-05-16"],
  );

  // 16 Aug 2026 is Sunday: the Monday 02:15 run carries 2026Q2_H1 once.
  assert.deepEqual(promptJobs(Date.parse("2026-08-16T02:30:00.000Z")), ["2026Q2_H1"]);
  assert.deepEqual(promptJobs(Date.parse("2026-08-17T02:15:00.000Z")), ["2026Q2_H1"]);
  assert.deepEqual(promptJobs(Date.parse("2026-08-18T02:15:00.000Z")), []);

  // 16 Nov 2026 is a Monday that is itself a filing date: once, that morning.
  assert.deepEqual(promptJobs(Date.parse("2026-11-16T02:15:00.000Z")), ["2026Q3"]);
  assert.deepEqual(promptJobs(Date.parse("2026-11-17T02:15:00.000Z")), []);

  // 1 Mar 2027 is a Monday and the stored deadline. 1 Mar 2026 is a Sunday
  // and is not an active date, so the following Monday does not catch it up.
  assert.deepEqual(promptJobs(Date.parse("2027-03-01T02:15:00.000Z")), ["2026FY_DEC"]);
  assert.deepEqual(promptJobs(Date.parse("2027-03-02T02:15:00.000Z")), []);
  assert.deepEqual(promptJobs(Date.parse("2026-03-01T02:30:00.000Z")), []);
  assert.deepEqual(promptJobs(Date.parse("2026-03-02T02:15:00.000Z")), []);

  // 16 May 2027 is Sunday: the Monday 02:15 run carries 2027Q1 once.
  assert.deepEqual(promptJobs(Date.parse("2027-05-16T02:30:00.000Z")), ["2027Q1"]);
  assert.deepEqual(promptJobs(Date.parse("2027-05-17T02:15:00.000Z")), ["2027Q1"]);
  assert.deepEqual(promptJobs(Date.parse("2027-05-18T02:15:00.000Z")), []);
});

function filingPrompt(activeDate, period) {
  return {
    workflow: "quarterly-filing-refresh.yml",
    inputs: { filing_period: period, filing_deadline: activeDate },
    activeDate,
  };
}

test("Saturday filing date is caught up on the next Monday, once", () => {
  assert.equal(weekdayName("2026-05-16"), "Saturday");
  const prompts = [filingPrompt("2026-05-16", "SAT")];
  assert.deepEqual(promptJobs(Date.parse("2026-05-16T02:15:00.000Z"), prompts), ["SAT"]);
  assert.deepEqual(promptJobs(Date.parse("2026-05-18T02:15:00.000Z"), prompts), ["SAT"]);
  assert.deepEqual(promptJobs(Date.parse("2026-05-19T02:15:00.000Z"), prompts), []);
  const monday = dispatchesForCron("15 2 * * MON-FRI", Date.parse("2026-05-18T02:15:00.000Z"), prompts);
  assert.deepEqual(monday.map((job) => job.workflow), ["daily.yml", "quarterly-filing-refresh.yml"]);
});

test("a midweek filing date dispatches that morning and is not caught up later", () => {
  assert.equal(weekdayName("2026-08-19"), "Wednesday");
  assert.equal(weekdayName("2026-11-13"), "Friday");
  const prompts = [
    filingPrompt("2026-08-19", "WED"),
    filingPrompt("2026-11-13", "FRI"),
  ];
  assert.deepEqual(promptJobs(Date.parse("2026-08-19T02:15:00.000Z"), prompts), ["WED"]);
  assert.deepEqual(promptJobs(Date.parse("2026-08-24T02:15:00.000Z"), prompts), []);
  assert.deepEqual(promptJobs(Date.parse("2026-11-13T02:15:00.000Z"), prompts), ["FRI"]);
  assert.deepEqual(promptJobs(Date.parse("2026-11-16T02:15:00.000Z"), prompts), []);
});

test("Monday filing date and a Saturday-Sunday pair are deduped per run", () => {
  const mondayPrompt = filingPrompt("2026-11-16", "2026Q3");
  const duplicatedMonday = dispatchesForCron(
    "15 2 * * MON-FRI",
    Date.parse("2026-11-16T02:15:00.000Z"),
    [mondayPrompt, { ...mondayPrompt, inputs: { ...mondayPrompt.inputs } }],
  );
  assert.equal(duplicatedMonday.length, 2);
  assert.equal(duplicatedMonday.filter((job) => job.workflow === "daily.yml").length, 1);
  assert.equal(duplicatedMonday.filter((job) => job.inputs?.filing_period === "2026Q3").length, 1);

  // Same inputs on Saturday and Sunday: one prompt, plus daily.yml.
  const shared = {
    workflow: "quarterly-filing-refresh.yml",
    inputs: { filing_period: "PAIR", filing_deadline: "2026-08-16" },
  };
  const pair = dispatchesForCron("15 2 * * 2-6", Date.parse("2026-08-17T02:15:00.000Z"), [
    { ...shared, activeDate: "2026-08-15" },
    { ...shared, activeDate: "2026-08-16" },
  ]);
  assert.deepEqual(pair.map((job) => job.workflow), ["daily.yml", "quarterly-filing-refresh.yml"]);
  assert.equal(pair.filter((job) => job.inputs?.filing_period === "PAIR").length, 1);

  // Distinct Saturday and Sunday prompts each go out once.
  const distinct = dispatchesForCron("15 2 * * MON-FRI", Date.parse("2026-08-17T02:15:00.000Z"), [
    filingPrompt("2026-08-15", "SAT"),
    filingPrompt("2026-08-16", "SUN"),
  ]);
  assert.deepEqual(
    distinct.map((job) => job.inputs?.filing_period ?? job.workflow),
    ["daily.yml", "SAT", "SUN"],
  );
});

test("07:00 and 11:00 stay disclosure-only on a filing morning", () => {
  const when = Date.parse("2026-11-16T02:15:00.000Z");
  for (const [cron, clock] of [
    ["0 7 * * MON-FRI", "2026-11-16T07:00:00.000Z"],
    ["0 11 * * MON-FRI", "2026-11-16T11:00:00.000Z"],
  ]) {
    const jobs = dispatchesForCron(cron, Date.parse(clock));
    assert.deepEqual(jobs, [{ workflow: "disclosure-refresh.yml" }]);
  }
  const morning = dispatchesForCron("15 2 * * MON-FRI", when);
  assert.equal(morning.length, 2);
  assert.equal(morning[0].workflow, "daily.yml");
  assert.equal(morning[0].inputs, undefined);
  assert.deepEqual(morning[1].inputs, { filing_period: "2026Q3", filing_deadline: "2026-11-16" });
});

async function runScheduled(event) {
  const calls = [];
  const previous = globalThis.fetch;
  globalThis.fetch = async (url, opts) => {
    calls.push({
      url: String(url),
      body: opts?.body ? JSON.parse(opts.body) : null,
    });
    const status = String(url).includes("api.github.com") ? 204 : 200;
    return new Response(null, { status });
  };
  const env = {
    GITHUB_TOKEN: "token",
    GITHUB_OWNER: "tasinpongk-jpg",
    GITHUB_REPO: "is1-coverage-dashboard",
    GITHUB_REF: "main",
    HEALTHCHECK_URL_DAILY: "https://hc.example/daily",
    HEALTHCHECK_URL_DISCLOSURE: "https://hc.example/disc",
  };
  try {
    await worker.scheduled(event, env, { waitUntil() {} });
  } finally {
    globalThis.fetch = previous;
  }
  return calls.filter((call) => call.url.includes("/dispatches"));
}

test("one 02:15 run dispatches daily and the filing prompt once each", async () => {
  const cases = [
    {
      scheduledTime: Date.parse("2026-11-16T02:15:00.000Z"),
      inputs: { filing_period: "2026Q3", filing_deadline: "2026-11-16" },
    },
    {
      scheduledTime: Date.parse("2027-03-01T02:15:00.000Z"),
      inputs: { filing_period: "2026FY_DEC", filing_deadline: "2027-03-01" },
    },
    {
      scheduledTime: Date.parse("2026-08-17T02:15:00.000Z"),
      inputs: { filing_period: "2026Q2_H1", filing_deadline: "2026-08-16" },
    },
    {
      scheduledTime: Date.parse("2027-05-17T02:15:00.000Z"),
      inputs: { filing_period: "2027Q1", filing_deadline: "2027-05-16" },
    },
  ];
  for (const item of cases) {
    for (const cron of ["15 2 * * MON-FRI", "15 2 * * 2-6"]) {
      const dispatches = await runScheduled({ cron, scheduledTime: item.scheduledTime });
      assert.equal(dispatches.length, 2, cron);
      assert.match(dispatches[0].url, /\/daily\.yml\/dispatches$/);
      assert.equal(dispatches[0].body.inputs, undefined);
      assert.match(dispatches[1].url, /\/quarterly-filing-refresh\.yml\/dispatches$/);
      assert.deepEqual(dispatches[1].body.inputs, item.inputs);
    }
  }
});

test("a normal Friday morning and the later weekday runs dispatch one workflow", async () => {
  assert.equal(weekdayName("2026-11-13"), "Friday");
  const friday = await runScheduled({
    cron: "15 2 * * MON-FRI",
    scheduledTime: Date.parse("2026-11-13T02:15:00.000Z"),
  });
  assert.equal(friday.length, 1);
  assert.match(friday[0].url, /\/daily\.yml\/dispatches$/);
  assert.equal(friday[0].body.inputs, undefined);

  const afternoon = await runScheduled({
    cron: "0 7 * * MON-FRI",
    scheduledTime: Date.parse("2026-11-16T07:00:00.000Z"),
  });
  assert.equal(afternoon.length, 1);
  assert.match(afternoon[0].url, /\/disclosure-refresh\.yml\/dispatches$/);

  const evening = await runScheduled({
    cron: "0 11 * * MON-FRI",
    scheduledTime: Date.parse("2026-11-16T11:00:00.000Z"),
  });
  assert.equal(evening.length, 1);
  assert.match(evening[0].url, /\/disclosure-refresh\.yml\/dispatches$/);
});
