# aiOS

aiOS is a set of contracts, skills, and plugins that guide agents working for an operator. It supports Claude Code and Codex. The core plugin checks file conventions, fills in timestamps, and records hook runs. See [features](plugins/aios-core/docs/features.md) for capabilities and status.

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

Codex requires hook approval. Use `/hooks` in the CLI or **Settings > Hooks** in the app. The [onboarding guide](plugins/aios-core/docs/onboarding.md#3-approve-the-hooks-codex-only) shows the approval steps.

## Set up a folder

1. Start an agent session in the folder where you want to set up aiOS.
2. Ask the agent to set up aiOS, for example "Set up aiOS in this folder."
3. Confirm the [workspaces](plugins/aios-core/docs/glossary.md) it proposes after interviewing you about your domains.
4. Approve hooks in Codex.
5. Start a new session and finish a turn in each agent harness you use.
6. Ask the agent to run the `aios-core:verify-aios` skill to verify hooks, the docs copy, and file conventions.

Setup creates `.aiOS/config.yaml`, `.aiOS/docs/`, top-level and workspace contracts, workspace glossaries, and `shared/AGENTS.md`. It adds `.aiOS/logs/` to `.gitignore`. Re-running setup adds missing pieces and reports existing files it skips.

Settings apply to the folder containing `.aiOS/config.yaml` and its contents. Checks skip subfolders with their own `.aiOS/config.yaml`.

The status report should show a hook run for each agent harness you used, matching docs, and `Problems: 0`.

- See [onboarding](plugins/aios-core/docs/onboarding.md) for script commands and troubleshooting.
- Use `aios-core:manage-agents-md` to maintain contracts as folders change, and `aios-core:manage-skills` to maintain skills.
- Browse the [setup example](plugins/aios-core/skills/setup-aios/references/example.md) for a complete fictional operator's aiOS and adaptation guidance.

Agents helping an operator set up aiOS should start with [the setup skill](plugins/aios-core/skills/setup-aios/SKILL.md).
It interviews the operator, proposes a structure, and uses the packaged example to guide the content.

## Update

See the [changelog](changelog.md) for release changes and upgrade actions.

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
- [Design records](design/AGENTS.md) hold product decisions, research, proposals, and specs.
- [Product contract](AGENTS.md) tells agents how to develop this repo.

## License

aiOS is available under the [MIT License](LICENSE).
