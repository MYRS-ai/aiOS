---
name: manage-skills
description: Creates, updates, and reviews skill packages and their references in applicable contracts. Use when the operator wants a new skill, when a skill's workflow, name, location, or files change, or to find outdated skills and references.
---

# Manage skills

Builds and maintains skill packages that follow the aiOS skill structure, so agents use them reliably in Claude Code and Codex.

## When to use

- The operator wants a skill for a task that repeats.
- A skill's workflow, scripts, references, or assets change.
- A skill is renamed, moved, or retired, or its invocation conditions change.
- The operator states a preference for how a skill should work.
- The operator wants skills checked for outdated or poorly structured content.

## Workflow

Before you begin:

- Read the [skill definition](../../docs/types/skill-md.md) first. It defines the package structure, front matter, sections, and writing style.
- Follow [Maintaining vocabulary](../../docs/glossary.md#maintaining-vocabulary) before introducing or changing concepts in a skill.
- Codex display names use `interface.display_name` in `agents/openai.yaml`. Match the skill title.

Follow [Create a skill](#create-a-skill), [Update a skill](#update-a-skill), or [Review skills](#review-skills).

### Create a skill

1. Confirm that a skill is the right tool, using the definition's "When to create a skill."
2. Ask the operator what the skill should achieve, when it should run, and what it should report. Walk through one real instance of the task together.
3. Choose the location and name using the definition's "Where skills live." Start [Contract and reference checks](#contract-and-reference-checks) before writing.
4. Draft the workflow as numbered steps. Put supporting files where they belong:

   - Repeatable mechanics in `scripts/`
   - Detail needed only sometimes in `references/`
   - Templates, examples, and other supporting material in `assets/`

5. Create the package. Start its `SKILL.md` from [assets/skill-template.md](assets/skill-template.md).
6. Write the description last: what the skill does, then "Use when" and the situations from step 2.
7. Complete [Contract and reference checks](#contract-and-reference-checks) for the new skill.

### Update a skill

1. Read `SKILL.md` and list the package's files.
2. Start [Contract and reference checks](#contract-and-reference-checks). Record existing names and paths before a rename or move.
3. Read affected files, their dependencies, and their uses. Expand your reading until you understand the change's impact.
4. Make the change. Keep `SKILL.md`, scripts, references, and assets consistent with each other.
5. Update the description if the situations it covers changed.
6. Run any changed script to confirm it works.
7. Complete [Contract and reference checks](#contract-and-reference-checks) against the resulting package.

### Review skills

1. Find every `SKILL.md` in the folder tree the operator names.
2. Read each whole package and compare it with the definition. Look for missing sections, files that `SKILL.md` names but the package lacks, files nothing uses, and a `SKILL.md` over about 100 lines. Change nothing yet.
3. Run [Contract and reference checks](#contract-and-reference-checks) for each skill. Record differences without editing.
4. Propose a fix for each difference. Apply the fixes the operator confirms.

## Contract and reference checks

These checks apply to all three workflows. Read contracts before editing; verify references after changes. During reviews, report proposed corrections without editing.

1. Read applicable `AGENTS.md` files where the skill lives and is used, including ancestors outside the repository.
2. Check where agents should discover the skill. Add missing guidance without repeating inherited instructions.
3. For renames, moves, retirements, or changed invocation conditions, search the skill's names and paths across the task's scope.
4. Correct maintained source references. Use `aios-core:manage-agents-md` for contract edits.
5. Repeat the search and verify names, paths, and invocation conditions. Explain any old references that must remain.

The stop hook checks the front matter of every changed `SKILL.md` when the turn ends.

## Report

1. Lead with the outcome or most consequential finding and its practical effect.
2. Give only the context needed to understand, use, or assess the result. Include useful links.
3. State any decision or action still needed, with a specific next step.

For reviews, prioritize findings by impact and recommend fixes. If no issues were found, say so and name what was checked.
