---
type: AGENTS.md
---

# AI operating system

The operator's aiOS: their workspaces and the resources they share.

## Instructions

### Follow folder contracts

Read a folder's `AGENTS.md` before working there. Follow its links until you reach the instructions and files the task needs. The agent harness doesn't load every contract on its own.

### Use aiOS terms and names

Before you create or change contracts, glossaries, skills, plugins, or `.aiOS/` settings, read the [aiOS glossary](.aiOS/docs/glossary.md) and the [naming conventions](.aiOS/docs/naming.md).

### Use workspace terms

Before working in a workspace, read the [shared glossary](shared/docs/glossary.md), then that workspace's `docs/glossary.md`.
Workspace terms add to aiOS terms and never redefine them.

### Diagnose problems

Use the `aios-core:status` skill when hooks seem not to run, a turn was blocked, or files changed outside a session.

### Keep contracts and skills current

Use the `aios-core:manage-agents-md` skill when a folder's purpose, instructions, or contents change.
Use the `aios-core:manage-skills` skill when you create or change a skill.

## Contents

| Path | What it holds | Read when |
|---|---|---|
| [.aiOS/](.aiOS/AGENTS.md) | Settings and the core plugin docs copy | Configuring aiOS or reading product docs |
{workspaces}
