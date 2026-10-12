---
type: doc
created: 2026-10-12T14:04-07:00
updated: 2026-10-12T14:10-07:00
---

# Spec: skill display names

## Status

Done. Display names shipped in 0.11.2, and the operator confirmed the labels after restarting Codex.
The maintenance skill now names the display-name field and file.

## Goal

Preserve aiOS capitalization and readable skill titles in Codex.

## Scope

Add skill display metadata, document its location, and refresh the local plugin.

## Requirements

1. Each core skill has `agents/openai.yaml` with `interface.display_name` matching its title.
2. Skill identifiers, invocation conditions, and workflows remain unchanged.
3. The installed Codex plugin contains the metadata from source.
4. `manage-skills` identifies the display-name field and file in one concise note.

## Design

Use Codex's optional display metadata. Keep the existing plugin display name, `aiOS Core`.

## Test plan

- Compare display names with skill titles and installed copies.
- Check documentation links and regenerate the context visualization.
- Confirm displayed labels after the operator restarts Codex.
- Confirm the maintenance note matches the installed metadata format.

## Tasks

1. Add metadata and update package documentation.
2. Refresh Codex and verify the installed metadata.

## Done when

All four display names are installed. The operator's restart checks the resulting UI labels.

## Open questions

None.
