# IS1 dispatcher Worker

A 60-line Cloudflare Worker whose only job is to POST to GitHub's
`workflow_dispatch` API at 09:50 BKK every weekday. Replaces GitHub Actions'
unreliable `schedule:` event as the primary trigger for `daily.yml`. The
GHA `schedule:` block in `daily.yml` stays in place as a redundant backup
(`concurrency:group=daily` in the workflow prevents double-runs).

## Architecture

```
  Cloudflare Cron Trigger              GHA schedule (backup)
   09:50 BKK Mon-Fri                    09:50 BKK Mon-Fri
        │                                       │
        ▼                                       │
  Worker dispatchWorkflow()                     │
   POST /repos/.../actions/workflows/           │
        daily.yml/dispatches                    │
        │                                       │
        └───────────────┬───────────────────────┘
                        ▼
                 GHA workflow run
                 (surveillance + build)
                        │
                        ▼
                 healthchecks.io ping
```

Worker fires within seconds of the scheduled minute (Cloudflare Cron Triggers
SLA). On any HTTP error from the GitHub API it retries 3 times with
exponential backoff (0, 2s, 6s). On final failure it pings the optional
`HEALTHCHECK_URL/fail` so healthchecks.io alerts you.

## First-time deploy

Prereqs: `npm install -g wrangler`, Cloudflare account with Workers enabled
(same account you use for Pages).

1. **Create a fine-grained GitHub PAT** at
   <https://github.com/settings/personal-access-tokens/new>:
   - Resource owner: `tasinpongk-jpg`
   - Repository access: `Only select repositories` → `is1-coverage-dashboard`
   - Permissions → Repository → **Actions: Read and write** (only this one)
   - Expiration: 90 days (set a calendar reminder to rotate)
   - Copy the token (starts with `github_pat_...`).

2. **Create a healthchecks.io check** (optional but recommended) at
   <https://healthchecks.io>:
   - New check: `is1-daily-dispatch`
   - Schedule: cron `50 2 * * 1-5` timezone UTC
   - Grace time: 30 minutes (build takes ~21 min)
   - Copy the ping URL (looks like `https://hc-ping.com/<uuid>`).

3. **Push secrets to the Worker** from this directory:
   ```bash
   cd cloudflare-cron
   wrangler secret put GITHUB_TOKEN          # paste the PAT
   wrangler secret put HEALTHCHECK_URL       # paste the hc-ping URL (optional)
   wrangler secret put MANUAL_TRIGGER_TOKEN  # any random string (optional)
   ```

4. **Deploy the Worker**:
   ```bash
   wrangler deploy
   ```

   wrangler prints the Worker URL (e.g.
   `https://is1-coverage-dispatcher.<account>.workers.dev`). The Cron Trigger
   is registered automatically by `wrangler.toml`.

5. **Smoke-test**:
   ```bash
   curl -X POST -H "Authorization: Bearer <MANUAL_TRIGGER_TOKEN>" \
        https://is1-coverage-dispatcher.<account>.workers.dev/
   ```
   Expect HTTP 204 and a fresh "Manually run by …" entry in the Actions tab
   within seconds.

## Day-to-day operations

- **Live logs:** `wrangler tail` from this directory shows every cron
  invocation and the GitHub API response.
- **Cron history:** Cloudflare dashboard → Workers → `is1-coverage-dispatcher`
  → Triggers → Past Cron Events. Lists last 100 fires with timestamps and
  exit status.
- **Rotate the PAT** when it expires (or sooner): regenerate at
  github.com/settings/personal-access-tokens, then re-run `wrangler secret put
  GITHUB_TOKEN`. No Worker redeploy needed.
- **Pause the dispatcher** (e.g. during a vendor outage): comment out the
  `crons` line in `wrangler.toml` and `wrangler deploy`, or delete the cron
  trigger from the dashboard. GHA backup still fires.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Worker logs show `GitHub API 401` | PAT expired or wrong permissions | Re-issue PAT with Actions:Read+Write, `wrangler secret put GITHUB_TOKEN`. |
| Worker logs show `GitHub API 404` | `GITHUB_WORKFLOW` value wrong, or repo renamed | Check `wrangler.toml` vars; the workflow filename must include the `.yml`. |
| healthchecks.io email "is1-daily-dispatch is down" | Worker fired and all 3 attempts failed | Open `wrangler tail` and re-trigger; if persistent, GitHub API is down — GHA backup will still fire. |
| No Actions run despite cron time passing | Worker not deployed, or cron paused | `wrangler deployments list`; redeploy. Backup GHA cron is the safety net. |
| Two Actions runs the same morning | Both Cloudflare and GHA cron fired | Expected occasionally. `concurrency:group=daily` in `daily.yml` queues the second; the second's commit will be a no-op (data unchanged). |
