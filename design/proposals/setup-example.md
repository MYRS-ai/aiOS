---
type: doc
created: 2026-10-10T13:18-07:00
updated: 2026-10-10T15:35-07:00
---

# Proposal: setup example

## Status

Proposed. The name, location, and operator are chosen. The open questions below remain.

## Idea

Replace `examples/sample-root/` with the example: a complete, detailed aiOS root for a fictional operator.
The `aios-core:setup` skill adapts the example into each new operator's aiOS root.

The current sample has 15 Markdown files and 228 lines. It shows the folder layout, but not the depth, writing style, or document structure of an aiOS root in daily use.
An agent setting up a new operator has to guess what good contracts, context, projects, and routines look like.

## Goals

- A new operator points an agent at the aiOS repo, and the agent finds the setup skill.
- The setup skill interviews the operator, then builds their aiOS root from the example.
- Every file shows real-world depth and the writing style aiOS expects.
- Guidance for the setup agent stays visibly separate from example content.
- The tests keep using the example as realistic test data.

## Sketch

### Name

Call it "the example." Add it to the glossary: a complete aiOS root for a fictional operator, which the setup skill adapts for each new operator.

### Location

The example ships inside the setup skill, at `plugins/aios-core/skills/setup/assets/example/`.

- Installing the plugin copies only `plugins/aios-core/`. Claude Code and Codex both leave out the repo's `examples/` folder. Setup can only use the example if the plugin contains it.
- Keep one copy. The README links to the example inside the skill, and the tests read it from there. `examples/` is removed.
- Files inside a skill folder skip front matter checks. The tests check a copy of the example as a standalone aiOS root.
- Product repo sessions load a folder's `AGENTS.md` when an agent reads a file there. Example contracts can then act as instructions in those sessions. The example's root contract should state that it is an example, as the sample does today.

### The fictional operator

Alex Rivera works in product development and runs a small studio on the side. They share a home with a partner, two children, and a parent who lives nearby. All names are fictional.

| Workspace | Domain | Folders |
|---|---|---|
| `work/` | Senior product manager at Fieldline, a mid-size company that makes scheduling software for home service businesses. Leads a mobile app team of eight. | `context/`, `projects/`, `routines/`, `workflows/`, `journal/`, `docs/` |
| `studio/` | Alex's own business, with three lines: product discovery advisory for early-stage founders, digital products such as a template kit and a short course, and Tally, a small e-ink desk display built in batches of 50 | `context/`, `clients/`, `products/`, `routines/`, `workflows/`, `journal/`, `docs/` |
| `home/` | Family life: meal plans and groceries with a child's peanut allergy, school and activity schedules, household upkeep, birthdays and gifts, date nights, and Alex's personal goals | `context/`, `projects/`, `routines/`, `goals/`, `journal/`, `docs/` |
| `shared/` | Resources more than one workspace uses | `standards/`, `docs/`, `clis/` |

The folders show both the standard aiOS folders and folders an operator adds for their own domain, such as `clients/` and `goals/`.

### Content

- Content is specific and plausible: named projects with goals and status, routines with schedules and steps, dated journal entries, and glossary terms with "Don't say" entries.
- Each contract shows the contract definition applied to a real folder.
- No content describes a real person or organization.

### Guidance callouts

Guidance for the setup agent goes in GitHub alert callouts, which render as boxes and are easy to find:

```markdown
> [!NOTE]
> **Setup:** Replace this purpose with one to three sentences about whose work this domain covers.
> Name the operator's role and the kind of organization. Ask the operator before naming their employer.
```

- Every guidance callout uses `[!NOTE]` and starts with `**Setup:**`, so agents and scripts can find each one.
- A callout says what a section should capture, what to ask the operator, and what to watch for.
- Text outside callouts is complete example content. It contains no `{placeholder}` markers or generic filler.
- Setup removes every callout from the operator's files.

### Setup flow

The [core skills proposal](core-skills.md) designs the full setup workflow. In short:

1. Interview the operator about their domains, files, and preferences.
2. Match each of the operator's domains to an example workspace, and choose the folders that fit.
3. Create each file from its example version. Rewrite the content for the operator, following the callouts.
4. Remove the callouts, then run the `aios-core:status` skill.

## Open questions

- Does the example replace the setup skill's other `assets/` templates?
- How does an agent pointed at the repo, before installing anything, find the setup skill? The README could address agents directly.
- Should a check report leftover `**Setup:**` callouts?
- Does the 1.0 release wait for this work?
