# Tools & Toolsets Overview

## What are Tools?
- Tools are functions that extend the Hermes Agent's capabilities.
- Organized into logical **toolsets**, which can be enabled/disabled per platform.
- Covers web search, browser automation, terminal execution, file manipulation, messaging, and much more.

---

## High-Level Tool Categories

- **Web**:
  - Examples: `web_search`, `web_extract`
  - Description: Search the web and extract page content.

- **Terminal & Files**:
  - Examples: `terminal`, `process`, `read_file`, `patch`
  - Description: Execute commands and manipulate files.

- **Browser**:
  - Examples: `browser_navigate`, `browser_snapshot`, `browser_vision`
  - Description: Interactive browser automation with text and vision support.

- **Media**:
  - Examples: `vision_analyze`, `image_generate`, `text_to_speech`
  - Description: Multimodal analysis and generation.

- **Agent Orchestration**:
  - Examples: `todo`, `clarify`, `execute_code`, `delegate_task`
  - Description: Planning, clarification, code execution, and subagent delegation.

- **Memory & Recall**:
  - Examples: `memory`, `session_search`
  - Description: Persistent memory management, recall, and session search.

---

## Additional Notes
- High-level categories ensure modularity and make tool management more efficient.
- Tools like Honcho memory are supported as plugins rather than built-in.
- For more detailed documentation, visit the [official Hermes documentation](https://hermes-agent.nousresearch.com/docs/user-guide/features/tools).
