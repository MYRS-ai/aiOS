---
type: doc
created: 2026-10-03T13:42-07:00
updated: 2026-10-04T13:57-07:00
---

# Claude Code desktop context audit

On 2026-10-03, the test configuration reduced context before the first message from about 53.6k to 32.7k tokens. This result applies to the full test configuration, which included settings later removed.

The audit used the Claude desktop app's Code tab in `<aiOS root>`, with Opus 5.5 and a 1M context window. The original measurement, taken after one exchange, was 70.4k / 1M (7%). These measurements describe the tested sessions. Paths and operator details are generalized.

## Findings

- Disabling built-in tools worked in the desktop app. System tool context fell from 29.6k to 7.4k tokens.
- The reported 317.1k total includes loaded and deferred MCP tool schemas. Only 14.4k was loaded; 302.7k remained deferred.
- `deniedMcpServers` removed connectors in the CLI but had no effect in the desktop test. MCP tool deny rules left schemas loaded in both.
- The desktop app documents a + → Connectors toggle. Its effect on context was not tested.
- No working control was found for the built-in browser, iOS Simulator, local visualize server, desktop system prompt, or compact buffer.

## How to read the evidence

Availability labels describe the audit's findings, including its uncertainty estimates.

| Label | Meaning |
|---|---|
| Yes | Tested successfully in the desktop app |
| Yes (CLI-tested) | Tested only in the CLI; estimated 95% confidence for desktop based on tests of other tools |
| Likely (N%) | Untested option, with the audit's confidence estimate |
| No | No control found, tested controls failed, or removal would break a needed feature |
| Unknown | No control could be found or tested |

| Evidence label | Source |
|---|---|
| T-DESK | Original or test desktop session's `/context` output |
| T-CLI | Headless `/context` in Claude Code 2.1.286, in the aiOS root or temporary test folders |
| APP | Desktop app tool description |
| FILE | Local configuration file |
| EST | Estimate from text length, with a confidence percentage |

## Desktop test

### Test configuration

The test used `<aiOS root>/.claude/settings.local.json`, which applied only to sessions in that folder.

```json
{
  "permissions": {
    "deny": ["Workflow", "ShareOnboardingGuide", "SearchPlugins", "SuggestPluginInstall", "SuggestSkills"]
  },
  "enableArtifact": false,
  "deniedMcpServers": [
    {"serverName": "Claude_Code_iOS_Simulator"},
    {"serverName": "visualize"},
    {"serverName": "claude.ai Zoom for Claude"}
  ]
}
```

### Results

`/context` in a new desktop session, before the first message:

| Row | Before (original session) | With test file | Verdict |
|---|---|---|---|
| System tools | 29.6k | 7.4k | `permissions.deny` and `enableArtifact` work in the desktop |
| System tools (deferred) | 23.5k | 15.6k | Artifact's companion tools are gone too |
| MCP tools (loaded) | 14.4k | 14.4k | `deniedMcpServers` does not work in the desktop: the iOS Simulator and visualize are still loaded |
| MCP tools (deferred) | 302.7k | 302.7k | Zoom's 20 tools are still listed. `deniedMcpServers` does not work for connectors in the desktop. |
| Memory files | 79 | 1.4k | Caused by deleting `~/CLAUDE.md`; unrelated to the test settings |
| Messages | 16.8k (after one exchange) | 10 (before first message) | The tool-name list and reminders arrive with the first message |
| Total | 70.4k | 32.7k | The comparable pre-message figure before was ~53.6k |

The same file reduced CLI context from 33.3k to 13.8k and removed Zoom. This suggests the desktop app attaches servers and connectors through a path that bypasses `deniedMcpServers`.

### Settings kept after the test

On 2026-10-03, the operator chose to keep `"Workflow"` in `permissions.deny` and `"enableArtifact": false`. The four small-tool deny rules and all `deniedMcpServers` entries were removed. The 32.7k result above therefore does not measure the retained configuration.

### Subagent tools

Each subagent was asked to list its tools in the CLI test (T-CLI).

| | Workflow | Artifact |
|---|---|---|
| Main session | present unless denied | present unless disabled |
| general-purpose subagent | never present | present unless disabled |
| Explore subagent | never present | never present |

Disabling Artifact also removes it from general-purpose subagents. The estimated saving is 10.7k per subagent, assuming the main session's schema size (85% confidence). Denying Workflow saves context only in the main session.

## Options ranked by savings

| Rank | Option | Saves per session | Status |
|---|---|---|---|
| 1 | `enableArtifact: false` (if you don't publish artifacts) | 10.7k | Tested in desktop |
| 2 | Deny `Workflow` (if you don't run workflows) | 8.3k | Tested in desktop |
| 3 | Turn off unused connectors with + → Connectors (Zoom, Atlassian Rovo, Looker, Fathom, Drive, visualize copy) | ~4–5k, and prevents another 14–27k from Zoom tools | Likely (85%); untested |
| 4 | Deny SearchPlugins, SuggestPluginInstall, SuggestSkills, ShareOnboardingGuide | ~3.2k | Tested in desktop |
| 5 | Deny ScheduleWakeup, ReportFindings, ListAgents | ~2.9k | CLI-tested (95% in desktop) |
| 6 | Turn off unused skills on claude.ai | ~0.1–0.3k each | Likely (75%) |
| 7 | Run `/context` headless or in a fresh session, not in a working session | ~15k per run | Tested |
| n/a | Remove the browser, iOS Simulator, visualize | 11.5k | Tested controls failed on iOS Simulator and visualize; browser behavior is inferred |

The test with options 1, 2, and 4 applied measured 32.7k before the first message (T-DESK). Adding options 3 and 5 was estimated to bring it to roughly 30k and shorten the first-message list. This estimate was not tested. The retained settings include only options 1 and 2.

The same settings keys can go in `~/.claude/settings.json` to apply across folders.

## Context costs and available controls

Costs below are for the desktop session unless labeled otherwise. Deferred costs apply only when those tools load.

| Item | Cost | Can you change it? | How / what you lose | Evidence |
|---|---|---|---|---|
| Artifact tool | 10.7k (+ deferred companions) | Yes | `"enableArtifact": false` in settings. You lose publishing claude.ai artifact pages. | T-DESK: gone in the test session. T-CLI: −10.7k |
| Workflow tool | 8.3k | Yes | Add `"Workflow"` to `permissions.deny`. You lose multi-agent workflow scripts. | T-DESK: gone. T-CLI: −8.3k |
| Connector tool-name list | ~8–12k, added with the first message | Likely (85%) | Turn off connectors you don't use with + → Connectors (see [Connectors](#connectors)). Settings-based removal fails in the desktop. | APP; size EST (60%) |
| Built-in browser (`Claude_Browser`) | 7.9k | No (85%) | No switch found in the desktop configuration. Both settings failed for the iOS Simulator and visualize, which are the same kind of server. An unobserved UI toggle may exist. | FILE; T-DESK by analogy |
| Desktop system prompt | 4.4k | No | No setting. The CLI's is 2.0k; the extra 2.4k is desktop guidance. | T-DESK, T-CLI |
| Compact buffer | 3.0k | No | Reserved even with `autoCompactEnabled: false`. | T-CLI, T-DESK |
| SearchPlugins + SuggestPluginInstall + SuggestSkills | ~2.7k combined | Yes | Deny rules. You lose Claude suggesting plugins and skills to install. | T-DESK: gone. Size derived from the drop (EST, 80%) |
| Skills (15, `anthropic-skills`) | 2.8k | Likely (75%) | Turn individual skills off on claude.ai (Settings → Capabilities → Skills). The desktop syncs them into a local plugin whose `manifest.json` has an `enabled` flag per skill. `skillOverrides` does not work for these. | FILE; T-CLI |
| Connector server instructions | 2.3k | Likely (85%) | Removed along with their connector (+ → Connectors). | T-CLI (row disappears); desktop toggle APP |
| iOS Simulator tool | 2.0k (+ ~0.45k system-prompt section, EST) | No | Both settings failed in the desktop: `permissions.deny` and `deniedMcpServers`. | T-DESK |
| ccd_session tools (including spawn_task and mark_chapter) | 1.8k | No (70%) | Desktop-app internals. No setting found. | FILE |
| ScheduleWakeup | 1.7k | Yes (CLI-tested) | Deny rule. You lose self-paced `/loop`. | T-CLI: −1.7k |
| visualize (local) | 1.6k | No | Same two settings failed. | T-DESK |
| AskUserQuestion, SendUserFile | ~1k combined (EST) | Likely (90%) | Deny rules, the same mechanism as above. You'd lose clarifying-question prompts and file delivery to your phone. Not recommended. | EST |
| Agent | 1.1k | No (practically) | A deny rule removes it, but you lose subagents. | T-CLI |
| Bash | 1.1k | No | A deny rule *raised* system tools by 0.5k (something loads in its place). You'd also lose the shell. | T-CLI |
| ReportFindings | 0.8k | Yes (CLI-tested) | Deny rule. You lose structured code-review output. | T-CLI: −0.8k |
| ToolSearch | 0.8k | No | Removing it turns off deferral: system tools jump to 49.7k and every connector schema loads (~255k). | T-CLI |
| Skill tool | 0.7k | No | A deny rule *raised* system tools by 2.3k. You'd also lose skills. | T-CLI |
| Agent-type list | ~0.7k | No (70%) | Built-in agent types. No setting found. | EST |
| Claude Docs connector (3 always-loaded tools) | 0.64k | Likely (85%) | + → Connectors. | APP |
| Read / Edit / Write | 0.6k / 0.4k / 0.3k | No | Core file tools. | T-CLI |
| ShareOnboardingGuide | 0.5k | Yes | Deny rule. | T-DESK: gone. T-CLI: −0.5k |
| ListAgents | 0.4k | Yes (CLI-tested) | Deny rule. You lose messaging other sessions. | T-CLI: −0.4k |
| terminal (read_terminal) | 0.4k | No (80%) | Same kind of desktop server as the iOS Simulator. | By analogy |
| Environment block, per-turn reminders | ~0.6k | No | Injected by the app. | EST |
| Memory files | 1.4k in test (79 originally) | Yes | Edit the memory files. See the loading rules below. | T-DESK, T-CLI |
| Running `/context` in a working session | ~15k per run | Yes | Run it headless in a terminal instead (free, ~2 s). See [Measure it yourself](#measure-it-yourself). | T-CLI; size EST (70%) |

## Connectors

### claude.ai connectors (12)

Names and tool counts come from the desktop app's connector status. All tools are deferred except 3 from Claude Docs. "Allowlist" indicates an `mcp__<id>__*` allow rule in `~/.claude/settings.json`. It suggests use but does not prove it.

| Connector | Tools | Full-schema cost if loaded | Allowlist | Instructions loaded every session |
|---|---|---|---|---|
| Airtable | 46 | 66.3k | yes | ~0.55k |
| Zoom for Claude | 20 | 46.9k | no | n/a |
| Asana | 31 | 39.4k | yes | n/a |
| Atlassian Rovo | 41 | 23.3k | no | n/a |
| Gmail | 30 | 22.9k | yes | n/a |
| Slack | 20 | 22.8k | yes | n/a |
| Looker | 32 | 16.4k | no | n/a |
| Google Calendar | 9 | 9.3k | yes | ~0.03k |
| Google Drive | 11 | 5.9k | no | ~0.03k |
| Fathom | 12 | 5.1k | no | ~0.55k |
| Claude Docs | 8 | 2.0k (0.64k always loaded) | no | ~0.6k |
| visualize (connector copy) | 2 | 1.6k | no | n/a |

Ways to turn a connector off:

| Method | Desktop | CLI |
|---|---|---|
| Composer + → Connectors toggle (also becomes the default for new sessions) | Likely (85%): the app's own tool description says so (APP); not flipped | n/a |
| Remove the connector on claude.ai (Settings → Connectors) | Likely (90%): removes it everywhere; untested | Likely (90%) |
| `"deniedMcpServers": [{"serverName": "claude.ai <Name>"}]` | No (T-DESK) | Yes (T-CLI) |
| `"disableClaudeAiConnectors": true` or env `ENABLE_CLAUDEAI_MCP_SERVERS=false` | Unknown: untested in desktop. Given the result above, 30% it works. | Yes (T-CLI) |
| `permissions.deny` on `mcp__<id>__*` or `mcp__<id>` | No: blocks calls, schemas stay (T-DESK) | No (T-CLI) |
| `"disabledMcpServers": [...]` in settings | Not tested | No (T-CLI). Probably a key that `/mcp` writes to `~/.claude.json`, not a settings.json key (60%). |

The allowlist suggests reviewing Zoom, Atlassian Rovo, Looker, Fathom, Google Drive, and the visualize connector copy for removal. Estimated savings total 4–5k per session (EST, 60%). Removing Zoom would also prevent its tools from loading another 14–27k.

### Servers provided by the desktop app

These servers come from the app and do not appear in the connector list. The tested settings failed on iOS Simulator and visualize. Other rows distinguish estimates from test results.

| Server | Tools | Cost | Can you change it? |
|---|---|---|---|
| Claude_Browser (browser pane) | 19 | 7.9k loaded | No (85%), by analogy with the tested servers |
| claude-in-chrome | 22 | 11.4k deferred, ~0.25k instructions loaded | Unknown. Unpairing the Chrome extension might remove it (40%). |
| ccd_* (session, sidebar, PR, view, window, connectors, directory) | 56 | 23.9k (1.8k loaded) | No (70%) |
| scheduled-tasks | 6 | 3.8k deferred | Likely (50%): the desktop configuration has `ccdScheduledTasksEnabled: true` (FILE). Turning that preference off might remove these. Untested. |
| Claude_Code_iOS_Simulator | 2 | 2.8k (2.0k loaded) | No (T-DESK) |
| terminal | 5 | 2.7k (0.4k loaded) | No (80%) |
| visualize (local) | 2 | 1.6k loaded | No (T-DESK) |
| mcp-registry | 3 | 1.2k deferred | Unknown |

## Settings tested

### Desktop app (T-DESK)

| Setting | Result |
|---|---|
| `permissions.deny` for built-in tools (Workflow, ShareOnboardingGuide, SearchPlugins, SuggestPluginInstall, SuggestSkills) | Works: removed from context |
| `enableArtifact: false` | Works: Artifact and its companions removed |
| A project `.claude/settings.local.json` | Read by the desktop, even by an already-running session, which dropped ArtifactComments/ArtifactData the moment the file was written |
| `deniedMcpServers` (connector or desktop server) | No effect |
| `permissions.deny` on MCP tools (the iOS Simulator and visualize rules) | No effect on context |
| `syncClaudeAiSkills: false`, `disableBundledSkills: true` | No effect on the 15 desktop skills |

### CLI (T-CLI)

These tests used headless `/context` without model calls.

| Setting | Result |
|---|---|
| `permissions.deny` / `--disallowedTools` for a built-in tool | Removed. Per tool: Artifact −10.7k, Workflow −8.3k, ScheduleWakeup −1.7k, Agent −1.1k, ReportFindings −0.8k, ShareOnboardingGuide −0.5k, ListAgents −0.4k |
| `enableArtifact: false` or `CLAUDE_CODE_DISABLE_ARTIFACT=1` | Removed |
| `deniedMcpServers` for one connector | Removed (CLI only) |
| `disableClaudeAiConnectors: true` / `ENABLE_CLAUDEAI_MCP_SERVERS=false` | All connectors removed |
| `skillOverrides: {"my-skill": "off"}` for a skill in `.claude/skills/` | Removed. `"user-invocable-only"` also removes it; `"name-only"` shrinks it from ~110 to 4 tokens. |
| `skillOverrides` for plugin skills (`plugin:skill` or bare `skill`) | No effect. `anthropic-skills` contains plugin skills. |
| `permissions.deny` on MCP tools | No effect |
| `disabledMcpServers` via settings | No effect |
| `autoCompactEnabled: false` | Compact buffer still 3k |
| `--tools` allowlist without `ToolSearch` | Deferral turns off and everything loads (~260k) |
| Denying `Bash` or `Skill` | Context *grows* (+0.5k, +2.3k) |

A research agent claimed that MCP deny rules remove schemas and that `/context` cannot run headless. Tests contradicted both claims. For those two claims, the tables use test results. The import-approval note below remains an unverified claim from that agent.

## Memory file loading

The tested desktop session loaded 1.4k tokens of memory files. This comprised `~/AGENTS.md` at 1.1k, `<aiOS root>/AGENTS.md` at 126, and `MEMORY.md` at 125 (T-DESK).

CLI tests in temporary folders found these loading rules:

1. Any `CLAUDE.md` in the folder chain caused every `AGENTS.md` in that chain to be ignored. This included the working folder's file. `<aiOS root>/AGENTS.md` therefore did not load while `~/CLAUDE.md` existed.
2. Without `CLAUDE.md`, every `AGENTS.md` from the working folder up to `~` loaded. Both files loaded after the deletion.
3. `@AGENTS.md` inside `CLAUDE.md` loaded a target inside the working folder. A parent `CLAUDE.md` importing outside the working folder silently failed, as with `~/CLAUDE.md` importing `~/AGENTS.md`. The research agent attributed this to one-time approval, with medium confidence. Only the silent failure was tested.
4. `MEMORY.md`, the auto-memory index, always loaded. Individual memory files did not load; only their index entries did.

Under the tested configuration without `CLAUDE.md`, sessions anywhere under the home folder loaded `~/AGENTS.md`, adding 1.1k tokens each.

## Measure it yourself

Headless `/context` makes no model call and adds no content to a working session. It provides a CLI measurement for built-in tools and memory files. Desktop-only items are absent, and server settings can behave differently.

For a quick measurement before connectors attach:

```bash
claude -p "/context" --no-session-persistence
```

With connectors attached (waits 15 s first):

```bash
(sleep 15; echo '{"type":"user","message":{"role":"user","content":"/context"}}') | claude -p --input-format stream-json --output-format stream-json --verbose --no-session-persistence | grep -E '^\| [A-Z]|Tokens:' | awk '!s[$0]++'
```

To try a setting without changing any file, add `--settings '{"enableArtifact":false}'` (or any settings JSON) to either command.

For a desktop measurement, open a new session and run `/context` before your first message. A working session would gain the measurement output in its context.

## Detailed breakdown (original desktop session, 70.4k)

| # | Category | Tokens | Can you change it? |
|---|---|---|---|
| 1 | System tools (18) | 29.6k | Mostly yes: 22.2k removed in the desktop test. The rest are core tools. |
| 2 | Messages | 16.8k | Partly: the connector-name list shrinks as you remove connectors (+ → Connectors). The rest is fixed. |
| 3 | MCP tools loaded (30) | 14.4k | No for the desktop servers (13.8k). Likely for Claude Docs (0.64k). |
| 4 | System prompt | 4.4k | No |
| 5 | Compact buffer | 3.0k | No |
| 6 | Skills | 2.8k | Likely (75%), via claude.ai |
| 7 | MCP server instructions | 2.3k | Likely (85%), via connectors |
| 8 | Memory files | 79 (1.4k in test) | Yes |

### System tools: 29.6k

Individual costs appear in [the controls table](#context-costs-and-available-controls). CLI tests measured one tool at a time. The desktop-only tool cost was derived from the desktop test's reduction.

The remaining 7.4k included Agent, Bash, ToolSearch, Skill, Read, Edit, Write, ScheduleWakeup, ReportFindings, ListAgents, AskUserQuestion, and SendUserFile. Denying ScheduleWakeup, ReportFindings, and ListAgents would reduce this to about 4.5k, based on CLI results.

### Messages: 16.8k (after one exchange)

A fresh desktop session shows `Messages: 10` before the first prompt (T-DESK). Everything below is added when you send your first message.

| Component | Tokens | Can you change it? |
|---|---|---|
| Deferred tool-name list (347 MCP + 21 system names; 259 names carry a 36-character connector ID, roughly 30 tokens each) | ~8–12k (EST, 60%) | Likely, partly: shrinks as you remove connectors |
| Agent-type descriptions | ~0.7k (EST) | No (70%) |
| Environment block | ~0.3k (EST) | No |
| Turn-1 reminders (memory wrapper, user email, attribution) | ~0.3k (EST) | No |
| Auto-mode instructions | ~0.15k (EST) | Only by leaving auto mode |
| Per-turn reminders (attribution, SendUserFile note) | ~0.15k per turn (EST) | No |
| The first exchange | ~0.05k | n/a |
| Unattributed | ~3–6k | Unknown |

### MCP tools loaded: 14.4k (reported total, 30 tools)

Unchanged in the test session.

| Server | Tools | Tokens | Can you change it? |
|---|---|---|---|
| Claude_Browser | 19 | 7.9k (computer 1.9k, browser_batch 805, preview_start 736, resize_window 667, read_page 453, others under 400) | No (85%) |
| Claude_Code_iOS_Simulator | 1 | 2.0k | No (T-DESK) |
| ccd_session | 4 | 1.8k | No (70%) |
| visualize | 2 | 1.6k | No (T-DESK) |
| Claude Docs | 3 | 0.64k | Likely (85%), via + → Connectors |
| terminal | 1 | 0.42k | No (80%) |

### System prompt: 4.4k (reported total; components are estimates)

No setting was found to change the system prompt, and its size was unchanged in the test session. The iOS Simulator section alone was estimated at ~450 tokens.

| Section | Tokens (EST) |
|---|---|
| Browser/computer-use safety policy | ~1.9k |
| Core identity, harness rules, git, memory instructions | ~0.9k |
| Desktop-app guidance (links, panes, PR tools, settings, worktrees) | ~0.7k |
| Browser and iOS Simulator guidance | ~0.6k |
| Pronouns, context management, misc | ~0.3k |

### Skills: 2.8k (reported total)

Source: the desktop app syncs claude.ai skills into a local plugin at `~/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/…/` (FILE). Its `manifest.json` lists each skill with `enabled: true`.

Turning skills off on claude.ai may remove them (75% confidence, untested). `skillOverrides` did not affect plugin skills in the CLI test.

| Skill | Tokens | Origin (from manifest) |
|---|---|---|
| docs | ~340 | Anthropic |
| morning-briefing | ~340 | Added by the operator |
| google-workspace | ~330 | Anthropic |
| pptx | ~330 | Anthropic |
| docx | ~320 | Anthropic |
| xlsx | ~320 | Anthropic |
| pdf | ~150 | Anthropic |
| citation-check | ~130 | Added by the operator |
| morning | ~120 | Anthropic |
| grill-me | ~90 | Added by the operator |
| explain-usage | ~80 | Anthropic |
| schedule | ~80 | Anthropic |
| consolidate-memory | ~40 | Anthropic |
| setup-claude | ~40 | Anthropic |
| unslop | ~40 | Added by the operator |

`morning` and `morning-briefing` overlap. The manifest also has `setup-cowork`, which the Code tab doesn't show.

### MCP server instructions: 2.3k (reported total; components are estimates)

Removing a connector is expected to remove its instruction block (85% confidence).

| Server | Tokens (EST) |
|---|---|
| Claude Docs | ~0.6k |
| Fathom | ~0.55k |
| Airtable | ~0.55k |
| Claude in Chrome | ~0.25k (desktop server; control unknown) |
| Google Drive, Google Calendar | ~0.03k each |

### Heaviest individual connector tools

These deferred schemas consume context only when loaded. Turning off the connector is expected to prevent loading (85% confidence).

| Tool | Tokens |
|---|---|
| Zoom meeting_create | 14.1k |
| Zoom meeting_update | 13.1k |
| Airtable create_field | 6.8k |
| Airtable create_automation | 4.9k |
| Asana create_project | 4.9k |
| Slack update_canvas | 4.8k |
| Airtable update_automation | 4.7k |
| Airtable list_records_for_table | 4.5k |
| Airtable create_base, list_records_for_page | 4.3k each |
| Airtable analyze_table, create_table | 4.2k each |
| Asana create_project_preview_v3 | 4.1k |

## Measurement method

- Connector and MCP numbers come from the desktop `/context` table, summed by hand. Loaded MCP tools sum to 14,362 (reported 14.4k); all 377 sum to 317,097 (reported 317.1k).
- Built-in tool costs were measured in the CLI by removing one tool at a time, and cross-checked by loading `ToolSearch` plus one tool at a time. The CLI tools sum to 27.4k against a reported 27.1k.
- Desktop results come from the test session's `/context` output, read from its transcript file.
- Connector names come from the desktop app's connector-status tool.
- Config files read: `~/.claude/settings.json`, `~/.claude.json` (no local MCP servers), `~/Library/Application Support/Claude/claude_desktop_config.json`, and the skills-plugin `manifest.json`.
- Not tested: changes to the claude.ai account or desktop defaults, such as toggling a connector or skill.
