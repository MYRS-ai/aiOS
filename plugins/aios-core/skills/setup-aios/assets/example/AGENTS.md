---
type: AGENTS.md
---

# AI operating system

Alex Rivera's aiOS supports a product management job, Rivera Studio, and family life. Shared resources support all three domains.
Alex, their family, and their organizations are fictional. These files describe the week of October 5, 2026, and plans for October 12.

## Instructions

### Follow instructions and conventions

- The main agent coordinates work and briefs subagents on their task, relevant contracts, and expected output.
- Read a folder's contract before working there. Follow its links to the instructions and files the task needs.
- Before creating or editing Markdown, read the applicable [file type definition](.aiOS/docs/types/AGENTS.md).
- Follow the [writing standard](shared/standards/writing.md). Lead with the result, separate evidence from assumptions, and give each action an owner.

### Use agreed vocabulary

- Read the [aiOS glossary](.aiOS/docs/glossary.md) and [naming conventions](.aiOS/docs/naming.md) before changing contracts, skills, or settings.
- Read the [shared glossary](shared/docs/glossary.md), then the current workspace's glossary.
- Follow [Maintaining vocabulary](.aiOS/docs/glossary.md#maintaining-vocabulary) when meanings change.

### Respect commitments

Use the [planning constraints](shared/docs/planning.md) when proposing work.

- Ask Alex before changing a commitment involving another person.
- Ask before sending messages, spending money, or publishing.
- Prepare drafts and record unresolved decisions while awaiting approval.

### Keep the system current

- Use `aios-core:manage-agents-md` when folders or instructions change.
- Use `aios-core:manage-skills` when skills change.
- Use `aios-core:verify-aios` when hooks fail, a turn is blocked, or files change outside a session.

## Domains and shared resources

| Contract | Work it supports | Read when |
|---|---|---|
| [Home](home/AGENTS.md) | Family plans, household projects, and personal goals | Working on family or personal matters |
| [Shared](shared/AGENTS.md) | Writing criteria and planning across domains | Working across workspaces |
| [Studio](studio/AGENTS.md) | Discovery services, digital products, and Tally | Working on Rivera Studio |
| [Work](work/AGENTS.md) | Alex's mobile product team at Fieldline | Working on the job |

## System configuration

| Path | What it holds | Read when |
|---|---|---|
| [.aiOS/](.aiOS/AGENTS.md) | Settings and generated product documentation | Configuring checks or reading product docs |
| [.gitignore](.gitignore) | Generated files excluded from Git | Changing tracked files |
