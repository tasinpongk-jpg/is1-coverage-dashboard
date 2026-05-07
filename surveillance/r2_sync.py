"""R2 sync helpers for the surveillance.duckdb file.

Used by the daily.yml workflow. Bypasses awscli + shell expansion entirely
(GitHub Actions secret masking can interfere with --flag-style args).

Reads creds from env vars:
  R2_ENDPOINT          — https://<account>.r2.cloudflarestorage.com
  R2_BUCKET            — bucket name (e.g. setsmart-data)
  AWS_ACCESS_KEY_ID    — R2 access key ID
  AWS_SECRET_ACCESS_KEY — R2 secret access key
  SURVEILLANCE_DB_PATH — local path (e.g. /tmp/surveillance.duckdb)

CLI:
  python r2_sync.py download    # download (silently OK if missing)
  python r2_sync.py upload      # upload (errors if local file missing)
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import boto3
from botocore.exceptions import ClientError


def _client():
    endpoint = os.environ.get("R2_ENDPOINT", "").strip()
    if not endpoint or not endpoint.startswith(("http://", "https://")):
        sys.exit(f"R2_ENDPOINT invalid (got len={len(endpoint)}): must start with http(s)://")
    return boto3.client(
        "s3",
        endpoint_url=endpoint,
        aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
        region_name=os.environ.get("AWS_DEFAULT_REGION", "auto"),
    )


def _bucket() -> str:
    b = os.environ.get("R2_BUCKET", "").strip()
    if not b:
        sys.exit("R2_BUCKET unset.")
    return b


def _local_path() -> Path:
    p = os.environ.get("SURVEILLANCE_DB_PATH", "").strip()
    if not p:
        sys.exit("SURVEILLANCE_DB_PATH unset.")
    return Path(p)


KEY = "surveillance.duckdb"


def download() -> int:
    s3 = _client()
    bucket = _bucket()
    target = _local_path()
    try:
        s3.download_file(bucket, KEY, str(target))
    except ClientError as e:
        code = e.response.get("Error", {}).get("Code", "")
        if code in ("404", "NoSuchKey"):
            print(f"::warning::No existing {KEY} in R2 — surveillance will start fresh.")
            return 0
        print(f"::error::R2 download failed: {e}")
        return 1
    size = target.stat().st_size
    print(f"Downloaded s3://{bucket}/{KEY} -> {target} ({size:,} bytes)")
    return 0


def upload() -> int:
    s3 = _client()
    bucket = _bucket()
    source = _local_path()
    if not source.exists():
        print(f"::error::Local file {source} does not exist; skipping upload.")
        return 1
    s3.upload_file(str(source), bucket, KEY)
    size = source.stat().st_size
    print(f"Uploaded {source} -> s3://{bucket}/{KEY} ({size:,} bytes)")
    return 0


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1] not in ("download", "upload"):
        print(__doc__)
        return 2
    return download() if sys.argv[1] == "download" else upload()


if __name__ == "__main__":
    sys.exit(main())
