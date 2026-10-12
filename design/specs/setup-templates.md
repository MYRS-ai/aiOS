---
type: doc
created: 2026-10-12T11:58-07:00
updated: 2026-10-12T13:16-07:00
---

# Spec: setup templates

## Status

Done. Included in 0.11.0. All six starter templates live in `assets/templates/`.
Both required Python test suites pass all 64 tests, including setup from a plugin-only copy.

## Goal

Group starter templates separately from the complete fictional example.

## Scope

Move the six starter files into `setup-aios/assets/templates/` and update their consumers and references.
Keep template contents, generated destinations, and `assets/example/` unchanged.

## Requirements

1. All six starter files live in `assets/templates/`, with identical contents.
2. Setup loads the new paths and preserves existing setup behavior.
3. Documentation and context visualization resolve the new locations.

## Design

Move `config.yaml`, `glossary.md`, and the four contract templates into `assets/templates/`.
Update the setup script's template directory, guide links, design records, and visualization paths.

## Test plan

1. Compare moved files with their original contents and scan for obsolete paths.
2. Run `python3 -m unittest discover -s tests -v` and `/usr/bin/python3 -m unittest discover -s tests -v`.
3. Check changed documentation, then rebuild `design/agent-context-flow.py` and run its `--check` mode.

## Tasks

1. Move templates and update setup and documentation references.
2. Update visualization sources and verify setup, links, and freshness.

## Done when

Setup works from the plugin package, moved files retain their contents, and maintained references resolve.

## Open questions

None.
