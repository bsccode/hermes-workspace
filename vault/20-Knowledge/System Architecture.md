# System Architecture

## Model Routing
- **Local inference servers:** Qwen-A and Qwen-B on 10.0.0.38 (http://10.0.0.38:8087 and http://10.0.0.38:8088). Both currently load the same model file (/home/blake/models/Qwen3.6.gguf), which duplicates storage (~18GB waste).
- **Stale/absent references:** older config references `prinny` / 10.0.0.18:8087 (Qwen-P4), but that host is not running a model server at the moment. Recommend removing or marking as offline in config.
- Config in `~/.hermes/config.yaml` should be updated to prefer the active local endpoints and avoid pointing to non‑responsive fallbacks.

## Workspace
- Working directory: `~/hermes-workspace` (git repo: github.com/bsccode/hermes-workspace)
- Private repo for all work
- Config lives in `~/.hermes/config.yaml`

## Knowledge Base
- Obsidian vault at `~/Documents/Obsidian Vault` (4 folders: Inbox, Projects, Knowledge, Debugging, User, Archive)
- Session memory via `session_search` (past conversations)
- Persistent memory via `memory` tool (compact, durable facts)
