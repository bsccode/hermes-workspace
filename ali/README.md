# Ali multi-node brain layout

This folder turns vanilla Hermes into Ali with a shared identity, shared skills, and separate machine-local brains.

Files here:
- `ALI-ARCHITECTURE.md` — the operating model: what is shared vs local.
- `NEW-NODE-BOOTSTRAP.md` — human-readable onboarding instructions.
- `NEW-NODE-PROMPT.md` — exact prompt to feed a fresh Hermes instance after bootstrap.
- `bootstrap-node.sh` — automation script that provisions a new node profile.
- `shared/skills/ali-operating-model/SKILL.md` — the shared Ali identity/operating skill.
- `bootstrap/ali-secrets.local.env` — local-only secrets bundle for onboarding a new node. This file is gitignored.
- `bootstrap/config.current.yaml` — current Hermes baseline config snapshot for cloning into a new node profile. This file is gitignored.

Design principle:
- Same assistant identity everywhere.
- Separate machine memories everywhere.
- Shared lessons promoted intentionally through journals, knowledge notes, and skills.

Additional artifact:
- `spawn-ali.sh` — single local-only file that can turn a vanilla Hermes install into a new Ali node with embedded config + credentials.
