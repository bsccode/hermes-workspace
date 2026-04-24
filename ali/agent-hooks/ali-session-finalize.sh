#!/usr/bin/env bash
set -euo pipefail

payload="$(cat || true)"
SYNC_SCRIPT="$HOME/hermes-workspace/ali/session-sync.sh"
LOG_DIR="${HERMES_HOME:-$HOME/.hermes}/logs"
LOG_FILE="$LOG_DIR/ali-session-sync-hook.log"
mkdir -p "$LOG_DIR"

session_id="$(printf '%s' "$payload" | python3 -c 'import json,sys
try:
 d=json.load(sys.stdin); print(d.get("session_id", ""))
except Exception:
 print("")')"

{
  echo "== on_session_finalize $(date '+%Y-%m-%d %H:%M:%S %Z') =="
  printf '%s\n' "$payload"
  if [[ "$session_id" == "test-session" ]]; then
    echo "Skipping real sync for synthetic hook test session"
  elif [[ -x "$SYNC_SCRIPT" ]]; then
    "$SYNC_SCRIPT" end
  else
    echo "Missing sync script: $SYNC_SCRIPT"
  fi
  echo
} >> "$LOG_FILE" 2>&1 || true

printf '{}\n'
