# Extend

Adds a workspace to an existing aiOS root.

1. Interview the operator about the new domain, using the Domains and Terms topics in [interview.md](interview.md).
2. Propose the workspace name, purpose, and subfolders. Build nothing until the operator confirms them.
3. From the aiOS root, run the setup script with only the new workspace:

   ```bash
   python3 <skill>/scripts/setup.py --workspace NAME="PURPOSE"
   ```

   The script adds the workspace contract and glossary, and skips every file that already exists.
4. Add the workspace to the root contract's Contents. The script doesn't change an existing root contract.
5. Write the workspace's content, as step 4 of [start-fresh.md](start-fresh.md) describes.
6. Return to the setup workflow to verify the aiOS root.
