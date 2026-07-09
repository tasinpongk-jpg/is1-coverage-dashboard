"""Thai-language enrichment helpers for Disclosure Pulse payloads."""

from __future__ import annotations

import sys
from typing import Any


def _chunks(values: list[str], size: int = 500):
    for i in range(0, len(values), size):
        yield values[i:i + size]


def _query_in(con, base_sql: str, values: list[str]) -> list[tuple]:
    rows: list[tuple] = []
    for chunk in _chunks(values):
        if not chunk:
            continue
        placeholders = ",".join("?" for _ in chunk)
        rows.extend(con.execute(f"{base_sql} ({placeholders})", chunk).fetchall())
    return rows


def _log_enrichment_error(stage: str, exc: Exception) -> None:
    print(
        f"[disclosure-pulse] Thai enrichment {stage} failed: "
        f"{type(exc).__name__}: {exc}",
        file=sys.stderr,
        flush=True,
    )


def _item_id(item: dict[str, Any]) -> str:
    return str(item.get("_id") or "").strip()


def _unique_ids(items: list[dict[str, Any]]) -> list[str]:
    return list(dict.fromkeys(news_id for news_id in (_item_id(item) for item in items) if news_id))


def _enrich_thai(con, items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Add Thai twin titles, Thai summaries, and translation fallbacks.

    Works on the normalized Disclosure Pulse item shape, so it is independent
    of whether the rows came from SURVEILLANCE_SQL or the proxy fallback SELECT.
    """
    if not items:
        return items

    try:
        twin_by_en: dict[str, str] = {}
        for item in items:
            news_id = _item_id(item)
            if len(news_id) >= 9 and news_id.endswith("00"):
                twin_by_en[news_id] = f"{news_id[:-2]}01"

        if twin_by_en:
            twin_rows = _query_in(
                con,
                "SELECT id, headline, url FROM news_items WHERE lang = 'th' AND id IN",
                list(dict.fromkeys(twin_by_en.values())),
            )
            th_by_id = {
                str(news_id): {"title": headline, "url": url}
                for news_id, headline, url in twin_rows
            }
            for item in items:
                twin = twin_by_en.get(_item_id(item))
                if not twin:
                    continue
                th = th_by_id.get(twin)
                if not th:
                    continue
                if th.get("title"):
                    item["title_th"] = th["title"]
                if th.get("url"):
                    item["url_th"] = th["url"]
    except Exception as exc:
        _log_enrichment_error("twin lookup", exc)

    ids = _unique_ids(items)
    if not ids:
        return items

    try:
        summary_rows = _query_in(
            con,
            "SELECT news_id, summary_th FROM classifications WHERE news_id IN",
            ids,
        )
        summary_by_id = {
            str(news_id): summary_th
            for news_id, summary_th in summary_rows
            if summary_th
        }
        for item in items:
            summary_th = summary_by_id.get(_item_id(item))
            if summary_th:
                item["_summary_th"] = summary_th
    except Exception as exc:
        _log_enrichment_error("summary lookup", exc)

    try:
        translation_rows = _query_in(
            con,
            "SELECT news_id, title_th FROM title_translations WHERE news_id IN",
            ids,
        )
        translation_by_id = {
            str(news_id): title_th
            for news_id, title_th in translation_rows
            if title_th
        }
        for item in items:
            if item.get("title_th"):
                continue
            title_th = translation_by_id.get(_item_id(item))
            if title_th:
                item["title_th"] = title_th
    except Exception as exc:
        _log_enrichment_error("translation lookup", exc)

    return items
