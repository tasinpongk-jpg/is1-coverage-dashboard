import assert from "node:assert/strict";
import test from "node:test";

import { canonicalCron, workflowForCron } from "../cloudflare-cron/worker.js";

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
});
