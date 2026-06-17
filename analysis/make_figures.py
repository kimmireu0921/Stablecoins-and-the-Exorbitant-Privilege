"""
make_figures.py — generate all publication figures for 0621_Final_Draft_for_Submission.

Figures produced:
  Figure 1: Key variables time-series overview (supply + spread)
  Figure 2: USDT liquid buffer L decline with threshold shading
  Figure 3: Threshold regime scatter (ΔlnS vs ΔSpread, colored by buffer regime)
  Figure 4: Event-study CAR paths for three stress episodes

All figures saved to results/fig_paper_*.png at 300 DPI.
"""

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker
import statsmodels.api as sm
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import DAILY_CSV, RESULTS_DIR, EVENTS, EST_WINDOW, EVENT_WINDOW

RESULTS = Path(RESULTS_DIR)
RESULTS.mkdir(exist_ok=True)

# ── shared style ──────────────────────────────────────────────────────────────
plt.rcParams.update({
    "font.family":      "serif",
    "font.size":        10,
    "axes.titlesize":   11,
    "axes.labelsize":   10,
    "legend.fontsize":  9,
    "xtick.labelsize":  9,
    "ytick.labelsize":  9,
    "axes.spines.top":  False,
    "axes.spines.right":False,
    "figure.dpi":       150,
})

# ── load data ─────────────────────────────────────────────────────────────────
panel = pd.read_csv("data/panel_long.csv", parse_dates=["date"])
fred  = pd.read_csv("data/fred_raw.csv",   parse_dates=["observation_date"])
dl    = pd.read_csv("data/defillama_raw.csv", parse_dates=["date"])

usdt  = panel[panel.issuer == "USDT"].sort_values("date").reset_index(drop=True)
usdc  = panel[panel.issuer == "USDC"].sort_values("date").reset_index(drop=True)

# monthly spread (from panel; already the within-month mean in % points)
monthly_spread = usdt[["date", "spread"]].set_index("date")

# daily spread
fred = fred.dropna(subset=["DGS3MO", "SOFR_daily"])
fred["spread_daily"] = fred["DGS3MO"] - fred["SOFR_daily"]
fred = fred.set_index("observation_date").sort_index()
daily_spread = fred["spread_daily"]

# DeFiLlama monthly supply (billions, month-end)
dl_monthly = (
    dl.set_index("date")
      .resample("ME")["USDT", "USDC"]
      .last()
      / 1e9
)
dl_monthly = dl_monthly.loc["2022-01-01":"2026-03-31"]

# ── FIGURE 1: Key variables overview ─────────────────────────────────────────
fig, axes = plt.subplots(2, 1, figsize=(7.5, 5.5), sharex=True,
                          gridspec_kw={"height_ratios": [1.3, 1]})

# Panel A — supply
ax = axes[0]
ax.fill_between(dl_monthly.index, dl_monthly["USDT"], alpha=0.18, color="#1f77b4")
ax.fill_between(dl_monthly.index, dl_monthly["USDC"], alpha=0.22, color="#ff7f0e")
ax.plot(dl_monthly.index, dl_monthly["USDT"], color="#1f77b4", lw=1.8, label="USDT")
ax.plot(dl_monthly.index, dl_monthly["USDC"], color="#ff7f0e", lw=1.8, label="USDC")
ax.set_ylabel("Circulating Supply (USD bn)")
ax.set_title("Panel A — USDT and USDC Circulating Supply (DeFiLlama)")
ax.legend(loc="upper left", frameon=False)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}bn"))

# shade key events
event_dates = {
    "LUNA\nCollapse": pd.Timestamp("2022-05-09"),
    "USDT\nDepeg":    pd.Timestamp("2022-05-12"),
    "USDC\n/SVB":     pd.Timestamp("2023-03-11"),
}
for label, dt in event_dates.items():
    ax.axvline(dt, color="grey", lw=0.8, ls="--", alpha=0.7)

# Panel B — spread
ax2 = axes[1]
ax2.axhline(0, color="black", lw=0.6, alpha=0.4)
ax2.fill_between(monthly_spread.index, monthly_spread["spread"],
                  where=monthly_spread["spread"] > 0,
                  alpha=0.25, color="#2ca02c", label="Spread > 0")
ax2.fill_between(monthly_spread.index, monthly_spread["spread"],
                  where=monthly_spread["spread"] < 0,
                  alpha=0.25, color="#d62728", label="Spread < 0")
ax2.plot(monthly_spread.index, monthly_spread["spread"],
          color="black", lw=1.5)
ax2.set_ylabel("Spread (pp)")
ax2.set_title("Panel B — OIS–Treasury Spread (DGS3MO − Overnight SOFR, monthly mean)")
ax2.legend(loc="upper right", frameon=False)

for label, dt in event_dates.items():
    ax2.axvline(dt, color="grey", lw=0.8, ls="--", alpha=0.7)

fig.autofmt_xdate()
fig.tight_layout(h_pad=1.0)
out1 = RESULTS / "fig_paper_1_timeseries.png"
fig.savefig(out1, dpi=300, bbox_inches="tight")
plt.close(fig)
print(f"Saved {out1}")


# ── FIGURE 2: USDT liquid buffer decline ─────────────────────────────────────
fig, ax = plt.subplots(figsize=(7.5, 3.8))

L = usdt.set_index("date")["liq_buffer"] * 100  # convert to %

# BDO attestation quarter-end points (the directly verified values)
bdo_dates = pd.to_datetime([
    "2024-03-31","2024-06-30","2024-12-31",
    "2025-03-31","2025-06-30","2025-09-30","2025-12-31","2026-03-31",
])
bdo_L = [6.10, 5.75, 4.84, 4.43, 4.06, 3.69, 2.99, 2.63]

# threshold shading
ax.axhspan(0, 4, color="#d62728", alpha=0.10, zorder=0)
ax.axhspan(4, 6, color="#ff7f0e", alpha=0.08, zorder=0)

ax.axhline(4, color="#d62728", lw=1.0, ls="--", alpha=0.7)
ax.axhline(6, color="#ff7f0e", lw=1.0, ls="--", alpha=0.6)

ax.plot(L.index, L.values, color="#1f77b4", lw=2.0, label="USDT liquid buffer L (interpolated)")
ax.scatter(bdo_dates, bdo_L, color="#1f77b4", s=40, zorder=5,
           label="BDO-attested quarter-end values", marker="o")

# labels on shading
ax.text(pd.Timestamp("2022-06-01"), 2.0, "L < 4%  (low-buffer regime)",
        color="#d62728", fontsize=8.5, va="center")
ax.text(pd.Timestamp("2022-06-01"), 5.0, "4% ≤ L < 6%  (moderate-buffer)",
        color="#ff7f0e", fontsize=8.5, va="center")

ax.set_ylabel("Liquid Buffer L (%)")
ax.set_title("Figure 2 — USDT Liquid Buffer Decline (Cash + MMF or Term Repos <90d)\n"
             "as a Share of Outstanding Supply (BDO ISAE 3000R Attestations)")
ax.legend(loc="upper right", frameon=False)
ax.set_ylim(0, L.max() * 1.08)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:.0f}%"))

fig.autofmt_xdate()
fig.tight_layout()
out2 = RESULTS / "fig_paper_2_buffer.png"
fig.savefig(out2, dpi=300, bbox_inches="tight")
plt.close(fig)
print(f"Saved {out2}")


# ── FIGURE 3: Threshold regime scatter ───────────────────────────────────────
# Compute ΔSpread and ΔlnS at the panel level (all issuers)
df_all = panel.sort_values(["issuer", "date"]).copy()
df_all["dspread"]    = df_all.groupby("issuer")["spread"].diff()
df_all["dln_supply"] = df_all["dln_supply"]   # already monthly log-diff of DeFiLlama supply
df_thresh = df_all.dropna(subset=["dspread"]).copy()

L_vals = df_thresh["liq_buffer"] * 100
regime = pd.cut(L_vals,
                bins=[-np.inf, 4, 6, np.inf],
                labels=["L < 4%", "4% ≤ L < 6%", "L ≥ 6%"])

colors  = {"L < 4%": "#d62728", "4% ≤ L < 6%": "#ff7f0e", "L ≥ 6%": "#1f77b4"}
markers = {"L < 4%": "D",        "4% ≤ L < 6%": "^",         "L ≥ 6%": "o"}
labels  = {"L < 4%": f"L < 4%  (n={sum(L_vals<4)})",
           "4% ≤ L < 6%": f"4% ≤ L < 6%  (n={sum((L_vals>=4)&(L_vals<6))})",
           "L ≥ 6%": f"L ≥ 6%  (n={sum(L_vals>=6)})"}

fig, ax = plt.subplots(figsize=(7.0, 5.0))

for reg, grp in df_thresh.groupby(regime, observed=True):
    ax.scatter(grp["dln_supply"] * 100,  # convert to %
               grp["dspread"],
               color=colors[reg], marker=markers[reg],
               alpha=0.75, s=35, label=labels[reg], zorder=3)

# fitted lines for low-buffer vs. high-buffer
for reg, mask, c in [
    ("L < 4%",    L_vals < 4,   "#d62728"),
    ("L ≥ 6%",   L_vals >= 6,  "#1f77b4"),
]:
    sub = df_thresh[mask.values]
    if len(sub) > 3:
        x = sub["dln_supply"].values * 100
        y = sub["dspread"].values
        z = np.polyfit(x, y, 1)
        xr = np.linspace(x.min(), x.max(), 50)
        ax.plot(xr, np.polyval(z, xr), color=c, lw=1.8, ls="-", alpha=0.85, zorder=4)

ax.axhline(0, color="black", lw=0.6, alpha=0.4)
ax.axvline(0, color="black", lw=0.6, alpha=0.4)
ax.set_xlabel("Monthly Supply Growth ΔlnS (%)")
ax.set_ylabel("Change in OIS–Treasury Spread ΔSpread (pp)")
ax.set_title("Figure 3 — Threshold Regime: Supply Growth vs. Spread Change\n"
             "by Liquid Buffer Level (Issuer-Month Panel, N = 100)")
ax.legend(loc="upper right", frameon=False)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:.1f}%"))

fig.tight_layout()
out3 = RESULTS / "fig_paper_3_threshold_scatter.png"
fig.savefig(out3, dpi=300, bbox_inches="tight")
plt.close(fig)
print(f"Saved {out3}")


# ── FIGURE 4: Event study CAR paths ──────────────────────────────────────────
NORMAL_CONTROLS = ["dvix", "dln_row_equity"]

def trading_days_offset(idx, anchor, offset):
    pos = idx.get_indexer([anchor], method="nearest")[0]
    t   = max(0, min(pos + offset, len(idx) - 1))
    return idx[t]

def get_window_slice(idx, anchor, lo, hi):
    return slice(trading_days_offset(idx, anchor, lo),
                 trading_days_offset(idx, anchor, hi))

# Use the pre-built daily panel which already has spread, vix, dln_row_equity
daily_raw = pd.read_csv(DAILY_CSV, parse_dates=["date"])
daily_raw = daily_raw.set_index("date").sort_index()
daily_raw["dspread"] = daily_raw["spread"].diff()
daily_raw["dvix"]    = daily_raw["vix"].diff()
df_daily = daily_raw.dropna(subset=["dspread", "dvix"])

events_cfg = {
    # Issuer-specific events only. LUNA/UST dropped (different protocol);
    # USDC/SVB dropped (external bank failure, not Circle's own problem).
    "USDT Partial\nDepeg (May 2022)":    {"date": "2022-05-12", "buffer": "High (~16%)", "color": "#d62728",
                                           "note": "USDT peg broke to $0.945;\n$10bn+ redemptions in 3 days"},
    "USDT FTX-Era\nStress (Nov 2022)":   {"date": "2022-11-09", "buffer": "High (~19%)", "color": "#ff7f0e",
                                           "note": "FTX collapse raised concerns\nabout Tether's Alameda exposure"},
}

fig, axes = plt.subplots(1, 2, figsize=(9, 4.5), sharey=False)

car_summary = {}
for ax, (name, meta) in zip(axes, events_cfg.items()):
    anchor = pd.Timestamp(meta["date"])
    idx    = df_daily.index

    est_sl = get_window_slice(idx, anchor, EST_WINDOW[0], EST_WINDOW[1])
    evt_sl = get_window_slice(idx, anchor, EVENT_WINDOW[0], EVENT_WINDOW[1])

    sub_est = df_daily.loc[est_sl].dropna(subset=["dspread"] + NORMAL_CONTROLS)
    if len(sub_est) < 10:
        car_summary[name] = {"car": np.nan, "se": np.nan}
        continue

    X_est   = sm.add_constant(sub_est[NORMAL_CONTROLS])
    model   = sm.OLS(sub_est["dspread"], X_est).fit()
    sigma   = model.resid.std()

    sub_evt = df_daily.loc[evt_sl].dropna(subset=["dspread"])
    if len(sub_evt) < 3:
        car_summary[name] = {"car": np.nan, "se": np.nan}
        continue

    X_evt   = sm.add_constant(sub_evt[NORMAL_CONTROLS], has_constant="add")
    pred    = model.predict(X_evt)
    ar      = sub_evt["dspread"].values - pred.values
    car     = np.cumsum(ar)
    n       = len(ar)
    ci      = 1.96 * sigma * np.sqrt(np.arange(1, n + 1))

    td = np.arange(EVENT_WINDOW[0], EVENT_WINDOW[0] + n)

    ax.axhline(0, color="black", lw=0.7, alpha=0.5)
    ax.axvline(0, color="grey", lw=0.8, ls="--", alpha=0.6)
    ax.fill_between(td, car - ci, car + ci, alpha=0.18, color=meta["color"])
    ax.plot(td, car, color=meta["color"], lw=2.0)

    ax.set_title(f"{name}\nBuffer at event: {meta['buffer']}", fontsize=9)
    ax.set_xlabel("Trading days relative to event", fontsize=9)
    if ax is axes[0]:
        ax.set_ylabel("Cumulative Abnormal Spread (pp)")
    ax.tick_params(labelsize=8)
    ax.text(0.97, 0.97, meta["note"], transform=ax.transAxes,
            fontsize=7.5, va="top", ha="right",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.75, edgecolor="lightgrey"))

    car_summary[name] = {"car": car[-1] * 100, "se": ci[-1] * 100}

fig.suptitle("Figure 4 — Issuer-Specific Event Study: Cumulative Abnormal Spread\n"
             "Normal model: ΔSpread = f(ΔVIX, ΔlnN*), pre-event window [−120, −6] trading days\n"
             "Events limited to USDT issuer-caused stress episodes; LUNA/UST and USDC/SVB excluded",
             fontsize=9.5)
fig.tight_layout(rect=[0, 0, 1, 0.88])
out4 = RESULTS / "fig_paper_4_event_study.png"
fig.savefig(out4, dpi=300, bbox_inches="tight")
plt.close(fig)
print(f"Saved {out4}")

print("\nAll figures saved.")
print("Files:")
for p in [out1, out2, out3, out4]:
    print(f"  {p}")
