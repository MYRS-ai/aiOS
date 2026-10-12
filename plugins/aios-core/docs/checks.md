---
type: doc
created: 2026-10-04T11:20-07:00
updated: 2026-10-12T10:47-07:00
---

# Check settings and development

This guide covers check settings and how to add or change a check. See [hooks.md](hooks.md) for when hooks run.

## How settings work

The `checks:` section of `.aiOS/config.yaml` overrides the `checks.yaml` plugin defaults. Each override replaces the entire setting. Overriding `frontmatter.rules` replaces all default rules, so include every rule you want to keep.

Settings cover the folder containing `.aiOS/config.yaml` and its contents. Checks skip subfolders with their own `.aiOS/config.yaml`; those settings apply separately. Checks also skip symbolic links, so they never read or change files outside the folder being checked.

A file that a check can't read, such as one that isn't valid UTF-8, is reported as a problem, and the other files are still checked.

### Supported YAML

Configuration supports nested mappings, single-line scalar values, and inline or indented multiline lists of scalar values.

- Use spaces for indentation.
- Quote strings containing `#` or `: `.
- Escape an apostrophe inside a single-quoted string as `''`.
- Use JSON-compatible escapes inside double-quoted strings.

Multiline strings, anchors, aliases, and nonempty inline mappings are unsupported and produce configuration errors. Duplicate setting names also produce errors.

These lists select the same files:

```yaml
include: ["personal/**", "shared/**"]
```

```yaml
include:
  - "personal/**"
  - "shared/**"
```

### Configuration errors

aiOS validates configuration before selecting files. Incorrect types, unknown checks, and unsupported modes produce explicit diagnostics.

- The start hook reports invalid configuration.
- The stop hook blocks until configuration is corrected or `max_blocks` is reached. An invalid limit defaults to 2.
- The status script exits with an error and reports that file checks did not run.

### Check modes and exclusions

Every check accepts `mode` and `exclude`. Set `mode` to one of these values:

- `block`: let the stop hook block on failure.
- `warn`: report failures without blocking.
- `off`: skip the check.

After the `max_blocks` limit, blocking failures become warnings.

`exclude` lists path patterns to skip, relative to the folder containing `.aiOS/config.yaml`.

## The frontmatter check

Each file uses the first matching rule. Put specific rules before general ones.

The default configuration defines three rules.

- `skill`: checks `SKILL.md` for the `name` and `description` required by the Agent Skills format.
- `skill-resource`: skips front matter checks for other files within a folder containing `SKILL.md`.
- `default`: checks all other Markdown files and requires an allowed `type`. Its fixer adds `created` and `updated` timestamps.

### Settings

| Setting | What it does |
|---|---|
| `match` | Files to check: `skill`, `skill-resource`, or path patterns |
| `required` | Fields each file must contain. Missing or empty fields fail the check. |
| `allowed` | Permitted values for each field |
| `timestamps` | Fields the hook fills in: `created`, `updated`, or both. The hook adds `created` only when it is missing and never changes it after that. It sets `updated` on every change. |
| `format` | `agent-skills` checks the file against the Agent Skills standard |
| `zone` | Time zone for timestamps. It applies to the whole check, so set it beside `rules`, not inside a rule. |

### Folder specific rules

To set requirements for a folder, add a rule before `default`. This example applies to every file in any folder named `meetings`. It requires `type: meeting` and a `date` field, and fills in both timestamps:

```yaml
meetings:
  match: ["**/meetings/**"]
  required: [type, date]
  allowed:
    type: [meeting]
  timestamps: [created, updated]
```

## The names check

For each selected file, `names` checks its folders below the folder containing `.aiOS/config.yaml`.

- Names must be lowercase, with one to four words separated by hyphens.
- The check ignores file names and hidden folders, such as `.aiOS/`.

## The docs-copy check

The `docs-copy` check warns when a file in `.aiOS/docs/` no longer matches what the last sync wrote. The sync records each file's hash in `.aiOS/docs/.sync.json`.

These files are copies of the aios-core docs. The next session start restores edits to the copy. Make custom changes in a workspace's `docs/` folder instead.

- Its default mode is `warn`.
- It covers Markdown and other files, including images.
- Markdown front matter checks still apply to the copy.
- The timestamp fixer never changes files in the copy.
- A fresh copy reports no warnings.

## Add or change a check

A check needs a Python file in the core plugin's `hooks/checks/` folder and a matching entry in `checks.yaml`. `hooks/hooks.py` calls these functions when defined:

- `check(files, settings, root)` returns a `(path, message)` pair for each problem. Each message should tell the agent how to fix it.
- `fix(files, settings, root)` edits files and returns their paths. Fixes run only when the hook allows the turn to end.

Both functions receive these arguments:

- `files`: absolute paths to Markdown files and other files in the docs copy. Select the file types the check supports.
- `settings`: the combined check defaults and configuration overrides.
- `root`: the folder containing `.aiOS/config.yaml`. Return paths relative to this folder.

Use only the Python 3.9 standard library. Read YAML with `common.py`; PyYAML is not included with macOS's Python.

To verify a change:

1. Keep the check defaults and the setup template consistent when their settings change.
2. Run enabled checks on all files in scope with the `aios-core:verify-aios` skill's script. `<core plugin>` means the installed `aios-core` folder:

   ```bash
   python3 "<core plugin>/skills/verify-aios/scripts/status.py"
   ```

3. Confirm that the Files section reports no problems and the command exits without an error.

A crash during a hook run stops the remaining checks. The turn ends without a check result in the log.
