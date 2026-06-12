"""
event_study_multi.py — multi-event study of CRYPTO-NATIVE stress episodes (rebuild).

Why this replaces the old 3-event design
-----------------------------------------
The committed event_study.py runs LUNA + USDT-depeg + USDC/SVB as a "low vs high
buffer" comparison. Per Prof. Hur:
  - SVB is confounded (it hit Treasuries through the banking channel, not just the
    USDC depeg) → "you cannot use this". Dropped here.
  - LUNA is good motivation; he asked for MORE similar (crypto-native) crises.

Dropping SVB removes the only "high-buffer" event, so the old low-vs-high design
collapses. This script reframes the event study around its defensible core: do
CRYPTO-NATIVE stress episodes systematically move the OIS–Treasury spread (the
privilege proxy)? More events + a proper cross-event test buys the power that the
single-event CARs (all insignificant) lacked.

Event-selection rule (the principled defense against "why these and not SVB"):
  Crypto-native stress with NO simultaneous banking/macro shock to Treasuries.

Events
------
  LUNA/UST collapse  2022-05-09   algorithmic-stablecoin death spiral (anchor)
  Celsius freeze     2022-06-13   crypto-credit run (part of the 2022 cascade)
  FTX collapse       2022-11-08   exchange failure, USDT brief depeg
  BUSD shutdown      2023-02-13   NYDFS forces Paxos to stop minting (regulatory)

NOTE on independence: LUNA and Celsius are one 2022 deleveraging chain — their
windows overlap, so they are NOT independent observations. FTX (autumn) and BUSD
(2023) are separate. The honest count is ~3 independent episodes, not 4. Reported
both per-event and pooled so the reader can judge.

Method
------
  1. Normal model in FIRST DIFFERENCES (removes the Fed-hiking trend that inflated
     the original levels CARs ~120x):  Δspread ~ α + ΔVIX + Δln(row_equity)
     estimated over EST_WINDOW = (-120,-6) trading days.
  2. AR_τ = Δspread_τ − predicted, over EVENT_WINDOW (-5,+20); CAR = cumsum.
  3. Per-event SE from the ESTIMATION-window residual σ (not the event window):
     SE(CAR over k days) = σ_est·√k. (The old code used the event window's own
     dispersion, which is contaminated by the event itself.)
  4. Cross-event CAAR: average AR across events at each relative day, cumulate,
     and test the final CAAR using the cross-event dispersion (events = unit of
     observation → robust to within-event daily autocorrelation).

Sign convention & hypothesis
----------------------------
spread = DTB3 − OIS, in bps. The fragility/New-Triffin prediction for a crypto
stress episode (redemptions → forced T-bill sales) is a WIDENING spread → CAR > 0
(privilege erosion). A flight-to-T-bills story predicts CAR < 0. We let the data
speak and report the sign.

Outputs: results/event_study_multi_{table,caar}.csv, results/event_study_multi.png
Leaves the original event_study.py untouched.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import statsmodels.api as sm
from scipy import stats

ROOT = Path(__file__).resolve().parent                 # main project root (for data)
DAILY_CSV = ROOT / "data" / "daily_panel.csv"
OUT = ROOT / "results"
OUT.mkdir(exist_ok=True)

EVENTS = {
    "LUNA_UST":   {"date": "2022-05-09", "label": "LUNA / UST collapse",   "indep": True},
    "Celsius":    {"date": "2022-06-13", "label": "Celsius freeze",        "indep": False},
    "FTX":        {"date": "2022-11-08", "label": "FTX collapse",          "indep": True},
    "BUSD":       {"date": "2023-02-13", "label": "BUSD shutdown (NYDFS)", "indep": True},
}

EST_WINDOW = (-120, -6)
EVENT_WINDOW = (-5, 20)
CAR_HORIZONS = [5, 10, 20]          # report CAR[0,+h] for these h
CONTROLS = ["dvix", "dln_row_equity"]


def offset_date(idx: pd.DatetimeIndex, anchor: pd.Timestamp, k: int) -> pd.Timestamp:
    pos = idx.get_indexer([anchor], method="nearest")[0]
    return idx[max(0, min(pos + k, len(idx) - 1))]


def run_event(df: pd.DataFrame, meta: dict) -> dict:
    idx = df.index
    anchor = pd.Timestamp(meta["date"])

    est = df.loc[offset_date(idx, anchor, EST_WINDOW[0]):offset_date(idx, anchor, EST_WINDOW[1])]
    est = est.dropna(subset=["dspread"] + CONTROLS)
    model = sm.OLS(est["dspread"], sm.add_constant(est[CONTROLS])).fit()
    sigma_est = np.sqrt(model.scale)        # residual std from the estimation window
    b = model.params                        # const, dvix, dln_row_equity

    # event-window AR indexed by relative trading day τ (vectorised prediction)
    pos = idx.get_indexer([anchor], method="nearest")[0]
    rel = {}
    for k in range(EVENT_WINDOW[0], EVENT_WINDOW[1] + 1):
        j = pos + k
        if 0 <= j < len(idx):
            row = df.iloc[j]
            if pd.notna(row["dspread"]) and all(pd.notna(row[c]) for c in CONTROLS):
                pred = b["const"] + b["dvix"] * row["dvix"] + b["dln_row_equity"] * row["dln_row_equity"]
                rel[k] = row["dspread"] - pred
    ar = pd.Series(rel).sort_index()

    # CAR from τ=0 onward, at each horizon, with estimation-based SE
    post = ar[ar.index >= 0]
    car_cum = post.cumsum()
    out = {"event": meta["label"], "date": meta["date"], "indep": meta["indep"],
           "ar": ar, "car_post": car_cum}
    for h in CAR_HORIZONS:
        days = post[post.index <= h]
        car = days.sum()
        se = sigma_est * np.sqrt(len(days))
        t = car / se if se > 0 else np.nan
        p = 2 * stats.t.sf(abs(t), df=max(len(est) - 3, 1)) if not np.isnan(t) else np.nan
        out[f"CAR_0_{h}"] = car
        out[f"p_0_{h}"] = p
    return out


def caar_test(results: list[dict], horizon: int = 20):
    """Cross-event CAAR: events are the unit of observation."""
    cars = np.array([r[f"CAR_0_{horizon}"] for r in results])
    n = len(cars)
    mean = cars.mean()
    sd = cars.std(ddof=1)
    se = sd / np.sqrt(n)
    t = mean / se if se > 0 else np.nan
    p = 2 * stats.t.sf(abs(t), df=n - 1) if not np.isnan(t) else np.nan
    # sign test: how many events share the majority sign
    n_pos = int((cars > 0).sum())
    return {"horizon": horizon, "n_events": n, "mean_CAR": mean, "sd": sd,
            "t": t, "p": p, "n_pos": n_pos, "cars": cars}


def build_caar_series(results: list[dict]) -> pd.DataFrame:
    """Average AR across events at each relative day, then cumulate (for the plot)."""
    mat = pd.DataFrame({r["event"]: r["ar"] for r in results})
    caar = mat.mean(axis=1).loc[0:].cumsum()
    return mat, caar


def sig(p):
    return "***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.10 else ""


def main():
    df = pd.read_csv(DAILY_CSV, index_col=0, parse_dates=True)
    df["spread"] = df["spread"] * 100        # pp → bps
    df["dspread"] = df["spread"].diff()
    df["dvix"] = df["vix"].diff()
    print(f"Daily panel: {len(df)} obs ({df.index[0].date()} – {df.index[-1].date()})\n")

    results = [run_event(df, meta) for meta in EVENTS.values()]

    # per-event table
    print("=" * 84)
    print("  PER-EVENT CARs (bps) — first-difference normal model, estimation-window SE")
    print("=" * 84)
    print(f"  {'event':24s} {'indep':5s} " + "  ".join(f'CAR[0,+{h}]' for h in CAR_HORIZONS))
    for r in results:
        cells = "  ".join(f"{r[f'CAR_0_{h}']:+7.2f}{sig(r[f'p_0_{h}']):3s}" for h in CAR_HORIZONS)
        print(f"  {r['event']:24s} {str(r['indep']):5s} {cells}")

    # cross-event pooled tests
    print("\n" + "=" * 84)
    print("  POOLED CROSS-EVENT CAAR (events = unit of observation)")
    print("=" * 84)
    pooled_rows = []
    for h in CAR_HORIZONS:
        pt = caar_test(results, h)
        pooled_rows.append(pt)
        print(f"  horizon +{h:2d}d: mean CAR = {pt['mean_CAR']:+7.2f} bps  "
              f"t={pt['t']:+.2f}  p={pt['p']:.3f}{sig(pt['p']):3s}  "
              f"({pt['n_pos']}/{pt['n_events']} positive)")

    # independent-only pooled (drop Celsius, the LUNA-clustered event)
    indep = [r for r in results if r["indep"]]
    print(f"\n  Independent-only ({len(indep)} events: "
          f"{', '.join(r['event'] for r in indep)}):")
    for h in CAR_HORIZONS:
        cars = np.array([r[f"CAR_0_{h}"] for r in indep])
        m, sd = cars.mean(), cars.std(ddof=1)
        se = sd / np.sqrt(len(cars)); t = m / se if se > 0 else np.nan
        p = 2 * stats.t.sf(abs(t), df=len(cars) - 1) if not np.isnan(t) else np.nan
        print(f"    horizon +{h:2d}d: mean CAR = {m:+7.2f} bps  t={t:+.2f}  p={p:.3f}{sig(p):3s}")

    # save tables
    tbl = pd.DataFrame([{**{"event": r["event"], "date": r["date"], "indep": r["indep"]},
                         **{f"CAR_0_{h}": r[f"CAR_0_{h}"] for h in CAR_HORIZONS},
                         **{f"p_0_{h}": r[f"p_0_{h}"] for h in CAR_HORIZONS}} for r in results])
    tbl.to_csv(OUT / "event_study_multi_table.csv", index=False)

    mat, caar = build_caar_series(results)
    caar.rename("CAAR").to_csv(OUT / "event_study_multi_caar.csv")

    # plot
    fig, axes = plt.subplots(1, len(results) + 1, figsize=(4 * (len(results) + 1), 3.6))
    for ax, r in zip(axes[:-1], results):
        c = r["car_post"]
        ax.plot(c.index, c.values, color="#d62728", lw=1.8)
        ax.axhline(0, color="black", lw=0.5); ax.axvline(0, color="black", ls="--", lw=0.7)
        ax.set_title(f"{r['event']}\nCAR[0,+20]={r['CAR_0_20']:+.1f} bps {sig(r['p_0_20'])}", fontsize=8)
        ax.set_xlabel("trading day τ"); ax.set_ylabel("CAR (bps)")
    axes[-1].plot(caar.index, caar.values, color="#1f77b4", lw=2.2)
    axes[-1].axhline(0, color="black", lw=0.5); axes[-1].axvline(0, color="black", ls="--", lw=0.7)
    pt20 = caar_test(results, 20)
    axes[-1].set_title(f"Pooled CAAR (all {pt20['n_events']})\n"
                       f"+20d={pt20['mean_CAR']:+.1f} bps, p={pt20['p']:.2f}", fontsize=8)
    axes[-1].set_xlabel("trading day τ"); axes[-1].set_ylabel("CAAR (bps)")
    plt.suptitle("Crypto-native stress episodes: cumulative abnormal OIS–Treasury spread (bps)", fontsize=10)
    plt.tight_layout()
    plt.savefig(OUT / "event_study_multi.png", dpi=150, bbox_inches="tight")

    write_summary(results, pooled_rows, indep)
    print(f"\n  -> {OUT/'event_study_multi_table.csv'}")
    print(f"  -> {OUT/'event_study_multi.png'}")
    print(f"  -> {OUT/'event_study_multi_summary.md'}")


def write_summary(results, pooled_rows, indep):
    p20 = next(p for p in pooled_rows if p["horizon"] == 20)
    direction = "widening (privilege erosion)" if p20["mean_CAR"] > 0 else "compression (flight to T-bills)"
    lines = [
        "# Multi-Event Study — Crypto-Native Stress Episodes",
        "",
        "**Rebuild of the event study per Prof. Hur:** SVB dropped (confounded by the "
        "banking channel); LUNA kept as the anchor; more crypto-native crises added. "
        "Dropping SVB removes the only high-buffer event, so the old low-vs-high design "
        "is replaced by a pooled test of whether crypto-native stress moves the spread.",
        "",
        "**Selection rule:** crypto-native stress with no simultaneous banking/macro shock "
        "to Treasuries — the principled reason SVB is out and these are in.",
        "",
        "**Method:** first-difference normal model (Δspread ~ ΔVIX + Δln equity) over "
        "(-120,-6); CAR over (0,+h) with the *estimation-window* residual σ; cross-event "
        "CAAR with events as the unit of observation. spread = DTB3 − OIS, in bps.",
        "",
        "## Per-event CAR (bps)",
        "",
        "| Event | Independent? | CAR[0,+5] | CAR[0,+10] | CAR[0,+20] |",
        "|---|---|---:|---:|---:|",
    ]
    for r in results:
        lines.append(f"| {r['event']} | {'yes' if r['indep'] else 'no (LUNA chain)'} "
                     f"| {r['CAR_0_5']:+.1f}{sig(r['p_0_5'])} "
                     f"| {r['CAR_0_10']:+.1f}{sig(r['p_0_10'])} "
                     f"| {r['CAR_0_20']:+.1f}{sig(r['p_0_20'])} |")
    lines += [
        "",
        "## Pooled cross-event CAAR (events = unit of observation)",
        "",
        "| Horizon | mean CAR (bps) | t | p | sign consistency |",
        "|---|---:|---:|---:|---|",
    ]
    for pt in pooled_rows:
        lines.append(f"| +{pt['horizon']}d | {pt['mean_CAR']:+.2f} | {pt['t']:+.2f} "
                     f"| {pt['p']:.3f}{sig(pt['p'])} | {pt['n_pos']}/{pt['n_events']} positive |")
    lines += [
        "",
        f"At +20 days the average crypto-native stress episode is associated with a "
        f"**{p20['mean_CAR']:+.1f} bps** abnormal spread move — i.e. {direction} — "
        f"with p={p20['p']:.3f} across {p20['n_events']} events "
        f"({p20['n_pos']}/{p20['n_events']} share the sign).",
        "",
        "## Honest caveats",
        "- **Independence:** LUNA and Celsius are one 2022 deleveraging chain; their "
        "windows overlap, so the effective number of independent episodes is ~3, not 4. "
        "The independent-only pooled test is reported alongside.",
        "- **Power:** with a handful of events the cross-event test has low power; treat "
        "this as **motivation / suggestive pattern**, not identification — which is exactly "
        "the role Prof. Hur assigned the event study.",
        "- **Overlapping estimation windows:** Celsius's pre-event estimation window "
        "contains the LUNA shock, mildly contaminating its normal model. FTX and BUSD are clean.",
    ]
    (OUT / "event_study_multi_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
