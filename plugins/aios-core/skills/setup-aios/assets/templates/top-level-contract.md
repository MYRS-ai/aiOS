---
type: AGENTS.md
---

# AI operating system

The operator's aiOS: their workspaces and the resources they share.

## Instructions

### Follow instructions and conventions

- The main agent coordinates the work, delegates to subagents, and briefs them.
- Read a folder's `AGENTS.md` before working there. Follow its links until you reach the instructions and files the task needs. The agent harness doesn't load every contract on its own.
- Before creating or editing Markdown, read the applicable [file type definition](.aiOS/docs/types/AGENTS.md).

### Maintain vocabulary

- Before you create or change contracts, glossaries, skills, plugins, or `.aiOS/` settings, read the [aiOS glossary](.aiOS/docs/glossary.md) and the [naming conventions](.aiOS/docs/naming.md).
- Before working in a workspace, read the [shared glossary](shared/docs/glossary.md), then that workspace's `docs/glossary.md`.
- Follow [Maintaining vocabulary](.aiOS/docs/glossary.md#maintaining-vocabulary) before introducing or changing a concept.

### Maintain and verify aiOS

- Use the `aios-core:manage-agents-md` skill when a folder's purpose, instructions, or contents change.
- Use the `aios-core:manage-skills` skill when you create or change a skill.
- Use the `aios-core:verify-aios` skill when hooks seem not to run, a turn was blocked, or files changed outside a session.

## Contents

| Path | What it holds | Read when |
|---|---|---|
| [.aiOS/](.aiOS/AGENTS.md) | Settings and the core plugin docs copy | Configuring aiOS or reading product docs |
{workspaces}
| [.gitignore](.gitignore) | Paths excluded from Git | Changing which files Git tracks |
