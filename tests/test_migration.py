"""Exercise the migration CLI and its interaction with the real timestamp fixer."""

from datetime import datetime
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import time
from types import SimpleNamespace
import unittest
from unittest.mock import patch
from zoneinfo import ZoneInfo


REPO = Path(__file__).resolve().parents[1]
PLUGIN = REPO / "plugins" / "aios-core"
SCRIPT = PLUGIN / "skills" / "setup-aios" / "scripts" / "migrate.py"
SOURCE_MTIME_NS = 1577934245123456789


class MigrationTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix=".aios-tests-migration-", dir=REPO)
        self.addCleanup(temporary.cleanup)
        self.temporary = Path(temporary.name)
        self.source = self.temporary / "source"
        self.root = self.temporary / "destination"
        self.source.mkdir()
        self.mapping = self.temporary / "mapping.json"
        self.record = self.temporary / "record.json"
        self.env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
        self.env.pop("PLUGIN_ROOT", None)

    def write_source(self, name="notes.md", data=b"# Original notes\n"):
        path = self.source / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        os.utime(path, ns=(SOURCE_MTIME_NS, SOURCE_MTIME_NS))
        return path

    def write_mapping(self, entries):
        self.mapping.write_text(json.dumps({"files": entries}))

    def entry(self, source, destination="notes.md", **fields):
        return dict(source=str(source), destination=str(self.root / destination), **fields)

    def cli(self, *args, success=True):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), str(self.mapping), *map(str, args)],
            cwd=self.temporary, env=self.env, text=True, capture_output=True, timeout=30,
        )
        if success:
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(result.stderr, "")
        else:
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("Migration stopped:", result.stderr)
            self.assertNotIn("Traceback", result.stderr)
        return result

    def apply(self, success=True, record=None):
        return self.cli("--zone", "UTC", "--apply", "--record", record or self.record,
                        success=success)

    @staticmethod
    def snapshot(path):
        info = path.stat()
        return (path.read_bytes(), info.st_mtime_ns, stat.S_IMODE(info.st_mode),
                getattr(info, "st_birthtime", None))

    @staticmethod
    def fields(path):
        header = path.read_text().split("---", 2)[1]
        return dict(line.split(": ", 1) for line in header.splitlines()
                    if ": " in line and not line.startswith(" "))

    def require_birthtime(self, source):
        if not hasattr(source.stat(), "st_birthtime"):
            self.skipTest("This filesystem does not expose creation time")

    def test_preview_changes_neither_sources_nor_destination(self):
        source = self.write_source(data=b"---\ntitle: Original\n---\n\n# Original notes\n")
        self.require_birthtime(source)
        before = self.snapshot(source)
        self.write_mapping([self.entry(source, type="doc")])
        preview = json.loads(self.cli("--zone", "UTC", "--record", self.record).stdout)
        self.assertEqual(preview["mode"], "preview")
        self.assertEqual(preview["files"][0]["status"], "planned")
        self.assertEqual(preview["files"][0]["source"], str(source))
        self.assertEqual(self.snapshot(source), before)
        self.assertFalse(self.root.exists())
        self.assertFalse(self.record.exists())

    def test_import_preserves_body_custom_fields_source_dates_and_receipt_hashes(self):
        body = b"\r\n# Original notes\r\n\r\nKeep this exact body.\r\n"
        source = self.write_source(data=(
            b"---\r\ntype: old\r\ncreated: 1990-01-01\r\nupdated: 1991-01-01\r\n"
            b"title: 'Original # notes' # Keep this comment\r\n"
            b"metadata:\r\n  owner: Example\r\n---\r\n" + body))
        self.require_birthtime(source)
        before = self.snapshot(source)
        info = source.stat()
        self.write_mapping([self.entry(source, type="doc")])
        earliest = datetime.now(ZoneInfo("UTC")).replace(second=0, microsecond=0)
        self.apply()
        latest = datetime.now(ZoneInfo("UTC"))
        destination = self.root / "notes.md"
        data, fields = destination.read_bytes(), self.fields(destination)
        self.assertEqual(data.split(b"---\r\n", 2)[2], body)
        self.assertIn(b"title: 'Original # notes' # Keep this comment\r\n", data)
        self.assertIn(b"metadata:\r\n  owner: Example\r\n", data)
        self.assertEqual(fields["type"], "doc")
        self.assertEqual(fields["created"], datetime.fromtimestamp(
            info.st_birthtime, ZoneInfo("UTC")).isoformat(timespec="minutes"))
        self.assertEqual(fields["updated"], "2020-01-02T03:04+00:00")
        self.assertLessEqual(earliest, datetime.fromisoformat(fields["migrated"]))
        self.assertLessEqual(datetime.fromisoformat(fields["migrated"]), latest)
        self.assertEqual(destination.stat().st_mtime_ns, info.st_mtime_ns)
        self.assertEqual(self.snapshot(source), before)
        receipt = json.loads(self.record.read_text())["files"][0]
        self.assertEqual(receipt["status"], "copied")
        self.assertEqual(receipt["source_sha256"], hashlib.sha256(before[0]).hexdigest())
        self.assertEqual(receipt["destination_sha256"], hashlib.sha256(data).hexdigest())
        self.assertEqual(receipt["source_mtime_ns"], info.st_mtime_ns)
        self.assertEqual(receipt["source_birthtime"], info.st_birthtime)
        self.assertEqual(receipt["migrated"], fields["migrated"])

    def test_prepared_contract_uses_source_dates_and_prepared_body(self):
        source = self.write_source("instructions.md")
        self.require_birthtime(source)
        prepared = self.write_source("prepared.md", b"# Adapted contract\n\nKeep inherited instructions.\n")
        os.utime(prepared, (1700000000, 1700000000))
        before = {path: self.snapshot(path) for path in (source, prepared)}
        self.write_mapping([self.entry(source, "AGENTS.md", type="AGENTS.md", content_file=str(prepared))])
        self.apply()
        destination = self.root / "AGENTS.md"
        self.assertTrue(destination.read_bytes().endswith(prepared.read_bytes()))
        self.assertEqual(self.fields(destination)["type"], "AGENTS.md")
        self.assertEqual(self.fields(destination)["updated"], "2020-01-02T03:04+00:00")
        for path, original in before.items():
            self.assertEqual(self.snapshot(path), original)

    def test_exempt_skill_foreign_frontmatter_and_binary_files_remain_byte_exact(self):
        contents = {
            "example/SKILL.md": b"---\nname: example\ndescription: An example.\n---\n\n# Example\n",
            "example/reference.md": b"# Skill reference\n",
            "foreign.md": b"---\nlayout: post\nsummary: |\n  Multiline text\n---\n\n# Post\n",
            "archive.bin": b"\x00\xff\x80\r\n",
        }
        sources = {name: self.write_source(name, data) for name, data in contents.items()}
        os.chmod(sources["archive.bin"], 0o750)
        before = {name: self.snapshot(path) for name, path in sources.items()}
        self.write_mapping([self.entry(path, name) for name, path in sources.items()])
        self.apply()
        for name, original in before.items():
            destination = self.root / name
            self.assertEqual(destination.read_bytes(), original[0])
            self.assertEqual(destination.stat().st_mtime_ns, original[1])
            self.assertEqual(stat.S_IMODE(destination.stat().st_mode), original[2])
            self.assertEqual(self.snapshot(sources[name]), original)
        receipt = json.loads(self.record.read_text())
        self.assertTrue(all(entry["fields"] == {} and entry["migrated"] for entry in receipt["files"]))

    def test_existing_destination_rejects_entire_batch_before_writing(self):
        source = self.write_source()
        conflict = self.root / "existing.md"
        conflict.parent.mkdir()
        conflict.write_bytes(b"Operator's existing content\n")
        before = self.snapshot(conflict)
        self.write_mapping([self.entry(source, "new.md"), self.entry(source, "existing.md")])
        self.apply(success=False)
        self.assertEqual(self.snapshot(conflict), before)
        self.assertFalse((self.root / "new.md").exists())
        self.assertFalse(self.record.exists())

    def test_existing_file_in_destination_parent_rejects_batch_before_writing(self):
        source = self.write_source()
        self.root.mkdir()
        blocker = self.root / "folder"
        blocker.write_bytes(b"Existing file, not a folder\n")
        before = self.snapshot(blocker)
        self.write_mapping([self.entry(source, "new.md"), self.entry(source, "folder/notes.md")])
        self.apply(success=False)
        self.assertEqual(self.snapshot(blocker), before)
        self.assertFalse((self.root / "new.md").exists())
        self.assertFalse(self.record.exists())

    def test_duplicate_and_conflicting_planned_destinations_write_nothing(self):
        source = self.write_source()
        for paths in [("notes.md", "notes.md"), ("folder", "folder/notes.md")]:
            with self.subTest(paths=paths):
                self.write_mapping([self.entry(source, path) for path in paths])
                self.apply(success=False)
                self.assertFalse(self.root.exists())
                self.assertFalse(self.record.exists())

    def test_existing_record_is_preserved_without_creating_destination(self):
        source = self.write_source()
        self.record.write_bytes(b"Existing migration record\n")
        before = self.snapshot(self.record)
        self.write_mapping([self.entry(source)])
        self.apply(success=False)
        self.assertEqual(self.snapshot(self.record), before)
        self.assertFalse(self.root.exists())

    def test_apply_requires_new_record(self):
        source = self.write_source()
        self.write_mapping([self.entry(source)])
        self.assertIn("--record", self.cli("--apply", success=False).stderr)
        self.assertFalse(self.root.exists())

    def test_rerunning_completed_mapping_refuses_changed_destination(self):
        source = self.write_source()
        self.write_mapping([self.entry(source)])
        self.apply()
        destination = self.root / "notes.md"
        destination.write_bytes(b"Operator edited this after import.\n")
        before = {path: self.snapshot(path) for path in (source, destination, self.record)}
        retry_record = self.temporary / "retry.json"
        self.apply(success=False, record=retry_record)
        for path, original in before.items():
            self.assertEqual(self.snapshot(path), original)
        self.assertFalse(retry_record.exists())

    def test_existing_and_planned_skill_packages_reject_aios_timestamps(self):
        skill = self.write_source("example/SKILL.md", b"# Example\n")
        resource = self.write_source("example/reference.md")
        source = self.write_source()
        self.require_birthtime(source)
        cases = [
            [self.entry(resource, type="doc")],
            [self.entry(source, "example/reference.md", type="doc"),
             self.entry(skill, "example/SKILL.md")],
        ]
        for entries in cases:
            with self.subTest(entries=entries):
                self.write_mapping(entries)
                self.assertIn("skill", self.apply(success=False).stderr.lower())
                self.assertFalse(self.root.exists())
                self.assertFalse(self.record.exists())

    def test_symbolic_links_and_git_metadata_paths_write_nothing(self):
        source = self.write_source()
        linked_source = self.temporary / "linked-source"
        linked_source.symlink_to(self.source, target_is_directory=True)
        linked_destination = self.temporary / "linked-destination"
        linked_destination.symlink_to(self.source, target_is_directory=True)
        cases = [
            dict(source=str(linked_source / source.name), destination=str(self.root / "notes.md")),
            dict(source=str(source), destination=str(linked_destination / "new.md")),
            self.entry(source, ".git/config"),
        ]
        before = self.snapshot(source)
        for entry in cases:
            with self.subTest(entry=entry):
                self.write_mapping([entry])
                self.apply(success=False)
                self.assertFalse(self.root.exists())
                self.assertFalse((self.source / "new.md").exists())
                self.assertFalse(self.record.exists())
                self.assertEqual(self.snapshot(source), before)

    def test_malformed_frontmatter_stops_before_writing(self):
        for data in [b"---\ntitle: Open block\n", b"---\ntitle: One\ntitle: Two\n---\n"]:
            with self.subTest(data=data):
                source = self.write_source(data=data)
                self.require_birthtime(source)
                before = self.snapshot(source)
                self.write_mapping([self.entry(source, type="doc")])
                self.apply(success=False)
                self.assertEqual(self.snapshot(source), before)
                self.assertFalse(self.root.exists())
                self.assertFalse(self.record.exists())

    def test_missing_creation_time_does_not_fall_back_to_ctime(self):
        source = self.write_source()
        before = self.snapshot(source)
        original_stat = Path.stat
        info = original_stat(source)
        without_birth = SimpleNamespace(
            st_mode=info.st_mode, st_mtime=info.st_mtime, st_mtime_ns=info.st_mtime_ns,
            st_atime_ns=info.st_atime_ns, st_ctime=info.st_ctime,
        )
        spec = importlib.util.spec_from_file_location("migration_under_test", SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        def filesystem_stat(path, *args, **kwargs):
            return without_birth if path == source else original_stat(path, *args, **kwargs)

        with patch.object(Path, "stat", autospec=True, side_effect=filesystem_stat):
            with self.assertRaisesRegex(ValueError, "Creation time unavailable"):
                module.prepare({"files": [self.entry(source, type="doc")]}, ZoneInfo("UTC"))
        self.assertEqual(self.snapshot(source), before)
        self.assertFalse(self.root.exists())

    def test_imported_timestamps_survive_fixer_and_later_hook_updates_only_updated(self):
        source = self.write_source()
        self.require_birthtime(source)
        self.write_mapping([self.entry(source, type="doc")])
        self.apply()
        destination = self.root / "notes.md"
        before, fields = self.snapshot(destination), self.fields(destination)
        settings = self.root / ".aiOS" / "config.yaml"
        settings.parent.mkdir()
        settings.write_text("checks:\n  frontmatter:\n    zone: UTC\n")
        fixer = subprocess.run(
            [sys.executable, "-c", "import json,sys; sys.path.insert(0,sys.argv[1]); "
             "import hooks; config,checks=hooks.load(sys.argv[2]); problems=[]; "
             "fixed=hooks.run_fixers([sys.argv[3]],{'frontmatter':checks['frontmatter']},sys.argv[2],problems); "
             "print(json.dumps({'fixed':fixed,'problems':problems}))",
             str(PLUGIN / "hooks"), str(self.root), str(destination)],
            cwd=self.temporary, env=self.env, text=True, capture_output=True, timeout=30,
        )
        self.assertEqual(fixer.returncode, 0, fixer.stdout + fixer.stderr)
        self.assertEqual(json.loads(fixer.stdout), {"fixed": [], "problems": []})
        self.assertEqual(self.snapshot(destination), before)
        payload = json.dumps({"session_id": "migration-test", "cwd": str(self.root)})
        for event in ("start", "stop"):
            if event == "stop":
                time.sleep(0.02)
                destination.write_bytes(destination.read_bytes() + b"\nA later normal edit.\n")
            result = subprocess.run(
                [sys.executable, str(PLUGIN / "hooks" / "hooks.py"), event],
                input=payload, cwd=self.root, env=self.env, text=True,
                capture_output=True, timeout=30,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(result.stdout.strip(), "")
        after = self.fields(destination)
        self.assertEqual(after["created"], fields["created"])
        self.assertEqual(after["migrated"], fields["migrated"])
        self.assertNotEqual(after["updated"], fields["updated"])
        self.assertTrue(destination.read_bytes().endswith(b"\nA later normal edit.\n"))
        event = json.loads((self.root / ".aiOS/logs/hook-events.jsonl").read_text().splitlines()[-1])
        self.assertEqual(event["decision"], "allow")
        self.assertEqual(event["problems"], [])
        self.assertEqual(event["fixed"], [{"check": "frontmatter", "path": "notes.md"}])


if __name__ == "__main__":
    unittest.main()
