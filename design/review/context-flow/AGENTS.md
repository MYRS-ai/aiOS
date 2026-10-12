---
type: AGENTS.md
created: 2026-10-12T14:41-07:00
updated: 2026-10-12T14:43-07:00
---

# Context flow

An offline visualization of intended agent reading paths across the product and fictional operator example. It shows instructions and reviewed scenarios, not observed agent activity.

## Instructions

### Maintain the visualization

Run these steps from the product repository:

1. Review `context-flow.json` scenarios and evidence against changed source files.
2. Rebuild with `python3 design/review/context-flow/context-flow.py`.
3. Confirm freshness with `python3 design/review/context-flow/context-flow.py --check`.

Rebuilding requires Python-Markdown. The saved HTML and freshness check work without it.

- Keep the viewer offline and distinguish reading instructions, references, and program access.
- After interface changes, run the browser checks in the [spec](../../specs/context-flow.md#test-plan).

## Contents

| Path | What it holds | Read when |
|---|---|---|
| [context-flow.html](context-flow.html) | Interactive map, scenario traces, and rendered file previews | Inspecting reading conditions and possible gaps |
| [context-flow.json](context-flow.json) | Reviewed scenarios, connections, and findings with source evidence | Revising the context model after instructions change |
| [context-flow.py](context-flow.py) | Generator, evidence validation, and freshness check | Rebuilding the viewer or changing source extraction |
| [context-flow.template.html](context-flow.template.html) | Offline interface used by the generator | Changing the layout or interactions |
