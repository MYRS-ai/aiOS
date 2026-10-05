---
type: AGENTS.md
created: 2026-10-04T14:19-07:00
updated: 2026-10-04T18:50-07:00
---

# AI operating system

The aiOS of a fictional operator who coordinates repairs, sells garden planners, and plans household projects.

## Instructions

### Follow folder contracts

Read a folder's `AGENTS.md` before working there. Follow its links until you reach the instructions and files the task needs. The agent harness doesn't load every contract on its own.

### Follow file conventions

Read [.aiOS/docs/glossary.md](.aiOS/docs/glossary.md) for aiOS terms, then the current workspace's glossary if one exists.
Workspace terms may add to the product terms but must not contradict them.
Use the `aios-core:check` skill to verify changes.

### Keep contracts current

Use the `aios-core:write-contract` skill when a folder's purpose, instructions, or contents change.

## Contents

| Path | What it holds | Read when |
|---|---|---|
| [.aiOS/](.aiOS/AGENTS.md) | Settings and the core plugin docs copy | Configuring aiOS or reading product docs |
| [day-job/](day-job/AGENTS.md) | The fictional operator coordinates equipment maintenance at a repair workshop. | Working in this domain |
| [personal/](personal/AGENTS.md) | The fictional operator plans household projects and weekend walks. | Working in this domain |
| [shared/](shared/AGENTS.md) | Resources used by more than one domain | Working across domains |
| [side-business/](side-business/AGENTS.md) | The fictional operator develops printable garden planners for a small shop. | Working in this domain |
