---
type: doc
created: 2026-10-11T09:34-07:00
updated: 2026-10-12T13:16-07:00
---

# Spec: consistency fixes

## Status

Done. Included in 0.11.0. Configuration validation, front matter parsing, and the approved documentation corrections pass both required test suites.

All 54 tests pass on Python 3.9 and the current Python. These changes have not been released.

## Goal

Make checks report invalid settings and interpret front matter correctly. Reconcile current instructions with settled behavior.

## Scope

- **Included:** Configuration diagnostics, front matter values, regression tests, and the approved documentation corrections.
- **Excluded:** Rename detection, vocabulary renaming, new plugin features, releases, and changes to installed plugin caches.

## Requirements

1. Inline and multiline lists in supported configuration settings select the same files. Verify through hook tests.
2. Invalid configuration types, unknown checks, and invalid modes produce explicit diagnostics instead of a successful empty check.
3. Hooks report configuration failures without a traceback or silent allowance. The existing block limit still applies.
4. Quoted front matter values and inline comments are interpreted as values. Test accepted quoted types and skill names.
5. Empty descriptions and skill fields present only inside another field fail validation. Test both cases.
6. Preserve file content and existing timestamps while parsing. Keep the timestamp tests passing.
7. Correct the retired skill description, delegation template, docs-copy warnings, release dependency, and missing doc definition.
8. Scope vocabulary guidance to aiOS meanings. Preserve unsettled names and the operator's existing edits.
9. The complete suite passes on Python 3.9 and the current Python. Status reports no file problems.

## Design

- Keep parsing within the supported Python 3.9 standard library implementation.
- Support the configuration forms documented by aiOS and reject unsupported forms with actionable messages.
- Validate configuration before selecting files. Keep runtime failure reporting consistent with hook logging and the block limit.
- Read top-level skill fields as decoded strings. Preserve source lines for timestamp updates.
- Update documentation in the product source. Refresh generated docs through the existing synchronization function.

## Test plan

1. Add hook-interface tests for requirements 1 through 6, including malformed settings and recovery after correction.
2. Review documentation changes against requirements 7 and 8. Check relative links and current skill references.
3. Run the tests and status report:

```bash
python3 -m unittest discover -s tests -v
/usr/bin/python3 -m unittest discover -s tests -v
python3 plugins/aios-core/skills/verify-aios/scripts/status.py
```

## Tasks

1. Correct configuration validation and front matter parsing with regression tests.
2. Reconcile the approved documentation and template differences.
3. Review changes, run the test plan, and report remaining terminology decisions.

## Done when

Every requirement passes its test or review. The operator's existing changes remain intact.

## Open questions

None for this scope. Rename detection and vocabulary naming decisions remain outside it.
