---
type: doc
created: 2026-10-04T13:19-07:00
updated: 2026-10-10T14:54-07:00
---

# Spec: aiOS 1.0 release

## Status

Draft. The refactor for public sharing is done: tasks 1 to 6 below. The scope decisions, the release check, and the version change remain.

## Goal

aiOS 1.0 is the first stable release for operators other than its author.
This spec covers three things. It refactors the project for broader sharing. It sets what the public release includes. It defines the checks that must pass before the release.

## Scope

### Included

- The core plugin, `aios-core`, with its hooks, checks, skills, and operator docs
- The marketplace files for Claude Code and Codex
- The README, license, examples, and tests
- The design records in `design/`

### Excluded

- Extension plugins. Their folders hold drafts without manifests, so no agent harness can install them.
- The draft skills and agent roles in `plugins/aios-core/drafts/`. No agent harness loads them.

## Requirements

1. No product file names an operator, their workspaces, or their organizations. The exceptions are author and owner fields in plugin manifests and the copyright notice in `LICENSE`.
2. The README's commands install the core plugin from GitHub in Claude Code and in Codex.
3. Setup builds a working aiOS root in an empty folder. The full check reports `Problems: 0`, and the status report shows a hook run for each agent harness.
4. An operator customizes aiOS only through the extension points listed under Design.
5. Operator docs describe current behavior. Every relative Markdown link resolves in the plugin and in the docs copy.
6. The tests pass on the current `python3` and on macOS's `/usr/bin/python3`, which is Python 3.9.
7. Both plugin manifests report version `1.0.0`.

## Design

### Three layers

| Layer | What it is | Where it lives |
|---|---|---|
| Product | Generic aiOS: plugins, operator docs, examples, tests, and design records | The product repo, published to GitHub |
| Instance | One operator's aiOS: settings, contracts, workspaces, and their own skills and docs | That operator's aiOS root, wherever they keep it |
| Promotion | How an instance's customization becomes part of the product | A deliberate step, described below |

### Extension points

An instance never edits product files. It customizes aiOS only through these extension points:

1. `.aiOS/config.yaml`, for checks, types, and front matter rules
2. Its own contracts: the root contract, workspace contracts, and folder contracts
3. Its own docs and glossaries, in each workspace's `docs/` folder, or in `shared/docs/` when more than one workspace uses them
4. Its own skills and extension plugins

### Promotion

When a customization proves broadly useful:

1. Generalize it, so it names no operator, workspace, or organization.
2. Add it to the product repo, with tests and docs.
3. Release a new plugin version, and update the instance.
4. Delete the instance's own copy, since the product now provides it.

### Product repo layout

```
aios/
├── README.md                 what aiOS is, and how to install it
├── .claude-plugin/           Claude Code marketplace file
├── .agents/plugins/          Codex marketplace file
├── plugins/
│   ├── aios-core/            hooks, checks, core skills, and operator docs
│   └── ...                   extension plugins, as drafts
├── design/                   research, proposals, specs, and decisions
├── examples/                 a sample aiOS root for a fictional operator
└── tests/                    automated tests of the hooks, checks, and setup
```

The core plugin holds everything an installed instance needs. After install, a plugin can't reach files outside its own folder.
The repo level holds what people evaluating or developing aiOS need.

### Instance layout

```
<aiOS root>/
├── .aiOS/
│   ├── config.yaml           the instance's settings
│   ├── docs/                 the docs copy; never edited by hand
│   └── logs/                 the hook log; ignored by Git
├── AGENTS.md                 root contract: the operator's workspaces
├── <workspace>/              one per domain, with docs/glossary.md
└── shared/                   resources more than one workspace uses
```

The [hooks guide](../../plugins/aios-core/docs/hooks.md) describes how the docs copy stays in sync.
The [onboarding guide](../../plugins/aios-core/docs/onboarding.md) describes guided setup.

## Test plan

| Role | How it's covered |
|---|---|
| Developer | The automated tests run the hooks and setup against `examples/` and other sample roots, with the default settings and a custom one. They need no agent harness. |
| Operator using their own instance | The instance installs the plugin from the local product repo. Changes arrive after a plugin update. |
| New operator | The release check: install from GitHub into isolated agent harness setups, then run setup in an empty folder. |

Run the automated tests from the product repo:

```bash
python3 -m unittest discover -s tests -v
/usr/bin/python3 -m unittest discover -s tests -v
```

Isolated Claude Code setups needed a separate login in earlier tests. The release check confirms whether that's still true.

## Tasks

1. Done. Create the product repo as its own Git repo, ignored by the instance repo.
2. Done. Move the plugins into the product's `plugins/` and point both marketplaces to them.
3. Done. Move operator docs into the core plugin and design records into `design/`. Remove operator details.
4. Done. Add the docs sync, the setup skill, and the manage-agents-md skill.
5. Done. Add the sample aiOS root and the automated tests.
6. Done. Delete the instance's copies of product files. Move the operator's own terms and decisions into their workspaces.
7. Resolve the open questions below.
8. Scan every product file for operator details and fix any found.
9. Run the release check in Claude Code and in Codex. Follow only the README, from install to a passing status report.
10. Set both plugin manifests to `1.0.0` and tag the release `v1.0.0`.

## Done when

- Every requirement passes.
- A new operator reaches a working aiOS root in both agent harnesses by following only the README.

## Open questions

- Does 1.0 wait for the [setup example](../proposals/setup-example.md) and the [core skills](../proposals/core-skills.md) redesign?
- Do the draft extension plugins and draft skills stay in the public repo for 1.0, or move out until they are ready?
