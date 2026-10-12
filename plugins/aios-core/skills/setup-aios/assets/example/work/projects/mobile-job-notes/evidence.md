---
type: doc
---

# Mobile job notes evidence

Evidence available at the 2026-10-09 delivery review. This record supports decisions; it does not establish that the pilot is ready.

## Sources

| Date | Evidence | Source and limitation |
|---|---|---|
| 2026-10-07 | Four technician and two dispatch-supervisor observations | [Observation journal](../../journal/2026-10-07-job-note-observations.md); a small qualitative sample |
| 2026-10-08 | Fifteen recorded runs across five note scenarios | Sam's manual review notes, transcribed below; these are not production measurements |
| 2026-10-09 | Decision to hold the pilot | [Delivery review](../../journal/2026-10-09-delivery-review.md); no start was authorized |

No automated report or live task-system connection is available in this workspace. The underlying test traces have not been attached.

## Manual test record from 2026-10-08

Sam reported three runs per scenario. Each group included two iOS runs and one Android run.

| Scenario | Result | Observation |
|---|---|---|
| Online save | 3 of 3 passed | The dispatcher view showed one complete note. |
| Connection lost before sending | 3 of 3 passed | Text remained available on the device. |
| Connection restored before first send | 3 of 3 passed | The waiting note sent once. |
| Response interrupted after the server accepted the note | 2 of 3 passed | The Android run produced two server copies after a retry. |
| State label after a completed send | 3 of 3 passed | The label changed to sent after confirmation. |

These fifteen runs are preliminary evidence. They do not meet the larger replay requirement or cover app restart and expired authentication.

## The unresolved duplicate

The reported sequence was: enter a note, send it, interrupt the response, then allow the app to retry. The Android run showed two copies with the same text.

The record does not yet show whether the retry reused its submission identifier. Mei and Luca will capture that detail on 2026-10-12.

## Evidence still needed

- A reproduction trace identifying the app version, platform, submission identifier, and resulting server records.
- Fresh replay results for ten iOS attempts and ten Android attempts using a test build with the reviewed fix.
- App-restart and expired-authentication results on both platforms.
- Confirmation that the saved, waiting, and sent labels are understandable in a follow-up observation.
- An approved pilot roster and the agreed handling of unsent notes.

The [acceptance criteria](acceptance.md) define what each result must establish. Record new evidence with its date and author; do not replace this dated summary with an unexplained pass.
