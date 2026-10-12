---
type: doc
created: 2026-10-12T13:50-07:00
updated: 2026-10-12T13:50-07:00
---

# Spec: verification history

## Status

Done. Included in 0.11.1 and installed in both agent harnesses. Both required Python suites pass all 69 tests.
Routine verification of the instance reports zero file problems without the old README block. Explicit history still shows that block.

## Goal

Keep routine verification focused on current state while preserving historical evidence for troubleshooting.

## Scope

Change the diagnostic report, skill guidance, related docs, and regression tests. Preserve hook behavior and log retention.

## Requirements

1. Default verification reports current file problems and hook activity without printing historical blocked turns.
2. `--last-block` includes the latest recorded block, clearly labeled historical and separate from current file results.
3. Resolved and excluded historical problems do not appear in routine output. Current problems remain visible.
4. Historical output does not claim that a problem remains active or was resolved, particularly for files outside current scope.
5. The skill uses historical output only when investigating a blocked turn or when the operator requests history.
6. Logs remain unchanged by either report mode.

## Design

Add `--last-block` to `status.py`. Keep last-run timestamps in routine output and gate the existing blocked-turn details behind the flag.
Explain the distinction in the skill and operator docs. Keep existing checks, settings, and exit behavior.

## Test plan

- Verify clean output before any blocks and after a blocked file is corrected.
- Verify excluded historical failures stay absent from default output without being labeled resolved.
- Verify current failures still appear and explicit historical output includes the recorded block.
- Confirm report execution does not change the log.
- Run both required Python suites, check local links, and refresh the context visualization.

## Tasks

1. Change the diagnostic and add regression coverage.
2. Update skill instructions, documentation, and release notes.
3. Validate current and historical reports and refresh the visualization.

## Done when

Routine verification omits historical failures, explicit troubleshooting retains them, and all checks pass.

## Open questions

None.
