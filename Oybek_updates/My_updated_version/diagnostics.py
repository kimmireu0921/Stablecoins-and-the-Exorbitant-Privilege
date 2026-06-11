"""
diagnostics.py — pre-writing checks: unit roots, optimal NW lags, VIF, robustness re-run.
Outputs: results/diagnostics.txt, results/fig_timeseries.png, results/fig_buffer.png
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.stattools import durbin_watson
from pathlib import Path

from config import MONTHLY_CSV, DAILY_CSV, RESULTS_DIR

Path(RESULTS_DIR).mkdir(exist_ok=True)
out_lines = []

def log(msg=""):
    print(msg)
    out_lines.append(msg)


# ── Load ────────────────────────────────────────────────────────────────────
df = pd.read_csv(MONTHLY_CSV, index_col=0, parse_dates=True)
df = df.dropna(subset=["spread", "dln_supply", "theta", "liq_buffer", "vix", "dln_row_equity"])
log(f"Sample: {df.index[0].date()} – {df.index[-1].date()}  (N={len(df)})")


# ── 1. ADF Unit Root Tests ──────────────────────────────────────────────────
log("\n" + "="*60)
log("1. ADF UNIT ROOT TESTS  (H0: unit root / non-stationary)")
log("="*60)

series_to_test = {
    "spread":         df["spread"],
    "dln_supply":     df["dln_supply"],
    "theta":          df["theta"],
    "liq_buffer":     df["liq_buffer"],
    "vix":            df["vix"],
    "dln_row_equity": df["dln_row_equity"],
    "buffer_ratio":   df["buffer_ratio"],
}

for name, s in series_to_test.items():
    s_clean = s.dropna()
    result = adfuller(s_clean, autolag="AIC")
    stat, pval, lags = result[0], result[1], result[2]
    conclusion = "STATIONARY ✓" if pval < 0.05 else "NON-STATIONARY ✗ (consider first-diff)"
    log(f"  {name:<20} ADF={stat:7.3f}  p={pval:.3f}  lags={lags}  → {conclusion}")


# ── 2. Optimal Newey-West Lags ──────────────────────────────────────────────
log("\n" + "="*60)
log("2. NEWEY-WEST LAG SELECTION  (rule of thumb: floor(4*(N/100)^(2/9)))")
log("="*60)

n = len(df)
nw_rule = int(np.floor(4 * (n / 100) ** (2/9)))
log(f"  N={n}  →  recommended NW lags = {nw_rule}")

y  = df["spread"]
X  = sm.add_constant(df[["dln_supply", "velocity", "theta", "liq_buffer", "L_x_dlns", "vix", "dln_row_equity"]])

log(f"\n  Comparing β₁ (ΔlnS) and β₄ (L×ΔlnS) across NW lag choices:")
log(f"  {'Lags':<6} {'β₁(ΔlnS)':<14} {'p':<8} {'β₄(L×ΔlnS)':<15} {'p'}")
for lags in [1, 2, 3, nw_rule]:
    res = sm.OLS(y, X, missing="drop").fit(cov_type="HAC", cov_kwds={"maxlags": lags})
    b1, p1 = res.params["dln_supply"], res.pvalues["dln_supply"]
    b4, p4 = res.params["L_x_dlns"],  res.pvalues["L_x_dlns"]
    log(f"  {lags:<6} {b1:<14.4f} {p1:<8.3f} {b4:<15.4f} {p4:.3f}")


# ── 3. VIF ──────────────────────────────────────────────────────────────────
log("\n" + "="*60)
log("3. VARIANCE INFLATION FACTORS  (VIF > 10 = problematic)")
log("="*60)

X_vif = df[["dln_supply", "velocity", "theta", "liq_buffer", "L_x_dlns", "vix", "dln_row_equity"]].dropna()
X_vif_arr = X_vif.values
for i, col in enumerate(X_vif.columns):
    vif = variance_inflation_factor(X_vif_arr, i)
    flag = " ← HIGH" if vif > 10 else ""
    log(f"  {col:<22} VIF = {vif:.2f}{flag}")


# ── 4. Re-run main regression with optimal NW lags ──────────────────────────
log("\n" + "="*60)
log(f"4. MAIN REGRESSION  (Newey-West, {nw_rule} lags)")
log("="*60)

res_main = sm.OLS(y, X, missing="drop").fit(cov_type="HAC", cov_kwds={"maxlags": nw_rule})
log(str(res_main.summary()))
log(f"  Durbin-Watson: {durbin_watson(res_main.resid):.3f}")


# ── 5. Sensitivity: post-2023 sub-sample (later attestation coverage) ────────
log("\n" + "="*60)
log("5. ROBUSTNESS: post-2023 sub-sample (N ≈ 27 months)")
log("   Tests whether results hold in the period with broadest attestation coverage.")
log("="*60)

df_sub = df.loc["2023-01-01":]
y_sub  = df_sub["spread"]
X_sub  = sm.add_constant(df_sub[["dln_supply", "velocity", "theta",
                                   "liq_buffer", "L_x_dlns", "vix", "dln_row_equity"]])
res_sub = sm.OLS(y_sub, X_sub, missing="drop").fit(
    cov_type="HAC", cov_kwds={"maxlags": 1})
log(f"  N={len(df_sub)}  β₁={res_sub.params['dln_supply']:.4f} (p={res_sub.pvalues['dln_supply']:.3f})"
    f"  β₄={res_sub.params['L_x_dlns']:.4f} (p={res_sub.pvalues['L_x_dlns']:.3f})")
robust = res_sub.pvalues["dln_supply"] < 0.1
log(f"  Conclusion: β₁ {'robust' if robust else 'not robust'} in post-2023 subsample.")


# ── Save diagnostics text ────────────────────────────────────────────────────
with open(f"{RESULTS_DIR}/diagnostics.txt", "w") as f:
    f.write("\n".join(out_lines))
print(f"\n  Saved to {RESULTS_DIR}/diagnostics.txt")


# ── 6. Figure 1: Time series overview ───────────────────────────────────────
daily = pd.read_csv(DAILY_CSV, index_col=0, parse_dates=True)
monthly = pd.read_csv(MONTHLY_CSV, index_col=0, parse_dates=True)

fig = plt.figure(figsize=(12, 8))
gs  = gridspec.GridSpec(3, 1, hspace=0.45)

# Panel A: OIS-Treasury spread
ax1 = fig.add_subplot(gs[0])
ax1.plot(daily.index, daily["spread"], color="#1f77b4", linewidth=0.8, alpha=0.9)
ax1.axhline(0, color="black", linewidth=0.5, linestyle="--")
for evt, meta in [("LUNA/UST", "2022-05-09"), ("USDT depeg", "2022-05-12"), ("USDC/SVB", "2023-03-11")]:
    ax1.axvline(pd.Timestamp(meta), color="#d62728", linewidth=0.8, linestyle=":")
ax1.set_ylabel("Spread (pp)", fontsize=9)
ax1.set_title("A. OIS–Treasury Spread (DTB3 − SOFR90DAYAVG)", fontsize=9, loc="left")
ax1.tick_params(labelsize=8)

# Panel B: Stablecoin total supply
ax2 = fig.add_subplot(gs[1])
ax2.fill_between(daily.index, daily["supply_USDT"], label="USDT", color="#ff7f0e", alpha=0.7)
ax2.fill_between(daily.index, daily["supply_USDT"] + daily["supply_USDC"],
                 daily["supply_USDT"], label="USDC", color="#2ca02c", alpha=0.7)
ax2.set_ylabel("Supply (USD bn)", fontsize=9)
ax2.set_title("B. USDT + USDC Circulating Supply", fontsize=9, loc="left")
ax2.legend(fontsize=8, loc="upper left")
ax2.tick_params(labelsize=8)

# Panel C: Liquid buffer (L)
ax3 = fig.add_subplot(gs[2])
buf = monthly["liq_buffer"].dropna()
ax3.plot(buf.index, buf.values, color="#9467bd", linewidth=1.5)
ax3.axhline(0, color="black", linewidth=0.5, linestyle="--")
ax3.axhline(0.1301, color="#d62728", linewidth=0.8, linestyle="--", label="q* = 0.1301")
ax3.fill_between(buf.index, buf.values, 0.1301,
                 where=(buf.values <= 0.1301), color="#d62728", alpha=0.15, label="Below threshold")
ax3.set_ylabel("Liquid buffer L", fontsize=9)
ax3.set_title("C. Aggregate Liquid Buffer L = Cash Reserves / Supply (USDT + USDC)", fontsize=9, loc="left")
ax3.legend(fontsize=8)
ax3.tick_params(labelsize=8)

plt.suptitle("Stablecoins and the OIS–Treasury Spread: Key Variables\n"
             "Jan 2022 – Mar 2026  |  Vertical lines: stress events", fontsize=10)

fig.savefig(f"{RESULTS_DIR}/fig_timeseries.png", dpi=180, bbox_inches="tight")
print(f"  Saved {RESULTS_DIR}/fig_timeseries.png")


# ── 7. Summary statistics table ─────────────────────────────────────────────
vars_for_table = {
    "spread":         "OIS–Treasury spread (pp)",
    "dln_supply":     "ΔlnS  (monthly log-change in stablecoin supply)",
    "theta":          "θ  (Treasury Exposure = T-bill holdings / supply)",
    "liq_buffer":     "L  (Liquid Buffer = cash reserves / supply)",
    "velocity":       "V  (7-day rolling std of daily supply changes)",
    "vix":            "VIX",
    "dln_row_equity": "ΔlnN*  (RoW equity log-change)",
}
stats_rows = []
for col, label in vars_for_table.items():
    s = df[col].dropna()
    stats_rows.append({
        "Variable": label,
        "N": len(s),
        "Mean": round(s.mean(), 4),
        "Std": round(s.std(), 4),
        "Min": round(s.min(), 4),
        "p25": round(s.quantile(0.25), 4),
        "Median": round(s.median(), 4),
        "p75": round(s.quantile(0.75), 4),
        "Max": round(s.max(), 4),
    })
stats_df = pd.DataFrame(stats_rows)
stats_df.to_csv(f"{RESULTS_DIR}/summary_stats.csv", index=False)
print(f"  Saved {RESULTS_DIR}/summary_stats.csv")
print("\n" + stats_df.to_string(index=False))
