---
type: doc
created: 2026-10-03T16:45-07:00
updated: 2026-10-12T13:50-07:00
---

# Decisions

This file records settled product decisions. Proposals remain in the other design docs.

## Folders and instructions

- Folder names are lowercase, hyphenated, and one to four words.
- Each folder's `AGENTS.md` is its contract. Add another canonical file only when no existing convention meets the need.
- Use `AGENTS.md` for instruction files. Do not add `CLAUDE.md` anywhere in the repo.
- Contracts provide task-based navigation. Group repetitive files while keeping applicable instructions and relevant resources discoverable through the listed paths.
- Group related instructions under descriptive headings. Record operator preferences alongside the instructions they relate to.
- Top-level operator contracts link to `.aiOS/docs/types/AGENTS.md` and require the applicable definition before creating or editing Markdown.

## Terms and names

- The aiOS glossary lives in the core plugin's `docs/glossary.md` and applies to every workspace. Only core plugin updates change it.
- Each workspace has a workspace glossary at `docs/glossary.md`. `shared/docs/glossary.md` holds terms that more than one workspace uses.
- Agents read glossaries in this order: aiOS, shared, then the current workspace. A workspace glossary adds terms without changing aiOS meanings. Ordinary domain meanings remain valid in their own context.
- Agents read the aiOS glossary and naming conventions before they create or change contracts, glossaries, skills, plugins, or `.aiOS/` settings. They read the shared and workspace glossaries before working in a workspace.
- The glossary uses topic sections with `Term`, `Meaning`, and `Notes` tables. Notes hold concise distinctions, usage guidance, examples, or links.
- Terms are alphabetical within each group and defined once. A linked section index precedes the tables; usage and maintenance guidance follows them.
- Small workspace glossaries start with one table. Add groups as topics grow, and split broad groups before splitting the glossary into files.
- Longer explanations belong in topic docs. If the glossary later spans files, retain its index and one authoritative definition per term.
- Propose a new concept, changed meaning, or replacement name with its boundaries and representative sentences in existing design records. Get agreement before propagating it.
- Update current instructions, docs, templates, examples, and messages together after agreement. Review previous wording in context and check related definitions.
- Record alternatives only for specific confusions. Ordinary domain meanings, quotations, identifiers, and external product names keep their wording.
- Meanings belong in the glossary, spelling in naming conventions, placement in contracts, and operating policy in operator docs.
- Retire `aiOS root` from current prose. Use `aiOS` for the system and describe the folder containing `.aiOS/config.yaml` directly when location matters.
- Naming conventions live in the core plugin's `docs/naming.md`.
- Refer to a plugin skill as `plugin:skill`, such as `aios-core:setup-aios`.

## Agents and plugins

- The main agent coordinates work, delegates to subagents, and briefs them.
- The skills and agent roles in `plugins/aios-core/drafts/` remain drafts. Extension plugin folders are placeholders.
- The core plugin ships four skills in `plugins/aios-core/skills/`: setup-aios, verify-aios, manage-agents-md, and manage-skills.
- `aios-core:setup-aios` creates aiOS, brings existing files into it, or adds workspaces.
- `aios-core:verify-aios` verifies settings, versions, hook activity, and files. It covers routine verification and troubleshooting.
- These names replace `aios-core:setup` and `aios-core:status`. The diagnostic skill was briefly named `check-aios` during source review.
- Internal script names remain `setup.py` and `status.py`.
- A skill exists only when it does work that no other skill, hook, or script does. The earlier `aios-core:check` skill was retired because hooks and the diagnostic report cover its work.
- `aios-core:verify-aios` names the full diagnostic workflow; it does not restore that retired skill.
- `docs/types/skill-md.md` defines the skill package. Skills an operator maintains live in their workspace's `skills/` folder, or in `shared/skills/`.
- Assets may include templates, examples, and other supporting material, grouped into subfolders when useful. Short workflow modes can remain inline.
- Read applicable ancestor contracts before editing. Keep inherited instructions in the ancestor that owns them; create additional contracts only when needed.
- Maintenance skills link directly to type definitions in their own plugin. Those prerequisites work before setup and match the skill's version.
- Skill creation, updates, and reviews check applicable contracts and where agents need to discover the skill. Existing inherited instructions count.
- Skill updates list package files and read affected files, dependencies, and uses until the impact is understood. Comprehensive reviews read whole packages.
- Maintenance skills distinguish alternative workflows from shared checks. Descriptive task headings identify the alternatives; workflow steps link to separate shared-check sections.
- Rename searches cover current references and applicable ancestor contracts, including ancestors outside a nested Git checkout.
- Skill maintenance uses `aios-core:manage-agents-md` for contract edits. Contract maintenance checks skill names, paths, and invocation conditions.
- Skill reports lead with the outcome and its effect, followed by essential context and any needed decision or action.
- Tailor reports to each skill: contract outcomes, setup readiness, or scoped verification results. Include file inventories and script output only when useful or requested.
- Update maintained sources and report remaining installation or regeneration steps. Preserve historical records and generated copies during source edits.
- `SKILL.md` governs skill maintenance. Contracts inside complete examples govern only those examples; templates describe their generated destinations.
- The core plugin lives at `plugins/aios-core/`. It holds system-level skills and hooks.
- Extension plugins come later. Each extends aiOS for one area of capability, such as writing and editing or creative media.
- An extension plugin may use the core plugin but should not depend on another extension plugin.
- Define extension plugin boundaries around shared goals, workflows, and components that work together.

## Front matter

- The standard fields are `type`, `created`, and `updated`.
- `created` and `updated` use ISO 8601 with minutes and a UTC offset. The configured time zone defaults to `America/Los_Angeles`.
- `status` is not a universal field. It may return for some file types.
- `AGENTS.md` has its own type, `type: AGENTS.md`, and needs its own type definition or template.
- Built-in file types have definitions in the core plugin's `docs/types/` folder, one file per type. Operators can configure custom types.
- Required front matter fields are decoded top-level values. Nested fields do not satisfy top-level requirements.

## Enforcement

- The aios-core plugin provides hooks in one `hooks.json` for Claude Code and Codex.
- Hook definitions and shared check code live in the plugin's `hooks/` folder. Skill scripts live inside their skills and reuse that code.
- Hooks check changed files at the end of each turn. Check modes and the block limit determine whether problems block the turn.
- After checks permit completion, enabled fixers fill in timestamps where configured.
- `.aiOS/config.yaml` enables enforcement for its containing folder and holds `enabled`, `include`, `exclude`, and settings for individual checks.
- The plugin searches upward from the session folder for that file. Without it, the plugin does nothing.
- Subfolders containing their own `.aiOS/config.yaml` use separate settings. Parent checks skip those folders and their contents.
- Settings use a bounded YAML reader from the Python standard library. Unsupported syntax and invalid settings produce explicit configuration diagnostics.
- Configuration failures follow the hook block limit. The diagnostic script exits with an error instead of reporting a successful file check.
- Routine verification reports current findings and hook activity. Historical blocks appear only with `--last-block` for explicit troubleshooting.
- Keep historical evidence separate from current results. An excluded file is unverified; exclusion does not prove a repair.

## Setup and product docs

- The setup skill confirms workspaces with the operator before creating contracts and settings.
- Setup creates a placeholder glossary in each workspace, including `shared/`.
- Setup preserves existing files and adds missing pieces. It appends the log exclusion to `.gitignore` when needed.
- Setup timestamps newly created Markdown through the existing front matter fixer, using effective settings and scope. Existing files remain unchanged.
- This initialization works before a hook session exists. Later hook events keep their existing file-selection behavior.
- The setup skill includes one complete fictional example at `assets/example/`, available after plugin installation.
- Setup adaptation and example maintenance guidance live in `references/example.md`. Example files contain fictional operator content without setup callouts.
- Starter templates live in `assets/templates/` and create initial files. Agents use the example to structure confirmed operator facts; the script never clones it into an operator's aiOS.
- The settings contract template is `assets/templates/settings-contract.md`. Setup writes it to `.aiOS/AGENTS.md`; it does not govern the skill's assets folder.
- Other contract templates are `top-level-contract.md`, `workspace-contract.md`, and `shared-contract.md`. The top-level contract links to `.gitignore`.
- Every setup mode reads relevant example content after the interview. Domain-specific folders follow the operator's needs rather than a mandatory example layout.
- Tests validate a temporary standalone example after generating its docs copy. They also verify a copy containing only the installed plugin.
- Generated docs and logs stay out of the packaged example. The repository has no separate `examples/` copy.
- The start hook syncs core plugin docs into `.aiOS/docs/` before logging, even when checks are off.
- Sync records the plugin version, source hash, and copied file hashes. Newer versions or changed source content replace the copy.
- The next session start also restores local edits to the copy, unless it came from a newer plugin.
- An older plugin keeps the newer copy and tells the agent to update that agent harness's plugin.
- The docs-copy check warns about edits to the copy. Custom docs belong in a workspace's `docs/` folder.
- The product README omits front matter for GitHub rendering and is excluded from this repo's checks.

## Design records

- `design/` holds research, proposals, specs, and `decisions.md`. It does not ship in any plugin.
- Proposals form the backlog. The operator sets their priority and decides which become specs.
- A spec gives a subagent enough detail to implement and test the work. Implementation starts only from a ready spec.
- When a spec's work ships, its settled design moves into `decisions.md`.
- Open topics get no placeholder file.

## Release history

- `changelog.md` records meaningful product changes and upgrade actions, starting with 0.11.0.
- Add completed changes under `Unreleased`. At release, move them to a dated version section matching both core plugin manifests.
- Version 0.11.0 remains a pre-1.0 release. The first stable release still follows its separate release spec.

## Context visualization

- [Agent context flow](agent-context-flow.html) is a standalone design artifact with an offline map, scenario traces, and source previews.
- Product development and the fictional operator example have separate entry points. Private operator files stay outside this artifact.
- Reading instructions, conditional paths, references, proposed connections, program execution, data access, and docs copying remain distinct.
- Scenario traces show reviewed intended reads. They do not prove an agent loaded the files or measure its live context.
- The generator validates source evidence and records file hashes. Review the model and rebuild after reading instructions change.
- Findings propose policy improvements. Their inclusion in the visualization does not settle or implement those proposals.
