---
name: manage-skills
description: Creates, updates, and reviews skill packages, meaning a SKILL.md with its scripts, references, and assets. Use when the operator wants a new skill, when a skill's workflow or files change, or to find skills that are outdated or poorly structured.
---

# Manage skills

Builds and maintains skill packages that follow the aiOS skill structure, so agents use them reliably in Claude Code and Codex.

## When to use

- The operator wants a skill for a task that repeats.
- A skill's workflow, scripts, references, or assets change.
- The operator states a preference for how a skill should work.
- The operator wants skills checked for outdated or poorly structured content.

## Workflow

Read `.aiOS/docs/types/skill-md.md` in the aiOS root first. It defines the package structure, front matter, sections, and writing style. Then follow the mode that fits.

### Create

1. Confirm that a skill is the right tool, using the definition's "When to create a skill."
2. Ask the operator what the skill should achieve, when it should run, and what it should report. Walk through one real instance of the task together.
3. Choose the location and the name. The location is the workspace that uses the skill, `shared/skills/` when more than one workspace does, or a plugin the operator maintains.
4. Draft the workflow as numbered steps. Put repeatable mechanics in `scripts/`, detail needed only sometimes in `references/`, and templates in `assets/`.
5. Create the package. Start its `SKILL.md` from [assets/skill-template.md](assets/skill-template.md).
6. Write the description last: what the skill does, then "Use when" and the situations from step 2.
7. Add the skill to the Skills section of the contract for the folder where it is used.

### Update

1. Read the whole package before changing it.
2. Make the change. Keep `SKILL.md`, scripts, references, and assets consistent with each other.
3. Update the description if the situations it covers changed.
4. Run any changed script to confirm it works.

### Review

1. Find every `SKILL.md` in the folder tree the operator names.
2. Compare each package with the definition. Look for missing sections, files that `SKILL.md` names but the package lacks, files nothing uses, and a `SKILL.md` over about 100 lines. Change nothing yet.
3. Propose a fix for each difference. Apply the fixes the operator confirms.

The stop hook checks the front matter of every changed `SKILL.md` when the turn ends.

## Report

1. Each package created or changed, and what changed in it.
2. For a new skill, where it lives. Remind the operator to install it in each agent harness that should use it.

For a review, report the differences and proposed fixes before changing anything.
