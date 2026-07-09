"""Backfill Thai translations for EN-only SET disclosure headlines.

The normal path should prefer SET's own TH twin row. This script only covers
legacy EN rows whose id stem has no Thai counterpart.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from typing import Any

import duckdb

from store import DB_PATH, conn

DEFAULT_LIMIT = 400
BATCH_SIZE = 20
MINIMAX_MODEL = os.environ.get("MINIMAX_MODEL", "MiniMax-M3")
MINIMAX_BASE_URL = os.environ.get("MINIMAX_BASE_URL", "https://api.minimax.io/anthropic")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODELS = ["openai/gpt-oss-120b", "llama-3.3-70b-versatile"]

SYSTEM_PROMPT = """You translate Stock Exchange of Thailand disclosure headlines from English to Thai for professional financial surveillance.

Translate naturally into concise Thai. Preserve tickers, company names, form codes, dates, percentages, security names, and standard market acronyms where appropriate. Do not add commentary or facts not present in the headline.

Return only a JSON object whose keys are the input ids and whose values are the Thai translations."""


class MiniMaxProvider:
    name = "minimax"

    def __init__(self) -> None:
        from anthropic import Anthropic

        self.model = MINIMAX_MODEL
        self.model_tag = f"minimax/{self.model}"
        self.client = Anthropic(
            api_key=os.environ["MINIMAX_API_KEY"],
            base_url=MINIMAX_BASE_URL,
        )

    def translate_text(self, rows: list[dict[str, str]]) -> str:
        msg = self.client.messages.create(
            model=self.model,
            max_tokens=2500,
            temperature=0.1,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": _user_prompt(rows)}],
        )
        return _anthropic_text(msg)


class GroqProvider:
    name = "groq"

    def __init__(self) -> None:
        env_model = os.environ.get("GROQ_MODEL")
        self.models = [env_model] if env_model else GROQ_MODELS
        self.model_tag = f"groq/{self.models[0]}"

    def translate_text(self, rows: list[dict[str, str]]) -> str:
        last_err: Exception | None = None
        for model in self.models:
            body = json.dumps({
                "model": model,
                "temperature": 0.1,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": _user_prompt(rows)},
                ],
            }, ensure_ascii=False).encode("utf-8")
            req = urllib.request.Request(GROQ_URL, data=body, headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {os.environ['GROQ_API_KEY']}",
                "User-Agent": "is1-surveillance/1.0",
            })
            try:
                with urllib.request.urlopen(req, timeout=60) as r:
                    payload = json.load(r)
                self.model_tag = f"groq/{model}"
                return payload["choices"][0]["message"]["content"]
            except urllib.error.HTTPError as exc:
                detail = exc.read().decode("utf-8", "ignore")[:400]
                last_err = RuntimeError(f"groq HTTP {exc.code} [{model}]: {detail}")
                if exc.code == 429:
                    continue
                raise last_err from exc
            except Exception as exc:
                last_err = exc
        raise RuntimeError(f"groq translation exhausted all models: {last_err}")


def _chunks(values: list[dict[str, str]], size: int = BATCH_SIZE):
    for i in range(0, len(values), size):
        yield values[i:i + size]


def _anthropic_text(msg: Any) -> str:
    parts: list[str] = []
    for block in msg.content:
        if getattr(block, "type", None) == "text":
            parts.append(getattr(block, "text", ""))
    text = "\n".join(parts).strip()
    if not text:
        raise RuntimeError(f"empty MiniMax response: {msg.content!r}")
    return text


def _user_prompt(rows: list[dict[str, str]]) -> str:
    payload = [{"id": row["id"], "headline": row["headline"]} for row in rows]
    return (
        "Translate this JSON array of SET disclosure headlines to Thai.\n"
        "Return a JSON object only, in this exact shape: {\"NEWS_ID\": \"Thai translation\"}.\n"
        f"Input:\n{json.dumps(payload, ensure_ascii=False)}"
    )


def _json_text(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].strip().startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines).strip()
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end < start:
        raise ValueError(f"no JSON object in response: {text[:200]}")
    return text[start:end + 1]


def _parse_translations(text: str, expected_ids: list[str]) -> dict[str, str]:
    data = json.loads(_json_text(text))
    if isinstance(data, dict) and isinstance(data.get("translations"), dict):
        data = data["translations"]
    if not isinstance(data, dict):
        raise ValueError("translation response is not a JSON object")

    expected = set(expected_ids)
    actual = {str(k) for k in data.keys()}
    unknown = actual - expected
    if unknown:
        raise ValueError(f"response included unknown id(s): {sorted(unknown)[:5]}")

    out: dict[str, str] = {}
    for news_id in expected_ids:
        value = data.get(news_id)
        if isinstance(value, str) and value.strip():
            out[news_id] = value.strip()
    if not out:
        raise ValueError("response contained no usable translations")
    return out


def _translate_batch(provider: Any, rows: list[dict[str, str]]) -> tuple[dict[str, str], str]:
    expected_ids = [row["id"] for row in rows]
    last_parse_err: Exception | None = None
    for _attempt in range(2):
        text = provider.translate_text(rows)
        try:
            return _parse_translations(text, expected_ids), provider.model_tag
        except Exception as exc:
            last_parse_err = exc
    raise RuntimeError(f"could not parse translation JSON after retry: {last_parse_err}")


def _table_exists(c, table: str) -> bool:
    return table in {str(row[0]) for row in c.execute("SHOW TABLES").fetchall()}


def _fetch_targets_from_connection(c, limit: int, has_translations: bool) -> list[dict[str, str]]:
    join_sql = "LEFT JOIN title_translations tt ON tt.news_id = en.id" if has_translations else ""
    translated_filter = "AND tt.news_id IS NULL" if has_translations else ""
    sql = f"""
    WITH stems AS (
        SELECT
            id,
            substring(id, 1, length(id) - 2) AS stem,
            lang,
            datetime_iso,
            headline
        FROM news_items
    )
    SELECT
        en.id,
        en.datetime_iso,
        en.headline
    FROM stems en
    {join_sql}
    WHERE en.lang = 'en'
      {translated_filter}
      AND coalesce(en.headline, '') <> ''
      AND NOT EXISTS (
          SELECT 1 FROM stems th
          WHERE th.stem = en.stem AND th.lang = 'th'
      )
    ORDER BY en.datetime_iso DESC
    LIMIT ?
    """
    return [
        {"id": str(news_id), "datetime_iso": str(datetime_iso), "headline": str(headline)}
        for news_id, datetime_iso, headline in c.execute(sql, [int(limit)]).fetchall()
    ]


def _fetch_targets(limit: int) -> list[dict[str, str]]:
    with conn() as c:
        return _fetch_targets_from_connection(c, limit, has_translations=True)


def _fetch_targets_read_only(limit: int) -> list[dict[str, str]]:
    if not DB_PATH.exists():
        return []
    c = duckdb.connect(str(DB_PATH), read_only=True)
    try:
        return _fetch_targets_from_connection(
            c,
            limit,
            has_translations=_table_exists(c, "title_translations"),
        )
    finally:
        c.close()


def _write_translations(translations: dict[str, str], model_tag: str) -> None:
    if not translations:
        return
    with conn() as c:
        c.executemany(
            """
            INSERT OR REPLACE INTO title_translations (news_id, title_th, model)
            VALUES (?, ?, ?)
            """,
            [(news_id, title_th, model_tag) for news_id, title_th in translations.items()],
        )


def _initial_provider() -> Any | None:
    if os.environ.get("MINIMAX_API_KEY"):
        return MiniMaxProvider()
    if os.environ.get("GROQ_API_KEY"):
        return GroqProvider()
    return None


def _fallback_provider(current: Any) -> Any | None:
    if current.name == "minimax" and os.environ.get("GROQ_API_KEY"):
        return GroqProvider()
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT,
                        help=f"Maximum EN-only headlines to translate, default {DEFAULT_LIMIT}")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print rows that would be translated, without API calls or writes")
    args = parser.parse_args()

    if not args.dry_run and not os.environ.get("MINIMAX_API_KEY") and not os.environ.get("GROQ_API_KEY"):
        print("No MINIMAX_API_KEY or GROQ_API_KEY set; skipping Thai title translation.")
        return 0

    if args.dry_run:
        rows = _fetch_targets_read_only(max(1, args.limit))
        if not rows:
            print("No EN-only headlines need Thai translation.")
            return 0
        print(f"Would translate {len(rows)} EN-only headline(s):")
        for row in rows:
            print(f"  {row['datetime_iso']} {row['id']} {row['headline']}")
        return 0

    rows = _fetch_targets(max(1, args.limit))
    if not rows:
        print("No EN-only headlines need Thai translation.")
        return 0

    provider = _initial_provider()

    translated = 0
    skipped = 0
    used_models: list[str] = []

    for batch in _chunks(rows):
        try:
            translations, model_tag = _translate_batch(provider, batch)
        except Exception as exc:
            fallback = _fallback_provider(provider)
            if fallback is None:
                print(f"Skipping batch after {provider.name} failure: {exc}", file=sys.stderr)
                skipped += len(batch)
                continue
            print(f"{provider.name} failed; falling back to {fallback.name}: {exc}", file=sys.stderr)
            provider = fallback
            try:
                translations, model_tag = _translate_batch(provider, batch)
            except Exception as fallback_exc:
                print(f"Skipping batch after {provider.name} failure: {fallback_exc}", file=sys.stderr)
                skipped += len(batch)
                continue

        _write_translations(translations, model_tag)
        translated += len(translations)
        skipped += len(batch) - len(translations)
        if model_tag not in used_models:
            used_models.append(model_tag)

    provider_used = ", ".join(used_models) if used_models else provider.model_tag
    print(f"Thai title translation complete: translated={translated}, skipped={skipped}, provider={provider_used}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
