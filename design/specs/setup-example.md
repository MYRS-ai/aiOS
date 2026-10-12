---
type: doc
created: 2026-10-11T11:23-07:00
updated: 2026-10-12T13:16-07:00
---

# Spec: setup example

## Status

Done. Included in 0.11.0. The packaged example, adaptation guide, setup connections, regression tests, and settings contract template rename are complete.

Promoted from the [setup example proposal](../proposals/setup-example.md).

## Goal

Give setup agents a complete, coherent example of an operator's aiOS, available after the core plugin is installed.

## Scope

Replace the small repository-only sample with one fictional example inside the setup skill. Update setup guidance, navigation, and tests.

Keep the existing setup script and starter templates. This work does not install the plugin or create external schedules and accounts.

## Requirements

1. Keep the example at `plugins/aios-core/skills/setup-aios/assets/example/` and remove the old `examples/` folder.
2. Use the proposal's fictional operator, Alex Rivera, with `work/`, `studio/`, `home/`, and `shared/` workspaces.
3. Populate contracts, context, projects, routines, workflows, journals, and grouped glossaries with specific, connected content.
4. Show domain-specific organization through studio clients and products, and household goals. Create only useful, populated folders.
5. Keep adaptation and maintenance guidance in `references/example.md`. Example files contain operator content, without setup callouts or placeholders.
6. Require every setup mode to consult the guide and relevant example files before writing operator content.
7. Retain starter templates for mechanical creation. Agents adapt content from interview evidence instead of copying fictional facts.
8. Keep generated docs and logs out of the example's tracked files. Validate a temporary standalone copy through the shipped setup and status scripts.
9. Keep one authoritative definition per term, current vocabulary, valid links, and accurate contract navigation.
10. Ensure tests can use the relocated example and a copy of only the installed plugin, without relying on repository-only files.
11. Name the settings contract template `assets/templates/settings-contract.md`. Setup must still create `.aiOS/AGENTS.md` with the same content.

## Design

The example shows Alex leading a mobile product team at Fieldline, running Rivera Studio, and managing family life.

| Workspace | Connected examples |
|---|---|
| `work/` | Team context, a mobile job-notes project, a weekly delivery review, its workflow, and a recorded review |
| `studio/` | Business context, a discovery client, digital products, a Tally display batch, a studio review, and its workflow |
| `home/` | Family context, a household project, a weekly plan, personal goals, and a recorded household review |
| `shared/` | Writing criteria, cross-domain planning guidance, shared terms, and a planning procedure |

The setup reference explains the operator profile, interview-to-file mapping, representative reading paths, and adaptation checks.
It also explains how maintainers generate docs in a temporary copy before validating links and conventions.

Example contracts describe their fictional folders. The setup guide identifies all content as fictional and limits its use to reference material.
The example's top-level purpose also identifies Alex as fictional, so reading its contracts cannot silently change the current operator's identity.

The setup script continues creating minimal contracts, settings, and glossaries. It does not copy the example into an operator's files.
Keep existing code identifiers such as `root` unless a path change requires an update. Retired `aiOS root` wording stays out of current guidance.

The settings contract template uses `settings-contract.md` so agents do not confuse it with instructions for `assets/`.
Update the setup script, context visualization model, and template-path resolver together. Preserve `AGENTS.md` names inside the complete example.

## Test plan

1. Run `python3 -m unittest discover -s tests -v` and `/usr/bin/python3 -m unittest discover -s tests -v`.
2. Validate a temporary example copy after running the setup script. Check front matter, names, generated docs, and every Markdown link.
3. Verify the example and its guide exist in a copy of only `plugins/aios-core/`.
4. Review each content chain from context through project or routine to workflow and journal. Confirm its names, dates, and state agree.
5. Search active docs and tests for stale sample paths, retired wording, setup callouts, and unfilled placeholders.
6. Run `git diff --check` and inspect the example's tracked files for generated state.
7. Verify the renamed template retains its content and setup still creates `.aiOS/AGENTS.md`. Rebuild the context visualization and check freshness.

### Validation results

- The example contains 79 Markdown files, including 33 contracts, across three domains and shared resources.
- All contracts cover their immediate contents. Workspace glossaries have unique terms in alphabetical topic groups.
- Every example Markdown link and heading anchor resolves after generating documentation in a temporary copy.
- Links and heading anchors also resolve in 72 product Markdown files outside output templates.
- A copy containing only the core plugin can set up and validate its bundled example using its own scripts.
- Both full test runs passed: 57 tests on the current Python and 57 tests on Python 3.9.
- The source example contains no generated docs or logs, setup callouts, or retired system name.
- Current navigation and tests use the packaged example. The superseded repository-level example was removed.
- The settings contract template is `settings-contract.md`, with its contents preserved. Fresh setup creates the same `.aiOS/AGENTS.md`, and repeat setup preserves it.
- Both 57-test suites passed after the rename. The context model resolves the renamed template, its links, and its source evidence.

## Tasks

1. Write the three fictional domain workspaces with complete content and contracts.
2. Write the shared workspace, top-level contract, settings, and adaptation reference.
3. Connect all setup modes and product navigation to the packaged example.
4. Replace test fixture paths and add coverage for the installed example.
5. Remove the old example after preserving its current working contents outside the repository.
6. Run the checks and record the resulting design and validation.
7. Rename the settings contract template, update its references, and verify unchanged setup output.

## Done when

- An installed setup skill contains the example and tells the agent how to use it.
- All four workspaces contain linked, usable content without fabricated operator facts leaking into setup output.
- A standalone example passes checks, all links resolve after docs generation, and both supported Python test runs pass.
- Current navigation and tests use the packaged example, with no second example copy in the product repository.

## Open questions

None. Separate guidance removes the need for setup callouts or a new callout check. Release timing remains outside this task.
