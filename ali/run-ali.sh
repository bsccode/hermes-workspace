#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SYNC_SCRIPT="$SCRIPT_DIR/session-sync.sh"
RAW_NODE_NAME="${ALI_NODE_NAME:-$(hostname -s)}"
NODE_NAME="$(printf '%s' "$RAW_NODE_NAME" | tr '[:upper:]' '[:lower:]' | tr -c 'a-z0-9_-' '-')"
PROFILE_NAME="${ALI_PROFILE_NAME:-ali-$NODE_NAME}"
HERMES_BIN="${ALI_HERMES_BIN:-hermes}"

if [[ ! -x "$SYNC_SCRIPT" ]]; then
  echo "Missing executable sync script: $SYNC_SCRIPT" >&2
  exit 1
fi

"$SYNC_SCRIPT" start

cleanup() {
  local exit_code=$?
  trap - EXIT INT TERM
  "$SYNC_SCRIPT" end || true
  exit "$exit_code"
}

trap cleanup EXIT INT TERM
"$HERMES_BIN" --profile "$PROFILE_NAME" -s ali-operating-model "$@"
