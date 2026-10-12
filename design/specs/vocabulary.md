---
type: doc
created: 2026-10-11T09:49-07:00
updated: 2026-10-12T13:16-07:00
---

# Spec: Vocabulary

## Status

Done. Included in 0.11.0, including the table layout follow-up. Earlier validation results are recorded below.

The glossary presents grouped, alphabetized tables before its usage and maintenance guidance. All 45 agreed meanings remain unchanged.

The original vocabulary pass verified:

- All 46 original concepts were reviewed. The glossary retains 45 entries and documents one retired name.
- Both Python test runs passed all 54 tests. All 349 relative links and section links resolve.
- Status reported no file problems in the product, sample, or operator's configured files.

The readability follow-up verified:

- All 45 glossary definitions remain unchanged.
- Both Python test runs passed all 54 tests. All 353 relative links and section links resolve.
- Source docs, skills, templates, and edited design records use clearer paragraphs, lists, and headings.
- The operator's generated docs copy was not edited. An existing wording change in its `naming.md` was preserved in source.
- Product and sample copies are refreshed only through the plugin's sync function during development verification.

The table layout follow-up verified:

- Seven topic tables contain all 45 terms, each defined once and alphabetized within its group.
- Every meaning matches the pre-layout source exactly. Notes retain the important distinctions and examples.
- The rendered tables have three columns. Section navigation and all 363 relative links and section links resolve.
- Workspace glossaries and the setup template use the same table structure.
- Both Python test runs passed all 54 tests. The operator's generated docs copy remains untouched.

## Goal

Give each aiOS concept one clear meaning and use it consistently across current product files. Prevent unagreed names from spreading through instructions, templates, and documentation.

## Scope

- **Included:** The glossary, naming guidance, current documentation, contracts, skills, templates, examples, and diagnostic wording.
- **Preserved:** Code identifiers, file paths, external terminology, and historical design records.
- **Excluded:** Runtime behavior changes and a plugin release.

## Requirements

1. Keep one aiOS glossary with focused topic sections and three-column tables: `Term`, `Meaning`, and `Notes`.
2. Review all 46 existing entries. Retain 31 concepts, refine 14 definitions, and retire the name `aiOS root`.
3. Use `aiOS` for the system. Describe the folder containing `.aiOS/config.yaml` directly when location or configuration scope matters.
4. Define concepts independently of storage conventions and operating policy. Link to those instructions instead of duplicating them.
5. Preserve ordinary domain meanings. Record alternatives only when they cause a specific confusion with an aiOS concept.
6. Require agreement on new or changed concepts before adding them to the glossary and propagating their names.
7. Use the same entry structure in workspace glossary templates and examples.
8. Reconcile current references to the refined concepts. Keep templates, examples, and diagnostic messages consistent.
9. Preserve extension plugin dependency policy and the existing scope and behavior of checks.
10. Use paragraphs for connected explanations, bullets for parallel points, and numbered steps for ordered actions.
11. Use headings and emphasis where they clarify hierarchy. Do not rely on single line breaks to separate independent ideas.
12. Make product documentation changes in plugin source. Verify generated copies through their sync records and preserve source wording separately from installed copies.
13. Put a linked section index before the terms and usage guidance after them. Alphabetize each group and define each term once.
14. Keep notes concise. Split groups when their subject becomes too broad; link to topic docs for longer explanations.

## Design

- `plugins/aios-core/docs/glossary.md` remains the source for agreed aiOS meanings.
- Tables use `Term`, `Meaning`, and `Notes`. Notes supply distinctions, usage guidance, examples, or links when useful.
- Seven focused sections group organization, files, agents and sessions, skills and tools, plugins, work, and enforcement.
- Definitions remain in one place. A linked section index supports lookup; maintenance guidance follows the terms.
- `docs/naming.md` covers written names. Contracts cover placement. Operator docs cover behavior.
- Existing design records hold proposed product terminology. Workspace glossary changes require the operator's agreement on meaning and examples.
- Source skills and setup templates apply the vocabulary process when introducing or changing concepts.
- Setup guidance distinguishes the operator's configured aiOS from its physical folder.
- Generated docs copies continue to use the existing sync mechanism.

## Test plan

1. Compare the rewritten glossary with all 46 reviewed entries.
2. Search current product files for retired wording and review remaining matches in context.
3. Review definitions against current documentation, code behavior, and examples.
4. Run `python3 -m unittest discover -s tests -v`.
5. Run `/usr/bin/python3 -m unittest discover -s tests -v`.
6. Run source status for the product and sample. Check relative links and scan for operator details.
7. Review the rendered document structure and confirm that generated docs were not edited by hand.
8. Compare all 45 meanings with the pre-layout source. Check grouping, alphabetical order, unique rows, and table navigation.

## Tasks

1. Rewrite the glossary and record the accepted vocabulary process.
2. Update current documentation, contracts, skills, templates, and examples.
3. Update diagnostic wording and its existing assertions where needed.
4. Review propagation, run verification, and record the results.
5. Improve readability in the edited documents and record the writing guidance.
6. Convert the glossary and workspace templates to grouped tables and verify that agreed meanings are preserved.

## Done when

All requirements pass their checks, both test runs pass, and product and sample status report no file problems. Source changes are ready for a later plugin release.

## Open questions

None.
