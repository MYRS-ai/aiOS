# aiOS

aiOS is a set of contracts, skills, and plugins that guide agents working for an operator.
It supports Claude Code and Codex. The core plugin checks file conventions, fills in timestamps, and records hook runs.
See [features](plugins/aios-core/docs/features.md) for capabilities and status.

## Install

You need Claude Code or Codex installed, and Python 3.9 or later. Run `python3 --version` to check Python.
For local development, use this repo's absolute path as the marketplace source.

Claude Code:

```bash
claude plugin marketplace add MYRS-ai/aiOS
claude plugin install aios-core@aios --scope user
```

Codex:

```bash
codex plugin marketplace add MYRS-ai/aiOS
codex plugin add aios-core@aios
```

Codex requires hook approval. Use `/hooks` in the CLI or **Settings > Hooks** in the app.
The [onboarding guide](plugins/aios-core/docs/onboarding.md#3-approve-the-hooks-codex-only) shows the approval steps.

## Set up a folder

1. Start an agent session in the folder you want to become the [aiOS root](plugins/aios-core/docs/glossary.md): the folder that holds your aiOS settings and everything inside it.
2. Ask the agent to set up aiOS, for example "Set up aiOS in this folder." It interviews you about your areas of work, then proposes [workspaces](plugins/aios-core/docs/glossary.md), one top-level folder for each area. Confirm the names before it builds them.
3. Approve hooks in Codex, then start a new session and finish a turn in each agent harness you use.
4. Ask the agent to run the `status` and `check` skills to verify hooks, the docs copy, and file conventions.

Setup creates `.aiOS/config.yaml`, `.aiOS/docs/`, root and workspace contracts, and `shared/AGENTS.md`.
It adds `.aiOS/logs/` to `.gitignore`. Re-running setup adds missing pieces and reports existing files it skips.
Each folder with its own `.aiOS/config.yaml` is a separate aiOS root. Parent checks skip nested aiOS roots.

The status report should show a hook run for each agent harness you used and matching docs.
The check should report `Problems: 0`.
See [onboarding](plugins/aios-core/docs/onboarding.md) for script commands and troubleshooting.
Use the `write-contract` skill to create or update contracts as folders change.
To see a finished result first, browse [examples/sample-root](examples/sample-root/AGENTS.md), a small aiOS root for a fictional operator.

## Update

Plugin updates are off by default for this marketplace. Update each agent harness separately.

Claude Code:

```bash
claude plugin marketplace update aios
claude plugin update aios-core@aios
```

Codex:

```bash
codex plugin marketplace upgrade aios
codex plugin add aios-core@aios
```

Start a new session after updating. Codex asks for approval again when hook definitions change.

## Docs

- [Operator docs](plugins/aios-core/docs/AGENTS.md) ship inside the core plugin's `docs/` folder.
- [Glossary](plugins/aios-core/docs/glossary.md) defines aiOS terms.
- [Onboarding](plugins/aios-core/docs/onboarding.md) covers setup, hook approval, verification, and updates.
- [Design records](design/AGENTS.md) hold product decisions, research, and the separation plan.
- [Product contract](AGENTS.md) tells agents how to develop this repo.

## License

aiOS is available under the [MIT License](LICENSE).
