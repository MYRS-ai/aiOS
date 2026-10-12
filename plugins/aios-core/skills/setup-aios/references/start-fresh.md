# Start fresh

Sets up the operator's aiOS when the interview is the only source of context.

1. Interview the operator with [interview.md](interview.md).
2. Read the [example guide](example.md) and representative files for the operator's domains. Propose the structure as a folder tree.
   Give each workspace a name and a one-sentence purpose.

   - Names are one to four lowercase words separated by hyphens. `shared` is reserved for resources more than one domain uses.
   - Show the subfolders each workspace needs, such as `context/`, `projects/`, `routines/`, `workflows/`, and `journal/`.
   - Build nothing until the operator confirms the structure.

3. Run the setup script once, with every confirmed workspace:

   ```bash
   python3 <skill>/scripts/setup.py [folder] --workspace NAME="PURPOSE" --workspace NAME="PURPOSE"
   ```

   `<skill>` is this skill's folder. `folder` defaults to the current folder.

   The script:

   - Creates `.aiOS/config.yaml`, the docs copy, the top-level and workspace contracts, a glossary in each workspace, and `shared/`.
   - Adds `.aiOS/logs/` to `.gitignore`.
   - Never overwrites a file. Review the files it reports as skipped.

4. Write each workspace's content from the interview, adapting relevant structures from the example:

   - Expand the workspace contract's purpose, and add instructions for the operator's preferences in that domain.
   - Create the confirmed subfolders, each with a contract, using `aios-core:manage-agents-md`.
   - Write context files with the background the operator gave.
   - Write the confirmed projects, routines, and workflows with owners, next actions, and completion criteria where applicable.
   - Record past events only when the operator or their sources establish what happened.
   - Add agreed concepts to the workspace glossaries using the [entry structure](../../../docs/glossary.md#maintaining-vocabulary).
   - Add operator preferences that apply everywhere to the top-level contract's Instructions.

5. Review the [adaptation checks](example.md#review-the-adapted-result), then return to the setup workflow to verify the operator's aiOS.
