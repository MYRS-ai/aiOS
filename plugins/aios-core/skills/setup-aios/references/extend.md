# Extend

Adds a workspace to the operator's aiOS.

1. Interview the operator about the new domain using [interview.md](interview.md). Cover its responsibilities, recurring work, sources, terms, and preferences.
   Skip facts and system-wide preferences already recorded in the existing aiOS.
2. Use the [example guide](example.md) to choose relevant structures. Follow the operator's existing choices when they differ from the example.
   Propose the workspace name, purpose, and subfolders. Build nothing until the operator confirms them.
3. From the folder containing `.aiOS/config.yaml`, run the setup script with only the new workspace:

   ```bash
   python3 <skill>/scripts/setup.py --workspace NAME="PURPOSE"
   ```

   The script adds the workspace contract and glossary, and skips every file that already exists.
4. Add the workspace to the top-level contract's Contents. The script doesn't change that existing contract.
5. Write the workspace's content, as step 4 of [start-fresh.md](start-fresh.md) describes.
6. Return to the setup workflow to verify the operator's aiOS.
