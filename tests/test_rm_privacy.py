"""Tests for scripts/rm_privacy.py and the snapshots that must obey it.

The rule: no published surface carries an RM nickname, only the initial.
The second test class guards data/ directly, so a future rebuild that
forgets the helper fails here rather than on the dashboard.
"""
import json
import os
import sys
import unittest

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from rm_privacy import anonymise_rm, anonymise_rm_map, RM_CODES  # noqa: E402

NICKNAMES = ("Champ", "Orn", "Pim", "Gift", "Tony", "Kae")


class TestAnonymiseRm(unittest.TestCase):
    def test_nickname_to_initial(self):
        self.assertEqual(anonymise_rm("Champ"), "C")
        self.assertEqual(anonymise_rm("Orn"), "O")
        self.assertEqual(anonymise_rm("Kae"), "K")

    def test_idempotent(self):
        # A builder may read a snapshot another builder already anonymised.
        for n in NICKNAMES:
            once = anonymise_rm(n)
            self.assertEqual(anonymise_rm(once), once)

    def test_whitespace_and_case(self):
        self.assertEqual(anonymise_rm("  orn "), "O")
        self.assertEqual(anonymise_rm("tony"), "T")

    def test_none_and_blank_pass_through(self):
        # An unassigned RM stays unassigned — it must not become a "" bucket.
        self.assertIsNone(anonymise_rm(None))
        self.assertEqual(anonymise_rm(""), "")
        self.assertEqual(anonymise_rm("   "), "   ")

    def test_every_current_nickname_maps_into_the_known_codes(self):
        for n in NICKNAMES:
            self.assertIn(anonymise_rm(n), RM_CODES)

    def test_no_collisions_among_current_rms(self):
        codes = [anonymise_rm(n) for n in NICKNAMES]
        self.assertEqual(len(set(codes)), len(NICKNAMES))


class TestAnonymiseRmMap(unittest.TestCase):
    def test_rekeys_and_preserves_totals(self):
        src = {"Champ": {"issuers": 6, "thbBn": 97.41},
               "Orn": {"issuers": 4, "thbBn": 45.89}}
        out = anonymise_rm_map(src)
        self.assertEqual(sorted(out), ["C", "O"])
        self.assertEqual(out["C"]["thbBn"], 97.41)
        self.assertEqual(round(sum(v["thbBn"] for v in out.values()), 2), 143.30)

    def test_collision_merges_rather_than_overwrites(self):
        # Two RMs sharing an initial must not silently drop a bucket.
        src = {"Champ": {"issuers": 2, "thbBn": 10.0},
               "Cat":   {"issuers": 3, "thbBn": 5.5}}
        out = anonymise_rm_map(src)
        self.assertEqual(list(out), ["C"])
        self.assertEqual(out["C"]["issuers"], 5)
        self.assertEqual(out["C"]["thbBn"], 15.5)

    def test_empty_input(self):
        self.assertEqual(anonymise_rm_map({}), {})
        self.assertEqual(anonymise_rm_map(None), {})


class TestSnapshotsCarryNoNicknames(unittest.TestCase):
    """Guards the published data/ snapshots, not just the helper."""

    def _rm_values(self, obj, found):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k == "rm" and isinstance(v, str):
                    found.add(v)
                self._rm_values(v, found)
        elif isinstance(obj, list):
            for v in obj:
                self._rm_values(v, found)
        return found

    def test_sec_bonds_rm_values_are_codes(self):
        path = os.path.join(ROOT, "data", "sec-bonds.json")
        with open(path, encoding="utf-8") as fh:
            d = json.load(fh)
        vals = self._rm_values(d, set())
        self.assertTrue(vals, "no rm values found — test is not exercising anything")
        for v in vals:
            self.assertEqual(len(v), 1, f"sec-bonds.json carries a full RM name: {v!r}")

    def test_sec_bonds_byrm_keys_are_codes(self):
        path = os.path.join(ROOT, "data", "sec-bonds.json")
        with open(path, encoding="utf-8") as fh:
            d = json.load(fh)
        for k in d.get("byRM", {}):
            self.assertLessEqual(len(k), 1,
                                 f"byRM is keyed on a full RM name: {k!r}")

    def test_tickers_rm_values_are_codes(self):
        path = os.path.join(ROOT, "data", "tickers.json")
        with open(path, encoding="utf-8") as fh:
            d = json.load(fh)
        for t in d["tickers"]:
            self.assertEqual(len(t["rm"]), 1, f"{t['tk']} carries {t['rm']!r}")


if __name__ == "__main__":
    unittest.main()
