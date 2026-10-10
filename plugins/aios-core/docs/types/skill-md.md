---
type: doc
created: 2026-10-10T15:35-07:00
updated: 2026-10-10T15:35-07:00
---

# SKILL.md

A `SKILL.md` file teaches an agent one capability. Its folder is a skill package: the `SKILL.md` and the files it uses.
aiOS skills follow the Agent Skills format, which Claude Code and Codex both load.

People read skills too, so write them in plain sentences.

## When to create a skill

Create a skill when a task repeats and needs a defined workflow or judgment. Skip it when:

- a hook or script does the work without an agent
- a sentence or two in a contract covers it
- an existing skill covers it; extend that skill instead

## Where skills live

| Location | Use for |
|---|---|
| `<workspace>/skills/<name>/` | Skills the operator maintains for one workspace |
| `shared/skills/<name>/` | Skills the operator maintains for more than one workspace |
| `<plugin>/skills/<name>/` | Skills distributed in a plugin |

A skill in a workspace is the source the operator maintains. Agent harnesses load installed skills from their own folders, so install a workspace skill in each agent harness that should use it.

## Package structure

```
<name>/
├── SKILL.md       instructions, required
├── scripts/       programs the skill runs
├── references/    detail the agent reads when it needs it
└── assets/        templates the skill copies into its output
```

- Name the folder after the skill.
- Include a folder only when it has files.
- Keep one topic per reference file. `SKILL.md` says when to read each one.
- Refer to a script by its path inside the package, such as `<skill>/scripts/setup.py`, where `<skill>` is the package folder.
- Refer to another skill by name, never by the path to its files.

## Front matter

| Field | What to write |
|---|---|
| `name` | The skill's name. It matches the folder name and uses lowercase letters, numbers, and hyphens, at most 64 characters. |
| `description` | What the skill does, then "Use when" and the situations that call for it. At most 1024 characters. |

Both fields are required. Agent harnesses show every description to the agent in each session so it can choose a skill. Keep implementation details out of it.
`SKILL.md` has no `type` field and no timestamps. Other files in the package need no front matter.

```markdown
---
name: plan-meals
description: Plans the week's meals and builds the grocery list from the family's preferences and allergies. Use when planning meals, shopping for groceries, or changing what the family eats.
---
```

## Structure

Use this outline:

```markdown
# Title

Purpose

## When to use

## Workflow

## Report
```

### Title and purpose

Use a short title that names the capability. Follow it with one or two sentences on what the skill achieves.

### When to use

List the situations that call for the skill. For similar requests that belong elsewhere, name the skill to use instead.

### Workflow

Write numbered steps. Each step is one action and says how to confirm it worked.
When a skill has modes, name each mode and how to choose it, then link the mode's reference file. The agent reads only the file it needs.

### Report

State what to tell the operator, in order. Lead with the outcome.

## Writing a skill

- Address the agent with direct instructions.
- Use the terms in the [aiOS glossary](../glossary.md) and write skill names as [naming.md](../naming.md) describes.
- Describe what the skill does now.
- Keep `SKILL.md` under about 100 lines. Move detail into `references/`.

## Keeping a skill current

Update the skill in the same turn when:

- its workflow changes
- you add, rename, or remove a script, reference, or asset
- the operator states a preference for how the skill should work

Use the `aios-core:manage-skills` skill to create, update, or review a skill.
