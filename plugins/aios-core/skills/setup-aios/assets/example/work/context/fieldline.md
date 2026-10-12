---
type: doc
---

# Fieldline

Fieldline makes scheduling software for home service businesses. Dispatchers plan visits in a browser; technicians use the mobile app while travelling between visits.

This context reflects the week beginning 2026-10-05. The latest delivery decision is recorded in the [2026-10-09 review](../journal/2026-10-09-delivery-review.md).

## Product direction

The mobile team's current focus is reliable information capture at the job site. A technician should record useful information without waiting for connectivity.

The [mobile job notes project](../projects/mobile-job-notes/brief.md) addresses one part of that problem. It does not replace the dispatch board or change how visits are assigned.

## What the team knows

- Four technicians and two dispatch supervisors contributed to the [2026-10-07 observations](../journal/2026-10-07-job-note-observations.md).
- Technicians need a clear distinction between a note saved on the device and a note available to a dispatcher.
- A replay test produced a duplicate remote note. The team has held the pilot until the [readiness criteria](../projects/mobile-job-notes/acceptance.md) pass.

These observations identify problems worth testing. They do not establish how common those problems are across Fieldline's customers.

## Constraints

- Existing visit assignment must continue to work while the project changes note capture.
- The first pilot covers text notes. Photos, attachments, shared editing, and browser editing remain outside its scope.
- The team must account for interrupted connections and app restarts before exposing offline capture to pilot crews.
- Alex's regular Fieldline hours are Monday through Friday, 09:00 to 17:00, with a 30-minute lunch.

## Questions still open

| Question | Owner | Next evidence |
|---|---|---|
| Which three crews can join the pilot? | Alex | Confirmed roster and contact arrangements before any pilot starts |
| How long should unsent notes remain on a device? | Priya | A documented recommendation reviewed with the appropriate internal decision owner |
| How often do customers lose connectivity during a visit? | Erin | A proposed measurement approach; no population estimate is available yet |

The workspace contains manually recorded information. It has no live connection to Fieldline's product data, customer records, or task system.
