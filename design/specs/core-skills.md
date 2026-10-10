---
type: doc
created: 2026-10-10T15:25-07:00
updated: 2026-10-10T15:35-07:00
---

# Spec: core skills

Promoted from the [core skills proposal](../proposals/core-skills.md).

## Status

In progress. Built and verified on 2026-10-10. It becomes done when the operator commits it.

## Goal

Redesign the core skills so each one has a clear purpose, complete workflows, and polished instructions.
The core plugin ships four skills: `aios-core:setup`, `aios-core:status`, `aios-core:manage-agents-md`, and `aios-core:manage-skills`.
A new `SKILL.md` file type defines how every skill package is built, the same way the `AGENTS.md` type defines contracts.

## Scope

### Included

- Retire `aios-core:check`. Its full check moves into the status report.
- Expand `aios-core:status` into a diagnostic report of the whole aiOS root.
- Give `aios-core:setup` three modes: start fresh, migrate, and extend.
- Add a review mode to `aios-core:manage-agents-md`.
- Add `aios-core:manage-skills`, which creates, updates, and reviews skill packages.
- Add the `SKILL.md` file type definition.
- Update every doc, template, and test that mentions the changed skills.

### Excluded

- The [setup example](../proposals/setup-example.md). Setup keeps its current templates until the next spec.
- Loading workspace skills into Claude Code or Codex. Operators install skills through the agent harness.
- New checks, such as broken links or folders without contracts.
- A skill that runs plugin updates. The status report shows the update commands instead.

## Requirements

1. The core plugin's `skills/` folder holds exactly `setup/`, `status/`, `manage-agents-md/`, and `manage-skills/`.
2. Every core `SKILL.md` follows the structure in `docs/types/skill-md.md` and passes the `frontmatter` check.
3. No `SKILL.md` runs another skill's script by path. Skills refer to each other by plugin-prefixed name.
4. The status script reports, in order: the aiOS root and skipped nested aiOS roots; settings; plugin and docs copy versions with any edited docs copy files; the last hook run in each agent harness and the latest blocked turn; and every check's result for every file.
5. The setup `SKILL.md` chooses a mode, then sends the agent to one reference file for that mode's workflow.
6. Migrate mode copies sources and never moves or deletes them.
7. `aios-core:manage-agents-md` covers creating, updating, and reviewing contracts.
8. `aios-core:manage-skills` covers creating, updating, and reviewing skill packages.
9. `docs/types/skill-md.md` defines the `SKILL.md` front matter, the package folders, the `SKILL.md` structure, the writing style, and where workspace skills live.
10. No shipped file, template, or test mentions `aios-core:check` or `skills/check/`.
11. The product repo check reports `Problems: 0`. The tests pass on `python3` and `/usr/bin/python3`.
12. Both plugin manifests report version `0.10.0`.

## Design

### The `SKILL.md` file type

`docs/types/skill-md.md` follows the pattern of `docs/types/agents-md.md`. It defines:

- **Front matter:** `name` and `description`, as the Agent Skills format requires. The description says what the skill does, then "Use when" with its scenarios. It holds no implementation details.
- **Package folders:** `scripts/` for programs the skill runs, `references/` for detail the agent reads when needed, and `assets/` for templates. A package includes a folder only when it has files for it.
- **`SKILL.md` structure:**

| Part | What it holds |
|---|---|
| Title and purpose | The skill's name and one or two sentences on what it achieves |
| When to use | The scenarios, and which skill to use instead for similar requests |
| Workflow | Numbered steps. Each is one action and says how to confirm it worked. Skills with modes list the modes and link each one's reference file. |
| Report | What to tell the operator, in order |

- **Writing style:** direct instructions to the agent, glossary terms, plugin-prefixed skill names, and a short `SKILL.md` with detail in `references/`.
- **Workspace skills:** skills an operator maintains live in their workspace's `skills/` folder, one folder per skill. Skills used by more than one workspace live in `shared/skills/`.

`docs/types/AGENTS.md` changes from front matter type definitions to file type definitions, since `SKILL.md` has no `type` field.

### `aios-core:setup`

```
setup/
├── SKILL.md
├── references/
│   ├── interview.md        questions for the operator, used by every mode
│   ├── start-fresh.md
│   ├── migrate.md
│   └── extend.md
├── scripts/setup.py
└── assets/                 current templates
```

`SKILL.md` picks the mode. An existing `.aiOS/config.yaml` means extend. Otherwise the agent asks whether the operator has files to bring in. Each reference file holds that mode's workflow as written in the proposal.
Every mode ends by running `aios-core:status` and resolving the file problems it reports.

### `aios-core:status`

`status.py` takes over the full check from `check.py`, which is removed. It prints one section per item in requirement 4.
The `SKILL.md` tells the agent to compare each section with the expected state, explain each difference and its fix, and lead the report with a one-line verdict.
The agent fixes file problems in files the current task changed and asks before fixing others.

### `aios-core:manage-agents-md`

Three modes in one `SKILL.md`:

- **Create:** inspect the folder, decide whether it needs a contract, write it, and add it to the parent contract's Contents.
- **Update:** compare the contract with the folder and correct it.
- **Review:** run update across a folder tree and report every contract that no longer matches its folder. Change nothing until the operator confirms.

### `aios-core:manage-skills`

The same three modes for skill packages, following `docs/types/skill-md.md`.
Create asks where the skill belongs: a workspace, `shared/`, or a plugin the operator maintains.
An `assets/SKILL.md` template gives the starting structure.

### Docs and templates

Update every mention of the changed skills: the README, `features.md`, `onboarding.md`, `hooks.md`, `checks.md`, `naming.md`, `skills/AGENTS.md`, the setup root template, the sample root, and `design/decisions.md`.
The operator's own instance contracts are outside this repo. The report lists the lines they need to change.

## Test plan

- Update the tests that run `skills/check/scripts/check.py` to run the status script and read its file results.
- Add a test that the status script prints every section in requirement 4, in order.
- Add a test that `skills/` holds exactly the four skill folders.
- Search the shipped files for `aios-core:check` and `skills/check/`. Expect no results.

```bash
python3 -m unittest discover -s tests -v
/usr/bin/python3 -m unittest discover -s tests -v
python3 plugins/aios-core/skills/status/scripts/status.py
```

## Tasks

1. Write `docs/types/skill-md.md`. Update `docs/types/AGENTS.md` and `docs/AGENTS.md`.
2. Move the full check into `status.py` and add the new sections. Update the tests that use `check.py`.
3. Remove `skills/check/`. Update every script message that names it.
4. Rewrite the status `SKILL.md`.
5. Write the setup references, then rewrite the setup `SKILL.md`.
6. Rewrite the `aios-core:manage-agents-md` `SKILL.md` with its three modes.
7. Write the `aios-core:manage-skills` `SKILL.md` and its `assets/SKILL.md` template.
8. Update the docs, templates, and decisions listed under Design.
9. Set both manifests to `0.10.0`.
10. Run the test plan and resolve every failure.

## Done when

- Every requirement passes its test or search.
- A fresh setup in an empty folder ends with a status report showing no file problems.

## Open questions

None.
