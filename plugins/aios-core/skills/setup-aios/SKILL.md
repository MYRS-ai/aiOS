---
name: setup-aios
description: Creates or extends an operator's aiOS through an interview and confirmed workspace choices. Use when setting up aiOS for the first time, bringing existing files or projects into aiOS, or adding a workspace.
---

# Set up aiOS

Builds an aiOS that fits the operator's work, then confirms that it works.

## When to use

- Setting up aiOS for the first time
- Bringing existing files, context, skills, or projects into aiOS
- Adding a workspace to an existing aiOS

To check an existing aiOS or diagnose problems, use `aios-core:verify-aios`.

## Workflow

Follow [Maintaining vocabulary](../../docs/glossary.md#maintaining-vocabulary) before introducing or changing concepts during setup.

1. Choose the mode.

   If no `.aiOS/config.yaml` exists in this folder or above it, ask whether the operator has existing files to bring in. Don't judge from the folder's contents; their files may be elsewhere.

   | Mode | When | Workflow |
   |---|---|---|
   | Start fresh | No aiOS exists, and the operator has nothing to bring in | [references/start-fresh.md](references/start-fresh.md) |
   | Migrate | The operator has existing files to bring into a new or existing aiOS | [references/migrate.md](references/migrate.md) |
   | Extend | An aiOS exists, and the operator wants to add a domain | [references/extend.md](references/extend.md) |

2. Read the mode's reference file and follow its workflow. Every mode uses [references/interview.md](references/interview.md).
   After the interview, use the [example guide](references/example.md) to choose relevant files from the packaged example.
   Adapt them to the operator's confirmed needs and facts.
3. Run `aios-core:verify-aios` and resolve every file problem it reports.

## Report

1. Lead with what is ready to use and where to begin.
2. Explain consequential workspace choices, migration results, or omissions.
3. State remaining decisions or activation steps.

For unverified agent harnesses, give the approval and new-session verification steps from [onboarding](../../docs/onboarding.md).
