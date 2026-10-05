---
type: doc
created: 2026-10-04T13:19-07:00
updated: 2026-10-04T19:11-07:00
---

# Plan: separate the aiOS product from the operator's instance

Status: rollout steps 1 to 6 are done. Step 7, the release check from GitHub, follows the first public release.

This plan turns aiOS into a product that any operator can install, and separates an operator's instance from the product. It is a proposal. Each part becomes settled when it's recorded in the decision log.

## Goals

- Anyone can find the aiOS repo, install it in Claude Code and Codex, and set it up for their own work.
- The operator develops the product, uses it daily, and tests it as a new operator would, without the three getting in each other's way.
- The operator's customizations never leak into the product, and product updates never overwrite them.
- A customization that proves broadly useful can be generalized and added to the product.

## Three layers

| Layer | What it is | Where it lives |
|---|---|---|
| Product | Generic aiOS: plugins, operator docs, generic examples, tests, and design records | `<product repo>/`, its own Git repo, published to GitHub |
| Instance | One operator's aiOS: config, contracts, workspaces, and their own skills and docs | That operator's aiOS root. The location belongs to the operator. |
| Promotion | How an instance's customization becomes part of the product | A deliberate step, described below |

### Customization boundary

An instance never edits product files. It customizes aiOS only through these extension points:

1. `.aiOS/config.yaml`, for checks, types, and front matter rules
2. Its own contracts: the root contract, workspace contracts, and folder contracts
3. Its own docs, kept in each workspace's `docs/` folder only when needed, or in `shared/docs/` when more than one workspace uses them
4. Its own skills and extension plugins

### Promotion

When a customization proves broadly useful:

1. Generalize it, so it names no operator, workspace, or organization.
2. Add it to the product repo, with tests and docs.
3. Release a new plugin version, and update the instance.
4. Delete the instance's own copy, since the product now provides it.

## The product repo

One repo holds everything. Both agent harnesses accept a marketplace in a repo that also holds other files, and a plugin can sit in a subfolder.

```
aios/
├── README.md                 what aiOS is, and how to install it
├── .claude-plugin/           Claude Code marketplace file
├── .agents/plugins/          Codex marketplace file
├── plugins/
│   ├── aios-core/           hooks, checks, core skills, and operator docs
│   └── ...                   extension plugins, when ready
├── design/                   decision log, research, and plans
├── examples/                 a complete sample aiOS root for a fictional operator
└── tests/                    automated tests of the hooks and checks
```

What goes where:

- **Inside the core plugin:** anything an installed instance needs, such as hooks, checks, skills, and operator docs. After install, a plugin can't reach files outside its own folder.
- **At the repo level:** anything for people evaluating or developing aiOS, such as the README, design records, examples, and tests.

## An instance

```
<aiOS root>/
├── .aiOS/
│   ├── config.yaml           the instance's settings
│   ├── docs/                 copy of the core plugin's docs; never edited by hand
│   └── logs/                 hook event log; ignored by Git
├── AGENTS.md                 root contract: the operator's workspaces
├── <workspace>/              one per area of work, with docs/ only when needed
└── shared/                   resources more than one workspace uses
```

### Keeping `.aiOS/docs/` in sync

At session start, the hook compares the core plugin's docs with the copy.

| Situation | What the hook does |
|---|---|
| The plugin is a newer version than the copy | Replaces the copy and records the new version |
| Same version, different content | Replaces the copy, so changes made during development show up without a version bump |
| The plugin is an older version than the copy | Keeps the copy and warns that this agent harness has an outdated plugin |

Each agent harness keeps its own copy of the plugin. The last row stops an out-of-date agent harness from rolling the docs back.

The `.aiOS/` contract says the copy is replaced on every update. A check warns when a file in it was edited, since the next sync would erase the change.

### Looking up a term

An agent reads `.aiOS/docs/glossary.md` first. Then it reads the glossary in the current workspace's `docs/`, if one exists. A workspace term may add to the product's terms but not contradict them.

## Guided setup

Setup is a skill that the agent runs with the operator.

1. **Interview.** Ask about the operator's areas of work, the kinds of files they keep, and their preferences.
2. **Build.** Create `.aiOS/` with the config, the docs copy, and the log folder. Create the root contract from a template, filled in with the operator's workspaces, and a starter contract for each workspace. Add `.aiOS/logs/` to `.gitignore`.
3. **Verify.** Run the full check, confirm the hooks run in each agent harness the operator uses, and walk through hook approval in Codex.

The sample aiOS root in `examples/` shows the setup agent what a good result looks like. The automated tests use it too.

Plugin updates are off by default for marketplaces outside the agent harnesses' official ones. The install docs explain how to update, and setup reminds the operator.

## Generalizing the current content

| Content | Destination |
|---|---|
| The instance's plugin folder | Product `plugins/` |
| Hooks, checks, and the contract definition | Product, inside the core plugin |
| Operator docs: front matter, hooks, checks, logging, onboarding, and features | Product, inside the core plugin, generalized |
| The glossary | Product glossary inside the core plugin. Terms specific to this operator move to the right workspace's `docs/`. |
| `decisions.md` | Split. Product decisions go to `design/`. This operator's decisions, such as choosing which domain to build first, stay in the instance. |
| Research and placeholder design topics | Product `design/` |
| The root contract, workspaces, standards, and CLIs | Stay in the instance |

Generalized content names no operator, workspace, or organization. Examples use the fictional operator in `examples/`.

## Testing

| Role | How it's covered |
|---|---|
| Developer | Automated tests in the product repo run the hooks against `examples/` and other sample roots, with the default config and with a custom one. They need no agent harness. |
| Operator using their own instance | The instance installs the plugins from the local product repo. Changes arrive after a plugin update. |
| New operator | Before each release, install from GitHub into isolated agent harness setups and run setup on an empty folder. |

Isolated Claude Code setups needed a separate login in earlier tests. The release check confirms whether that's still true.

## Rollout

Each step ends when its check passes.

1. **Create the product repo.** Make `<product repo>/` its own Git repo, and have the instance repo ignore it. Check: `git status` in each repo shows only its own files.
2. **Move the plugins.** Move the instance's plugin folder into the product's `plugins/`, point both marketplaces to the new path, and reinstall. Check: hooks run in both agent harnesses.
3. **Sort and generalize the docs.** Move operator docs into the core plugin and design records into `design/`. Remove operator-specific content. Check: no product file names this operator or their workspaces.
4. **Update the core plugin.** Add the docs sync, the guided setup skill, and skills for agent guidance, such as writing a contract. Check: setup builds a working instance in an empty folder.
5. **Add examples and tests.** Check: the tests pass with the default config and a custom one.
6. **Separate the instance.** Delete its copies of product files, and move this operator's terms and decisions to the right workspaces. Check: the full check passes, and `.aiOS/docs/` matches the plugin.
7. **Run the release check.** Install from GitHub into isolated agent harness setups. Check: a new operator reaches a working instance by following only the README.

## Open questions

- The product's public name and GitHub location
- Whether extension plugins ever need synced docs. If they do, `.aiOS/docs/` gets one subfolder per plugin.
- Which skills carry agent guidance, and how they're named
