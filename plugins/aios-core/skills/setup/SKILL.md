---
name: setup
description: Builds an operator's aiOS root from an interview, brings their existing files into one, or adds workspaces to an existing one. Use when setting up aiOS, moving existing files or projects into aiOS, or adding a domain.
---

# Setup

Builds an aiOS root that fits the operator's work, then confirms that it works.

## When to use

- Setting up aiOS for the first time
- Bringing existing files, context, skills, or projects into aiOS
- Adding a domain to an existing aiOS root

To add or reorganize folders inside a workspace, use `aios-core:manage-agents-md`. To check an aiOS root, use `aios-core:status`.

## Workflow

1. Choose the mode. If no `.aiOS/config.yaml` exists in this folder or above it, ask whether the operator has existing files to bring in. Don't judge from the folder's contents; their files may be elsewhere.

   | Mode | When | Workflow |
   |---|---|---|
   | Start fresh | No aiOS root exists, and the operator has nothing to bring in | [references/start-fresh.md](references/start-fresh.md) |
   | Migrate | The operator has existing files to bring into a new or existing aiOS root | [references/migrate.md](references/migrate.md) |
   | Extend | An aiOS root exists, and the operator wants to add a domain | [references/extend.md](references/extend.md) |

2. Read the mode's reference file and follow its workflow. Every mode interviews the operator with [references/interview.md](references/interview.md).
3. Run `aios-core:status` and resolve every file problem it reports.

## Report

1. What was created, and what was skipped because it already existed.
2. The choices the operator made, and where the contracts record them.
3. The next steps:
   - Start a new session in each agent harness the operator uses, then run `aios-core:status` there.
   - In Codex, approve the hooks first.
   - Plugin updates are manual in each agent harness. `.aiOS/docs/onboarding.md` gives the commands.
