"""RM slices, digest labels, and the empty-brief check.

Run from the repo root:
    python -m pytest tests/test_rm_brief.py -q

No email is sent. The private nickname map is not required: fixtures and
data/tickers.json use single-letter codes.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "surveillance"))

import build_morning_push as brief  # noqa: E402
import check_rm_assignment as check  # noqa: E402
from rm_privacy import (  # noqa: E402
    RM_CODES,
    UNASSIGNED,
    coverage_rm_map,
    digest_label,
    group_by_rm,
    known_rm_code,
)


def _write(directory: Path, name: str, payload: dict) -> None:
    (directory / f"{name}.json").write_text(
        json.dumps(payload), encoding="utf-8"
    )


def _fixture(tmp_path: Path, monkeypatch, tickers, rows=None, alerts=None, filings=None):
    monkeypatch.setattr(brief, "DATA", tmp_path)
    _write(tmp_path, "tickers", {"tickers": tickers})
    _write(tmp_path, "morning-brief", {"asOf": "2026-10-16", "rows": rows or []})
    _write(tmp_path, "unusual-trading", {"alerts": alerts or []})
    _write(tmp_path, "disclosure-pulse", {"filings": filings or [], "status": []})


def test_rm_slices_group_initials(tmp_path, monkeypatch):
    _fixture(
        tmp_path,
        monkeypatch,
        tickers=[{"tk": "AAA", "rm": "C"}, {"tk": "BBB", "rm": "K"}],
        rows=[{"tk": "AAA", "pct1d": 3.0}, {"tk": "BBB", "pct1d": -4.0, "lo52": True}],
    )
    slices, as_of = brief.rm_slices()
    assert as_of == "2026-10-16"
    assert [r["tk"] for r in slices["C"]["movers"]] == ["AAA"]
    assert [r["tk"] for r in slices["K"]["movers"]] == ["BBB"]
    assert slices["K"]["extremes"][0]["tk"] == "BBB"
    assert set(slices) == set(RM_CODES)


def test_rm_slices_ignore_names_when_no_private_map(tmp_path, monkeypatch):
    monkeypatch.delenv("RM_NAME_MAP", raising=False)
    monkeypatch.delenv("RM_NAME_MAP_FILE", raising=False)
    _fixture(
        tmp_path,
        monkeypatch,
        tickers=[{"tk": "AAA", "rm": "C"}, {"tk": "ZZZ", "rm": "Zed"}],
        rows=[{"tk": "AAA", "pct1d": 3.0}, {"tk": "ZZZ", "pct1d": 9.0}],
    )
    slices, _ = brief.rm_slices()
    assert [r["tk"] for r in slices["C"]["movers"]] == ["AAA"]
    assert all(r["tk"] != "ZZZ" for bucket in slices.values() for r in bucket["movers"])
    coverage = brief.rm_coverage()
    assert coverage["C"] == ["AAA"]
    assert all("ZZZ" not in names for names in coverage.values())


def test_private_map_assigns_a_nickname(tmp_path, monkeypatch):
    monkeypatch.setenv("RM_NAME_MAP", json.dumps({"Zed": "K"}))
    _fixture(
        tmp_path,
        monkeypatch,
        tickers=[{"tk": "ZZZ", "rm": "Zed"}],
        rows=[{"tk": "ZZZ", "pct1d": 3.5}],
    )
    assert known_rm_code("Zed") == "K"
    slices, _ = brief.rm_slices()
    assert [r["tk"] for r in slices["K"]["movers"]] == ["ZZZ"]
    assert brief.rm_coverage()["K"] == ["ZZZ"]


def test_local_map_file(tmp_path, monkeypatch):
    path = tmp_path / "rm-names.local.json"
    path.write_text(json.dumps({"Zed": "P"}), encoding="utf-8")
    monkeypatch.delenv("RM_NAME_MAP", raising=False)
    monkeypatch.setenv("RM_NAME_MAP_FILE", str(path))
    assert known_rm_code("zed") == "P"


def test_digest_lookup_uses_initials_and_marks_gaps_unassigned():
    rm_map = {"AAA": "C", "BBB": "G"}
    assert digest_label("AAA", rm_map) == "C"
    assert digest_label("BBB", rm_map) == "G"
    assert digest_label("MISSING", rm_map) == UNASSIGNED
    grouped = group_by_rm(
        [{"symbol": "AAA"}, {"symbol": "MISSING"}, {"symbol": "BBB"}],
        rm_map,
    )
    assert [r["symbol"] for r in grouped["C"]] == ["AAA"]
    assert [r["symbol"] for r in grouped[UNASSIGNED]] == ["MISSING"]
    rendered = f"RM: {digest_label('MISSING', rm_map)}"
    assert rendered == "RM: Unassigned"


def test_digest_lookup_from_tickers_file_without_duckdb(tmp_path):
    path = tmp_path / "tickers.json"
    path.write_text(json.dumps({
        "tickers": [
            {"tk": "AAA", "rm": "C"},
            {"tk": "BBB", "rm": "T"},
            {"tk": "CCC", "rm": "Q"},
        ]
    }), encoding="utf-8")
    rm_map = coverage_rm_map(path)
    assert rm_map == {"AAA": "C", "BBB": "T"}
    assert digest_label("CCC", rm_map) == UNASSIGNED


def test_alerts_rm_lookup_reads_tickers_json():
    duckdb = pytest.importorskip("duckdb")
    assert duckdb is not None
    import alerts

    repo_map = alerts._rm_lookup()
    assert repo_map["AQUA"] == "C"
    assert repo_map
    assert all(code in RM_CODES for code in repo_map.values())
    assert all(len(code) == 1 for code in repo_map.values())
    # The gitignored duckdb is not on this machine. Every coverage symbol
    # still resolves, which is the CI path.
    missing = ROOT / "rm_db" / "rm.duckdb"
    assert not missing.exists()


def test_empty_brief_check_fails_on_zero_tickers(tmp_path, monkeypatch):
    _fixture(tmp_path, monkeypatch, tickers=[])
    problems = check.brief_problems()
    assert "brief has zero tickers" in problems
    assert "brief has zero RM slices" in problems


def test_empty_brief_check_fails_when_no_code_matches(tmp_path, monkeypatch):
    monkeypatch.delenv("RM_NAME_MAP", raising=False)
    _fixture(
        tmp_path,
        monkeypatch,
        tickers=[{"tk": "AAA", "rm": "Zed"}, {"tk": "BBB", "rm": ""}],
        rows=[{"tk": "AAA", "pct1d": 5}],
    )
    problems = check.brief_problems()
    assert "brief has zero tickers" not in problems
    assert "brief has zero RM slices" in problems


def test_check_passes_on_initials_and_does_not_send(tmp_path, monkeypatch):
    _fixture(
        tmp_path,
        monkeypatch,
        tickers=[{"tk": "AAA", "rm": "C"}, {"tk": "BBB", "rm": "O"}],
        rows=[{"tk": "AAA", "pct1d": 2.5}],
    )

    def _explode(*_args, **_kwargs):
        raise AssertionError("email send was called from check mode")

    monkeypatch.setattr(brief, "send", _explode)
    monkeypatch.setattr(brief, "ai_takes", _explode)
    problems = check.brief_problems()
    assert problems == []
    assert check.main(["--brief-only"]) == 0
    assert brief.main(["--check"]) == 0


def test_digest_check_flags_unassigned_symbol(tmp_path, monkeypatch):
    _fixture(
        tmp_path,
        monkeypatch,
        tickers=[{"tk": "AAA", "rm": "C"}, {"tk": "ORPHAN", "rm": "Zed"}],
    )
    monkeypatch.setattr(check, "TICKERS", tmp_path / "tickers.json")
    problems = check.digest_problems()
    assert problems == ["digest would contain RM: Unassigned for ORPHAN"]
    assert check.main(["--digest-only"]) == 1


def test_repo_tickers_pass_the_check():
    # The committed universe is what CI has. This fails if codes and the
    # brief filter drift apart again.
    monkeypatch_data = brief.DATA
    assert monkeypatch_data == ROOT / "data"
    coverage = brief.rm_coverage()
    assert sum(len(v) for v in coverage.values()) > 0
    assert any(coverage.values())
    assert check.brief_problems() == []
    assert check.digest_problems() == []
