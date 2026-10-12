---
type: doc
created: 2026-10-12T12:22-07:00
updated: 2026-10-12T14:41-07:00
---

# Spec: type guidance

## Status

Done. Included in 0.11.0. Contract guidance and setup contracts use grouped instructions and expose file type definitions.
Fresh setup, the standalone example, links, and visualization checks pass.

## Goal

Keep type definitions and maintenance instructions consistent with current skill packages and concise reporting.

## Scope

Update the skill and contract definitions, contract creation workflow, feature summary, and context visualization.
Apply task-based contract navigation to the screenshot collection. Use targeted reading for skill updates and complete reading for reviews.
Preserve the operator's wording elsewhere, including reporting and reference-search scope.
Clarify the same heading hierarchy in both maintenance skills and the skill definition.
Align the contract definition, maintenance workflow, starter contract, and fictional example with the approved grouped instructions.

## Requirements

1. Assets include templates, examples, and other supporting material, with optional grouping folders.
2. Short workflow modes may remain inline; substantial detail belongs in references.
3. Contract guidance requires reading applicable ancestors before editing and retaining shared instructions there.
4. Contract creation, parent navigation, and verification depend on a contract being needed.
5. Shared reporting guidance retains outcome, context, and action without the removed reporting distinctions.
6. The verification feature summary and context visualization reflect current instructions.
7. Contracts provide clear paths to relevant resources without requiring a row for every file.
8. The screenshot contract keeps naming instructions and links to the app and CLI sections of onboarding.
9. Skill updates list package files, then read affected files, dependencies, and uses until the impact is understood.
10. Comprehensive skill reviews read the whole package. Reading guidance uses concise steps without a redundant fallback instruction.
11. Maintenance skills identify Create, Update, and Review as alternative workflows with descriptive headings.
12. Shared checks sit outside those alternatives, with working links from the steps that use them.
13. Workflow and upkeep guidance separates parallel instructions into concise bullets without changing their scope.
14. Contract guidance groups related instructions under descriptive headings and records preferences alongside related instructions.
15. Top-level contracts require the applicable file type definition before creating or editing Markdown, using a portable type-index link.
16. The starter contract and fictional example consolidate related instructions while preserving their content, relevant anchors, and boundaries.

## Design

Replace the affected wording in `types/skill-md.md`, `types/agents-md.md`, and the maintenance skills.
Update `features.md` and visualization evidence. Keep lasting conventions in type definitions and procedures in skills.
Align contract coverage checks with navigation needs. Show targeted update reads separately from comprehensive review reads in the context model.

## Test plan

1. Walk through inline and referenced modes, asset grouping, and contract creation with both decision outcomes.
2. Check front matter, Markdown links, and changed-line whitespace.
3. Rebuild `design/review/context-flow/context-flow.py`, validate source evidence and preview links, then run its `--check` mode.
4. Walk through screenshot discovery, a scoped skill update, and a comprehensive skill review.
5. Confirm reporting edits and reference-search scope remain unchanged.
6. Check heading hierarchy and links for all three workflows in both maintenance skills.
7. Validate type-index links in fresh setup and a temporary example copy. Confirm existing instructions and fictional boundaries remain intact.

## Tasks

1. Align the approved source instructions and feature summary.
2. Review context evidence, validate documentation, and record settled guidance.

## Done when

The approved conventions and workflows agree across maintained sources, and documentation and visualization checks pass.

## Open questions

None.
