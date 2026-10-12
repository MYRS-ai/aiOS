---
type: doc
created: 2026-10-12T13:13-07:00
updated: 2026-10-12T13:16-07:00
---

# Spec: plugin releases

## Status

Done. Version 0.11.0 includes the approved improvements and release history. Both required Python suites pass all 64 tests.
Installed plugins and generated docs match the source in both agent harnesses. File, link, and visualization checks pass.
Start a new session to load the updated skills; automatic hook activation in a fresh session remains an operator check.

## Goal

Release the approved improvements as 0.11.0 and keep a useful change history for future releases.

## Scope

Include the accumulated product changes, release documentation, plugin versions, validation, and local installation refresh.
Keep instance changes in their separate repository. The 1.0 release plan remains open.

## Requirements

1. Both core plugin manifests use version `0.11.0`.
2. A product changelog records meaningful changes and upgrade actions, with an `Unreleased` section for future work.
3. The product contract requires changelog upkeep and version agreement before a release.
4. The approved contract guidance and setup files use grouped instructions and expose file type definitions.
5. Automated tests pass with both required Python interpreters; links and the context visualization pass validation.
6. Installed plugins and generated docs match the release. Report any remaining session or hook approval requirement.
7. Commit and push the product changes. Commit instance changes separately; do not invent a remote for the instance.

## Design

- Keep `changelog.md` at the product repository level and link it from the README and product contract.
- Start the release history at 0.11.0. Do not reconstruct older releases from incomplete records.
- Use Added, Changed, and Fixed sections where useful; give renamed skills explicit upgrade guidance.
- Keep future release instructions in the product contract and version details in the changelog.
- Refresh each installed plugin through its agent harness. Generate docs through the installed plugin's sync code.

## Test plan

- Run `python3 -m unittest discover -s tests -v` and `/usr/bin/python3 -m unittest discover -s tests -v`.
- Check relative Markdown links, including setup output and the standalone example.
- Rebuild `design/agent-context-flow.html` and run the generator's freshness check.
- Compare plugin manifests, installed versions, and docs hashes; run `aios-core:verify-aios` in both repositories.
- Check the commit contents and confirm the product's remote branch matches the pushed commit.

## Tasks

1. Apply the approved source guidance and standardize the instance's types link.
2. Add release history and ongoing release instructions.
3. Set the plugin version and validate the release.
4. Commit and push the product changes.
5. Refresh installed plugins and generated docs, then verify the instance.
6. Commit instance changes and report any activation steps.

## Done when

The release is committed, pushed, installed, and verified, with any session activation limit stated explicitly.

## Open questions

None. The glossary wording proposal is separate and is included only if the operator approves it.
