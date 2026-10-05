"""Exercise the installed plugin interface without importing its implementation."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import textwrap
import time
import unittest
from datetime import datetime


REPO = Path(__file__).resolve().parents[1]
PLUGIN = REPO / "plugins" / "aios-core"
SAMPLE = REPO / "examples" / "sample-root"
DOC = "---\ntype: doc\n---\n\n# Notes\n"


def ignore_generated(folder, names):
    """Copy the sample as it appears in a checkout, without generated state."""
    return [name for name in names if name == "__pycache__"
            or (Path(folder).name == ".aiOS" and name in ("docs", "logs"))]


class HookTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix=".aios-tests-", dir=REPO)
        self.addCleanup(temporary.cleanup)
        self.temporary = Path(temporary.name)
        self.root = self.temporary / "root"
        shutil.copytree(SAMPLE, self.root, ignore=ignore_generated)
        # Fixture files must predate every turn, regardless of checkout mtimes.
        for path in self.root.rglob("*"):
            if path.is_file():
                os.utime(path, (946684800, 946684800))
        self.plugin = PLUGIN
        self.env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
        self.env.pop("PLUGIN_ROOT", None)

    def run_script(self, script, *args, stdin=None, cwd=None):
        result = subprocess.run(
            [sys.executable, str(script), *map(str, args)],
            input=stdin, text=True, capture_output=True,
            cwd=cwd or self.root, env=self.env, timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(result.stderr, "", result.stderr)
        return result.stdout

    def hook(self, event, session="session", cwd=None):
        output = self.run_script(
            self.plugin / "hooks" / "hooks.py", event,
            stdin=json.dumps({"session_id": session, "cwd": str(cwd or self.root)}),
        )
        # Logs have millisecond precision; selection starts 1 ms after the entry.
        time.sleep(0.01)
        return json.loads(output) if output.strip() else {}

    def events(self, root=None):
        path = (root or self.root) / ".aiOS" / "logs" / "hook-events.jsonl"
        return [json.loads(line) for line in path.read_text().splitlines()]

    def write(self, relative, content=DOC):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        return path

    def config(self, text):
        self.write(".aiOS/config.yaml", textwrap.dedent(text).lstrip())

    def setup_root(self, root=None, *workspaces):
        return self.run_script(
            self.plugin / "skills" / "setup" / "scripts" / "setup.py",
            root or self.root,
            *[arg for workspace in workspaces for arg in ("--workspace", workspace)],
            cwd=self.temporary,
        )

    def assert_allowed(self, reply, checked=None):
        self.assertEqual(reply, {})
        event = self.events()[-1]
        self.assertEqual(event["event"], "stop")
        self.assertEqual(event["decision"], "allow")
        self.assertEqual(event["problems"], [])
        if checked is not None:
            self.assertEqual(event["checked"], checked)
        return event

    def assert_blocked(self, reply, path, *messages):
        self.assertEqual(reply["decision"], "block")
        for text in (path, *messages):
            self.assertIn(text, reply["reason"])
        event = self.events()[-1]
        self.assertEqual(event["decision"], "block")
        self.assertEqual(event["fixed"], [])

    @staticmethod
    def fields(path):
        front = path.read_text().split("---", 2)[1]
        return dict(line.split(": ", 1) for line in front.splitlines() if ": " in line)

    @staticmethod
    def snapshot(folder):
        return {str(path.relative_to(folder)): (path.read_bytes(), path.stat().st_mtime_ns)
                for path in folder.rglob("*") if path.is_file()}

    def copy_plugin(self, version="0.9.0"):
        self.plugin = self.temporary / "plugin"
        shutil.copytree(PLUGIN, self.plugin, ignore=shutil.ignore_patterns("__pycache__"))
        self.set_version(version)

    def set_version(self, version):
        for harness in (".claude-plugin", ".codex-plugin"):
            path = self.plugin / harness / "plugin.json"
            manifest = json.loads(path.read_text())
            manifest["version"] = version
            path.write_text(json.dumps(manifest))

    def test_setup_builds_working_root_in_empty_folder(self):
        shutil.rmtree(self.root)
        self.root.mkdir()
        self.setup_root(self.root, "work=Fictional equipment repairs.")
        for relative in ("AGENTS.md", "work/AGENTS.md", "shared/AGENTS.md",
                         ".aiOS/AGENTS.md", ".aiOS/config.yaml", ".aiOS/docs/.sync.json"):
            self.assertTrue((self.root / relative).is_file(), relative)
        self.assertTrue((self.root / ".aiOS/logs").is_dir())
        self.assertIn(".aiOS/logs/", (self.root / ".gitignore").read_text().splitlines())
        audit = self.run_script(PLUGIN / "skills/check/scripts/check.py")
        self.assertIn("Problems: 0.", audit)
        self.hook("start", cwd=self.root / "work")
        path = self.write("work/notes.md")
        self.assert_allowed(self.hook("stop", cwd=self.root / "work"), checked=1)
        self.assertIn("created", self.fields(path))

    def test_setup_adds_missing_pieces_without_overwriting_files(self):
        self.setup_root()
        self.write("AGENTS.md", "---\ntype: AGENTS.md\n---\n\n# Custom root\n")
        self.write(".aiOS/config.yaml", "enabled: true\n# Keep this preference.\n")
        self.write(".aiOS/docs/local.md", DOC)
        self.write("personal/notes.md", DOC + "Keep this note.\n")
        (self.root / "shared/AGENTS.md").unlink()
        shutil.rmtree(self.root / ".aiOS/logs")
        before = self.snapshot(self.root)
        output = self.setup_root(self.root, "study=Fictional evening classes.")
        after = self.snapshot(self.root)
        self.assertIn("Skipped existing", output)
        for path, original in before.items():
            self.assertEqual(after[path], original, path)
        self.assertEqual(set(after) - set(before), {"shared/AGENTS.md", "study/AGENTS.md"})
        self.assertTrue((self.root / ".aiOS/logs").is_dir())
        self.setup_root()
        self.assertEqual(self.snapshot(self.root), after)
        self.hook("start")
        self.write("personal/notes.md", DOC + "A new action.\n")
        self.assert_allowed(self.hook("stop"), checked=1)

    def test_setup_appends_log_exclusion_only_once(self):
        self.write(".gitignore", "custom-cache/")
        self.setup_root()
        expected = "custom-cache/\n.aiOS/logs/\n"
        self.assertEqual((self.root / ".gitignore").read_text(), expected)
        self.setup_root()
        self.assertEqual((self.root / ".gitignore").read_text(), expected)
        self.hook("start")
        self.write("personal/notes.md")
        self.assert_allowed(self.hook("stop"), checked=1)

    def test_missing_type_blocks_with_file_and_rule(self):
        self.hook("start")
        self.write("personal/missing.md", "# No front matter\n")
        self.assert_blocked(self.hook("stop"), "personal/missing.md",
                            "missing front matter: type", "Rule: default")

    def test_disallowed_type_blocks_with_file_and_rule(self):
        self.hook("start")
        self.write("personal/memo.md", "---\ntype: memo\n---\n")
        self.assert_blocked(self.hook("stop"), "personal/memo.md",
                            "type 'memo' is not allowed", "Rule: default")

    def test_bad_folder_name_blocks(self):
        self.hook("start")
        self.write("personal/Bad_Folder/notes.md")
        self.assert_blocked(self.hook("stop"), "personal/Bad_Folder", "[names]",
                            "lowercase, hyphenated, one to four words")

    def test_hidden_folder_names_are_exempt(self):
        self.hook("start")
        self.write(".aiOS/notes.md")
        self.write(".Hidden_Folder/invalid.md", "No front matter\n")
        # .aiOS is checked, while other hidden folders are outside the scope.
        self.assert_allowed(self.hook("stop"), checked=1)

    def test_skill_name_must_match_its_folder(self):
        self.hook("start")
        self.write("personal/skills/weekly-review/SKILL.md",
                   "---\nname: wrong-name\ndescription: Review the week.\n---\n")
        self.assert_blocked(self.hook("stop"), "personal/skills/weekly-review/SKILL.md",
                            "must match its folder 'weekly-review'", "Rule: skill")

    def test_skill_resources_need_no_front_matter(self):
        self.hook("start")
        skill = self.write("personal/skills/weekly-review/SKILL.md",
                           "---\nname: weekly-review\ndescription: Review the week.\n---\n")
        resource = self.write("personal/skills/weekly-review/references/questions.md",
                              "# What remains unfinished?\n")
        before = (skill.read_bytes(), resource.read_bytes())
        event = self.assert_allowed(self.hook("stop"), checked=2)
        self.assertEqual(event["fixed"], [])
        self.assertEqual((skill.read_bytes(), resource.read_bytes()), before)

    def test_passing_turn_fills_created_and_updated(self):
        self.hook("start")
        path = self.write("personal/notes.md")
        event = self.assert_allowed(self.hook("stop"), checked=1)
        fields = self.fields(path)
        self.assertEqual(fields["created"], fields["updated"])
        self.assertIsNotNone(datetime.fromisoformat(fields["created"]).tzinfo)
        self.assertEqual(event["fixed"], [{"check": "frontmatter", "path": "personal/notes.md"}])
        self.assertTrue(path.read_text().endswith("\n# Notes\n"))

    def test_existing_created_survives_an_edit(self):
        self.hook("start")
        path = self.write("personal/notes.md",
                          "---\ntype: doc\ncreated: 2001-01-02T03:04-08:00\n"
                          "updated: 2001-01-02T03:04-08:00\n---\n\n# Changed notes\n")
        self.assert_allowed(self.hook("stop"), checked=1)
        fields = self.fields(path)
        self.assertEqual(fields["created"], "2001-01-02T03:04-08:00")
        self.assertNotEqual(fields["updated"], fields["created"])

    def test_existing_created_survives_replacement_with_identical_content(self):
        path = self.write("personal/notes.md",
                          "---\ntype: doc\ncreated: 2001-01-02T03:04-08:00\n---\n\n# Notes\n")
        self.hook("start")
        content = path.read_bytes()
        original_inode = path.stat().st_ino
        replacement = self.root / "replacement.tmp"
        replacement.write_bytes(content)
        os.replace(replacement, path)
        self.assertNotEqual(path.stat().st_ino, original_inode)
        self.assertEqual(path.read_bytes(), content)
        self.assert_allowed(self.hook("stop"), checked=1)
        self.assertEqual(self.fields(path)["created"], "2001-01-02T03:04-08:00")
        self.assertIn("updated", self.fields(path))

    def test_other_sessions_timestamp_change_is_not_restamped(self):
        self.hook("start", session="first")
        self.hook("start", session="second")
        path = self.write("personal/notes.md")
        self.assert_allowed(self.hook("stop", session="second"), checked=1)
        before = (path.read_bytes(), path.stat().st_mtime_ns)
        event = self.assert_allowed(self.hook("stop", session="first"), checked=1)
        self.assertEqual(event["session"], "first")
        self.assertEqual(event["fixed"], [])
        self.assertEqual((path.read_bytes(), path.stat().st_mtime_ns), before)

    def test_max_blocks_allows_third_attempt_with_warning_and_resets(self):
        self.config("enabled: true\nmax_blocks: 2\n")
        self.hook("start")
        self.write("personal/missing.md", "# Missing type\n")
        for _ in range(2):
            self.assert_blocked(self.hook("stop"), "personal/missing.md", "Rule: default")
        reply = self.hook("stop")
        self.assertNotIn("decision", reply)
        self.assertIn("personal/missing.md", reply["systemMessage"])
        self.assertEqual(self.events()[-1]["decision"], "allow")
        self.assertEqual(len(self.events()[-1]["problems"]), 1)
        self.assert_allowed(self.hook("stop"), checked=0)
        self.write("personal/missing.md", "# Still missing type\n")
        self.assert_blocked(self.hook("stop"), "personal/missing.md", "Rule: default")

    def test_docs_sync_copies_missing_docs_before_turn_starts(self):
        self.assertFalse((self.root / ".aiOS/docs").exists())
        self.hook("start")
        self.assertEqual(self.events()[-1]["docs"]["action"], "copied")
        source = self.snapshot(PLUGIN / "docs")
        copied = self.snapshot(self.root / ".aiOS/docs")
        self.assertEqual(set(copied), set(source) | {".sync.json"})
        for path in source:
            self.assertEqual(copied[path][0], source[path][0], path)
        marker = json.loads(copied[".sync.json"][0])
        self.assertEqual(marker["version"], self.events()[-1]["docs"]["version"])
        self.assertRegex(marker["hash"], r"^[0-9a-f]{64}$")
        self.write("personal/notes.md")
        self.assert_allowed(self.hook("stop"), checked=1)

    def test_docs_sync_leaves_identical_version_and_content_unchanged(self):
        self.hook("start")
        before = self.snapshot(self.root / ".aiOS/docs")
        self.hook("start", session="next")
        self.assertEqual(self.events()[-1]["docs"]["action"], "unchanged")
        self.assertEqual(self.snapshot(self.root / ".aiOS/docs"), before)
        self.write("personal/notes.md")
        self.assert_allowed(self.hook("stop", session="next"), checked=1)

    def test_docs_sync_replaces_copy_for_newer_plugin_version(self):
        self.copy_plugin("0.9.0")
        self.hook("start")
        self.write(".aiOS/docs/obsolete.md")
        self.set_version("0.10.0")
        self.hook("start", session="next")
        self.assertEqual(self.events()[-1]["docs"], {"action": "replaced", "version": "0.10.0"})
        marker = json.loads((self.root / ".aiOS/docs/.sync.json").read_text())
        self.assertEqual(marker["version"], "0.10.0")
        self.assertFalse((self.root / ".aiOS/docs/obsolete.md").exists())
        self.write("personal/notes.md")
        self.assert_allowed(self.hook("stop", session="next"), checked=1)

    def test_docs_sync_replaces_changed_source_at_same_version(self):
        self.copy_plugin()
        self.hook("start")
        marker_path = self.root / ".aiOS/docs/.sync.json"
        before = json.loads(marker_path.read_text())
        (self.plugin / "docs/new-doc.md").write_text(DOC)
        (self.plugin / "docs/hooks.md").unlink()
        self.hook("start", session="next")
        after = json.loads(marker_path.read_text())
        self.assertEqual(self.events()[-1]["docs"]["action"], "replaced")
        self.assertEqual(after["version"], before["version"])
        self.assertNotEqual(after["hash"], before["hash"])
        self.assertEqual((self.root / ".aiOS/docs/new-doc.md").read_text(), DOC)
        self.assertFalse((self.root / ".aiOS/docs/hooks.md").exists())
        self.write("personal/notes.md")
        self.assert_allowed(self.hook("stop", session="next"), checked=1)

    def test_docs_sync_keeps_newer_copy_and_warns_about_older_plugin(self):
        self.copy_plugin("0.10.0")
        self.hook("start")
        before = self.snapshot(self.root / ".aiOS/docs")
        self.set_version("0.9.0")
        (self.plugin / "docs/hooks.md").write_text(DOC)
        reply = self.hook("start", session="older")
        context = reply["hookSpecificOutput"]
        self.assertEqual(context["hookEventName"], "SessionStart")
        self.assertIn("outdated aios-core plugin", context["additionalContext"])
        self.assertEqual(self.events()[-1]["docs"], {"action": "kept-newer", "version": "0.9.0"})
        self.assertEqual(self.snapshot(self.root / ".aiOS/docs"), before)
        self.write("personal/notes.md")
        self.assert_allowed(self.hook("stop", session="older"), checked=1)
        report = self.run_script(self.plugin / "skills/check/scripts/check.py")
        self.assertIn("Problems: 0.", report)

    def test_marker_without_file_hashes_is_resynced(self):
        self.hook("start")
        marker = self.root / ".aiOS/docs/.sync.json"
        old = json.loads(marker.read_text())
        marker.write_text(json.dumps({"version": old["version"], "hash": old["hash"]}))
        self.hook("start", session="next")
        self.assertEqual(self.events()[-1]["docs"]["action"], "replaced")
        self.assertIn("files", json.loads(marker.read_text()))

    def test_locally_edited_copy_is_restored_at_next_start(self):
        self.hook("start")
        path = self.root / ".aiOS/docs/hooks.md"
        original = path.read_text()
        path.write_text(original + "\nA local edit.\n")
        self.hook("start", session="next")
        self.assertEqual(self.events()[-1]["docs"]["action"], "replaced")
        self.assertEqual(path.read_text(), original)
        self.hook("start", session="third")
        self.assertEqual(self.events()[-1]["docs"]["action"], "unchanged")

    def test_editing_docs_copy_warns_without_blocking(self):
        self.hook("start")
        path = self.root / ".aiOS/docs/hooks.md"
        path.write_text(path.read_text() + "\nA local edit.\n")
        reply = self.hook("stop")
        self.assertNotIn("decision", reply)
        self.assertIn("[docs-copy] .aiOS/docs/hooks.md", reply["systemMessage"])
        event = self.events()[-1]
        self.assertEqual(event["decision"], "allow")
        self.assertEqual(len(event["problems"]), 1)
        self.assertEqual(event["problems"][0]["mode"], "warn")

    def test_sync_during_another_sessions_turn_is_not_flagged_or_restamped(self):
        self.copy_plugin()
        self.hook("start", session="first")
        (self.plugin / "docs/hooks.md").write_text((self.plugin / "docs/hooks.md").read_text() + "\nNew text.\n")
        self.hook("start", session="second")
        synced = (self.root / ".aiOS/docs/hooks.md").read_text()
        self.write("personal/notes.md")
        self.assert_allowed(self.hook("stop", session="first"))
        self.assertEqual(self.events()[-1]["problems"], [])
        self.assertEqual((self.root / ".aiOS/docs/hooks.md").read_text(), synced)

    def test_edited_docs_copy_is_not_restamped(self):
        self.hook("start")
        path = self.root / ".aiOS/docs/hooks.md"
        edited = path.read_text() + "\nA local edit.\n"
        path.write_text(edited)
        self.hook("stop")
        self.assertEqual(path.read_text(), edited)

    def test_editing_non_markdown_docs_copy_also_warns(self):
        self.hook("start")
        self.write(".aiOS/docs/media/sample.svg", "<svg/>\n")
        reply = self.hook("stop")
        self.assertIn("[docs-copy] .aiOS/docs/media/sample.svg", reply["systemMessage"])
        self.assertEqual(self.events()[-1]["decision"], "allow")
        self.assertEqual(len(self.events()[-1]["problems"]), 1)

    def test_outer_root_skips_nested_root_checks(self):
        nested = self.root / "personal/nested-root"
        self.setup_root(nested)
        self.hook("start", session="outer")
        self.hook("start", session="inner", cwd=nested)
        self.write("personal/nested-root/Bad_Folder/missing.md", "# Missing type\n")
        self.write("personal/notes.md")
        self.assert_allowed(self.hook("stop", session="outer"), checked=1)
        reply = self.hook("stop", session="inner", cwd=nested)
        self.assertEqual(reply["decision"], "block")
        self.assertIn("Bad_Folder/missing.md", reply["reason"])
        self.assertEqual(self.events(nested)[-1]["decision"], "block")

    def test_meetings_rule_requires_date_at_any_depth(self):
        self.config("""
            checks:
              frontmatter:
                rules:
                  meetings:
                    match: ["**/meetings/**"]
                    required: [type, date]
                    allowed:
                      type: [meeting]
                    timestamps: [created, updated]
                  default:
                    match: ["**"]
                    required: [type]
                    allowed:
                      type: [AGENTS.md, doc]
                    timestamps: [created, updated]
        """)
        self.hook("start")
        paths = ("meetings/notes.md", "day-job/projects/meetings/notes.md")
        for path in paths:
            self.write(path, "---\ntype: meeting\n---\n")
        reply = self.hook("stop")
        for path in paths:
            self.assert_blocked(reply, path, "missing front matter: date", "Rule: meetings")
            self.write(path, "---\ntype: meeting\ndate: 2026-04-12\n---\n")
        self.assert_allowed(self.hook("stop"), checked=2)
        for path in paths:
            self.assertIn("created", self.fields(self.root / path))

    def test_meetings_rule_requires_meeting_type_before_default_rule(self):
        self.config("""
            checks:
              frontmatter:
                rules:
                  meetings:
                    match: ["**/meetings/**"]
                    required: [type, date]
                    allowed:
                      type: [meeting]
                  default:
                    match: ["**"]
                    required: [type]
                    allowed:
                      type: [AGENTS.md, doc]
        """)
        self.hook("start")
        self.write("day-job/meetings/notes.md", "---\ntype: doc\ndate: 2026-04-12\n---\n")
        self.assert_blocked(self.hook("stop"), "day-job/meetings/notes.md",
                            "type 'doc' is not allowed", "Rule: meetings")
        self.write("day-job/meetings/notes.md", "---\ntype: meeting\ndate: 2026-04-12\n---\n")
        self.write("personal/notes.md")
        self.assert_allowed(self.hook("stop"), checked=2)

    def test_custom_allowed_types_replace_defaults(self):
        self.config("""
            checks:
              frontmatter:
                rules:
                  custom:
                    match: ["**"]
                    required: [type]
                    allowed:
                      type: [AGENTS.md, memo]
                    timestamps: [created, updated]
        """)
        self.hook("start")
        self.write("personal/notes.md")
        self.assert_blocked(self.hook("stop"), "personal/notes.md",
                            "type 'doc' is not allowed", "Rule: custom")
        path = self.write("personal/notes.md", "---\ntype: memo\n---\n")
        self.assert_allowed(self.hook("stop"), checked=1)
        self.assertIn("created", self.fields(path))

    def test_names_mode_off_allows_bad_folder_name(self):
        self.config("checks:\n  names:\n    mode: off\n")
        self.hook("start")
        self.write("personal/Bad_Folder/notes.md")
        self.assert_allowed(self.hook("stop"), checked=1)

    def test_check_names_cannot_import_paths(self):
        self.copy_plugin()
        marker = self.temporary / "executed"
        payload = self.temporary / "payload.py"
        payload.write_text(f"open({str(marker)!r}, 'w').write('executed')\n")
        checks = self.plugin / "hooks/checks"
        (checks / "linked.py").symlink_to(payload)
        for name in ("Upper", "under_score", "9check"):
            shutil.copy(payload, checks / (name + ".py"))
        names = [str(payload.with_suffix("")), "../../../../payload", "linked",
                 "Upper", "under_score", "9check", "missing"]
        self.config("checks:\n" + "".join(f"  {name}:\n    mode: block\n" for name in names))
        self.hook("start")
        self.write("personal/notes.md")
        self.assert_allowed(self.hook("stop"), checked=1)
        self.assertFalse(marker.exists())

    def test_symlinks_are_outside_check_and_fixer_scope(self):
        self.hook("start")
        outside = self.temporary / "outside"
        outside.mkdir()
        target = outside / "notes.md"
        target.write_text(DOC)
        before = self.snapshot(outside)
        (self.root / "personal/linked.md").symlink_to(target)
        (self.root / "personal/linked-folder").symlink_to(outside, target_is_directory=True)
        (self.root / ".aiOS/docs/linked.md").symlink_to(target)
        (self.root / "personal/broken.md").symlink_to(outside / "missing.md")
        self.write("personal/notes.md")
        self.assert_allowed(self.hook("stop"), checked=1)
        self.assertEqual(self.snapshot(outside), before)

    def test_unreadable_file_does_not_disable_turn(self):
        self.hook("start")
        bad = self.write("personal/a-unreadable.md")
        content = DOC.encode("utf-8") + b"\xff"
        bad.write_bytes(content)
        self.write("personal/missing.md", "# Missing type\n")
        valid = self.write("personal/notes.md")
        for _ in range(2):
            reply = self.hook("stop")
            self.assert_blocked(reply, "personal/a-unreadable.md", "could not read:", "utf-8")
            self.assert_blocked(reply, "personal/missing.md", "missing front matter: type")
        reply = self.hook("stop")
        self.assertIn("could not read:", reply["systemMessage"])
        event = self.events()[-1]
        self.assertEqual(event["decision"], "allow")
        self.assertEqual(event["checked"], 3)
        self.assertEqual(len(event["problems"]), 2)
        self.assertEqual(bad.read_bytes(), content)
        self.assertIn("created", self.fields(valid))
        self.assertEqual(len(self.events()), 4)

    def test_corrupt_log_lines_do_not_break_hooks_or_status(self):
        self.hook("start")
        log = self.root / ".aiOS/logs/hook-events.jsonl"
        with log.open("a") as stream:
            stream.write('not json\n\n{"time": "unfinished"')
        self.write("personal/missing.md", "# Missing type\n")
        for _ in range(2):
            reply = self.hook("stop")
            self.assertEqual(reply["decision"], "block")
            self.assertIn("personal/missing.md", reply["reason"])
            event = json.loads(log.read_text().splitlines()[-1])
            self.assertEqual(event["decision"], "block")
        self.hook("stop")
        event = json.loads(log.read_text().splitlines()[-1])
        self.assertEqual(event["decision"], "allow")
        report = self.run_script(self.plugin / "skills/status/scripts/status.py")
        self.assertIn("claude-code hooks: last ran " + event["time"], report)
        self.assertEqual(self.hook("stop"), {})
        self.assertEqual(json.loads(log.read_text().splitlines()[-1])["checked"], 0)

    def test_generated_files_are_ignored_by_sync_and_checks(self):
        self.hook("start")
        docs = self.root / ".aiOS/docs"
        before = self.snapshot(docs)
        for relative in (".aiOS/docs/.DS_Store", ".aiOS/docs/__pycache__/bad.md",
                         ".aiOS/docs/media/__pycache__", ".aiOS/docs/media/.DS_Store/bad.md",
                         "personal/__pycache__/bad.md"):
            self.write(relative, "generated content\n")
        self.assert_allowed(self.hook("stop"), checked=0)
        self.hook("start")
        self.assertEqual(self.events()[-1]["docs"]["action"], "unchanged")
        after = self.snapshot(docs)
        for path, original in before.items():
            self.assertEqual(after[path], original)

    def test_docs_sync_accepts_version_suffixes(self):
        self.copy_plugin("0.9.0-beta")
        for version, action in (("0.9.0-beta", "copied"), ("0.9.beta", "unchanged"),
                                ("0.10.2rc1", "replaced"), ("0.9.9", "kept-newer")):
            self.set_version(version)
            self.hook("start")
            self.assertEqual(self.events()[-1]["docs"], {"action": action, "version": version})

    def test_yaml_comments_preserve_quoted_hashes(self):
        self.config('exclude: ["**/Chapter #1/**", \'**/Chapter #2/**\'] # ignore these\n')
        self.hook("start")
        self.write("personal/Chapter #1/missing.md", "# Missing type\n")
        self.write("personal/Chapter #2/missing.md", "# Missing type\n")
        self.write("personal/notes.md")
        self.assert_allowed(self.hook("stop"), checked=1)

    def test_failed_docs_rollback_logs_backup_path(self):
        self.copy_plugin()
        self.hook("start")
        before = self.snapshot(self.root / ".aiOS/docs")
        (self.plugin / "docs/new-doc.md").write_text(DOC)
        runner = self.temporary / "failed-swap.py"
        runner.write_text(textwrap.dedent(f"""
            import os, sys
            from unittest.mock import patch
            sys.path.insert(0, {str(self.plugin / 'hooks')!r})
            import hooks
            replace = os.replace
            def fail_swap(source, target):
                if os.path.basename(target) == "docs":
                    raise OSError("simulated swap or rollback failure")
                replace(source, target)
            with patch("os.replace", fail_swap):
                hooks.hook("start")
        """))
        self.run_script(runner, stdin=json.dumps({"session_id": "next", "cwd": str(self.root)}))
        backups = list((self.root / ".aiOS").glob(".docs-old-*"))
        self.assertEqual(len(backups), 1)
        self.assertEqual(self.snapshot(backups[0]), before)
        docs = self.events()[-1]["docs"]
        self.assertEqual(docs["action"], "error")
        self.assertIn(str(backups[0]), docs["message"])
        self.assertIn("simulated swap or rollback failure", docs["message"])

    def test_frontmatter_mode_warn_allows_failure_and_runs_fixer(self):
        self.config("checks:\n  frontmatter:\n    mode: warn\n")
        self.hook("start")
        path = self.write("personal/notes.md", "---\ntype: memo\n---\n")
        reply = self.hook("stop")
        self.assertNotIn("decision", reply)
        self.assertIn("personal/notes.md", reply["systemMessage"])
        self.assertIn("Rule: default", reply["systemMessage"])
        event = self.events()[-1]
        self.assertEqual(event["decision"], "allow")
        self.assertEqual(event["problems"][0]["mode"], "warn")
        self.assertIn("created", self.fields(path))

    def test_disabled_checks_announce_state_and_skip_checks_and_fixers(self):
        self.config("enabled: false\n")
        reply = self.hook("start")
        context = reply["hookSpecificOutput"]
        self.assertEqual(context["hookEventName"], "SessionStart")
        self.assertIn("Checks are off", context["additionalContext"])
        self.assertEqual(self.events()[-1]["docs"]["action"], "copied")
        bad = self.write("Bad_Folder/missing.md", "# Missing type\n")
        valid = self.write("personal/notes.md")
        self.assertEqual(self.hook("stop"), {})
        self.assertEqual(bad.read_text(), "# Missing type\n")
        self.assertEqual(valid.read_text(), DOC)
        self.assertEqual([event["event"] for event in self.events()], ["start", "stop"])
        self.assertEqual(self.events()[-1]["decision"], "skip")


if __name__ == "__main__":
    unittest.main()
