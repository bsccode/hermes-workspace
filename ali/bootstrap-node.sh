#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SECRETS_FILE="${ALI_SECRETS_FILE:-$SCRIPT_DIR/bootstrap/ali-secrets.local.env}"
CONFIG_SNAPSHOT="${ALI_CONFIG_SNAPSHOT:-$SCRIPT_DIR/bootstrap/config.current.yaml}"
SHARED_SKILL_SRC="$SCRIPT_DIR/shared/skills/ali-operating-model/SKILL.md"

if [[ ! -f "$SECRETS_FILE" ]]; then
  echo "Missing secrets file: $SECRETS_FILE" >&2
  exit 1
fi

if [[ ! -f "$CONFIG_SNAPSHOT" ]]; then
  echo "Missing config snapshot: $CONFIG_SNAPSHOT" >&2
  exit 1
fi

if [[ ! -f "$SHARED_SKILL_SRC" ]]; then
  echo "Missing shared skill file: $SHARED_SKILL_SRC" >&2
  exit 1
fi

source "$SECRETS_FILE"

RAW_NODE_NAME="${ALI_NODE_NAME:-$(hostname -s)}"
NODE_NAME="$(printf '%s' "$RAW_NODE_NAME" | tr '[:upper:]' '[:lower:]' | tr -c 'a-z0-9_-' '-')"
PROFILE_NAME="${ALI_PROFILE_NAME:-ali-$NODE_NAME}"
HERMES_HOME_BASE="${HERMES_HOME_BASE:-$HOME/.hermes}"
PROFILE_DIR="$HERMES_HOME_BASE/profiles/$PROFILE_NAME"
PROFILE_SKILL_DIR="$PROFILE_DIR/skills/custom/ali-operating-model"
WORKSPACE_DIR="${ALI_WORKSPACE_DIR:-$HOME/hermes-workspace}"
REPO_DIR="$WORKSPACE_DIR"
GIT_REMOTE_URL="${ALI_REPO_URL:-https://github.com/${ALI_REPO_OWNER}/${ALI_REPO_NAME}.git}"
GIT_PUSH_URL="${ALI_REPO_PUSH_URL:-$GIT_REMOTE_URL}"
ALI_BRANCH="${ALI_BRANCH:-main}"

mkdir -p "$PROFILE_DIR" "$PROFILE_SKILL_DIR" "$PROFILE_DIR/memory" "$PROFILE_DIR/sessions"

if command -v git >/dev/null 2>&1; then
  git config --global user.name "${GITHUB_USERNAME:-bsccode}"
  git config --global user.email "${GITHUB_EMAIL:-bsccoding@gmail.com}"
  git config --global credential.helper store
  if [[ -n "${GITHUB_TOKEN:-}" ]]; then
    cat > "$HOME/.git-credentials" <<EOF
https://${GITHUB_USERNAME:-bsccode}:${GITHUB_TOKEN}@github.com
EOF
    chmod 600 "$HOME/.git-credentials"
  fi
fi

if [[ ! -e "$REPO_DIR" ]]; then
  git clone "$GIT_PUSH_URL" "$REPO_DIR"
elif [[ ! -d "$REPO_DIR/.git" ]]; then
  echo "Refusing to overwrite non-git directory: $REPO_DIR" >&2
  exit 1
fi

git -C "$REPO_DIR" remote set-url origin "$GIT_PUSH_URL" || true
git -C "$REPO_DIR" fetch origin || true
git -C "$REPO_DIR" checkout "$ALI_BRANCH" || true
git -C "$REPO_DIR" pull --ff-only origin "$ALI_BRANCH" || true

cp "$CONFIG_SNAPSHOT" "$PROFILE_DIR/config.yaml"
cp "$SECRETS_FILE" "$PROFILE_DIR/.env"
cp "$SHARED_SKILL_SRC" "$PROFILE_SKILL_DIR/SKILL.md"

mkdir -p \
  "$REPO_DIR/ali/journal/$NODE_NAME" \
  "$REPO_DIR/ali/nodes/$NODE_NAME" \
  "$REPO_DIR/ali/knowledge" \
  "$REPO_DIR/ali/playbooks"

if [[ ! -f "$REPO_DIR/ali/nodes/$NODE_NAME/README.md" ]]; then
  cat > "$REPO_DIR/ali/nodes/$NODE_NAME/README.md" <<EOF
# $NODE_NAME

- Hostname: $NODE_NAME
- Profile: $PROFILE_NAME
- Workspace: $WORKSPACE_DIR
- Initialized by: ali/bootstrap-node.sh
EOF
fi

echo
echo "Ali bootstrap complete."
echo "Profile: $PROFILE_NAME"
echo "Workspace: $WORKSPACE_DIR"
echo
echo "Next steps:"
echo "  $REPO_DIR/ali/run-ali.sh"
echo "Or manually:"
echo "  hermes --profile $PROFILE_NAME -s ali-operating-model"
echo "Then feed in: $REPO_DIR/ali/NEW-NODE-PROMPT.md"
