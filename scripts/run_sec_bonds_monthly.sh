#!/usr/bin/env bash
# run_sec_bonds_monthly.sh — wrapper for is1-sec-bonds-monthly-15-21 cron.
# Sources the SEC API key from the secrets file, then invokes the scraper.
# Uses $LOCALAPPDATA (NOT $HOME) to dodge the MSYS $HOME rewrap trap (pitfall #14).
set -e
SECRET_FILE="$LOCALAPPDATA/hermes/secrets/sec_bonds.env"
if [ -f "$SECRET_FILE" ]; then
    # shellcheck disable=SC1090
    set -a; . "$SECRET_FILE"; set +a
fi
SCRIPT_PATH="$LOCALAPPDATA/hermes/scripts/scrape_sec_bonds.py"
exec python "$SCRIPT_PATH"
