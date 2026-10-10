# Start fresh

Builds a new aiOS root when the interview is the only source of context.

1. Interview the operator with [interview.md](interview.md).
2. Propose the structure as a folder tree. Give each workspace a name and a one-sentence purpose.
   - Names are one to four lowercase words separated by hyphens. `shared` is reserved for resources more than one domain uses.
   - Show the subfolders each workspace needs, such as `context/`, `projects/`, `routines/`, `workflows/`, and `journal/`.
   - Build nothing until the operator confirms the structure.
3. Run the setup script once, with every confirmed workspace:

   ```bash
   python3 <skill>/scripts/setup.py [folder] --workspace NAME="PURPOSE" --workspace NAME="PURPOSE"
   ```

   `<skill>` is this skill's folder. `folder` defaults to the current folder.
   The script creates `.aiOS/config.yaml`, the docs copy, the root and workspace contracts, a glossary in each workspace, and `shared/`. It adds `.aiOS/logs/` to `.gitignore`.
   It never overwrites a file. Review the files it reports as skipped.
4. Write each workspace's content from the interview:
   - Expand the workspace contract's purpose, and add instructions for the operator's preferences in that domain.
   - Create the confirmed subfolders, each with a contract, using `aios-core:manage-agents-md`.
   - Write context files with the background the operator gave.
   - Add the operator's terms to the workspace glossaries.
   - Add operator preferences that apply everywhere to the root contract's Instructions.
5. Return to the setup workflow to verify the aiOS root.
