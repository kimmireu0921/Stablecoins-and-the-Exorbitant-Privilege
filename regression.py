"""
regression.py — main OLS regression with Newey-West standard errors.

Model (Maggiori eq. 21 extension with buffer decomposition):
  Spread_t = α + β1·ΔlnS_t + β2·θ_t + β3·L_t + β4·(L_t × ΔlnS_t)
             + β5·V_t + β6·VIX_t + β7·ΔlnN*_t + ε_t

Variables:
  θ (theta) = Treasury Exposure = T-bill Holdings / Supply
  L (liq_buffer) = Liquid Buffer = Cash Reserves / Supply

Hypotheses:
  β1 < 0  (issuance compresses spreads — exorbitant privilege amplification)
  β2 > 0  (higher T-bill exposure amplifies demand and compresses spreads further)
  β4 > 0  (larger liquid buffer dampens crisis transmission during redemptions)

Outputs: results/regression_main.txt, results/regression_robustness.txt
"""

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.stattools import durbin_watson
from pathlib import Path

from config import MONTHLY_CSV, RESULTS_DIR

Path(RESULTS_DIR).mkdir(exist_ok=True)


def load_panel() -> pd.DataFrame:
    df = pd.read_csv(MONTHLY_CSV, index_col=0, parse_dates=True)
    return df


def run_ols(y: pd.Series, X: pd.DataFrame, label: str, lags: int = 1) -> sm.regression.linear_model.RegressionResultsWrapper:
    Xc = sm.add_constant(X)
    model = sm.OLS(y, Xc, missing="drop")
    # Newey-West HAC with 1 lag (per proposal)
    res = model.fit(cov_type="HAC", cov_kwds={"maxlags": lags})
    print(f"\n{'='*60}")
    print(f"  {label}")
    print(f"{'='*60}")
    print(res.summary())
    print(f"  Durbin-Watson: {durbin_watson(res.resid):.3f}")
    return res


def save_results(res_main, res_rob, outfile: str):
    with open(outfile, "w") as f:
        f.write("MAIN REGRESSION\n")
        f.write("=" * 60 + "\n")
        f.write(str(res_main.summary()))
        f.write("\n\nROBUSTNESS — without buffer interaction\n")
        f.write("=" * 60 + "\n")
        f.write(str(res_rob.summary()))
    print(f"\n  Results saved to {outfile}")


def granger_test(df: pd.DataFrame, dep: str = "spread", cause: str = "dln_supply", max_lag: int = 3):
    """Granger causality: does ΔlnS Granger-cause Spread?"""
    from statsmodels.tsa.stattools import grangercausalitytests
    print("\n--- Granger Causality: ΔlnS → Spread ---")
    data = df[[dep, cause]].dropna()
    results = grangercausalitytests(data, maxlag=max_lag, verbose=False)
    for lag, res in results.items():
        f_stat = res[0]["ssr_ftest"][0]
        p_val  = res[0]["ssr_ftest"][1]
        sig    = "*" if p_val < 0.1 else ""
        print(f"  Lag {lag}: F={f_stat:.3f}, p={p_val:.3f} {sig}")


def main():
    df = load_panel()
    print(f"Loaded monthly panel: {len(df)} observations ({df.index[0].date()} – {df.index[-1].date()})")

    y = df["spread"]
    has_buffer = df["theta"].notna().sum() > 10

    # ── Main specification ──────────────────────────────────────────────────
    base_controls = ["vix", "dln_row_equity"]
    supply_vars   = ["dln_supply", "velocity"]

    if has_buffer:
        # NEW DECOMPOSED SPECIFICATION: theta, liq_buffer, and L × ΔlnS interaction
        X_main = df[supply_vars + ["theta", "liq_buffer", "L_x_dlns"] + base_controls]
        res_main = run_ols(y, X_main, "Main: theta (Treasury Exposure) + L (Liquid Buffer) decomposition")
    else:
        print("\n  NOTE: theta and liq_buffer not available — running without decomposed buffer.")
        X_main = df[supply_vars + base_controls]
        res_main = run_ols(y, X_main, "Main: without buffer (attestation data missing)")

    # ── Robustness: old unified buffer specification ────────────────────────
    if has_buffer and "buffer_ratio" in df.columns:
        X_rob = df[supply_vars + ["buffer_ratio", "buf_x_dlns"] + base_controls]
        res_rob = run_ols(y, X_rob, "Robustness: unified buffer_ratio (for comparison)")
    else:
        print("\n  NOTE: buffer_ratio not available for robustness check.")
        X_rob = None
        res_rob = None

    # ── Robustness: alternative DV (bid-cover ratio) ────────────────────────
    if "bid_cover_ratio" in df.columns and df["bid_cover_ratio"].notna().sum() > 10:
        y_alt = df["bid_cover_ratio"]
        X_alt = df[supply_vars + (["theta", "liq_buffer", "L_x_dlns"] if has_buffer else []) + base_controls]
        run_ols(y_alt, X_alt, "Robustness: bid-cover ratio as DV")

    # ── Save ────────────────────────────────────────────────────────────────
    save_results(res_main, res_rob, f"{RESULTS_DIR}/regression_main.txt")

    # ── Granger causality ───────────────────────────────────────────────────
    granger_test(df)

    # ── Key coefficient table ───────────────────────────────────────────────
    print("\n--- Key coefficient summary ---")
    rows = []
    for label, res in [("Main", res_main), ("Old buffer_ratio spec", res_rob)]:
        for var in ["dln_supply", "theta", "liq_buffer", "L_x_dlns", "buffer_ratio", "buf_x_dlns"]:
            if res is not None and var in res.params:
                rows.append({
                    "spec": label, "variable": var,
                    "coef": res.params[var],
                    "p_value": res.pvalues[var],
                    "sig": "***" if res.pvalues[var] < 0.01 else "**" if res.pvalues[var] < 0.05 else "*" if res.pvalues[var] < 0.1 else "",
                })
    coef_df = pd.DataFrame(rows)
    print(coef_df.to_string(index=False))
    coef_df.to_csv(f"{RESULTS_DIR}/coefficients.csv", index=False)


if __name__ == "__main__":
    main()
