# Persistent Memory Overview

## Key Features:
- Hermes Agent has bound, curated memory that persists across sessions.
- Enables the agent to remember user preferences, projects, environments, and learned information.
- Memory is injected into each session as a frozen snapshot.

---

## Memory Structure
- **Files**:
  1. `MEMORY.md`
     - Purpose: Agent's personal notes (environment facts, conventions, learnings).
     - Character Limit: 2,200 chars (~800 tokens).
  2. `USER.md`
     - Purpose: User profile (preferences, style, expectations).
     - Character Limit: 1,375 chars (~500 tokens).
- Stored in: `~/.hermes/memories/`

---

## Session Behavior
- Memory is loaded from disk at session start and appears as a frozen block (not modifiable during a session).
- Changes are persisted immediately but will only update in the prompt during the next session.

### Memory Representation:
```plaintext
══════════════════════════════════════════════
MEMORY (your personal notes) [67% — 1,474/2,200 chars]
══════════════════════════════════════════════
User's project is a Rust web service at ~/code/myapi using Axum + SQLx
§ This machine runs Ubuntu 22.04, has Docker and Podman installed
§ User prefers concise responses, dislikes verbose explanations
```

---

## Supported Actions
- `add`: Add a new memory entry.
- `replace`: Modify an existing memory entry.
- `remove`: Delete an existing memory entry.
- Memory consolidation occurs when limits are exceeded.

---

## Benefits
- Focused memory improves contextual relevance and responsiveness.
- Persistent preferences minimize repetitive interactions.

---

## Additional Information
- Learn more in related features like:
  - [Memory Providers](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory-providers)
  - [Context Files](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files)
