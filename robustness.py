"""
robustness.py — addresses the three diagnostic issues before paper writing:
  1. Mean-centering to reduce interaction-term VIF
  2. Engle-Granger cointegration test + first-differenced regression
  3. Re-runs main spec with 3 NW lags (rule-of-thumb N≈50)

Uses the decomposed buffer variables: theta (Treasury Exposure) and
liq_buffer (Liquid Buffer), consistent with the main regression spec.

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
df = df.dropna(subset=["spread", "dln_supply", "theta", "liq_buffer", "vix", "dln_row_equity"])
NW_LAGS = 3
log(f"N={len(df)}  NW lags={NW_LAGS}")


# ── 1. Mean-centering (fixes VIF on interaction term) ───────────────────────
log("\n" + "="*60)
log("1. MEAN-CENTERED SPECIFICATION  (reduces interaction-term VIF)")
log("   Main spec: theta, liq_buffer, L × ΔlnS")
log("="*60)

df["dln_supply_c"]  = df["dln_supply"]  - df["dln_supply"].mean()
df["theta_c"]       = df["theta"]       - df["theta"].mean()
df["liq_buffer_c"]  = df["liq_buffer"]  - df["liq_buffer"].mean()
df["L_x_dlns_c"]    = df["dln_supply_c"] * df["liq_buffer_c"]

X_c = sm.add_constant(df[["dln_supply_c", "velocity", "theta_c",
                            "liq_buffer_c", "L_x_dlns_c", "vix", "dln_row_equity"]])
y   = df["spread"]

res_c = sm.OLS(y, X_c, missing="drop").fit(
    cov_type="HAC", cov_kwds={"maxlags": NW_LAGS})
log(str(res_c.summary()))

# VIF after centering
X_vif = df[["dln_supply_c", "velocity", "theta_c",
            "liq_buffer_c", "L_x_dlns_c", "vix", "dln_row_equity"]].dropna()
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
log("   If spread and regressors are both I(1) but cointegrated,")
log("   OLS super-consistently estimates the long-run relationship.\n")

pairs = [
    ("spread", "dln_supply"),
    ("spread", "theta"),
    ("spread", "liq_buffer"),
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
log("   ΔSpread_t = α + β1·Δ²lnS_t + β2·Δθ_t + β3·ΔL_t")
log("             + β4·(ΔL_t × Δ²lnS_t) + β5·ΔV_t + β6·ΔVIX_t + β7·ΔlnN*_t + ε_t\n")

dfd = df[["spread", "dln_supply", "theta", "liq_buffer", "velocity",
          "vix", "dln_row_equity"]].diff().dropna()
dfd["L_x_dlns_fd"] = dfd["dln_supply"] * dfd["liq_buffer"]

y_fd = dfd["spread"]
X_fd = sm.add_constant(dfd[["dln_supply", "velocity", "theta",
                              "liq_buffer", "L_x_dlns_fd", "vix", "dln_row_equity"]])
res_fd = sm.OLS(y_fd, X_fd, missing="drop").fit(
    cov_type="HAC", cov_kwds={"maxlags": NW_LAGS})
log(str(res_fd.summary()))

b1_fd = res_fd.params["dln_supply"];   p1_fd = res_fd.pvalues["dln_supply"]
b4_fd = res_fd.params["L_x_dlns_fd"]; p4_fd = res_fd.pvalues["L_x_dlns_fd"]
robust = (p1_fd < 0.1) or (p4_fd < 0.1)
log(f"\n  Summary: β₁={b1_fd:.4f} (p={p1_fd:.3f})  β₄={b4_fd:.4f} (p={p4_fd:.3f})")
log(f"  Key results {'survive' if robust else 'do not survive'} first-differencing.")


# ── 4. Summary table ────────────────────────────────────────────────────────
log("\n" + "="*60)
log("4. COEFFICIENT COMPARISON ACROSS SPECIFICATIONS")
log("="*60)
log(f"  {'Spec':<35} {'β₁(ΔlnS)':<12} {'p':<8} {'β₄(L×ΔlnS)':<14} {'p':<8} R²")

specs = [
    ("Mean-centered (NW=3)",        res_c,  "dln_supply_c",  "L_x_dlns_c"),
    ("First-differenced (NW=3)",    res_fd, "dln_supply",    "L_x_dlns_fd"),
]
for label, res, b1k, b4k in specs:
    b1 = res.params.get(b1k, np.nan); p1 = res.pvalues.get(b1k, np.nan)
    b4 = res.params.get(b4k, np.nan); p4 = res.pvalues.get(b4k, np.nan)
    r2 = res.rsquared
    log(f"  {label:<35} {b1:<12.4f} {p1:<8.3f} {b4:<14.4f} {p4:<8.3f} {r2:.3f}")


# ── Save ─────────────────────────────────────────────────────────────────────
with open(f"{RESULTS_DIR}/robustness.txt", "w") as f:
    f.write("\n".join(out_lines))
log(f"\n  Saved to {RESULTS_DIR}/robustness.txt")
