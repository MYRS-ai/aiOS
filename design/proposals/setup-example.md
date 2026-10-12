---
type: doc
created: 2026-10-10T13:18-07:00
updated: 2026-10-12T10:47-07:00
---

# Proposal: setup example

## Status

Promoted to the [setup example spec](../specs/setup-example.md). The spec resolves the implementation details and is authoritative.

## Idea

Replace the repository-only sample with a complete, detailed aiOS for a fictional operator.
The `aios-core:setup-aios` skill uses it as a reference when creating each new operator's aiOS.

At proposal time, the sample had 15 Markdown files and 228 lines. It showed folder layout without demonstrating daily use.
An agent setting up a new operator has to guess what good contracts, context, projects, and routines look like.

## Goals

- A new operator points an agent at the aiOS repo, and the agent finds the setup skill.
- The setup skill interviews the operator, then adapts relevant example structures to their aiOS.
- Every file shows real-world depth and the writing style aiOS expects.
- Guidance for the setup agent stays visibly separate from example content.
- The tests keep using the example as realistic test data.

## Sketch

### Name

Use the ordinary word "example." It does not require a new aiOS glossary concept.

### Location

The example ships inside the setup skill, at `plugins/aios-core/skills/setup-aios/assets/example/`.

- Installing the plugin copies only `plugins/aios-core/`. The example must live there to be available after installation.
- Keep one copy. The README links to the packaged example, and the tests read it from there.
- Files inside a skill folder skip front matter checks. Tests validate a standalone copy outside the skill package.
- Example contracts can become instructions when an agent reads their files. The top-level purpose must identify the operator as fictional.

### The fictional operator

Alex Rivera works in product development and runs a small studio on the side. They share a home with a partner, two children, and a parent who lives nearby. All names are fictional.

| Workspace | Domain | Folders |
|---|---|---|
| `work/` | Senior product manager at Fieldline, a mid-size company that makes scheduling software for home service businesses. Leads a mobile app team of eight. | `context/`, `projects/`, `routines/`, `workflows/`, `journal/`, `docs/` |
| `studio/` | Alex's own business, with three lines: product discovery advisory for early-stage founders, digital products such as a template kit and a short course, and Tally, a small e-ink desk display built in batches of 50 | `context/`, `clients/`, `products/`, `routines/`, `workflows/`, `journal/`, `docs/` |
| `home/` | Family life: meal plans and groceries with a child's peanut allergy, school and activity schedules, household upkeep, and Alex's personal goals | `context/`, `projects/`, `routines/`, `workflows/`, `goals/`, `journal/`, `docs/` |
| `shared/` | Resources more than one workspace uses | `standards/`, `docs/`, `routines/`, `workflows/`, `journal/` |

The folders show both the standard aiOS folders and folders an operator adds for their own domain, such as `clients/` and `goals/`.

### Content

- Content is specific and plausible: projects with goals and status, routines linked to workflows, and dated journal entries.
- Glossaries use the agreed `Term`, `Meaning`, and `Notes` columns.
- Each contract shows the contract definition applied to a real folder.
- No content describes a real person or organization.

### Adaptation guidance

Keep guidance in the skill's `references/example.md`, separate from the fictional operator's files.
The guide maps interview answers to files and explains how to adapt content without inventing operator facts.
Example content contains no setup callouts or placeholder markers.

### Setup flow

The [setup example spec](../specs/setup-example.md) extends the existing setup workflow:

1. Interview the operator about their domains, files, and preferences.
2. Use relevant example files to propose folders that fit the operator's work.
3. Create the initial files with the existing templates, then write content from confirmed facts.
4. Review the adapted files, then run the `aios-core:verify-aios` skill.

## Open questions

None for implementation. The spec retains templates, adds README navigation, and keeps guidance outside example content.
Release timing remains in the [1.0 release spec](../specs/v1-release.md).
