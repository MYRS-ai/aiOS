---
type: doc
created: 2026-10-11T14:17-07:00
updated: 2026-10-12T13:16-07:00
---

# Spec: agent context flow

## Status

Done. Included in 0.11.0. The standalone visualization includes conditional reading paths, file summaries, rendered previews, scenarios, and findings.
The generator validates evidence against source text. Browser checks cover both scopes, traces, previews, navigation, and narrow screens.

## Goal

Make the intended context flow inspectable so the operator can find missing reading instructions, ambiguous conditions, and unnecessary context.

## Scope

Build a standalone `design/agent-context-flow.html`, with a reproducible generator and source-backed scenario definitions.
Cover the product repository and the packaged operator example as separate entry points. Exclude the real operator's private instance content.

This is an inspection artifact. It does not change reading instructions, install plugins, or claim to observe an agent's live context.

## Requirements

1. Begin each map at its top-level contract and show conditional paths to deeper contracts, skills, references, and work files.
2. Distinguish explicit reads, conditional navigation, ordinary references, recommended missing connections, and program execution or data access.
3. Show a short file summary on hover or keyboard focus, with a working button to open a rendered Markdown preview.
4. Keep previews inside the visualization. Resolve links between embedded files and preserve headings, lists, tables, and code blocks.
5. Provide scenario traces for product changes, vocabulary, setup, diagnosis, and representative work in the fictional operator's domains.
6. Explain why each trace includes a file and identify its supporting instruction. Label inferred ordering and recommendations explicitly.
7. Surface missing or ambiguous reading instructions with evidence and possible fixes, without silently applying those fixes.
8. Explain harness-dependent entry loading separately from agent-directed reading. Copying docs or running a script does not load its files into model context.
9. Keep the HTML usable offline without a server, external fonts, or JavaScript libraries. Show snapshot provenance and a rebuild command.
10. Check model references, standalone rendering, hover interactions, scenario selection, keyboard operation, and Markdown navigation in a browser.

## Design

Use two scope choices: product repository and operator example. The example represents an operator's aiOS without exposing the real operator's files.
Map the example's generated documentation paths to their plugin sources and make that mapping visible.

The interface combines an expandable file map, ordered scenario traces, file search, and a findings view.
Keep the selected file's conditions and evidence available beside the map. A modal displays the embedded file's rendered content.

The generator reads local files, extracts navigation links and their source lines, and adds reviewed semantic rules and scenario traces.
Source hashes allow a check command to detect drift. A file link alone is never classified as an automatic context load.

| File | Responsibility |
|---|---|
| `design/agent-context-flow.html` | Generated, standalone viewer with embedded source previews |
| `design/agent-context-flow.py` | Source inventory, evidence validation, safe Markdown rendering, and freshness check |
| `design/agent-context-flow.json` | Reviewed scenarios, semantic connections, findings, and scope boundaries |
| `design/agent-context-flow.template.html` | Offline interface, map, traces, inspector, and preview dialog |

Rebuilding requires Python-Markdown. The saved viewer and the generator's `--check` command do not.
The generator excludes docs copies, logs, interpreter caches, and its own generated output from the source inventory.
Generated docs paths preview plugin source and never claim to reflect the locally installed plugin.

## Test plan

1. Generate the HTML and validate every scenario node, edge, evidence source, and rendered internal link.
2. Run the generator's freshness check against the current repository.
3. Open the file directly in Chromium using Playwright. Exercise both scopes, scenarios, search, hover previews, modal links, and keyboard dismissal.
4. Inspect desktop and narrow-screen screenshots. Check for JavaScript errors and unintended network requests.
5. Review the findings against their cited source lines and distinguish current official harness documentation from historical repository tests.
6. Run repository checks and `git diff --check` on the changed files.

## Tasks

1. Audit source reading rules and gather representative traces.
2. Build the source model and standalone interactive interface.
3. Connect the artifact and generator from the design contract.
4. Validate data, interactions, readability, and snapshot freshness.

## Done when

- The operator can follow a scenario from entry to task files and inspect the condition behind each step.
- File summaries reveal working rendered previews, including navigation to other embedded Markdown files.
- Findings point to concrete evidence and possible repairs without overstating what agents actually load.
- The artifact opens offline, passes interaction checks, and can be regenerated after source changes.

## Open questions

None. The scope labels and source snapshot explain the distinction between product development and operator use.
