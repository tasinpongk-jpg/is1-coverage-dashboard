# IS1 dispatcher Worker

A small Cloudflare Worker that POSTs to GitHub's `workflow_dispatch` API at
each scheduled fire time. Replaces GitHub Actions' unreliable `schedule:`
events as the primary trigger for both `daily.yml` and
`disclosure-refresh.yml`. The GHA `schedule:` blocks stay in place as
redundant backups.

Deduplication is done by the `guard` job at the top of `daily.yml`, **not** by
the `concurrency` group. `concurrency: group=daily` with
`cancel-in-progress: false` queues the backup rather than dropping it, so both
triggers used to run the full ~20-minute pipeline and land two `daily snapshot`
commits every weekday. The guard skips a `schedule` run once a
`workflow_dispatch` run has already succeeded the same UTC day, and fails open
(runs anyway) if it cannot reach the API — a missed day costs more than a
duplicate one.

## What it dispatches

| Cron (UTC) | Bangkok local | Workflow | Notes |
|---|---|---|---|
| `15 2 * * 1-5` | 09:15 | `daily.yml` | full pipeline (surveillance + emails + 4 dashboards) |
| `0 7 * * 1-5` | 14:00 | `disclosure-refresh.yml` | afternoon catch-up, disclosure-pulse only |
| `0 11 * * 1-5` | 18:00 | `disclosure-refresh.yml` | end-of-day sweep, disclosure-pulse only |

Routing lives in `worker.js` (`CRON_TO_WORKFLOW`). Adding a new fire time
requires one entry there plus one line in `wrangler.toml [triggers]`.

## Architecture

```
  Cloudflare Cron Trigger              GHA schedule (redundant backup)
   09:15 / 14:00 / 18:00 BKK            same times in both YAML files
        │                                       │
        ▼                                       │
  Worker.scheduled(event)                       │
   ↓ event.cron → CRON_TO_WORKFLOW              │
   POST /repos/.../workflows/<file>/dispatches  │
        │                                       │
        └───────────────┬───────────────────────┘
                        ▼
                 GHA workflow run
                 (surveillance + build, or disclosure refresh)
                        │
                        ▼
                 healthchecks.io ping
                 (separate URLs for daily vs disclosure)
```

Worker fires within seconds of the scheduled minute. On HTTP errors from
the GitHub API it retries 3 times with backoff (0, 2s, 6s). On final
failure it pings the workflow-specific `HEALTHCHECK_URL_*/fail`.

## First-time deploy

Prereqs: `npm install -g wrangler`, Cloudflare account with Workers enabled.

1. **Create a fine-grained GitHub PAT** at
   <https://github.com/settings/personal-access-tokens/new>:
   - Resource owner: `tasinpongk-jpg`
   - Repository access: only `is1-coverage-dashboard`
   - Permissions → Repository → **Actions: Read and write**
   - Expiration: 90 days (calendar reminder to rotate).
   - Copy the token.

2. **(Optional) Create two healthchecks.io checks** at
   <https://healthchecks.io>:
   - `is1-daily-dispatch` — cron `15 2 * * 1-5` UTC, grace 30 min
   - `is1-disclosure-dispatch` — cron `0 7,11 * * 1-5` UTC, grace 15 min
   - Copy the two `hc-ping.com/<uuid>` URLs.

3. **Push secrets** from this directory:
   ```bash
   cd cloudflare-cron
   wrangler secret put GITHUB_TOKEN                # paste PAT
   wrangler secret put HEALTHCHECK_URL_DAILY       # optional
   wrangler secret put HEALTHCHECK_URL_DISCLOSURE  # optional
   wrangler secret put MANUAL_TRIGGER_TOKEN        # any random string (for smoke test)
   ```

4. **Deploy**:
   ```bash
   wrangler deploy
   ```

   wrangler prints the Worker URL and registers all 3 cron triggers from
   `wrangler.toml`.

5. **Smoke-test each workflow**:
   ```bash
   # Daily (default)
   curl -X POST -H "Authorization: Bearer <MANUAL_TRIGGER_TOKEN>" \
        https://is1-coverage-dispatcher.<account>.workers.dev/

   # Disclosure refresh
   curl -X POST -H "Authorization: Bearer <MANUAL_TRIGGER_TOKEN>" \
        "https://is1-coverage-dispatcher.<account>.workers.dev/?workflow=disclosure-refresh.yml"
   ```
   Expect HTTP 204 and a new run in the Actions tab within seconds.

## Upgrading from the previous (single-cron) version

If you already deployed the older version that handled only `daily.yml`:

1. Pull latest: `git pull origin main` from a clone that has the new files.
2. Re-run: `wrangler deploy` from `cloudflare-cron/`.
3. (Optional) rename old healthcheck secret:
   ```bash
   wrangler secret put HEALTHCHECK_URL_DAILY  # paste your old HEALTHCHECK_URL value
   wrangler secret delete HEALTHCHECK_URL     # remove the old name
   ```
   Worker will function without these — they're optional alerting.
4. Remove the stale `GITHUB_WORKFLOW` variable if it was set as a secret:
   `wrangler secret delete GITHUB_WORKFLOW` (it's now per-cron, not env-wide).

## Day-to-day operations

- **Live logs:** `wrangler tail` shows every cron invocation and the API response.
- **Cron history:** Cloudflare dashboard → Workers → `is1-coverage-dispatcher`
  → Triggers → Past Cron Events.
- **Rotate the PAT** when it expires: `wrangler secret put GITHUB_TOKEN`. No
  redeploy needed.
- **Pause one specific cron:** comment out the line in `wrangler.toml`
  `[triggers].crons` and `wrangler deploy`. GHA backup still fires.
- **Pause the entire dispatcher:** delete the cron triggers from the
  Cloudflare dashboard (Triggers tab) or run `wrangler deployments delete`.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Worker logs: `No workflow mapped for cron "<expr>"` | wrangler.toml has a cron that's not in `CRON_TO_WORKFLOW` (or vice versa) | Add the missing entry in `worker.js` and redeploy. |
| Worker logs: `GitHub API 401` | PAT expired or wrong permissions | Re-issue PAT, `wrangler secret put GITHUB_TOKEN`. |
| Worker logs: `GitHub API 404` | Workflow filename wrong, or repo renamed | Check the `CRON_TO_WORKFLOW` values match files in `.github/workflows/`. |
| One cron fires, another doesn't | Cron not registered in Cloudflare. Check `wrangler.toml` against `wrangler deployments list`. | Re-run `wrangler deploy`. |
| healthchecks.io email "down" | Worker fired and all 3 retries failed | `wrangler tail` and re-trigger; GHA backup will still attempt. |
| Two Actions runs the same minute | Both Cloudflare and GHA cron fired | Expected occasionally. `concurrency:group=daily` queues the second; the second's commit step is typically a no-op. |
