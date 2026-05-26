"""
event_study.py — buffer-conditioned event study around three stablecoin stress episodes.

Events (from config.py):
  LUNA/UST collapse   2022-05-09  (low buffer)
  USDT partial depeg  2022-05-12  (low buffer)
  USDC / SVB failure  2023-03-11  (high buffer)

Method:
  1. Estimate normal-spread model over EST_WINDOW (−120, −6) trading days
  2. Compute abnormal spread (actual − predicted) over EVENT_WINDOW (−5, +20)
  3. Accumulate into CAR; test CAR ≠ 0 via t-test
  4. Compare low-buffer vs high-buffer CARs

Outputs: results/event_study_table.csv, results/event_study_cars.png
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from scipy import stats
from pathlib import Path

from config import DAILY_CSV, RESULTS_DIR, EVENTS, EST_WINDOW, EVENT_WINDOW

Path(RESULTS_DIR).mkdir(exist_ok=True)


def trading_days_offset(daily_idx: pd.DatetimeIndex, anchor: pd.Timestamp, offset: int) -> pd.Timestamp:
    """Return the date that is `offset` trading days from anchor."""
    pos = daily_idx.get_indexer([anchor], method="nearest")[0]
    target = pos + offset
    target = max(0, min(target, len(daily_idx) - 1))
    return daily_idx[target]


def get_window_slice(daily_idx, anchor, lo, hi):
    start = trading_days_offset(daily_idx, anchor, lo)
    end   = trading_days_offset(daily_idx, anchor, hi)
    return slice(start, end)


# First-difference model: model daily CHANGES in spread to eliminate trend contamination.
# This is consistent with standard event study methodology (akin to using returns, not price levels).
# Controls: ΔVIX (in levels since VIX is already a vol measure) and global equity log-returns.
NORMAL_CONTROLS = ["dvix", "dln_row_equity"]


def estimate_normal_model(df: pd.DataFrame, est_slice) -> sm.regression.linear_model.RegressionResultsWrapper:
    """OLS of Δspread on ΔVIX and dln_row_equity over the estimation window."""
    sub = df.loc[est_slice].dropna(subset=["dspread"] + NORMAL_CONTROLS)
    X = sm.add_constant(sub[NORMAL_CONTROLS])
    return sm.OLS(sub["dspread"], X).fit()


def compute_abnormal(df: pd.DataFrame, evt_slice, normal_model) -> pd.Series:
    """AR_t = Δspread_t − predicted Δspread_t; cumsum gives the CAR level above pre-event baseline."""
    sub = df.loc[evt_slice].dropna(subset=["dspread"])
    Xe  = sm.add_constant(sub[NORMAL_CONTROLS], has_constant="add")
    predicted = normal_model.predict(Xe)
    return (sub["dspread"] - predicted).rename("abnormal_spread")


def run_event(df: pd.DataFrame, name: str, meta: dict) -> dict:
    anchor = pd.Timestamp(meta["date"])
    idx    = df.index

    est_sl = get_window_slice(idx, anchor, EST_WINDOW[0], EST_WINDOW[1])
    evt_sl = get_window_slice(idx, anchor, EVENT_WINDOW[0], EVENT_WINDOW[1])

    normal = estimate_normal_model(df, est_sl)
    ar     = compute_abnormal(df, evt_sl, normal)

    car    = ar.cumsum()
    n      = len(ar)
    se     = ar.std() * np.sqrt(n)        # approximate SE of CAR
    t_stat = car.iloc[-1] / se if se > 0 else float("nan")
    p_val  = 2 * stats.t.sf(abs(t_stat), df=n - 1) if not np.isnan(t_stat) else float("nan")

    print(f"\n{name} ({meta['date']}, buffer={meta['buffer']})")
    print(f"  CAR[0,+20]: {car.iloc[-1]:.4f} pp | t={t_stat:.2f} | p={p_val:.3f}")

    return {
        "event":    meta["label"],
        "date":     meta["date"],
        "buffer":   meta["buffer"],
        "car_full": round(car.iloc[-1], 4),
        "t_stat":   round(t_stat, 3),
        "p_value":  round(p_val, 3),
        "sig":      "***" if p_val < 0.01 else "**" if p_val < 0.05 else "*" if p_val < 0.1 else "",
        "car_series": car,
        "ar_series":  ar,
    }


def test_buffer_difference(results: list[dict]):
    """
    Test whether CAR differs between low- and high-buffer events.
    Simple Welch t-test on the [-5, +20] daily AR series.
    """
    low_ars  = pd.concat([r["ar_series"] for r in results if r["buffer"] == "low"])
    high_ars = pd.concat([r["ar_series"] for r in results if r["buffer"] == "high"])
    t_stat, p_val = stats.ttest_ind(low_ars.dropna(), high_ars.dropna(), equal_var=False)
    print(f"\n--- Buffer difference test (low vs high) ---")
    print(f"  Welch t = {t_stat:.3f}, p = {p_val:.3f}")
    return {"t_stat": round(t_stat, 3), "p_value": round(p_val, 3)}


def plot_cars(results: list[dict], outfile: str):
    fig, axes = plt.subplots(1, len(results), figsize=(5 * len(results), 4), sharey=False)
    colors = {"low": "#d62728", "high": "#1f77b4"}

    for ax, res in zip(axes, results):
        car = res["car_series"].reset_index(drop=True)
        car.index -= (car.index.get_loc(car.index[5]) if len(car) > 5 else 0)  # center at τ=0 approx
        car.index = range(-5, -5 + len(car))
        ax.plot(car.index, car.values, color=colors[res["buffer"]], linewidth=1.8)
        ax.axvline(0, color="black", linestyle="--", linewidth=0.8)
        ax.axhline(0, color="black", linewidth=0.5)
        ax.set_title(f"{res['event']}\n(buffer: {res['buffer']})", fontsize=9)
        ax.set_xlabel("Trading days relative to event")
        ax.set_ylabel("CAR (pp)")
        sig = res["sig"]
        ax.annotate(f"CAR={res['car_full']:.3f} {sig}", xy=(0.05, 0.9),
                    xycoords="axes fraction", fontsize=8)

    plt.suptitle("Buffer-Conditioned Cumulative Abnormal OIS-Treasury Spread", fontsize=10)
    plt.tight_layout()
    plt.savefig(outfile, dpi=150, bbox_inches="tight")
    print(f"  Plot saved to {outfile}")


def main():
    df = pd.read_csv(DAILY_CSV, index_col=0, parse_dates=True)
    # First-difference variables for the normal model
    df["dspread"] = df["spread"].diff()
    df["dvix"]    = df["vix"].diff()
    print(f"Daily panel: {len(df)} obs ({df.index[0].date()} – {df.index[-1].date()})")

    results = [run_event(df, name, meta) for name, meta in EVENTS.items()]

    diff = test_buffer_difference(results)

    # Save table
    table_rows = [{k: v for k, v in r.items() if k not in ("car_series", "ar_series")} for r in results]
    table_rows.append({"event": "Low vs High (diff test)", "t_stat": diff["t_stat"], "p_value": diff["p_value"]})
    table = pd.DataFrame(table_rows)
    table.to_csv(f"{RESULTS_DIR}/event_study_table.csv", index=False)
    print(f"\n  Table saved to {RESULTS_DIR}/event_study_table.csv")
    print(table.to_string(index=False))

    plot_cars(results, f"{RESULTS_DIR}/event_study_cars.png")


if __name__ == "__main__":
    main()
