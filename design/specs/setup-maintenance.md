---
type: doc
created: 2026-10-12T10:31-07:00
updated: 2026-10-12T13:16-07:00
---

# Spec: setup maintenance

## Status

Done. Included in 0.11.0, including concise contract review and task-relevant reporting in `manage-skills`.
The wording was reviewed across creation, updates, renames, retirement, reviews, and incomplete work. Front matter, links, and visualization evidence pass.

Previous verification:

- Both required Python test suites pass all 64 tests, including Python 3.9.
- A plugin-only copy resolves maintenance prerequisites and runs setup and diagnostics under the new skill paths.
- Repository checks report zero file problems. Operator contract edits correct stale skill references; generated docs were not edited.
- Scanned 69 maintained contracts, including hidden files and applicable ancestors. No retired skill invocations remain in those contracts.
- Walked through Create, Update, Review, and the diagnostic-skill rename. Contract placement, inherited coverage, and scoped reference checks are explicit.
- The context visualization validates source evidence and previews. Desktop, mobile, keyboard, hover, and touch checks pass.

## Goal

Use consistent timestamp handling, make templates identifiable, and keep maintenance instructions connected to their matching definitions.

## Scope

Change setup initialization, its templates, maintenance prerequisites, contract guidance, skill names, and the context visualization.
Correct stale skill references in applicable operator contracts. Preserve other operator content, timestamp history, and generated docs.
Do not install or release the plugin.

## Requirements

1. Setup uses the front matter check's existing fixer for newly created Markdown files. It does not calculate timestamps itself.
2. Initial files receive configured timestamps without an earlier hook event. Respect enabled checks, modes, rules, exclusions, and nested settings.
3. Existing files and the docs copy keep their contents and timestamps. Report invalid settings and fixer errors explicitly.
4. The generated top-level contract links to `.gitignore`.
5. Rename `root.md`, `workspace.md`, and `shared.md` to `top-level-contract.md`, `workspace-contract.md`, and `shared-contract.md`.
6. Contract guidance distinguishes skill maintenance instructions from contracts contained in complete examples. Preserve example `AGENTS.md` names.
7. Maintenance skills read type definitions from their own plugin's docs through relative Markdown links.
8. Source evidence, scenario traces, template mappings, and the HTML snapshot reflect the resulting paths and prerequisites.
9. Rename the skills to `aios-core:setup-aios` and `aios-core:verify-aios`. Update current invocations, discovery metadata, paths, and tests together.
10. Skill descriptions distinguish creating or extending aiOS from checking its configuration, hooks, docs copy, and files.
11. Skill creation, updates, and reviews examine applicable contracts and where agents need to discover the skill.
12. Renames search the task's folder tree and applicable ancestor contracts, including ancestors outside a nested product checkout.
13. Current skill names, paths, and invocation conditions stay consistent across contracts and maintained references. Classify remaining historical or generated matches.
14. Skill maintenance uses `aios-core:manage-agents-md` for contract edits. Contract maintenance verifies skill names and invocation conditions.
15. Keep contract review concise without losing its scope or verification requirements. Reports lead with the outcome, then essential context and needed action.

## Design

Setup tracks Markdown files only when its writer creates them. Select eligible new files through the existing scope logic.
Load the effective configuration and run only the front matter fixer. The hook's later file-selection behavior remains unchanged.
Remove timestamp placeholders from the settings contract template. Preserve existing `created` values and skipped files.

The other contract templates use descriptive filenames while their generated outputs remain `AGENTS.md`.
Keep maintenance definitions within the same source or installed plugin copy as the skill that invokes them.

### Agreed skill names

| Name | Meaning and boundary | Representative use |
|---|---|---|
| `aios-core:setup-aios` | Creates aiOS, brings existing files into it, or adds workspaces. | "Use `aios-core:setup-aios` to add a workspace." |
| `aios-core:verify-aios` | Checks settings, versions, hook activity, and files; diagnoses differences and guides repairs. | "Run `aios-core:verify-aios` after updating the plugin or when hooks fail." |

`verify-aios` replaces the full diagnostic `status` skill, briefly named `check-aios` during source review.
It does not restore the earlier, narrower `check` skill.
Keep the internal script filenames `setup.py` and `status.py`. Their roles remain creating files and producing the diagnostic report.
Preserve historical proposal wording and add a pointer to the current names where needed.

### Contract maintenance

Keep the reference review in `aios-core:manage-skills`, shared by Create, Update, and Review.
Read applicable contracts before editing. Check where the capability is used, rather than only the folder storing its package.
An existing inherited instruction can cover a skill; avoid adding the same instruction to every child contract.
For renames, inspect old names and paths across current contracts, docs, skills, templates, and examples within the task's scope.
Update sources for generated files. Report installation or regeneration steps separately from source edits.

`aios-core:manage-agents-md` checks a contract's skill names, paths, and invocation conditions against the maintained skill.
It directs package changes to `aios-core:manage-skills`. Reviewing a contract does not authorize unrelated package changes.

Reporting should fit creation, updates, renames, retirement, reviews, and incomplete work. Include details only when they support understanding, confidence, use, or a decision.

## Test plan

1. Add behavioral tests for initial timestamp creation with a different host timezone, configured rules, exclusions, disabled modes, and existing-file preservation.
2. Verify fresh setup and extension, including `.gitignore` navigation and the renamed templates.
3. Verify maintenance prerequisite links in a plugin-only copy, without an operator docs copy.
4. Run `python3 -m unittest discover -s tests -v` and `/usr/bin/python3 -m unittest discover -s tests -v`.
5. Regenerate the context visualization, validate source evidence and preview links, and run its freshness check.
6. Run repository file checks and `git diff --check`.
7. Verify installed-package discovery and both renamed scripts. Search current sources for retired skill invocations and paths.
8. Walk through Create, Update, Review, and a rename in a nested checkout to verify contract coverage and inherited placement.
9. Check authoritative operator contracts for retired invocations. Validate maintenance links, file conventions, and visualization evidence after prose edits.
10. Walk through reporting for a new skill, a small edit, a rename, retirement, reviews with or without findings, and incomplete work.

For the wording-only refinement, use the documentation checks in 5–6 and walkthrough 10. No runtime behavior changes.

## Tasks

1. Implement setup's shared timestamp initialization and behavioral tests.
2. Rename templates and reconcile documentation and maintenance prerequisites.
3. Update the context visualization and verify the completed changes.
4. Rename skills, update invocation guidance, and verify installed-package behavior.
5. Add shared contract-reference checks, correct applicable operator contracts, and reconcile definitions and visualization traces.

## Done when

All approved requirements pass their checks. The timestamp explanation distinguishes setup initialization from hook events.

## Open questions

None.
