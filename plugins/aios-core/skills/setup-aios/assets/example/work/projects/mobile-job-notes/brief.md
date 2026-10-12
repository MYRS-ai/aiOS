---
type: doc
---

# Mobile job notes

Give technicians a dependable way to record a text note during a visit, including when their connection is interrupted.

## Current state

| Item | Current record |
|---|---|
| Product owner | Alex Rivera |
| Engineering owner | Priya Shah |
| State | In progress; pilot held |
| Last reviewed | 2026-10-09 |
| Next decision | Readiness review planned for 2026-10-13 |
| Earliest proposed pilot start | 2026-10-15, only if the readiness gate passes |

The [2026-10-09 review](../../journal/2026-10-09-delivery-review.md) kept the pilot on hold after a duplicate appeared during replay. No pilot crew has received the change.

## Why this project exists

The [2026-10-07 observations](../../journal/2026-10-07-job-note-observations.md) showed technicians checking whether a note had reached the dispatcher. They could not consistently distinguish a local save from a completed send.

The project separates those states and tests whether interrupted delivery preserves a single complete note. See the [evidence record](evidence.md) for sample sizes and limits.

## Scope

- Create and read text notes attached to an existing visit.
- Preserve unsent text through a connection interruption and an app restart.
- Show whether a note is saved locally, waiting to send, or sent.
- Keep one server copy when a submission is repeated.

Photos, attachments, concurrent editing, browser editing, and changes to visit assignment are outside this project.

## Next action

On 2026-10-12, Mei and Luca will reproduce the duplicate submission together and record their proposed fix. Priya will review that approach before Sam begins a fresh replay run.

This is a planned action. The [plan](plan.md) identifies its expected evidence and dependent work.

## Completion

The project ends after the [readiness gate and pilot completion criteria](acceptance.md) pass. Alex records the resulting wider-release or stop decision, and the team documents who supports the delivered behavior.
