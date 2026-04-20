# Skills System Overview

## What are Skills?
Skills are on-demand knowledge documents enabling the Hermes Agent to perform specific tasks efficiently. They follow the [agentskills.io specification](https://agentskills.io/specification) and are optimized to minimize token usage.

### Key Features:
1. Token-efficient loading (progressive disclosure).
2. Compatibility with open standards.
3. Stored locally under the directory `~/.hermes/skills/`.
4. External skill directories can be configured to extend functionality.

---

## Using Skills
### Interaction Modes:
1. **Slash Commands**:
Example: `/plan rollout for auth provider` creates a structured implementation plan.

2. **Natural Language Queries**:
Example: "Show me the Axolotl skill" or "What skills do you have?"

`/plan` is an example skill, which inspects context and saves implementation plans in `.hermes/plans/`.

---

## Progressive Disclosure
Skills use a minimalist loading pattern to reduce memory/CPU overhead:
- **Level 0**: List available skills with summaries (~3k tokens).
- **Level 1**: Load full skill content and metadata when needed.
- **Level 2**: Drill into specific references in a skill file only on demand.

---

## SKILL.md Format
Skills are formatted as Markdown documents. These files allow:
- Procedural tasks to be defined clearly.
- Easy updates and collaboration.

---

## Additional Resources
- [Bundled Skills Catalog](https://hermes-agent.nousresearch.com/docs/reference/skills-catalog)
- [Optional Skills Catalog](https://hermes-agent.nousresearch.com/docs/reference/optional-skills-catalog)