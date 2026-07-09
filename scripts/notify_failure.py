"""Send a one-line failure email from a GitHub Actions workflow.

Stdlib-only on purpose: this runs in the failure path, so it must not depend
on any project module that could itself be broken.

Inputs (all env vars, all required except SMTP_HOST/PORT):
  EMAIL_USERNAME       — Gmail account
  EMAIL_APP_PASSWORD   — Gmail App Password (NOT the account password)
  EMAIL_FROM           — From address (falls back to EMAIL_USERNAME)
  EMAIL_TO             — Recipient
  GITHUB_WORKFLOW      — set by GH Actions
  GITHUB_JOB           — set by GH Actions
  GITHUB_RUN_ID        — set by GH Actions
  GITHUB_REPOSITORY    — set by GH Actions ("owner/repo")
  GITHUB_REF_NAME      — branch (set by GH Actions)
  SMTP_HOST            — default smtp.gmail.com
  SMTP_PORT            — default 587

Exits 0 on success, 1 on misconfiguration, 2 on send failure. Never re-raises.
"""

from __future__ import annotations

import os
import smtplib
import ssl
import sys
from email.message import EmailMessage


def main() -> int:
    user = os.environ.get("EMAIL_USERNAME", "").strip()
    pw = os.environ.get("EMAIL_APP_PASSWORD", "").replace(" ", "")
    from_addr = os.environ.get("EMAIL_FROM", "").strip() or user
    to_addr = os.environ.get("EMAIL_TO", "").strip() or user
    if not (user and pw and to_addr):
        print("notify_failure: EMAIL_USERNAME / EMAIL_APP_PASSWORD / EMAIL_TO missing.",
              file=sys.stderr)
        return 1

    workflow = os.environ.get("GITHUB_WORKFLOW", "?")
    job = os.environ.get("GITHUB_JOB", "?")
    run_id = os.environ.get("GITHUB_RUN_ID", "?")
    repo = os.environ.get("GITHUB_REPOSITORY", "?/?")
    branch = os.environ.get("GITHUB_REF_NAME", "?")
    url = f"https://github.com/{repo}/actions/runs/{run_id}"

    msg = EmailMessage()
    msg["Subject"] = f"[IS1 CI failed] {workflow} / {job}  (branch: {branch})"
    msg["From"] = from_addr
    msg["To"] = to_addr
    msg.set_content(
        f"Workflow {workflow} (job {job}) failed on branch {branch}.\n\n"
        f"Run: {url}\n\n"
        f"Click the run link, find the first red step, and read the FAIL lines.\n"
        f"Common causes:\n"
        f"  - invalid MINIMAX_API_KEY (rotate in console.minimax.io)\n"
        f"  - MiniMax workspace spend cap hit (raise it or wait for reset)\n"
        f"  - SET portal returning 4xx (Imperva cookie outage — usually transient)\n"
        f"  - R2 sync timeout (re-run usually fixes)\n"
    )

    host = os.environ.get("SMTP_HOST", "smtp.gmail.com")
    port = int(os.environ.get("SMTP_PORT", "587"))
    try:
        with smtplib.SMTP(host, port, timeout=15) as s:
            s.starttls(context=ssl.create_default_context())
            s.login(user, pw)
            s.send_message(msg)
    except Exception as e:  # noqa: BLE001
        print(f"notify_failure: SMTP send failed — {type(e).__name__}: {e}", file=sys.stderr)
        return 2

    print(f"notify_failure: sent to {to_addr}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
