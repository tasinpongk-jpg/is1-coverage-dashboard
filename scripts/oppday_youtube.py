"""Opp Day YouTube playlist -> vault transcripts + summaries (laptop tool).

Every quarter SET publishes one YouTube playlist with an Opportunity Day video
per listed company (400+). This tool keeps only IS1 coverage tickers
(data/tickers.json), pulls each video's Thai captions, summarises them with
MiniMax M3 into the same 6-section Thai report the existing Opp Day summaries
use, and writes both into the vault:

  1-Raw/01-Filings/calls/<TK>/<TK>_oppday_<period>_transcript.md   raw source
  3-Outputs/02-Deliverables/Reports/<TK>_oppday_<period>_summary.md  report

build_oppday_minutes.py (run daily by vault_notes_cron.py) picks the reports
up for oppday-minutes.html; nothing here touches data/ or git.

Usage (laptop; needs yt-dlp, MINIMAX_API_KEY and the OneDrive vault):
  python scripts/oppday_youtube.py URL --period q2y2026 --list      # match titles only
  python scripts/oppday_youtube.py URL --period q2y2026 --limit 5   # first 5 new videos
  python scripts/oppday_youtube.py URL --period q2y2026             # all new videos
  options: --only TU,CPN   --force (redo existing)   --dry-run (no writes, no M3)
           --assign VIDEO_ID=KBS,KBSPIF  (joint session or ambiguous title: one report per ticker)
           --pause 20 (seconds between videos)  --cookies-from-browser firefox | --cookies FILE

Rules carried from CLAUDE.md: no number the speaker did not say. After
summarising, every number in the report is checked against the transcript
(same checker as the filing summaries). Untraced numbers are listed at the
end of the report; if more than a quarter of them are untraced the report is
held as <name>.review.md, which the dashboard builder ignores.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

DEFAULT_VAULT = Path.home() / "OneDrive - The Stock Exchange of Thailand" / "Claude-Vault"
LISTED = Path("Work-SET") / "Listed Company"
TRANSCRIPT_DIR = LISTED / "1-Raw" / "01-Filings" / "calls"
REPORTS_DIR = LISTED / "3-Outputs" / "02-Deliverables" / "Reports"

MAX_TRANSCRIPT_CHARS = 100_000   # middle-trimmed beyond this; Q&A sits at the end
HOLD_RATIO = 0.25                 # untraced numbers / all numbers above this -> held
TAG = "[oppday_youtube]"

# Uppercase words that appear in Opp Day titles and are never the ticker.
NOT_TICKERS = {"SET", "MAI", "OPP", "OPPDAY", "DAY", "PCL", "PLC", "Q1", "Q2", "Q3", "Q4",
               "YE", "FY", "THB", "CEO", "CFO", "IR", "LIVE", "PUBLIC", "COMPANY", "LIMITED"}

SYSTEM_PROMPT = """คุณเป็นนักวิเคราะห์ของฝ่ายกำกับบริษัทจดทะเบียน ตลาดหลักทรัพย์แห่งประเทศไทย
เขียนรายงานสรุป Opportunity Day จากคำถอดเสียงที่ให้มาเท่านั้น เป็นภาษาไทย

ใช้โครงสร้างนี้ทุกครั้ง ห้ามเพิ่มหรือตัดหัวข้อ:
# รายงานสรุป Opportunity Day — {TICKER}
**วันที่:** {DATE_LINE}

---

## 1. ภาพรวมธุรกิจ
(ย่อหน้าเดียว 3 ถึง 5 ประโยค)

---

## 2. ผลการดำเนินงาน
(ตารางตัวเลขที่ผู้บริหารพูดถึง พร้อมงวดที่เปรียบเทียบ)

---

## 3. ปัจจัยขับเคลื่อน / ปัจจัยเสี่ยง

---

## 4. แนวโน้มและเป้าหมาย

---

## 5. สรุปคำถาม-ตอบ (Q&A Highlights)

---

## 6. ประเด็นสำคัญสำหรับ RM

กฎ:
- ใช้เฉพาะข้อมูลที่อยู่ในคำถอดเสียง ห้ามเติมตัวเลขหรือข้อเท็จจริงจากความรู้ภายนอก
- ตัวเลขทุกตัวต้องเป็นตัวเลขที่ผู้พูดกล่าวจริง ถ้าไม่ได้ยินชัดให้เขียนว่า ไม่ระบุ
- คำถอดเสียงมาจากคำบรรยายอัตโนมัติ อาจสะกดผิด ให้สรุปตามความหมายที่ชัดเจนเท่านั้น
- ไม่ใช้เครื่องหมายคำพูด ชื่อย่อหลักทรัพย์เป็นภาษาอังกฤษตัวพิมพ์ใหญ่
- งวดรายงานใช้ปี พ.ศ. เช่น Q2/2569
- หัวข้อ 6 เขียนสิ่งที่ RM ควรติดตาม เช่น ความเสี่ยงด้านการเปิดเผยข้อมูล หรือสิ่งที่ผู้บริหารพูดแต่ยังไม่ได้แจ้งตลาดฯ
- ไม่มีข้อความเกริ่นนำหรือสรุปท้ายนอกโครงสร้าง"""


# ---------------------------------------------------------------- matching

def load_coverage() -> set[str]:
    data = json.loads((REPO / "data" / "tickers.json").read_text(encoding="utf-8"))
    return {t["tk"].upper() for t in data["tickers"]}


def match_title(title: str, coverage: set[str]) -> tuple[str | None, str]:
    """Return (ticker, reason). Ticker is None when not ours or ambiguous.

    A title token counts only if it is a coverage ticker. Single-letter tickers
    (M, J) must stand alone in brackets or after a separator, since a bare
    capital letter is too common in titles.
    """
    tokens = re.findall(r"[A-Z0-9][A-Z0-9&.\-]*", title.upper())
    hits: list[str] = []
    for tok in tokens:
        tok = tok.strip(".-")
        if tok in NOT_TICKERS or tok not in coverage:
            continue
        if len(tok) == 1 and not re.search(rf"(^|[\(\[|:\-–]\s*){re.escape(tok)}(\s*[\)\]|:\-–]|$)", title.upper()):
            continue
        if tok not in hits:
            hits.append(tok)
    if not hits:
        return None, "not in coverage"
    if len(hits) > 1:
        return None, "ambiguous: " + ",".join(hits)
    return hits[0], "ok"


# ---------------------------------------------------------------- captions

def parse_vtt(text: str) -> str:
    """WebVTT -> plain text, dropping timing lines, tags and the rolling
    duplicates that YouTube auto-captions emit."""
    out: list[str] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line == "WEBVTT" or "-->" in line or line.isdigit():
            continue
        if line.startswith(("Kind:", "Language:", "NOTE", "STYLE")):
            continue
        line = re.sub(r"<[^>]+>", "", line).strip()
        if line and (not out or line != out[-1]):
            out.append(line)
    return "\n".join(out)


def trim_middle(text: str, limit: int = MAX_TRANSCRIPT_CHARS) -> str:
    if len(text) <= limit:
        return text
    head = int(limit * 0.6)
    tail = limit - head
    return text[:head] + "\n\n[... ตัดช่วงกลางออกเพื่อความยาว ...]\n\n" + text[-tail:]


# Extra yt-dlp options for every call, e.g. ["--cookies-from-browser", "firefox"].
# YouTube throttles unauthenticated caption downloads (HTTP 429) much sooner.
YTDLP_EXTRA: list[str] = []


def _ytdlp(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, "-m", "yt_dlp", *YTDLP_EXTRA, *args], capture_output=True, text=True)


def pick_track(subs: list[str], auto: list[str]) -> tuple[str, bool] | None:
    """One Thai track to download: (lang, is_auto). Uploaded Thai first, then the
    original-language auto track (th-orig, the speech itself), then auto th.
    One request per video keeps the caption endpoint under its rate limit."""
    for lang in ("th", "th-TH"):
        if lang in subs:
            return lang, False
    for lang in ("th-orig", "th"):
        if lang in auto:
            return lang, True
    return None


def list_playlist(url: str) -> list[dict]:
    proc = _ytdlp("--flat-playlist", "-J", url)
    if proc.returncode != 0:
        raise SystemExit(f"{TAG} yt-dlp could not read the playlist: {proc.stderr.strip()[:300]}")
    data = json.loads(proc.stdout)
    return [{"id": e["id"], "title": e.get("title") or ""} for e in data.get("entries") or [] if e.get("id")]


class CaptionsBlocked(RuntimeError):
    """yt-dlp could not read the video (bot check, rate limit, private)."""


def caption_langs(meta: dict) -> tuple[list[str], list[str]]:
    """(uploaded, auto) caption language codes YouTube lists for the video."""
    return sorted((meta.get("subtitles") or {}).keys()), sorted((meta.get("automatic_captions") or {}).keys())


def fetch_captions(video_id: str) -> tuple[str, dict]:
    """Thai captions (uploaded first, then auto) as plain text, plus video metadata.

    Raises CaptionsBlocked when YouTube refuses the request, so a blocked run
    is never reported as videos without captions. meta["_caption_note"] says
    which tracks exist when there is no Thai one."""
    url = f"https://www.youtube.com/watch?v={video_id}"
    meta_proc = _ytdlp("-J", "--skip-download", url)
    if meta_proc.returncode != 0:
        raise CaptionsBlocked(meta_proc.stderr.strip().splitlines()[-1][:200] if meta_proc.stderr.strip()
                              else f"yt-dlp exit {meta_proc.returncode}")
    meta = json.loads(meta_proc.stdout)
    subs, auto = caption_langs(meta)
    if not any(l.startswith("th") for l in subs + auto):
        meta["_caption_note"] = (f"no Thai track; uploaded={','.join(subs) or '-'} "
                                 f"auto={','.join(a for a in auto if len(a) <= 3)[:60] or '-'}")
        return "", meta
    lang, is_auto = pick_track(subs, auto) or ("th", True)
    with tempfile.TemporaryDirectory() as tmp:
        proc = _ytdlp("--skip-download", "--write-auto-subs" if is_auto else "--write-subs",
                      "--sub-langs", lang, "--sub-format", "vtt",
                      "-o", str(Path(tmp) / "%(id)s.%(ext)s"), url)
        files = sorted(Path(tmp).glob(f"{video_id}*.vtt"))
        if not files and proc.returncode != 0:
            raise CaptionsBlocked(proc.stderr.strip().splitlines()[-1][:200] if proc.stderr.strip()
                                  else f"yt-dlp exit {proc.returncode}")
        text = parse_vtt(files[0].read_text(encoding="utf-8")) if files else ""
    if not text:
        meta["_caption_note"] = "Thai track listed but download returned nothing"
    return text, meta


# ---------------------------------------------------------------- report

def be_date(upload_date: str) -> str:
    try:
        d = datetime.strptime(upload_date, "%Y%m%d")
    except (TypeError, ValueError):
        return "ไม่ระบุวันที่"
    months = ["มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน", "กรกฎาคม",
              "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"]
    return f"{d.day} {months[d.month - 1]} {d.year + 543}"


def period_be(period: str) -> str:
    m = re.fullmatch(r"q([1-4])y?(\d{4})", period)
    if m:
        return f"Q{m.group(1)}/{int(m.group(2)) + 543}"
    m = re.fullmatch(r"ye(\d{4})", period)
    return f"ปีเต็ม {int(m.group(1)) + 543}" if m else period.upper()


_TITLE_PERIOD = re.compile(
    r"\b(Q[1-4]|[369]M|H[12]|YE|FY)\s*/?\s*((?:25|20)\d{2})(?:\s*/\s*((?:25|20)\d{2}))?", re.I)


def title_period(title: str) -> str | None:
    """The company's own period as printed in the title, in BE: Q3/2569,
    9M/2569, Q1/2569/2570. None when the title carries no period.

    Companies with a non-calendar fiscal year (KTIS, EPG, the REITs) present
    their own quarter during the calendar Q2 season, so the season code alone
    would mislabel them."""
    m = _TITLE_PERIOD.search(title or "")
    if not m:
        return None
    be = lambda y: str(int(y) + 543 if int(y) < 2500 else int(y))
    label = f"{m.group(1).upper()}/{be(m.group(2))}"
    return label + (f"/{be(m.group(3))}" if m.group(3) else "")


def period_label_for(title: str, period: str) -> str:
    return title_period(title) or period_be(period)


def numbers_in(text: str) -> list[str]:
    return re.findall(r"\d[\d,]*(?:\.\d+)?", text)


# Formatting, not claims: section numbers, period labels (Q2/2569, H1/2026,
# FY2568, 6M26) and calendar years, which the prompt asks for in BE and the
# speaker may say either way.
_NOT_CLAIMS = re.compile(
    r"^#+\s*\d+\.|^\s*\d+\.\s|\b(?:Q[1-4]|H[12]|[369]M|FY)\s*/?\s*\d{2,4}\b|"
    r"\b(?:25[5-9]\d|20[1-3]\d)\b", re.MULTILINE)


def check_numbers(summary: str, transcript: str) -> tuple[list[str], int]:
    """(untraced numbers, total numbers) for the report body, header excluded."""
    from enrich_filing import _norm_numbers, _untraced_numbers
    body = _NOT_CLAIMS.sub(" ", summary.split("## 1.", 1)[-1])
    return _untraced_numbers(body, _norm_numbers(transcript)), len(numbers_in(body))


def transcript_note(tk: str, period: str, video_id: str, title: str, meta: dict, text: str) -> str:
    fetched = datetime.now(timezone.utc).isoformat(timespec="seconds")
    return (f"---\nticker: {tk}\nperiod: {period_label_for(title, period)}\nsource: youtube-captions\n"
            f"video_id: {video_id}\nurl: https://www.youtube.com/watch?v={video_id}\n"
            f"upload_date: {meta.get('upload_date', '')}\nfetched: {fetched}\n---\n\n"
            f"# {title}\n\n{text}\n")


def summarise(tk: str, period: str, meta: dict, transcript: str, chat, others: list[str] | None = None) -> str:
    label = period_label_for(meta.get("title", ""), period)
    date_line = f"ผลประกอบการ {label} ({be_date(meta.get('upload_date', ''))})"
    system = SYSTEM_PROMPT.replace("{TICKER}", tk).replace("{DATE_LINE}", date_line)
    joint = (f"คลิปนี้เป็นการนำเสนอร่วมกับ {', '.join(others)} ให้สรุปเฉพาะข้อมูลของ {tk} "
             f"ถ้าผู้พูดไม่ได้แยกข้อมูลของ {tk} ให้เขียนว่า ไม่ระบุ\n\n") if others else ""
    user = f"{joint}ชื่อคลิป: {meta.get('title', '')}\n\nคำถอดเสียง:\n{trim_middle(transcript)}"
    text = chat(system, user, max_tokens=6000, temperature=0.2)
    return text.strip() + "\n"


def finalise(summary: str, transcript: str) -> tuple[str, bool, list[str]]:
    """Append the number check. Returns (text, held, untraced)."""
    untraced, total = check_numbers(summary, transcript)
    held = bool(total) and len(untraced) / total > HOLD_RATIO
    if untraced:
        summary += ("\n---\n\n## หมายเหตุการตรวจสอบตัวเลข\n\n"
                    f"ตัวเลขที่ไม่พบในคำถอดเสียง {len(untraced)} จาก {total} ตัว ควรตรวจกับสไลด์หรือคลิปก่อนใช้: "
                    + ", ".join(untraced[:30]) + "\n")
    return summary, held, untraced


# ---------------------------------------------------------------- run

def run(args, *, lister=list_playlist, fetcher=fetch_captions, chat=None) -> int:
    vault = Path(os.environ.get("VAULT_ROOT") or DEFAULT_VAULT)
    if not args.list and not args.dry_run and not (vault / LISTED).is_dir():
        print(f"{TAG} vault not found: {vault}", file=sys.stderr)
        return 2
    coverage = load_coverage()
    only = {t.strip().upper() for t in (args.only or "").split(",") if t.strip()}
    assign: dict[str, list[str]] = {}
    for spec in args.assign or []:
        vid, _, tks = spec.partition("=")
        picked = [t.strip().upper() for t in tks.split(",") if t.strip()]
        bad = [t for t in picked if t not in coverage]
        if not vid or not picked or bad:
            print(f"{TAG} bad --assign {spec!r}" + (f": not coverage {bad}" if bad else ""), file=sys.stderr)
            return 1
        assign[vid.strip()] = picked
    entries = lister(args.url)
    matched, skipped = [], {"not in coverage": 0}
    for e in entries:
        if e["id"] in assign:
            # Joint session or ambiguous title, resolved by hand: one report per ticker.
            group = assign[e["id"]]
            for tk in group:
                if not only or tk in only:
                    matched.append((tk, dict(e, others=[t for t in group if t != tk])))
            continue
        tk, why = match_title(e["title"], coverage)
        if tk and (not only or tk in only):
            matched.append((tk, e))
        elif why.startswith("ambiguous"):
            print(f"{TAG} AMBIGUOUS {e['id']} {e['title']} -> {why}  "
                  f"(resolve with --assign {e['id']}=TICKER[,TICKER])")
        else:
            skipped["not in coverage"] += 1
    print(f"{TAG} playlist {len(entries)} videos; coverage matches {len(matched)}; "
          f"not ours {skipped['not in coverage']}")
    if args.list:
        season = period_be(args.period)
        for tk, e in matched:
            own = title_period(e["title"])
            note = f"\tperiod {own}" if own and own != season else ""
            print(f"{tk}\t{e['id']}\t{e['title']}{note}")
        missing = sorted(coverage - {tk for tk, _ in matched})
        print(f"{TAG} coverage tickers with no video: {len(missing)}")
        print(", ".join(missing))
        return 0

    if chat is None and not args.dry_run:
        # setx writes HKCU but running shells (Hermes) keep their old env;
        # fill in the missing variables from the registry, as the cron shim does.
        from cron_shim import _load_user_env
        _load_user_env()
        import minimax_chat
        if not minimax_chat.available():
            print(f"{TAG} MINIMAX_API_KEY not set (process env or HKCU\\Environment)", file=sys.stderr)
            return 1
        chat = minimax_chat.chat

    stats = {"published": 0, "held": 0, "no_captions": 0, "exists": 0, "failed": 0}
    done = 0
    fetched: dict[str, tuple[str, dict]] = {}
    fetched_any = False
    for tk, e in matched:
        if args.limit and done >= args.limit:
            break
        stem = f"{tk}_oppday_{args.period}"
        report = vault / REPORTS_DIR / f"{stem}_summary.md"
        review = vault / REPORTS_DIR / f"{stem}_summary.review.md"
        tpath = vault / TRANSCRIPT_DIR / tk / f"{stem}_transcript.md"
        if not args.force and (report.exists() or review.exists()):
            stats["exists"] += 1
            continue
        done += 1
        if args.dry_run:
            print(f"{TAG} DRY_RUN would process {tk} {e['id']} {e['title'][:60]}")
            continue
        try:
            if e["id"] in fetched:          # joint session: one download for all its tickers
                text, meta = fetched[e["id"]]
            else:
                if fetched_any and args.pause:
                    time.sleep(args.pause)
                fetched_any = True
                text, meta = fetcher(e["id"])
                fetched[e["id"]] = (text, dict(meta))
                meta = dict(meta)
            meta.setdefault("title", e["title"])
            if len(text) < 500:
                stats["no_captions"] += 1
                why = meta.get("_caption_note") or f"only {len(text)} chars"
                print(f"{TAG} {tk}: no usable Thai captions ({why}); skipped")
                continue
            tpath.parent.mkdir(parents=True, exist_ok=True)
            tpath.write_text(transcript_note(tk, args.period, e["id"], e["title"], meta, text), encoding="utf-8")
            summary, held, untraced = finalise(
                summarise(tk, args.period, meta, text, chat, e.get("others")), text)
            report.parent.mkdir(parents=True, exist_ok=True)
            (review if held else report).write_text(summary, encoding="utf-8")
            stats["held" if held else "published"] += 1
            print(f"{TAG} {tk}: {'HELD for review' if held else 'written'}; untraced numbers {len(untraced)}")
        except CaptionsBlocked as exc:
            stats["blocked"] = stats.get("blocked", 0) + 1
            print(f"{TAG} {tk}: YouTube refused the request: {exc}", file=sys.stderr)
            if stats["blocked"] >= 3:
                print(f"{TAG} stopping: 3 refusals in a row looks like a block; retry later", file=sys.stderr)
                break
            continue
        except Exception as exc:  # one bad video must not stop the batch
            stats["failed"] += 1
            print(f"{TAG} {tk}: failed: {exc}", file=sys.stderr)
    print(f"{TAG} done: {stats}")
    return 1 if stats["failed"] or stats.get("blocked") else 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("url", help="YouTube playlist URL")
    p.add_argument("--period", required=True, help="file period code, e.g. q2y2026 or ye2025")
    p.add_argument("--list", action="store_true", help="match titles to coverage only; no downloads")
    p.add_argument("--only", help="comma-separated tickers")
    p.add_argument("--assign", action="append", metavar="VIDEO_ID=TK[,TK]",
                   help="process a joint-session or ambiguous video for these tickers (repeatable)")
    p.add_argument("--limit", type=int, default=0, help="max new videos this run")
    p.add_argument("--force", action="store_true", help="redo tickers that already have a report")
    p.add_argument("--dry-run", action="store_true", help="show what would run; no downloads or writes")
    p.add_argument("--pause", type=float, default=20.0,
                   help="seconds between videos (default 20); YouTube returns HTTP 429 when rushed")
    p.add_argument("--cookies-from-browser", metavar="BROWSER",
                   help="pass the signed-in browser session to yt-dlp (firefox works best on Windows)")
    p.add_argument("--cookies", metavar="FILE", help="Netscape cookies.txt exported from the browser")
    args = p.parse_args(argv)
    YTDLP_EXTRA.clear()
    if args.cookies_from_browser:
        YTDLP_EXTRA.extend(["--cookies-from-browser", args.cookies_from_browser])
    if args.cookies:
        YTDLP_EXTRA.extend(["--cookies", args.cookies])
    if not re.fullmatch(r"(q[1-4]y?\d{4}|ye\d{4})", args.period):
        p.error("--period must look like q2y2026 or ye2025")
    return run(args)


if __name__ == "__main__":
    sys.exit(main())
