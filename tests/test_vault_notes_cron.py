"""vault_notes_cron: rebuild, push only from main, fail loudly without the vault."""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

import vault_notes_cron as cron  # noqa: E402

BUILDER = '''import sys, pathlib
p = pathlib.Path("data/vault-ticker-notes.json")
if "{mode}" == "missing":
    print("[build_vault_ticker_notes] vault not found; keeping existing JSON: X"); sys.exit(0)
p.write_text('{{"generated": "new"}}\\n', encoding="utf-8")
print("Wrote vault-ticker-notes.json")
'''


def git(cwd, *args):
    return subprocess.run(["git", "-C", str(cwd), *args], check=True, capture_output=True, text=True).stdout


class TestVaultNotesCron(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.remote = self.tmp / "remote.git"
        git(self.tmp, "init", "-q", "--bare", "-b", "main", str(self.remote))
        self.repo = self.tmp / "repo"
        git(self.tmp, "clone", "-q", str(self.remote), str(self.repo))
        git(self.repo, "config", "user.email", "t@example.invalid")
        git(self.repo, "config", "user.name", "t")
        git(self.repo, "checkout", "-q", "-b", "main")
        (self.repo / "data").mkdir()
        (self.repo / "scripts").mkdir()
        (self.repo / cron.TARGET).write_text('{"generated": "old"}\n', encoding="utf-8")
        (self.repo / cron.OPPDAY).write_text('{"generated": "old"}\n', encoding="utf-8")
        self._builder("ok")
        self._oppday("ok")
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-q", "-m", "init")
        git(self.repo, "push", "-q", "origin", "main")
        self.env = mock.patch.dict(os.environ, {"IS1_REPO": str(self.repo)})
        self.env.start()

    def tearDown(self):
        self.env.stop()

    def _oppday(self, mode):
        body = ('import sys; sys.exit("ERROR: reports folder not found: X")' if mode == "fail" else
                'import pathlib; pathlib.Path("data/oppday-minutes.json").write_text(\'{"generated": "new"}\\n\')')
        (self.repo / "scripts" / "build_oppday_minutes.py").write_text(body + "\n", encoding="utf-8")

    def _builder(self, mode):
        (self.repo / "scripts" / "build_vault_ticker_notes.py").write_text(BUILDER.format(mode=mode), encoding="utf-8")

    def test_rebuild_is_pushed_to_main(self):
        self.assertEqual(cron.main([]), 0)
        self.assertEqual(git(self.remote, "log", "-1", "--format=%s", "main").strip(),
                         "chore(data): rebuild vault-ticker-notes + oppday-minutes")

    def test_oppday_failure_still_pushes_vault_notes(self):
        self._oppday("fail")
        git(self.repo, "commit", "-qam", "oppday breaks")
        git(self.repo, "push", "-q", "origin", "main")
        self.assertEqual(cron.main([]), 1)
        self.assertEqual(git(self.remote, "log", "-1", "--format=%s", "main").strip(),
                         "chore(data): rebuild vault-ticker-notes")
        self.assertEqual(git(self.repo, "status", "--porcelain"), "")

    def test_dry_run_restores_the_file(self):
        self.assertEqual(cron.main(["--dry-run"]), 0)
        self.assertEqual(git(self.repo, "status", "--porcelain"), "")
        self.assertEqual(git(self.remote, "log", "-1", "--format=%s", "main").strip(), "init")

    def test_missing_vault_exits_2_without_commit(self):
        self._builder("missing")
        git(self.repo, "commit", "-qam", "builder")
        self.assertEqual(cron.main([]), 2)
        self.assertEqual(git(self.repo, "log", "-1", "--format=%s").strip(), "builder")

    def test_never_pushes_from_another_branch(self):
        git(self.repo, "checkout", "-q", "-b", "wip")
        self.assertEqual(cron.main([]), 1)
        self.assertEqual(git(self.remote, "log", "-1", "--format=%s", "main").strip(), "init")


if __name__ == "__main__":
    unittest.main()
