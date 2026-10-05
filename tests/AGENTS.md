---
type: AGENTS.md
created: 2026-10-04T14:18-07:00
updated: 2026-10-04T18:50-07:00
---

# aiOS automated tests

Automated tests that run setup and the hooks the way an agent harness does. Each test works in a temporary aiOS root, copied from the sample or built by setup.

## Instructions

### Test the agent harness interface

Send hook JSON through stdin to `hooks.py start` and `hooks.py stop`.
Assert replies, log entries, and file changes. Keep one behavior per test.
Use only the Python 3.9 standard library and the interpreter running unittest.
Keep temporary folders inside the product repo and remove them after each test.

### Run the tests

From the product repo, run `python3 -m unittest discover -s tests -v`.
Also run `/usr/bin/python3 -m unittest discover -s tests -v` to verify Python 3.9 compatibility.
Tests restore generated docs themselves, so a fresh checkout needs no setup first.

## Contents

| Path | What it holds | Read when |
|---|---|---|
| [test_hooks.py](test_hooks.py) | Setup, default checks, custom settings, timestamps, and docs sync tests | Changing core plugin behavior |
