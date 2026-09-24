#!/usr/bin/env python3
"""The RM anonymisation rule, in one place.

RMs are identified on every published surface by the initial of their
nickname, never the nickname itself: Champ -> C, Orn -> O, Kae -> K.
data/tickers.json has always done this; the rule lived inline in
build_tickers.py, so any other builder that read an `rm` field straight from
a vault note or a spreadsheet published the full nickname instead. That is
how data/sec-bonds.json ended up rendering real names on bond-data-sec.html.

Two things depend on the codes, not just privacy:

  - the cross-page RM context (`localStorage.is1_rm`) validates against
    /^[CKOGPT]$/, so a snapshot carrying nicknames silently breaks the RM
    filter on that page — it compares "C" against "Champ" and matches nothing;
  - data/tickers.json keys the whole universe on the code, so anything
    joining to it on `rm` needs the same shape.

Import this rather than re-implementing the slice.

    from rm_privacy import anonymise_rm
    rec["rm"] = anonymise_rm(frontmatter.get("rm"))
"""

__all__ = ["anonymise_rm", "anonymise_rm_map", "RM_CODES"]

# The codes currently in data/tickers.json. Used only to sanity-check a
# rebuild — anonymise_rm itself takes any name and never validates against
# this, so a new RM joining the desk does not need a code change here.
RM_CODES = ("C", "O", "K", "T", "P", "G")


def anonymise_rm(value):
    """Return the RM's single-letter code.

    Already-anonymised input passes through unchanged, so this is safe to
    apply twice (a builder may read a snapshot another builder wrote).
    None and blank pass through untouched rather than becoming an empty
    string — an unassigned RM stays unassigned, it does not become a new
    bucket keyed on "".

    >>> anonymise_rm("Champ")
    'C'
    >>> anonymise_rm("C")
    'C'
    >>> anonymise_rm("  orn ")
    'O'
    >>> anonymise_rm(None) is None
    True
    """
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return value
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


if __name__ == "__main__":
    import doctest
    fails, _ = doctest.testmod()
    raise SystemExit(1 if fails else 0)
