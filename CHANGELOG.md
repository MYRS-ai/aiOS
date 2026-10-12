---
type: doc
created: 2026-10-12T13:13-07:00
updated: 2026-10-12T14:41-07:00
---

# Changelog

Meaningful aiOS product changes and upgrade actions. This history starts with 0.11.0; earlier releases are recorded in Git history.
Versions remain below 1.0 while the first stable release is being prepared.

## Unreleased

No unreleased changes.

## 0.11.1 — October 12th, 2026

### Fixed

- Routine verification no longer repeats historical blocked turns as potential current problems. Use `--last-block` for explicit troubleshooting.
- Added explicit Codex display names for all four core skills, including `Manage AGENTS.md`, preserving aiOS capitalization.

### Changed

- Streamlined contract and verification reporting around results, relevant context, and needed actions.
- Documented Codex display metadata in the skill definition and `manage-skills` package guidance.

## 0.11.0 — October 12th, 2026

### Added

- A complete fictional aiOS inside the setup skill, with examples of work, business, and household planning.
- Setup guidance for adapting the example to an operator's confirmed needs and facts.
- An offline context visualization with reading conditions, scenario traces, source previews, and findings.
- General Markdown document guidance alongside the contract and skill definitions.

### Changed

- Renamed `aios-core:setup` to `aios-core:setup-aios` and `aios-core:status` to `aios-core:verify-aios`.
- Grouped setup starter files in `assets/templates/`; the complete example lives in `assets/example/`.
- Organized the glossary into topic tables and added vocabulary agreement and maintenance guidance.
- Retired `aiOS root` from current prose. Location instructions identify the folder containing `.aiOS/config.yaml`.
- Made contract and skill maintenance check discovery, inherited instructions, and references after names or paths change.
- Focused skill updates on affected files and dependencies; comprehensive reviews still read whole packages.
- Streamlined skill reports around outcomes, essential context, and needed actions.
- Grouped related contract instructions and linked file type definitions from setup's top-level contracts.

### Fixed

- Invalid check settings and unsupported YAML now produce explicit diagnostics instead of silently changing behavior.
- Required front matter fields use decoded top-level values; nested fields cannot satisfy those requirements.
- Setup initializes timestamps through the same fixer as hooks, respecting the configured time zone and check scope.
- Documentation now reflects when generated docs refresh and how older plugins preserve a newer docs copy.

### Upgrade

1. Update the plugin in each agent harness using the [update instructions](plugins/aios-core/docs/onboarding.md#5-update-the-plugin).
2. Start a new session so the updated skills load and the docs copy refreshes. Approve changed hooks if prompted.
3. Update maintained skill references to `aios-core:setup-aios` and `aios-core:verify-aios`.
4. Run `aios-core:verify-aios` to check settings, docs, hook activity, and files.

`aios-core:check-aios`, used during source review, also becomes `aios-core:verify-aios`.
The plugin refreshes generated docs. Existing operator contracts and content remain operator-maintained.
