"""
robustness.py — addresses the three diagnostic issues before paper writing:
  1. Mean-centering to reduce interaction-term VIF
  2. Engle-Granger cointegration test + first-differenced regression
  3. Re-runs main spec with 3 NW lags (rule-of-thumb N=75)

Outputs: results/robustness.txt
"""

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.stattools import coint, adfuller
from statsmodels.stats.outliers_influence import variance_inflation_factor
from pathlib import Path

from config import MONTHLY_CSV, RESULTS_DIR

Path(RESULTS_DIR).mkdir(exist_ok=True)
out_lines = []

def log(msg=""):
    print(msg)
    out_lines.append(msg)


df = pd.read_csv(MONTHLY_CSV, index_col=0, parse_dates=True)
df = df.dropna(subset=["spread", "dln_supply", "buffer_ratio", "vix", "dln_row_equity"])
NW_LAGS = 3
log(f"N={len(df)}  NW lags={NW_LAGS}")


# ── 1. Mean-centering (fixes VIF) ───────────────────────────────────────────
log("\n" + "="*60)
log("1. MEAN-CENTERED SPECIFICATION  (reduces interaction-term VIF)")
log("="*60)

df["dln_supply_c"]   = df["dln_supply"]   - df["dln_supply"].mean()
df["buffer_ratio_c"] = df["buffer_ratio"] - df["buffer_ratio"].mean()
df["buf_x_dlns_c"]   = df["dln_supply_c"] * df["buffer_ratio_c"]

X_c = sm.add_constant(df[["dln_supply_c", "velocity", "buffer_ratio_c",
                            "buf_x_dlns_c", "vix", "dln_row_equity"]])
y   = df["spread"]

res_c = sm.OLS(y, X_c, missing="drop").fit(
    cov_type="HAC", cov_kwds={"maxlags": NW_LAGS})
log(str(res_c.summary()))

# VIF after centering
X_vif = df[["dln_supply_c", "velocity", "buffer_ratio_c",
            "buf_x_dlns_c", "vix", "dln_row_equity"]].dropna()
log("\n  VIF after mean-centering:")
for i, col in enumerate(X_vif.columns):
    vif = variance_inflation_factor(X_vif.values, i)
    flag = " ← still HIGH" if vif > 10 else " ✓"
    log(f"    {col:<25} VIF = {vif:.2f}{flag}")


# ── 2. Cointegration test (Engle-Granger) ───────────────────────────────────
log("\n" + "="*60)
log("2. ENGLE-GRANGER COINTEGRATION TEST")
log("   H0: no cointegration (i.e., regression IS spurious)")
log("="*60)
log("   If spread and dln_supply are both I(1) but cointegrated,")
log("   OLS super-consistently estimates the long-run relationship.\n")

pairs = [
    ("spread", "dln_supply"),
    ("spread", "buffer_ratio"),
]
for y_name, x_name in pairs:
    s1 = df[y_name].dropna()
    s2 = df[x_name].dropna()
    idx = s1.index.intersection(s2.index)
    stat, pval, _ = coint(s1[idx], s2[idx])
    conclusion = "COINTEGRATED ✓  (OLS valid)" if pval < 0.05 else "NOT cointegrated ✗"
    log(f"  {y_name} ~ {x_name}:  t={stat:.3f}  p={pval:.3f}  → {conclusion}")


# ── 3. First-differenced regression (robustness for non-stationarity) ────────
log("\n" + "="*60)
log("3. FIRST-DIFFERENCED REGRESSION  (robustness for I(1) variables)")
log("="*60)
log("   ΔSpread_t = α + β1·Δ²lnS_t + β2·ΔB_t + β3·(ΔB_t × Δ²lnS_t)")
log("             + β4·ΔV_t + β5·ΔVIX_t + β6·ΔlnN*_t + ε_t\n")

dfd = df[["spread", "dln_supply", "buffer_ratio", "velocity",
          "vix", "dln_row_equity"]].diff().dropna()
dfd["buf_x_dlns_fd"] = dfd["dln_supply"] * dfd["buffer_ratio"]

y_fd = dfd["spread"]
X_fd = sm.add_constant(dfd[["dln_supply", "velocity", "buffer_ratio",
                              "buf_x_dlns_fd", "vix", "dln_row_equity"]])
res_fd = sm.OLS(y_fd, X_fd, missing="drop").fit(
    cov_type="HAC", cov_kwds={"maxlags": NW_LAGS})
log(str(res_fd.summary()))

b1_fd = res_fd.params["dln_supply"];    p1_fd = res_fd.pvalues["dln_supply"]
b3_fd = res_fd.params["buf_x_dlns_fd"]; p3_fd = res_fd.pvalues["buf_x_dlns_fd"]
robust = (p1_fd < 0.1) or (p3_fd < 0.1)
log(f"\n  Summary: β₁={b1_fd:.4f} (p={p1_fd:.3f})  β₃={b3_fd:.4f} (p={p3_fd:.3f})")
log(f"  Key results {'survive' if robust else 'do not survive'} first-differencing.")


# ── 4. Summary table ────────────────────────────────────────────────────────
log("\n" + "="*60)
log("4. COEFFICIENT COMPARISON ACROSS SPECIFICATIONS")
log("="*60)
log(f"  {'Spec':<35} {'β₁(ΔlnS)':<12} {'p':<8} {'β₃(B×ΔlnS)':<14} {'p':<8} R²")

specs = [
    ("Main (NW=3 lags)",           "dln_supply",   "buf_x_dlns",    res_c,  "dln_supply_c", "buf_x_dlns_c"),
    ("First-differenced (NW=3)",   "dln_supply",   "buf_x_dlns_fd", res_fd, "dln_supply",   "buf_x_dlns_fd"),
]
for label, _, _, res, b1k, b3k in specs:
    b1 = res.params.get(b1k, np.nan); p1 = res.pvalues.get(b1k, np.nan)
    b3 = res.params.get(b3k, np.nan); p3 = res.pvalues.get(b3k, np.nan)
    r2 = res.rsquared
    log(f"  {label:<35} {b1:<12.4f} {p1:<8.3f} {b3:<14.4f} {p3:<8.3f} {r2:.3f}")


# ── Save ─────────────────────────────────────────────────────────────────────
with open(f"{RESULTS_DIR}/robustness.txt", "w") as f:
    f.write("\n".join(out_lines))
log(f"\n  Saved to {RESULTS_DIR}/robustness.txt")
