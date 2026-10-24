#!/usr/bin/env python3
"""The RM anonymisation rule, in one place.

Published surfaces identify each RM by a single-letter code (RM_CODES).
Nicknames are not stored in this repo. A nickname-to-code map is read from
private config, in this order:

  1. RM_NAME_MAP — a JSON object, for example {"RM_ONE": "C", "RM_TWO": "O"}
  2. RM_NAME_MAP_FILE — path to a JSON object of the same shape
  3. config/rm-names.local.json — gitignored. Copy config/rm-names.example.json
     and replace the placeholder keys locally. Do not commit that file.

Without that config, a value that is already a code passes through. That is
the shape of data/tickers.json in CI. Builders that still receive a nickname
and have no config reduce it to its first letter so a full name is never
written into a snapshot. Choosing whose book a brief or digest covers does
not use that guess: known_rm_code() accepts a code, or a nickname present in
the private map, and nothing else.

    from rm_privacy import anonymise_rm
    rec["rm"] = anonymise_rm(frontmatter.get("rm"))
"""

from __future__ import annotations

import json
import os
from pathlib import Path

__all__ = [
    "anonymise_rm",
    "anonymise_rm_map",
    "coverage_rm_map",
    "digest_label",
    "group_by_rm",
    "known_rm_code",
    "load_rm_name_map",
    "RM_CODES",
    "UNASSIGNED",
]

# Codes currently in data/tickers.json. The chat dock validates the same set.
RM_CODES = ("C", "O", "K", "T", "P", "G")
UNASSIGNED = "Unassigned"

_ENV_MAP = "RM_NAME_MAP"
_ENV_MAP_FILE = "RM_NAME_MAP_FILE"
_DEFAULT_MAP = Path(__file__).resolve().parent.parent / "config" / "rm-names.local.json"
_DEFAULT_TICKERS = Path(__file__).resolve().parent.parent / "data" / "tickers.json"


def load_rm_name_map(path=None):
    """Return the private nickname-to-code object, or {} when it is absent.

    An explicit path wins. Otherwise RM_NAME_MAP, then RM_NAME_MAP_FILE, then
    config/rm-names.local.json. A missing file is not an error: CI has no
    private config and reads codes from data/tickers.json.
    """
    if path is not None:
        return _read_map_file(Path(path))
    raw = os.environ.get(_ENV_MAP, "").strip()
    if raw:
        data = json.loads(raw)
        if not isinstance(data, dict):
            raise ValueError("RM_NAME_MAP must be a JSON object of name to code")
        return data
    file_env = os.environ.get(_ENV_MAP_FILE, "").strip()
    file = Path(file_env) if file_env else _DEFAULT_MAP
    if not file.is_file():
        return {}
    return _read_map_file(file)


def _read_map_file(path: Path):
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must be a JSON object of name to code")
    return data


def _folded_map(mapping):
    table = load_rm_name_map() if mapping is None else mapping
    out = {}
    for key, val in (table or {}).items():
        name = str(key).strip()
        code = str(val).strip()[:1].upper()
        if name and code in RM_CODES:
            out[name.casefold()] = code
    return out


def known_rm_code(value, mapping=None):
    """Return a code in RM_CODES, or None.

    A single letter that is already a code passes through with no private
    config. A longer name resolves only when the private map lists it.
    None and blank stay unresolved so an unassigned RM does not become a
    bucket of its own.
    """
    if value is None:
        return None
    if isinstance(value, (list, tuple)):
        # A frontmatter parser that reads a bracketed rm value hands us a
        # one-element list. Fold it before the code check.
        value = value[0] if value else None
        if value is None:
            return None
    text = str(value).strip()
    if not text:
        return None
    hit = _folded_map(mapping).get(text.casefold())
    if hit:
        return hit
    if len(text) == 1 and text.upper() in RM_CODES:
        return text.upper()
    return None


def anonymise_rm(value, mapping=None):
    """Return a single-letter RM code for a published snapshot.

    Already-anonymised input passes through unchanged, so this is safe to
    apply twice. None and blank pass through untouched rather than becoming
    an empty string.

    >>> anonymise_rm("C")
    'C'
    >>> anonymise_rm("  o ")
    'O'
    >>> anonymise_rm(None) is None
    True
    >>> anonymise_rm(["K"])
    'K'
    """
    if value is None:
        return None
    if isinstance(value, (list, tuple)):
        value = value[0] if value else None
        if value is None:
            return None
    text = str(value).strip()
    if not text:
        return value
    code = known_rm_code(text, mapping)
    if code:
        return code
    # Last resort for a published field: never write the rest of the name.
    return text[:1].upper()


def anonymise_rm_map(mapping):
    """Re-key a {rm: ...} aggregate onto codes, merging any collisions.

    Values are merged rather than overwritten so a rebuild cannot silently
    drop a bucket. Numeric fields are summed; anything else takes the first
    value seen and is left alone.
    """
    out = {}
    for name, val in (mapping or {}).items():
        code = anonymise_rm(name)
        if code not in out:
            out[code] = dict(val) if isinstance(val, dict) else val
            continue
        prev = out[code]
        if isinstance(prev, dict) and isinstance(val, dict):
            for k, v in val.items():
                if isinstance(v, (int, float)) and isinstance(prev.get(k), (int, float)):
                    prev[k] = round(prev[k] + v, 10)
                elif k not in prev:
                    prev[k] = v
        elif isinstance(prev, (int, float)) and isinstance(val, (int, float)):
            out[code] = prev + val
    return out


def coverage_rm_map(path=None, mapping=None):
    """ticker -> RM code from tickers.json. Symbols with no known code are omitted.

    This is the map CI can build. It does not read rm.duckdb.
    """
    src = Path(path) if path is not None else _DEFAULT_TICKERS
    if not src.is_file():
        return {}
    data = json.loads(src.read_text(encoding="utf-8"))
    out = {}
    for row in data.get("tickers") or []:
        tk = row.get("tk")
        code = known_rm_code(row.get("rm"), mapping)
        if tk and code:
            out[tk] = code
    return out


def digest_label(symbol, rm_map, mapping=None):
    """RM label a digest would print for one symbol.

    Missing symbols, and values that are not a known code, are Unassigned.
    """
    raw = (rm_map or {}).get(symbol)
    code = known_rm_code(raw, mapping) if raw is not None else None
    return code or UNASSIGNED


def group_by_rm(rows, rm_map, mapping=None):
    """Group digest rows the way the email subjects are labelled."""
    from collections import defaultdict

    by_rm = defaultdict(list)
    for row in rows or []:
        by_rm[digest_label(row.get("symbol"), rm_map, mapping)].append(row)
    return dict(by_rm)


if __name__ == "__main__":
    import doctest
    fails, _ = doctest.testmod()
    raise SystemExit(1 if fails else 0)
