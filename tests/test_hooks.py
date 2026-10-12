"""Exercise the installed plugin interface without importing its implementation."""

import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap
import time
import unittest
from datetime import datetime
from urllib.parse import unquote, urlsplit
from zoneinfo import ZoneInfo


REPO = Path(__file__).resolve().parents[1]
PLUGIN = REPO / "plugins" / "aios-core"
SAMPLE = PLUGIN / "skills" / "setup-aios" / "assets" / "example"
DOC = "---\ntype: doc\n---\n\n# Notes\n"


def ignore_generated(folder, names):
    """Copy the example or plugin without generated state."""
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
            self.plugin / "skills" / "setup-aios" / "scripts" / "setup.py",
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

    def assert_markdown_links(self, folder, paths=None):
        """Validate local inline links and heading anchors outside fenced examples."""
        folder = folder.resolve()

        def prose(path):
            lines, fence = [], None
            for line in path.read_text(encoding="utf-8").splitlines():
                match = re.match(r"^\s*(`{3,}|~{3,})", line)
                if match:
                    marker = match.group(1)
                    if fence is None:
                        fence = marker
                    elif marker[0] == fence[0] and len(marker) >= len(fence):
                        fence = None
                elif fence is None:
                    lines.append(line)
            return "\n".join(lines)

        def anchors(path):
            found, counts = set(), {}
            for title in re.findall(r"^#{1,6}\s+(.+?)(?:\s+#+)?$", prose(path), re.MULTILINE):
                slug = re.sub(r"[^\w\- ]", "", title.lower()).replace(" ", "-")
                count = counts.get(slug, 0)
                found.add(slug + (f"-{count}" if count else ""))
                counts[slug] = count + 1
            return found

        for path in paths if paths is not None else sorted(folder.rglob("*.md")):
            for destination in re.findall(r"\[[^\]]*\]\(([^)]+)\)", prose(path)):
                link = urlsplit(destination.strip("<>"))
                if link.scheme or link.netloc:
                    continue
                target = (path.parent / unquote(link.path)).resolve() if link.path else path.resolve()
                detail = f"{path.relative_to(folder)}: {destination}"
                self.assertTrue(target == folder or folder in target.parents, "Link leaves the packaged content: " + detail)
                self.assertTrue(target.exists(), "Missing link target: " + detail)
                if link.fragment and target.suffix == ".md":
                    self.assertIn(unquote(link.fragment), anchors(target), "Missing heading anchor: " + detail)

    def copy_plugin(self, version="0.9.0"):
        self.plugin = self.temporary / "plugin"
        shutil.copytree(PLUGIN, self.plugin, ignore=ignore_generated)
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
                         "work/docs/glossary.md", "shared/docs/glossary.md",
                         ".aiOS/AGENTS.md", ".aiOS/config.yaml", ".aiOS/docs/.sync.json"):
            self.assertTrue((self.root / relative).is_file(), relative)
        self.assertTrue((self.root / ".aiOS/logs").is_dir())
        self.assertIn(".aiOS/logs/", (self.root / ".gitignore").read_text().splitlines())
        self.assertIn("[.gitignore](.gitignore)", (self.root / "AGENTS.md").read_text())
        report = self.run_script(PLUGIN / "skills/verify-aios/scripts/status.py")
        self.assertIn("Problems: 0.", report)
        self.hook("start", cwd=self.root / "work")
        path = self.write("work/notes.md")
        self.assert_allowed(self.hook("stop", cwd=self.root / "work"), checked=1)
        self.assertIn("created", self.fields(path))

    def test_setup_initializes_timestamps_without_an_earlier_hook_event(self):
        shutil.rmtree(self.root)
        self.root.mkdir()
        self.env["TZ"] = "UTC"
        self.setup_root(self.root, "work=Fictional equipment repairs.")
        paths = (".aiOS/AGENTS.md", "AGENTS.md", "work/AGENTS.md",
                 "work/docs/glossary.md", "shared/AGENTS.md", "shared/docs/glossary.md")
        for relative in paths:
            fields = self.fields(self.root / relative)
            self.assertEqual(fields["created"], fields["updated"], relative)
            stamp = datetime.fromisoformat(fields["created"])
            self.assertEqual(stamp.utcoffset(), stamp.astimezone(ZoneInfo("America/Los_Angeles")).utcoffset())
        for source in (PLUGIN / "docs").rglob("*.md"):
            copied = self.root / ".aiOS/docs" / source.relative_to(PLUGIN / "docs")
            self.assertEqual(copied.read_bytes(), source.read_bytes())
        self.assertFalse((self.root / ".aiOS/logs/hook-events.jsonl").exists())
        before = self.snapshot(self.root)
        self.assertEqual(self.hook("stop"), {})
        self.assertEqual(self.events()[-1]["decision"], "skip")
        self.hook("start", session="next-session")
        self.assert_allowed(self.hook("stop", session="next-session"), checked=0)
        after = self.snapshot(self.root)
        for relative in paths:
            self.assertEqual(after[relative], before[relative], relative)

    def test_setup_timestamps_respect_enabled_modes_and_exclusions(self):
        paths = {".aiOS/AGENTS.md", "AGENTS.md", "work/AGENTS.md",
                 "work/docs/glossary.md", "shared/AGENTS.md", "shared/docs/glossary.md"}
        cases = [
            ("disabled", "enabled: false\n", set()),
            ("off", "checks:\n  frontmatter:\n    mode: off\n", set()),
            ("warn", "checks:\n  frontmatter:\n    mode: warn\n", paths),
            ("included", 'include: ["work/**"]\n', {"work/AGENTS.md", "work/docs/glossary.md"}),
            ("excluded", 'exclude: ["shared/**"]\n', {p for p in paths if not p.startswith("shared/")}),
            ("check-excluded", 'checks:\n  frontmatter:\n    exclude: ["**/glossary.md"]\n',
             {p for p in paths if not p.endswith("glossary.md")}),
        ]
        for name, config, expected in cases:
            with self.subTest(name=name):
                target = self.temporary / name
                (target / ".aiOS").mkdir(parents=True)
                (target / ".aiOS/config.yaml").write_text(config)
                self.setup_root(target, "work=Fictional equipment repairs.")
                for relative in paths:
                    fields = self.fields(target / relative)
                    for field in ("created", "updated"):
                        self.assertEqual(field in fields, relative in expected, (relative, field))

    def test_setup_timestamps_follow_custom_zone_and_first_matching_rule(self):
        target = self.temporary / "custom-rules"
        (target / ".aiOS").mkdir(parents=True)
        (target / ".aiOS/config.yaml").write_text(textwrap.dedent("""\
            checks:
              frontmatter:
                zone: Asia/Tokyo
                rules:
                  work:
                    match: ["work/**"]
                    timestamps: [updated]
                  other:
                    match: ["**"]
                    timestamps: []
        """))
        self.env["TZ"] = "UTC"
        self.setup_root(target, "work=Fictional equipment repairs.")
        for relative in ("work/AGENTS.md", "work/docs/glossary.md"):
            fields = self.fields(target / relative)
            self.assertNotIn("created", fields)
            self.assertTrue(fields["updated"].endswith("+09:00"), relative)
        for relative in (".aiOS/AGENTS.md", "AGENTS.md", "shared/AGENTS.md", "shared/docs/glossary.md"):
            fields = self.fields(target / relative)
            self.assertNotIn("created", fields)
            self.assertNotIn("updated", fields)

    def test_setup_timestamps_skip_folders_with_separate_settings(self):
        target = self.temporary / "nested-settings"
        (target / "work/.aiOS").mkdir(parents=True)
        nested = target / "work/.aiOS/config.yaml"
        nested.write_text("enabled: true\n")
        before = (nested.read_bytes(), nested.stat().st_mtime_ns)
        self.setup_root(target, "work=Fictional equipment repairs.")
        for relative in ("work/AGENTS.md", "work/docs/glossary.md"):
            self.assertNotIn("created", self.fields(target / relative))
            self.assertNotIn("updated", self.fields(target / relative))
        self.assertIn("created", self.fields(target / "AGENTS.md"))
        self.assertEqual((nested.read_bytes(), nested.stat().st_mtime_ns), before)

    def test_setup_runs_only_the_frontmatter_fixer(self):
        self.copy_plugin()
        (self.plugin / "hooks/checks/unrelated.py").write_text(
            'def fix(files, settings, root):\n    raise RuntimeError("unrelated fixer ran")\n')
        self.config("checks:\n  unrelated:\n    mode: block\n")
        self.setup_root(self.root, "study=Fictional evening classes.")
        self.assertIn("created", self.fields(self.root / "study/AGENTS.md"))

    def test_setup_reports_invalid_configuration_before_creating_markdown(self):
        target = self.temporary / "invalid-settings"
        (target / ".aiOS").mkdir(parents=True)
        (target / ".aiOS/config.yaml").write_text('include: "**"\n')
        before = self.snapshot(target)
        result = subprocess.run(
            [sys.executable, str(PLUGIN / "skills/setup-aios/scripts/setup.py"), str(target)],
            cwd=self.temporary, env=self.env, text=True, capture_output=True, timeout=30,
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("Invalid .aiOS/config.yaml: include must be a list", result.stderr)
        self.assertNotIn("Traceback", result.stderr)
        self.assertEqual(self.snapshot(target), before)

    def test_setup_reports_timestamp_fixer_failures(self):
        self.copy_plugin()
        (self.plugin / "hooks/checks/frontmatter.py").write_text(
            'def fix(files, settings, root):\n    raise OSError("timestamp write failed")\n')
        before = self.snapshot(self.root)
        result = subprocess.run(
            [sys.executable, str(self.plugin / "skills/setup-aios/scripts/setup.py"), str(self.root),
             "--workspace", "study=Fictional evening classes."],
            cwd=self.temporary, env=self.env, text=True, capture_output=True, timeout=30,
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("Could not initialize timestamps", result.stderr)
        self.assertIn("[frontmatter] study/AGENTS.md: could not read: timestamp write failed", result.stderr)
        self.assertNotIn("Traceback", result.stderr)
        after = self.snapshot(self.root)
        for relative, original in before.items():
            self.assertEqual(after[relative], original, relative)

    def test_standalone_example_passes_status_without_changing_source(self):
        before = self.snapshot(SAMPLE)
        self.assertFalse((SAMPLE / ".aiOS/docs").exists())
        self.setup_root()
        report = self.status()
        self.assertIn("Problems: 0.", report)
        self.assertIn("matches the installed plugin", report)
        self.assertTrue((self.root / ".aiOS/docs/.sync.json").is_file())
        self.assertEqual(self.snapshot(SAMPLE), before)

    def test_standalone_example_links_resolve_after_docs_generation(self):
        self.setup_root()
        self.assert_markdown_links(self.root)

    def test_plugin_only_copy_can_set_up_and_validate_its_example(self):
        self.copy_plugin()
        skill = self.plugin / "skills/setup-aios"
        guide = skill / "references/example.md"
        packaged_example = skill / "assets/example"
        self.assertTrue(guide.is_file())
        self.assert_markdown_links(self.plugin, paths=[guide, *sorted((self.plugin / "skills").glob("*/SKILL.md"))])
        standalone = self.temporary / "installed-example"
        shutil.copytree(packaged_example, standalone, ignore=ignore_generated)
        self.setup_root(standalone)
        report = self.run_script(self.plugin / "skills/verify-aios/scripts/status.py", cwd=standalone)
        self.assertIn("Problems: 0.", report)
        marker = json.loads((standalone / ".aiOS/docs/.sync.json").read_text())
        self.assertEqual(marker["version"], "0.9.0")
        self.assertFalse((packaged_example / ".aiOS/docs").exists())
        self.assert_markdown_links(standalone)

    def test_setup_adds_missing_pieces_without_overwriting_files(self):
        self.setup_root()
        self.write("AGENTS.md", "---\ntype: AGENTS.md\n---\n\n# Custom root\n")
        self.write(".aiOS/config.yaml", "enabled: true\n# Keep this preference.\n")
        self.write(".aiOS/docs/local.md", DOC)
        self.write("home/notes.md", DOC + "Keep this note.\n")
        (self.root / "shared/AGENTS.md").unlink()
        shutil.rmtree(self.root / ".aiOS/logs")
        before = self.snapshot(self.root)
        output = self.setup_root(self.root, "study=Fictional evening classes.")
        after = self.snapshot(self.root)
        self.assertIn("Skipped existing", output)
        for path, original in before.items():
            self.assertEqual(after[path], original, path)
        self.assertEqual(set(after) - set(before), {"shared/AGENTS.md", "study/AGENTS.md", "study/docs/glossary.md"})
        for relative in set(after) - set(before):
            fields = self.fields(self.root / relative)
            self.assertEqual(fields["created"], fields["updated"], relative)
        self.assertTrue((self.root / ".aiOS/logs").is_dir())
        self.setup_root()
        self.assertEqual(self.snapshot(self.root), after)
        self.hook("start")
        self.write("home/notes.md", DOC + "A new action.\n")
        self.assert_allowed(self.hook("stop"), checked=1)

    def test_setup_appends_log_exclusion_only_once(self):
        self.write(".gitignore", "custom-cache/")
        self.setup_root()
        expected = "custom-cache/\n.aiOS/logs/\n"
        self.assertEqual((self.root / ".gitignore").read_text(), expected)
        self.setup_root()
        self.assertEqual((self.root / ".gitignore").read_text(), expected)
        self.hook("start")
        self.write("home/notes.md")
        self.assert_allowed(self.hook("stop"), checked=1)

    def test_missing_type_blocks_with_file_and_rule(self):
        self.hook("start")
        self.write("home/missing.md", "# No front matter\n")
        self.assert_blocked(self.hook("stop"), "home/missing.md",
                            "missing front matter: type", "Rule: default")

    def test_disallowed_type_blocks_with_file_and_rule(self):
        self.hook("start")
        self.write("home/memo.md", "---\ntype: memo\n---\n")
        self.assert_blocked(self.hook("stop"), "home/memo.md",
                            "type 'memo' is not allowed", "Rule: default")

    def test_bad_folder_name_blocks(self):
        self.hook("start")
        self.write("home/Bad_Folder/notes.md")
        self.assert_blocked(self.hook("stop"), "home/Bad_Folder", "[names]",
                            "lowercase, hyphenated, one to four words")

    def test_hidden_folder_names_are_exempt(self):
        self.hook("start")
        self.write(".aiOS/notes.md")
        self.write(".Hidden_Folder/invalid.md", "No front matter\n")
        # .aiOS is checked, while other hidden folders are outside the scope.
        self.assert_allowed(self.hook("stop"), checked=1)

    def test_skill_name_must_match_its_folder(self):
        self.hook("start")
        self.write("home/skills/weekly-review/SKILL.md",
                   "---\nname: wrong-name\ndescription: Review the week.\n---\n")
        self.assert_blocked(self.hook("stop"), "home/skills/weekly-review/SKILL.md",
                            "must match its folder 'weekly-review'", "Rule: skill")

    def test_skill_resources_need_no_front_matter(self):
        self.hook("start")
        skill = self.write("home/skills/weekly-review/SKILL.md",
                           "---\nname: weekly-review\ndescription: Review the week.\n---\n")
        resource = self.write("home/skills/weekly-review/references/questions.md",
                              "# What remains unfinished?\n")
        before = (skill.read_bytes(), resource.read_bytes())
        event = self.assert_allowed(self.hook("stop"), checked=2)
        self.assertEqual(event["fixed"], [])
        self.assertEqual((skill.read_bytes(), resource.read_bytes()), before)

    def test_passing_turn_fills_created_and_updated(self):
        self.hook("start")
        path = self.write("home/notes.md")
        event = self.assert_allowed(self.hook("stop"), checked=1)
        fields = self.fields(path)
        self.assertEqual(fields["created"], fields["updated"])
        self.assertIsNotNone(datetime.fromisoformat(fields["created"]).tzinfo)
        self.assertEqual(event["fixed"], [{"check": "frontmatter", "path": "home/notes.md"}])
        self.assertTrue(path.read_text().endswith("\n# Notes\n"))

    def test_existing_created_survives_an_edit(self):
        self.hook("start")
        path = self.write("home/notes.md",
                          "---\ntype: doc\ncreated: 2001-01-02T03:04-08:00\n"
                          "updated: 2001-01-02T03:04-08:00\n---\n\n# Changed notes\n")
        self.assert_allowed(self.hook("stop"), checked=1)
        fields = self.fields(path)
        self.assertEqual(fields["created"], "2001-01-02T03:04-08:00")
        self.assertNotEqual(fields["updated"], fields["created"])

    def test_existing_created_survives_replacement_with_identical_content(self):
        path = self.write("home/notes.md",
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
        path = self.write("home/notes.md")
        self.assert_allowed(self.hook("stop", session="second"), checked=1)
        before = (path.read_bytes(), path.stat().st_mtime_ns)
        event = self.assert_allowed(self.hook("stop", session="first"), checked=1)
        self.assertEqual(event["session"], "first")
        self.assertEqual(event["fixed"], [])
        self.assertEqual((path.read_bytes(), path.stat().st_mtime_ns), before)

    def test_max_blocks_allows_third_attempt_with_warning_and_resets(self):
        self.config("enabled: true\nmax_blocks: 2\n")
        self.hook("start")
        self.write("home/missing.md", "# Missing type\n")
        for _ in range(2):
            self.assert_blocked(self.hook("stop"), "home/missing.md", "Rule: default")
        reply = self.hook("stop")
        self.assertNotIn("decision", reply)
        self.assertIn("home/missing.md", reply["systemMessage"])
        self.assertEqual(self.events()[-1]["decision"], "allow")
        self.assertEqual(len(self.events()[-1]["problems"]), 1)
        self.assert_allowed(self.hook("stop"), checked=0)
        self.write("home/missing.md", "# Still missing type\n")
        self.assert_blocked(self.hook("stop"), "home/missing.md", "Rule: default")

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
        self.write("home/notes.md")
        self.assert_allowed(self.hook("stop"), checked=1)

    def test_docs_sync_leaves_identical_version_and_content_unchanged(self):
        self.hook("start")
        before = self.snapshot(self.root / ".aiOS/docs")
        self.hook("start", session="next")
        self.assertEqual(self.events()[-1]["docs"]["action"], "unchanged")
        self.assertEqual(self.snapshot(self.root / ".aiOS/docs"), before)
        self.write("home/notes.md")
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
        self.write("home/notes.md")
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
        self.write("home/notes.md")
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
        self.write("home/notes.md")
        self.assert_allowed(self.hook("stop", session="older"), checked=1)
        report = self.run_script(self.plugin / "skills/verify-aios/scripts/status.py")
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
        self.write("home/notes.md")
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
        nested = self.root / "home/nested-root"
        self.setup_root(nested)
        self.hook("start", session="outer")
        self.hook("start", session="inner", cwd=nested)
        self.write("home/nested-root/Bad_Folder/missing.md", "# Missing type\n")
        self.write("home/notes.md")
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
        paths = ("meetings/notes.md", "work/projects/meetings/notes.md")
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
        self.write("work/meetings/notes.md", "---\ntype: doc\ndate: 2026-04-12\n---\n")
        self.assert_blocked(self.hook("stop"), "work/meetings/notes.md",
                            "type 'doc' is not allowed", "Rule: meetings")
        self.write("work/meetings/notes.md", "---\ntype: meeting\ndate: 2026-04-12\n---\n")
        self.write("home/notes.md")
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
        self.write("home/notes.md")
        self.assert_blocked(self.hook("stop"), "home/notes.md",
                            "type 'doc' is not allowed", "Rule: custom")
        path = self.write("home/notes.md", "---\ntype: memo\n---\n")
        self.assert_allowed(self.hook("stop"), checked=1)
        self.assertIn("created", self.fields(path))

    def test_names_mode_off_allows_bad_folder_name(self):
        self.config("checks:\n  names:\n    mode: off\n")
        self.hook("start")
        self.write("home/Bad_Folder/notes.md")
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
        self.write("home/notes.md")
        self.assert_blocked(self.hook("stop"), ".aiOS/config.yaml", "unknown or unavailable check")
        self.assertFalse(marker.exists())

    def test_block_and_inline_configuration_lists_select_the_same_files(self):
        for index, config in enumerate((
            'include: ["home/**"]\nexclude: ["home/skipped/**"]\n',
            'include:\n  - "home/**"\nexclude:\n  - "home/skipped/**"\n',
        )):
            with self.subTest(config=config):
                self.config(config)
                session = f"list-{index}"
                self.hook("start", session=session)
                self.write("home/notes.md")
                self.write("home/skipped/missing.md", "# Missing type\n")
                self.write("other/missing.md", "# Missing type\n")
                self.assert_allowed(self.hook("stop", session=session), checked=1)

    def test_invalid_configuration_is_reported_before_file_checks(self):
        cases = (
            ('include: "**"\n', "include must be a list"),
            ('exclude: false\n', "exclude must be a list"),
            ('enabled: "false"\n', "enabled must be true or false"),
            ('max_blocks: -1\n', "max_blocks must be a nonnegative integer"),
            ('checks: []\n', "checks must be a mapping"),
            ('checks:\n  names: off\n', "checks.names must be a mapping"),
            ('checks:\n  frontmater:\n    mode: block\n', "unknown or unavailable check"),
            ('checks:\n  common:\n    mode: block\n', "no callable check or fix function"),
            ('checks:\n  names:\n    mode: warning\n', "mode must be block, warn, or off"),
            ('checks:\n  names:\n    exclude: "**"\n', "exclude must be a list"),
            ('checks:\n  names:\n    mod: off\n', "unknown settings: mod"),
            ('checks:\n  frontmatter:\n    zone: No/Such_Zone\n', "not a known time zone"),
            ('checks:\n  frontmatter:\n    rules: []\n', "rules must be a mapping"),
            ('checks:\n  frontmatter:\n    rules:\n      default:\n        required: type\n', "required must be a list"),
            ('include: ["**"\n', "close the inline list"),
            ('include: ["**"]\ninclude: []\n', "duplicate setting 'include'"),
            ('enabled: true\nunknown: true\n', "unknown settings: unknown"),
        )
        for index, (config, expected) in enumerate(cases):
            with self.subTest(config=config):
                self.config(config)
                session = f"invalid-{index}"
                reply = self.hook("start", session=session)
                self.assertIn(expected, reply["hookSpecificOutput"]["additionalContext"])
                self.assertEqual(self.events()[-1]["problems"][0]["check"], "configuration")
                self.assert_blocked(self.hook("stop", session=session), ".aiOS/config.yaml", expected)
                self.assertEqual(self.events()[-1]["checked"], 0)

    def test_configuration_failures_obey_block_limit_and_recover(self):
        self.config('max_blocks: 1\ninclude: "**"\n')
        self.hook("start")
        path = self.write("home/notes.md")
        self.assert_blocked(self.hook("stop"), ".aiOS/config.yaml", "include must be a list")
        self.assertEqual(path.read_text(), DOC)
        reply = self.hook("stop")
        self.assertIn("[configuration]", reply["systemMessage"])
        self.assertEqual(self.events()[-1]["decision"], "allow")
        self.config('max_blocks: 1\ninclude: ["**"]\n')
        self.write("home/notes.md", DOC + "A later edit.\n")
        self.assert_allowed(self.hook("stop"), checked=1)
        self.assertIn("created", self.fields(path))

    def test_custom_fix_only_check_runs_with_its_own_settings(self):
        self.copy_plugin()
        (self.plugin / "hooks/checks/append-note.py").write_text(textwrap.dedent("""
            import os
            def fix(files, settings, root):
                changed = []
                for path in files:
                    with open(path, "a", encoding="utf-8") as stream:
                        stream.write(settings["note"] + "\\n")
                    changed.append(os.path.relpath(path, root))
                return changed
        """))
        self.config('checks:\n  append-note:\n    mode: block\n    note: Added by the custom fixer.\n')
        self.hook("start")
        path = self.write("home/notes.md")
        event = self.assert_allowed(self.hook("stop"), checked=1)
        self.assertTrue(path.read_text().endswith("Added by the custom fixer.\n"))
        self.assertIn({"check": "append-note", "path": "home/notes.md"}, event["fixed"])

    def test_repairing_configuration_checks_files_from_the_blocked_turn(self):
        self.config('max_blocks: nope\n')
        self.hook("start")
        self.write("home/missing.md", "# Missing type\n")
        self.assert_blocked(self.hook("stop"), ".aiOS/config.yaml", "max_blocks")
        self.config('enabled: true\n')
        self.assert_blocked(self.hook("stop"), "home/missing.md", "missing front matter: type")

    def test_status_reports_configuration_failure_with_nonzero_exit(self):
        self.config('include: "**"\n')
        result = subprocess.run(
            [sys.executable, str(PLUGIN / "skills/verify-aios/scripts/status.py")],
            cwd=self.root, env=self.env, text=True, capture_output=True, timeout=30,
        )
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stderr, "")
        self.assertIn("[configuration] .aiOS/config.yaml: include must be a list", result.stdout)
        self.assertIn("File checks did not run", result.stdout)
        self.assertNotIn("Problems: 0", result.stdout)

    def test_quoted_front_matter_and_inline_comments_use_decoded_values(self):
        self.hook("start")
        path = self.write("home/notes.md",
                          '---\ntype: "doc" # Document type\n'
                          'created: "2001-01-02T03:04-08:00" # Keep this timestamp\n'
                          'updated: \'2001-01-02T03:04-08:00\'\n---\n\n# Notes\n')
        skill = self.write("home/skills/weekly-review/SKILL.md",
                           '---\nname: "weekly-review" # Matches the folder\n'
                           "description: 'Reviews the operator''s week, including #1.' # Comment\n---\n# Review\n")
        original = skill.read_bytes()
        self.assert_allowed(self.hook("stop"), checked=2)
        self.assertIn('created: "2001-01-02T03:04-08:00" # Keep this timestamp', path.read_text())
        self.assertTrue(path.read_text().endswith("\n# Notes\n"))
        self.assertEqual(skill.read_bytes(), original)

    def test_skill_fields_must_be_nonempty_top_level_strings(self):
        cases = (
            ('name: weekly-review\ndescription: ""', "missing front matter: description"),
            ('name: weekly-review\ndescription: "   "', "description must be a nonempty top-level string"),
            ('name: weekly-review\ndescription: false', "description must be a nonempty top-level string"),
            ('name: weekly-review\ndescription: 123', "description must be a nonempty top-level string"),
            ('name: false\ndescription: Review the week.', "name must be a nonempty top-level string"),
            ('metadata:\n  name: weekly-review\n  description: Review the week.', "missing front matter: name, description"),
        )
        for index, (fields, expected) in enumerate(cases):
            with self.subTest(fields=fields):
                session = f"skill-fields-{index}"
                self.hook("start", session=session)
                self.write("home/skills/weekly-review/SKILL.md", f"---\n{fields}\n---\n# Review\n")
                self.assert_blocked(self.hook("stop", session=session), "SKILL.md", expected)

    def test_invalid_front_matter_is_reported_without_rewriting_it(self):
        self.config('max_blocks: 0\n')
        self.hook("start")
        content = '---\ntype: "doc\n---\n# Preserve this content\n'
        path = self.write("home/notes.md", content)
        reply = self.hook("stop")
        self.assertIn("invalid front matter", reply["systemMessage"])
        self.assertNotIn("could not read", reply["systemMessage"])
        self.assertEqual(path.read_text(), content)
        self.assertEqual(self.events()[-1]["fixed"], [])

    def test_symlinks_are_outside_check_and_fixer_scope(self):
        self.hook("start")
        outside = self.temporary / "outside"
        outside.mkdir()
        target = outside / "notes.md"
        target.write_text(DOC)
        before = self.snapshot(outside)
        (self.root / "home/linked.md").symlink_to(target)
        (self.root / "home/linked-folder").symlink_to(outside, target_is_directory=True)
        (self.root / ".aiOS/docs/linked.md").symlink_to(target)
        (self.root / "home/broken.md").symlink_to(outside / "missing.md")
        self.write("home/notes.md")
        self.assert_allowed(self.hook("stop"), checked=1)
        self.assertEqual(self.snapshot(outside), before)

    def test_unreadable_file_does_not_disable_turn(self):
        self.hook("start")
        bad = self.write("home/a-unreadable.md")
        content = DOC.encode("utf-8") + b"\xff"
        bad.write_bytes(content)
        self.write("home/missing.md", "# Missing type\n")
        valid = self.write("home/notes.md")
        for _ in range(2):
            reply = self.hook("stop")
            self.assert_blocked(reply, "home/a-unreadable.md", "could not read:", "utf-8")
            self.assert_blocked(reply, "home/missing.md", "missing front matter: type")
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
        self.write("home/missing.md", "# Missing type\n")
        for _ in range(2):
            reply = self.hook("stop")
            self.assertEqual(reply["decision"], "block")
            self.assertIn("home/missing.md", reply["reason"])
            event = json.loads(log.read_text().splitlines()[-1])
            self.assertEqual(event["decision"], "block")
        self.hook("stop")
        event = json.loads(log.read_text().splitlines()[-1])
        self.assertEqual(event["decision"], "allow")
        report = self.run_script(self.plugin / "skills/verify-aios/scripts/status.py")
        self.assertIn("claude-code: last ran " + event["time"], report)
        self.assertEqual(self.hook("stop"), {})
        self.assertEqual(json.loads(log.read_text().splitlines()[-1])["checked"], 0)

    def test_generated_files_are_ignored_by_sync_and_checks(self):
        self.hook("start")
        docs = self.root / ".aiOS/docs"
        before = self.snapshot(docs)
        # Keep .DS_Store as a file; directories with that name trigger security alerts.
        for relative in (".aiOS/docs/.DS_Store", ".aiOS/docs/__pycache__/bad.md",
                         ".aiOS/docs/media/__pycache__/bad.md", ".aiOS/docs/media/.DS_Store",
                         "home/__pycache__/bad.md"):
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
        self.write("home/Chapter #1/missing.md", "# Missing type\n")
        self.write("home/Chapter #2/missing.md", "# Missing type\n")
        self.write("home/notes.md")
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
        path = self.write("home/notes.md", "---\ntype: memo\n---\n")
        reply = self.hook("stop")
        self.assertNotIn("decision", reply)
        self.assertIn("home/notes.md", reply["systemMessage"])
        self.assertIn("Rule: default", reply["systemMessage"])
        event = self.events()[-1]
        self.assertEqual(event["decision"], "allow")
        self.assertEqual(event["problems"][0]["mode"], "warn")
        self.assertIn("created", self.fields(path))

    def status(self, *args, cwd=None):
        return self.run_script(PLUGIN / "skills/verify-aios/scripts/status.py", *args, cwd=cwd)

    def test_status_prints_sections_in_order(self):
        self.hook("start")
        lines = self.status().splitlines()
        self.assertTrue(lines[0].startswith("Folder: "), lines[0])
        headings = [line for line in lines if line in ("Settings", "Versions", "Hooks", "Files")]
        self.assertEqual(headings, ["Settings", "Versions", "Hooks", "Files"])
        self.assertIn("  Check modes: frontmatter block, names block, docs-copy warn", lines)
        self.assertIn("  Docs copy: " + json.loads((PLUGIN / ".claude-plugin/plugin.json").read_text())["version"]
                      + "; matches the installed plugin", lines)
        self.assertIn("Problems: 0.", lines[-1])
        self.assertNotIn("Latest blocked turn", "\n".join(lines))
        self.assertNotIn("Historical block", lines)

    def test_status_lists_edited_docs_copy_files(self):
        self.hook("start")
        self.assertIn("  Edited docs copy files: none\n", self.status())
        path = self.root / ".aiOS/docs/hooks.md"
        path.write_text(path.read_text() + "\nA local edit.\n")
        report = self.status()
        self.assertIn("  Edited docs copy files: .aiOS/docs/hooks.md\n", report)
        self.assertIn("  [docs-copy] .aiOS/docs/hooks.md: ", report)

    def test_status_omits_corrected_historical_failure(self):
        self.hook("start")
        self.write("home/missing.md", "# Missing type\n")
        self.assertEqual(self.hook("stop")["decision"], "block")
        self.write("home/missing.md")
        self.assert_allowed(self.hook("stop"))
        event = self.events()[-1]
        report = self.status()
        self.assertIn("claude-code: last ran " + event["time"], report)
        self.assertIn("Problems: 0.", report)
        self.assertNotIn("home/missing.md", report)
        self.assertNotIn("Latest blocked turn", report)
        self.assertNotIn("Historical block", report)

    def test_status_omits_excluded_historical_failure_without_claiming_resolution(self):
        self.hook("start")
        path = self.write("home/missing.md", "# Missing type\n")
        self.assertEqual(self.hook("stop")["decision"], "block")
        self.config('exclude: ["home/**"]\n')
        report = self.status()
        self.assertIn("Problems: 0.", report)
        self.assertNotIn("home/missing.md", report)
        self.assertNotIn("Latest blocked turn", report)
        self.assertNotIn("Historical block", report)
        self.assertNotIn("resolved", report.lower())
        self.assertNotIn("fixed", report.lower())
        self.assertEqual(path.read_text(), "# Missing type\n")
        history = self.status("--last-block")
        self.assertIn("Historical block\n", history)
        self.assertIn("Recorded hook result; does not establish current status.", history)
        self.assertIn("    [frontmatter] home/missing.md: missing front matter: type", history)
        self.assertIn("Problems: 0.", history)
        self.assertNotIn("resolved", history.lower())
        self.assertNotIn("fixed", history.lower())

    def test_status_reports_current_failure_without_repeating_its_history(self):
        self.hook("start")
        self.write("home/missing.md", "# Missing type\n")
        self.assertEqual(self.hook("stop")["decision"], "block")
        report = self.status()
        self.assertIn("Files\n  [frontmatter] home/missing.md: missing front matter: type", report)
        self.assertIn("Problems: 1.", report)
        self.assertEqual(report.count("home/missing.md"), 1)
        self.assertNotIn("Latest blocked turn", report)
        self.assertNotIn("Historical block", report)

    def test_status_last_block_reports_no_recorded_block(self):
        log = self.root / ".aiOS/logs/hook-events.jsonl"
        self.assertFalse(log.exists())
        report = self.status("--last-block")
        self.assertIn("Historical block\n  Latest blocked turn: none\n", report)
        self.assertIn("claude-code: never ran here", report)
        self.assertIn("Problems: 0.", report)
        self.assertFalse(log.exists())
        self.hook("start")
        self.assertIn("Historical block\n  Latest blocked turn: none\n", self.status("--last-block"))

    def test_status_last_block_shows_latest_record_even_after_correction(self):
        self.hook("start")
        self.write("home/first.md", "# Missing type\n")
        self.assertEqual(self.hook("stop")["decision"], "block")
        self.write("home/first.md")
        self.write("home/latest.md", "# Missing type\n")
        self.assertEqual(self.hook("stop")["decision"], "block")
        event = self.events()[-1]
        self.write("home/latest.md")
        self.assert_allowed(self.hook("stop"))
        report = self.status("--last-block")
        headings = [line for line in report.splitlines()
                    if line in ("Settings", "Versions", "Hooks", "Historical block", "Files")]
        self.assertEqual(headings, ["Settings", "Versions", "Hooks", "Historical block", "Files"])
        self.assertIn("Recorded hook result; does not establish current status.", report)
        self.assertIn(f"  Latest blocked turn: {event['time']} in claude-code: 1 problem\n", report)
        self.assertIn("    [frontmatter] home/latest.md: missing front matter: type", report)
        self.assertNotIn("home/first.md", report)
        self.assertIn("Problems: 0.", report)

    def test_status_modes_leave_hook_log_unchanged(self):
        self.hook("start")
        self.write("home/missing.md", "# Missing type\n")
        self.assertEqual(self.hook("stop")["decision"], "block")
        logs = self.root / ".aiOS/logs"
        before = self.snapshot(logs)
        self.status()
        self.assertEqual(self.snapshot(logs), before)
        self.status("--last-block")
        self.assertEqual(self.snapshot(logs), before)

    def test_status_lists_nested_roots_it_skips(self):
        self.assertIn("Folders with separate settings skipped: none\n", self.status())
        self.setup_root(self.root / "home/nested-root")
        self.write("home/nested-root/Bad_Folder/missing.md", "# Missing type\n")
        report = self.status()
        self.assertIn("Folders with separate settings skipped: home/nested-root\n", report)
        self.assertNotIn("Bad_Folder", report)

    def test_core_plugin_ships_exactly_four_skills(self):
        skills = {path.name for path in (PLUGIN / "skills").iterdir() if path.is_dir()}
        self.assertEqual(skills, {"manage-agents-md", "manage-skills", "setup-aios", "verify-aios"})
        for name in skills:
            self.assertEqual(self.fields(PLUGIN / "skills" / name / "SKILL.md")["name"], name)

    def test_disabled_checks_announce_state_and_skip_checks_and_fixers(self):
        self.config("enabled: false\n")
        reply = self.hook("start")
        context = reply["hookSpecificOutput"]
        self.assertEqual(context["hookEventName"], "SessionStart")
        self.assertIn("Checks are off", context["additionalContext"])
        self.assertEqual(self.events()[-1]["docs"]["action"], "copied")
        bad = self.write("Bad_Folder/missing.md", "# Missing type\n")
        valid = self.write("home/notes.md")
        self.assertEqual(self.hook("stop"), {})
        self.assertEqual(bad.read_text(), "# Missing type\n")
        self.assertEqual(valid.read_text(), DOC)
        self.assertEqual([event["event"] for event in self.events()], ["start", "stop"])
        self.assertEqual(self.events()[-1]["decision"], "skip")


if __name__ == "__main__":
    unittest.main()
