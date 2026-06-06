"""
build_lux_scanner.py — Daily SET Lux Algo scan for the IS1 dashboard.

Runs after SET market close (scheduled at 11:30 UTC = 18:30 BKK).
Downloads 6-month daily OHLCV from Yahoo Finance for 150+ SET tickers,
computes Lux Algo–equivalent signals, calls Claude for the AI brief,
then writes data/lux-scanner.json.

Secrets required: ANTHROPIC_API_KEY (already present in the repo secrets).
No other secrets needed — yfinance is public.
"""

from __future__ import annotations

import json
import os
import sys
import time
import warnings
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import yfinance as yf

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"


# ─────────────────────────────────────────────────────────────────────────────
# SET TICKER UNIVERSE  (~150 liquid tickers across 14 sectors)
# ─────────────────────────────────────────────────────────────────────────────

SET_UNIVERSE: dict[str, list[str]] = {
    "ENERGY":       ["PTT","PTTEP","PTTGC","TOP","IRPC","BCP","SPRC","TASCO","BANPU","RATCH","EGCO","GPSC","EA","GUNKUL","TPIPP","GULF","CKP","DEMCO","BGRIM","WHAUP","EASTW"],
    "BANKING":      ["KBANK","SCB","BBL","KTB","TTB","TISCO","KKP","TCAP"],
    "FINANCE":      ["AEONTS","MTC","SAWAD","JMT","TIDLOR","KTC","THANI","MFC","TKT"],
    "INDUSTRIAL":   ["SCC","SCCC","IVL","HANA","DELTA","KCE","SVI","FORTH","ICC","SMT","ESTAR"],
    "PROPERTY":     ["LH","QH","SPALI","SIRI","AP","ORI","SC","PSH","NOBLE","ANAN","GRAND","PLANET","KOOL","MJD"],
    "PFREIT":       ["CPNREIT","FTREIT","WHART","AIMIRT","DIF","FUTUREPF","POPF","SSPF"],
    "FOOD":         ["CPF","TU","GFPT","CBG","OSP","TKN","SAPPE","TIPCO"],
    "RETAIL":       ["CPALL","BJC","CPN","HMPRO","CRC","DOHOME","BEAUTY","MK","MINT","ERW","CENTEL"],
    "HEALTHCARE":   ["BDMS","BCH","BH","VIBHA","CHG","EKH","PR9","PHOL","RAM"],
    "TELECOM":      ["ADVANC","TRUE","INTUCH","JAS","THCOM","INET","SIS","MSC","IT"],
    "TRANSPORT":    ["AOT","BTS","BEM","THAI","AAV","BA","PSL","TTA","WICE","LEO"],
    "MEDIA":        ["VGI","MAJOR","RS","BEC","MONO","MCOT","WORK","PLANB","JMART"],
    "MATERIALS":    ["STA","STGT","TPBI","AGE","PANEL","SYNTEC","CK","ITD","SEAFCO"],
    "AGRI":         ["TFG","CFRESH","TVO","MILL"],
}


def _rsi(s: pd.Series, n: int = 14) -> pd.Series:
    d = s.diff()
    g = d.clip(lower=0).ewm(com=n - 1, adjust=False).mean()
    l = (-d).clip(lower=0).ewm(com=n - 1, adjust=False).mean()
    return 100 - 100 / (1 + g / l.replace(0, np.nan))


def _atr(df: pd.DataFrame, n: int = 14) -> pd.Series:
    h, l, c = df["High"], df["Low"], df["Close"]
    tr = pd.concat([h - l, (h - c.shift()).abs(), (l - c.shift()).abs()], axis=1).max(axis=1)
    return tr.rolling(n).mean()


def compute_score(df: pd.DataFrame) -> dict | None:
    if len(df) < 50:
        return None
    try:
        close = df["Close"]
        high, low = df["High"], df["Low"]
        vol = df.get("Volume", pd.Series(1, index=df.index))

        # ── SuperTrend ──────────────────────────────────────────────────────
        atr10 = _atr(df, 10)
        hl2 = (high + low) / 2
        ub = hl2 + 3 * atr10
        lb = hl2 - 3 * atr10
        st_val = pd.Series(np.nan, index=df.index)
        st_dir = pd.Series(1, index=df.index)
        for i in range(1, len(df)):
            pv = st_val.iloc[i - 1] if not pd.isna(st_val.iloc[i - 1]) else close.iloc[i]
            pc = close.iloc[i - 1]
            if close.iloc[i] > ub.iloc[i] if not pd.isna(ub.iloc[i]) else pv:
                st_dir.iloc[i] = 1
                st_val.iloc[i] = max(lb.iloc[i] if not pd.isna(lb.iloc[i]) else pv, pv) if st_dir.iloc[i - 1] == 1 else lb.iloc[i] if not pd.isna(lb.iloc[i]) else pv
            elif close.iloc[i] < lb.iloc[i] if not pd.isna(lb.iloc[i]) else pv:
                st_dir.iloc[i] = -1
                st_val.iloc[i] = min(ub.iloc[i] if not pd.isna(ub.iloc[i]) else pv, pv) if st_dir.iloc[i - 1] == -1 else ub.iloc[i] if not pd.isna(ub.iloc[i]) else pv
            else:
                st_dir.iloc[i] = st_dir.iloc[i - 1]
                st_val.iloc[i] = pv

        st_buy_recent = ((st_dir == 1) & (st_dir.shift(1) == -1)).iloc[-5:].any()

        # ── Smart Trail ─────────────────────────────────────────────────────
        atr14 = _atr(df, 14)
        trail = pd.Series(np.nan, index=df.index)
        trail_dir = pd.Series(1, index=df.index)
        for i in range(1, len(df)):
            pv = trail.iloc[i - 1] if not pd.isna(trail.iloc[i - 1]) else close.iloc[i]
            sd = 2.0 * (atr14.iloc[i] if not pd.isna(atr14.iloc[i]) else 0)
            if close.iloc[i] > pv:
                trail.iloc[i] = max(pv, close.iloc[i] - sd)
                trail_dir.iloc[i] = 1
            else:
                trail.iloc[i] = min(pv, close.iloc[i] + sd)
                trail_dir.iloc[i] = -1
        trail_buy_recent = ((close > trail) & (close.shift(1) <= trail.shift(1))).iloc[-5:].any()

        # ── EMA Ribbon ──────────────────────────────────────────────────────
        emas = {p: close.ewm(span=p, adjust=False).mean() for p in [9, 21, 50, 100, 200]}
        ribbon = int(
            (emas[9].iloc[-1] > emas[21].iloc[-1]) +
            (emas[21].iloc[-1] > emas[50].iloc[-1]) +
            (emas[50].iloc[-1] > emas[100].iloc[-1]) +
            (emas[100].iloc[-1] > emas[200].iloc[-1])
        )
        above_200 = int(close.iloc[-1] > emas[200].iloc[-1])

        # ── RSI & Oscillator ─────────────────────────────────────────────────
        rsi = _rsi(close, 14)
        stoch_k = 100 * (close - low.rolling(14).min()) / (high.rolling(14).max() - low.rolling(14).min() + 1e-10)
        tp = (high + low + close) / 3
        cci = (tp - tp.rolling(20).mean()) / (0.015 * tp.rolling(20).std() + 1e-10)
        mfm = ((close - low) - (high - close)) / (high - low + 1e-10)
        mfi_raw = (mfm * vol).rolling(14).sum() / vol.rolling(14).sum()
        osc = ((rsi - 50) * 2 + (stoch_k - 50) * 2 + cci.clip(-100, 100) + mfi_raw * 100) / 4
        osc_sig = osc.ewm(span=9, adjust=False).mean()
        osc_cross_up = ((osc > osc_sig) & (osc.shift(1) <= osc_sig.shift(1))).iloc[-5:].any()
        osc_last = osc.iloc[-1]

        # ── MACD ─────────────────────────────────────────────────────────────
        macd = close.ewm(span=12, adjust=False).mean() - close.ewm(span=26, adjust=False).mean()
        macd_sig = macd.ewm(span=9, adjust=False).mean()
        macd_bull = bool(not pd.isna(macd.iloc[-1]) and macd.iloc[-1] > macd_sig.iloc[-1])
        macd_cross = ((macd > macd_sig) & (macd.shift(1) <= macd_sig.shift(1))).iloc[-5:].any()

        # ── Volume ───────────────────────────────────────────────────────────
        vol_ratio = vol / vol.rolling(20).mean().replace(0, np.nan)
        vol_surge = bool(vol_ratio.iloc[-1] > 1.5 if not pd.isna(vol_ratio.iloc[-1]) else False)
        obv = (vol * np.sign(close.diff())).cumsum()
        obv_trend = int(obv.iloc[-1] > obv.ewm(span=20, adjust=False).mean().iloc[-1])

        # ── AI Cluster (simplified KMeans) ───────────────────────────────────
        try:
            from sklearn.cluster import KMeans
            from sklearn.preprocessing import StandardScaler
            feat = pd.DataFrame({
                "rsi": rsi,
                "ema_r": (emas[9] / emas[21] - 1) * 100,
                "atr_p": atr14 / close * 100,
                "vol_r": vol_ratio,
            }).dropna()
            if len(feat) >= 30:
                sc = StandardScaler()
                X = sc.fit_transform(feat)
                km = KMeans(n_clusters=3, random_state=42, n_init=10)
                labels = km.fit_predict(X)
                ctrs = sc.inverse_transform(km.cluster_centers_)
                bull_c = int(np.argmax(ctrs[:, 0] + ctrs[:, 1]))
                bear_c = int(np.argmin(ctrs[:, 0] + ctrs[:, 1]))
                last_label = labels[feat.index.get_loc(feat.index[-1])]
                ai_cluster = "BULL" if last_label == bull_c else ("BEAR" if last_label == bear_c else "NEUTRAL")
            else:
                ai_cluster = "NEUTRAL"
        except Exception:
            ai_cluster = "NEUTRAL"

        # ── Scoring ──────────────────────────────────────────────────────────
        st_s = 35 if st_dir.iloc[-1] == 1 else 0
        if st_buy_recent:
            st_s = min(st_s + 15, 50)
        trail_s = 20 if trail_dir.iloc[-1] == 1 else 0
        cluster_s = 15 if ai_cluster == "BULL" else (-5 if ai_cluster == "BEAR" else 0)
        if pd.isna(osc_last):
            osc_s = 7
        elif osc_last > 20:
            osc_s = 15
        elif osc_last > 0:
            osc_s = 10
        elif osc_last > -20:
            osc_s = 5
        else:
            osc_s = 0
        ribbon_s = ribbon * 2 + above_200 * 2
        macd_s = 5 if macd_bull else 0
        vol_s = int(vol_surge) * 3 + obv_trend * 2
        total = min(100, max(0, st_s + trail_s + cluster_s + osc_s + ribbon_s + macd_s + vol_s))

        # ── Active signals list ───────────────────────────────────────────────
        sigs = []
        if st_buy_recent:   sigs.append("LUX_BUY")
        if trail_buy_recent: sigs.append("TRAIL_BUY")
        if ai_cluster == "BULL": sigs.append("AI_BULL_CLUSTER")
        if osc_cross_up:    sigs.append("OSC_CROSS_UP")
        if ribbon >= 3:     sigs.append("EMA_RIBBON_BULL")
        if macd_cross:      sigs.append("MACD_CROSS")
        if vol_surge:       sigs.append("VOL_SURGE")

        c1d = float(close.iloc[-1] / close.iloc[-2] - 1) * 100 if len(close) > 1 else 0
        trend = ("STRONG BUY" if total >= 75 else "BUY" if total >= 55 else
                 "NEUTRAL" if total >= 40 else "SELL" if total >= 25 else "STRONG SELL")

        return {
            "score": round(total, 1),
            "trend": trend,
            "close": round(float(close.iloc[-1]), 2),
            "pct_change_1d": round(c1d, 2),
            "rsi": round(float(rsi.iloc[-1]), 1) if not pd.isna(rsi.iloc[-1]) else None,
            "supertrend_dir": "BULL" if st_dir.iloc[-1] == 1 else "BEAR",
            "ai_cluster": ai_cluster,
            "ema_ribbon": f"{ribbon}/4",
            "macd_bull": macd_bull,
            "vol_surge": vol_surge,
            "signals": sigs,
            "signal_count": len(sigs),
            "support":     round(float(low.rolling(20).min().iloc[-1]), 2),
            "resistance":  round(float(high.rolling(20).max().iloc[-1]), 2),
            "score_breakdown": {
                "supertrend": st_s, "smart_trail": trail_s,
                "ai_cluster": cluster_s, "oscillator": osc_s,
                "ema_ribbon": ribbon_s, "macd": macd_s, "volume": vol_s,
            },
        }
    except Exception:
        return None


def fetch_and_score(ticker: str, sector: str) -> dict | None:
    try:
        df = yf.download(f"{ticker}.BK", period="6mo", interval="1d",
                         progress=False, auto_adjust=True, timeout=20)
        if df is None or len(df) < 30:
            return None
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        r = compute_score(df)
        if r is None:
            return None
        r["ticker"] = ticker
        r["sector"] = sector
        return r
    except Exception:
        return None


def run_scan(max_workers: int = 10) -> list[dict]:
    tasks = [(tk, sec) for sec, tks in SET_UNIVERSE.items() for tk in tks]
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futures = {ex.submit(fetch_and_score, tk, sec): (tk, sec) for tk, sec in tasks}
        for fut in as_completed(futures):
            r = fut.result()
            if r:
                results.append(r)
    results.sort(key=lambda x: x["score"], reverse=True)
    return results


def get_ai_summary(picks: list[dict], total_scanned: int) -> str:
    api_key = os.getenv("ANTHROPIC_API_KEY", "")
    if not api_key:
        return ""
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        top_text = ""
        for i, p in enumerate(picks[:15], 1):
            top_text += (
                f"{i}. {p['ticker']} ({p['sector']}) Score:{p['score']}/100 "
                f"Price:{p['close']}฿ 1D:{p['pct_change_1d']:+.1f}% RSI:{p['rsi']} "
                f"ST:{p['supertrend_dir']} Cluster:{p['ai_cluster']} "
                f"Signals:[{', '.join(p['signals'])}]\n"
            )
        strong_sectors = {}
        for p in picks:
            if p["trend"] in ("STRONG BUY", "BUY"):
                strong_sectors[p["sector"]] = strong_sectors.get(p["sector"], 0) + 1
        sector_summary = ", ".join(f"{k}:{v}" for k, v in
                                   sorted(strong_sectors.items(), key=lambda x: -x[1])[:5])
        resp = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=600,
            messages=[{"role": "user", "content":
                f"SET Daily Lux Algo Scan — {today}\n"
                f"Tickers scanned: {total_scanned} | Buy signals: {len(picks)}\n"
                f"Top sectors: {sector_summary}\n\n"
                f"TOP PICKS:\n{top_text}\n"
                "Write a 3-sentence market tone summary for an IS1 Relationship Manager. "
                "Focus on: (1) market breadth, (2) top 3 highest-conviction picks with price/target, "
                "(3) key sector theme. Be concise and actionable. Thai stock market context."}],
        )
        return resp.content[0].text.strip()
    except Exception as e:
        print(f"[AI summary] skipped: {e}", file=sys.stderr)
        return ""


def build(out_path: Path | None = None) -> None:
    if out_path is None:
        out_path = DATA_DIR / "lux-scanner.json"

    print("[lux-scanner] Starting scan…", flush=True)
    t0 = time.time()
    results = run_scan(max_workers=10)
    elapsed = round(time.time() - t0, 1)

    picks = [r for r in results if r["score"] >= 55]
    strong_buys = [r for r in results if r["trend"] == "STRONG BUY"]

    print(f"[lux-scanner] Scanned {len(results)} tickers in {elapsed}s | "
          f"Buy: {len(picks)} | Strong Buy: {len(strong_buys)}", flush=True)

    # Market tone
    avg_score = round(sum(r["score"] for r in results) / len(results), 1) if results else 0
    buy_pct   = round(len(picks) / len(results) * 100, 1) if results else 0
    market_tone = ("STRONGLY BULLISH" if buy_pct >= 35 else
                   "BULLISH" if buy_pct >= 20 else
                   "NEUTRAL" if buy_pct >= 10 else "BEARISH")

    # Sector breakdown
    sector_counts: dict[str, dict] = {}
    for r in results:
        s = r["sector"]
        if s not in sector_counts:
            sector_counts[s] = {"buy": 0, "total": 0, "scores": []}
        sector_counts[s]["total"] += 1
        sector_counts[s]["scores"].append(r["score"])
        if r["trend"] in ("STRONG BUY", "BUY"):
            sector_counts[s]["buy"] += 1
    sector_summary = sorted([
        {"sector": s, "buy_count": v["buy"], "total": v["total"],
         "avg_score": round(sum(v["scores"]) / len(v["scores"]), 1)}
        for s, v in sector_counts.items()
    ], key=lambda x: -x["avg_score"])

    # AI summary (best-effort)
    ai_summary = get_ai_summary(picks, len(results))

    payload = {
        "built_at":       datetime.now(timezone.utc).isoformat(),
        "scan_date":      datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "scan_elapsed_s": elapsed,
        "total_scanned":  len(results),
        "buy_signals":    len(picks),
        "strong_buy_signals": len(strong_buys),
        "avg_score":      avg_score,
        "buy_pct":        buy_pct,
        "market_tone":    market_tone,
        "ai_summary":     ai_summary,
        "picks":          picks[:40],
        "sector_summary": sector_summary,
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    print(f"[lux-scanner] Written → {out_path}", flush=True)


if __name__ == "__main__":
    build()
