# Import files

Use [scripts/migrate.py](../scripts/migrate.py) for an approved batch of regular files. It leaves sources untouched and refuses existing destinations.
Handle repositories, worktrees, and symbolic links separately, following the migration plan.

## Prepare

1. Create `mapping.json` under the migration project's `batches/<batch-name>/`, with one entry per file. Use absolute paths:

   ```json
   {
     "files": [
       {
         "source": "/source/project/notes.md",
         "destination": "/aios/work/projects/project/notes.md",
         "type": "doc"
       }
     ]
   }
   ```

   - Set `type` to `doc` or `AGENTS.md` for ordinary aiOS Markdown files.
   - Omit `type` for skill packages, other front matter standards, and other formats. Their content stays unchanged.
   - For approved adaptations, store prepared content in the batch folder and reference it with `content_file`. Dates still come from `source`.
   - Use real paths; the script rejects symbolic links and `.git` entries.

2. Preview the mapping. Confirm destinations, hashes, and source dates against the plan:

   ```sh
   python3 <skill>/scripts/migrate.py <mapping.json> --zone <configured-zone>
   ```

   The script reads filesystem creation and modification times. If creation time is unavailable, resolve that date before importing.

## Apply and verify

1. Apply the reviewed mapping, saving a new copy record in the same batch folder:

   ```sh
   python3 <skill>/scripts/migrate.py <mapping.json> --zone <configured-zone> --apply --record <record.json>
   ```

   The script adds `migrated` to eligible files and restores source modification times after writing.
   The record saves source and destination hashes, dates, and progress after each copy.

2. Run [Verify a batch](migrate.md#verify-a-batch). Link the mapping and record from the migration plan.
3. If interrupted, compare existing files with the record before preparing a mapping for unfinished items. Never overwrite completed or unrecorded output.

The script runs only when invoked. It creates no hook, persistent migration mode, or settings override.
