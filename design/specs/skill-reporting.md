---
type: doc
created: 2026-10-12T11:55-07:00
updated: 2026-10-12T13:16-07:00
---

# Spec: skill reporting

## Status

Done. Included in 0.11.0. Reporting covers contract outcomes, setup readiness, and scoped verification results.

- Reviewed successful, partial, clean, and failed cases across each skill's modes.
- Front matter, local links, visualization evidence, and onboarding preview navigation pass.
- The operator's latest `manage-skills` edits remain unchanged.

Plugin installation and release remain separate.

## Goal

Help the operator understand the result, assess its limits, and take any needed action.

## Scope

Revise reporting in `manage-agents-md`, `setup-aios`, and `verify-aios`, plus the shared skill definition.
Preserve the operator's latest edits to `manage-skills`. Update context evidence to match current source instructions.
Draft skills, runtime scripts, plugin installation, and generated docs copies are outside this change.

## Requirements

1. Reports lead with the outcome and include only context needed to understand, use, or assess it.
2. Contract reports distinguish applied changes, proposed fixes, clean reviews, and cases needing no new contract.
3. Setup reports explain readiness and significant migration or workspace outcomes. Routine skipped files need no inventory.
4. Preserve hook approval and session-verification guidance for agent harnesses that remain unverified.
5. Verification reports distinguish resolved findings, remaining problems, and checks that could not run.
6. Limit verification conclusions to the checks and agent harnesses actually verified. Raw output is conditional on usefulness or request.
7. Reporting states any remaining decision or action with a specific next step.
8. Shared guidance and context evidence agree with the skill instructions.

## Design

Keep a short, tailored Report section in each skill. The shared definition records the common outcome, context, and action order.
Setup retains a conditional link to onboarding for activation and session verification.
Verification summarizes evidence without treating clean file results as proof of every hook or workspace.

## Test plan

1. Review reports against successful, partial, clean, and failed cases in each skill's modes.
2. Validate front matter and local links for changed source files.
3. Rebuild the context visualization, validate its evidence, and check freshness.
4. Check changes for whitespace issues and confirm `manage-skills` is unchanged from the turn's baseline.

No runtime behavior changes. New tests or a repeated runtime suite are unnecessary for these prose edits.

## Tasks

1. Revise the three Report sections and shared guidance.
2. Review scenario coverage and reconcile context evidence with current sources.
3. Validate the edits and record the settled reporting guidance.

## Done when

Reports explain the result and any needed action without mandatory file inventories or redundant script output.
All changed instructions pass the documentation checks.

## Open questions

None.
