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

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import MONTHLY_CSV, RESULTS_DIR, DATA_DIR

Path(RESULTS_DIR).mkdir(exist_ok=True)

# Issuer-level long panel produced by build_panel.py (#2). Defined here so
# config.py is left untouched.
PANEL_LONG_CSV = f"{DATA_DIR}/panel_long.csv"

# Main spec follows the prof: drop theta, keep L + L×ΔlnS (spec C).
# We ALSO always run the theta-retained spec (spec B) as a side-by-side robustness,
# because empirically θ+L≈0.72 (not 1), corr(θ,L)=0.13, VIF<2 — so θ is NOT linearly
# dependent on L in this data and turns out significant. Reporting both lets the team
# decide. Set INCLUDE_THETA_MAIN=True to make the theta version the *main* one instead.
INCLUDE_THETA_MAIN = False


def load_panel() -> pd.DataFrame:
    df = pd.read_csv(MONTHLY_CSV, index_col=0, parse_dates=True)
    return df


def run_panel(outfile: str, include_theta: bool = False):
    """
    Issuer-level panel regression: each row is one issuer in one month (USDT, USDC).

    Spec (prof's corrections):
        Spread_t = α + β₁·ΔlnS_it + β₃·L_it + β₄·(L_it × ΔlnS_it)
                   + γ·controls + δ·USDT_i + ε_it

    - USDT_i: issuer fixed effect (1 if USDT, 0 if USDC). With only 2 issuers
      this is a single dummy. Absorbs any time-invariant level difference between
      Tether and Circle (e.g. average reserve composition, reporting conventions).
    - NO month fixed effects: spread_t is the same macro variable for both issuers
      in a given month — month FE would absorb all variation in the dependent variable.
    - SE clustered by month: shared macro shock within a month.
    - include_theta=False → prof's spec (theta dropped).
    - include_theta=True  → theta-retained robustness.
    """
    try:
        p = pd.read_csv(PANEL_LONG_CSV, parse_dates=["date"])
    except FileNotFoundError:
        print(f"  NOTE: {PANEL_LONG_CSV} not found — run build_panel.py first.")
        return None

    need = ["spread", "dln_supply", "liq_buffer"] + (["theta"] if include_theta else [])
    p = p.dropna(subset=need)

    # Issuer fixed effect: one dummy for USDT (baseline = USDC)
    p["usdt"] = (p["issuer"] == "USDT").astype(int)

    vars_ = ["dln_supply"] + (["theta"] if include_theta else []) \
            + ["liq_buffer", "L_x_dlns", "vix", "dln_row_equity", "usdt"]
    X = sm.add_constant(p[vars_])
    y = p["spread"]

    # cluster-robust by month (shared macro spread within a month)
    groups = p["date"].astype("int64")
    res = sm.OLS(y, X).fit(cov_type="cluster", cov_kwds={"groups": groups})

    tag = "WITH theta" if include_theta else "NO theta (prof spec)"
    print(f"\n{'='*60}")
    print(f"  PANEL [{tag}] + issuer FE: N={len(p)}, "
          f"issuers={sorted(p['issuer'].unique())}")
    print(f"  Spread_t = α + β₁ΔlnS_it"
          f"{' + β₂θ_it' if include_theta else ''} + β₃L_it + β₄(L_it×ΔlnS_it)"
          f" + controls + δ·USDT_i")
    print(f"{'='*60}")
    print(res.summary())
    b1, p1 = res.params["dln_supply"], res.pvalues["dln_supply"]
    b3, p3 = res.params["liq_buffer"], res.pvalues["liq_buffer"]
    b4, p4 = res.params["L_x_dlns"],  res.pvalues["L_x_dlns"]
    bd, pd_ = res.params["usdt"],      res.pvalues["usdt"]
    print(f"\n  β₁ (ΔlnS)     = {b1:+.4f}  p={p1:.4f}")
    print(f"  β₃ (L)        = {b3:+.4f}  p={p3:.4f}")
    print(f"  β₄ (L×ΔlnS)   = {b4:+.4f}  p={p4:.4f}   ← key coefficient")
    print(f"  δ  (USDT FE)  = {bd:+.4f}  p={pd_:.4f}")

    with open(outfile, "w") as f:
        f.write("ISSUER-LEVEL PANEL REGRESSION — continuous L spec\n")
        f.write("=" * 60 + "\n")
        f.write(f"N = {len(p)} issuer-month obs; issuers = {sorted(p['issuer'].unique())}\n")
        f.write("Spread_t = α + β₁ΔlnS_it + β₃L_it + β₄(L_it×ΔlnS_it) + controls + δ·USDT_i\n")
        f.write("Issuer FE: USDT dummy (baseline=USDC). No month FE (spread is common).\n")
        f.write("SE clustered by month.\n")
        f.write("=" * 60 + "\n")
        f.write(str(res.summary()))
    print(f"  Results saved to {outfile}")
    return res


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
        f.write("Spread = α + β₁·ΔlnS + β₃·L + β₄·(L×ΔlnS) + controls\n")
        f.write("(theta dropped; no combined treasury+liquid variable — prof feedback #1)\n")
        f.write("=" * 60 + "\n")
        f.write(str(res_main.summary()))
        if res_rob is not None:
            f.write("\n\nROBUSTNESS\n")
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


def run_asymmetric(df: pd.DataFrame, outfile: str):
    """
    Split regressions for growth vs. contraction periods.
    Buying T-bills (ΔlnS > 0) is orderly; forced liquidation (ΔlnS < 0) is not.
    Buffer L should only matter significantly in contraction periods.
    """
    base_controls = ["velocity", "vix", "dln_row_equity"]
    # #1: theta dropped here too — keep only the liquid buffer L.
    buffer_vars   = ["liq_buffer"]

    df_pos = df[df["dln_supply"] > 0].copy()
    df_neg = df[df["dln_supply"] < 0].copy()

    res_pos = run_ols(
        df_pos["spread"],
        df_pos[["dln_supply_pos"] + buffer_vars + ["L_x_dlns_pos"] + base_controls],
        f"Asymmetric A — Growth periods (ΔlnS > 0, N={len(df_pos)})",
        lags=3,
    )
    res_neg = run_ols(
        df_neg["spread"],
        df_neg[["dln_supply_neg"] + buffer_vars + ["L_x_dlns_neg"] + base_controls],
        f"Asymmetric B — Contraction periods (ΔlnS < 0, N={len(df_neg)})",
        lags=3,
    )

    print("\n--- Asymmetric coefficient comparison ---")
    print(f"{'':30s} {'Growth':>10s} {'Contraction':>12s}")
    for var, pos_var, neg_var in [
        ("ΔlnS",       "dln_supply_pos", "dln_supply_neg"),
        ("L × ΔlnS",   "L_x_dlns_pos",  "L_x_dlns_neg"),
    ]:
        b_pos = res_pos.params.get(pos_var, float("nan"))
        p_pos = res_pos.pvalues.get(pos_var, float("nan"))
        b_neg = res_neg.params.get(neg_var, float("nan"))
        p_neg = res_neg.pvalues.get(neg_var, float("nan"))
        sig = lambda p: "***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.1 else ""
        print(f"  {var:28s} {b_pos:+.3f}{sig(p_pos):3s}    {b_neg:+.3f}{sig(p_neg):3s}")

    with open(outfile, "w") as f:
        f.write("ASYMMETRIC REGRESSION — Growth vs. Contraction Periods\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Growth periods (ΔlnS > 0): N = {len(df_pos)}\n")
        f.write(str(res_pos.summary()))
        f.write(f"\n\nContraction periods (ΔlnS < 0): N = {len(df_neg)}\n")
        f.write(str(res_neg.summary()))
    print(f"\n  Results saved to {outfile}")
    return res_pos, res_neg


def run_threshold_panel(outfile: str, thresholds: list = None):
    """
    Threshold panel regression: tests whether the buffer L effect is nonlinear,
    concentrated at very low buffer states (prof's suggestion).

    Spec:
        DV_t = α + β₁·ΔlnS_it + β₂·1[L_it < c] + β₃·1[L_it < c]·ΔlnS_it
               + γ·controls + δ·USDT_i + ε_it

    Run for c ∈ {4%, 6%} × DV ∈ {Spread_t, ΔSpread_t}.
    β₃ < 0 and significant → low-buffer states amplify the supply→spread channel.
    Caution: few low-buffer obs, mostly late-2025/2026 USDT — verify data first.
    """
    if thresholds is None:
        thresholds = [0.04, 0.06]

    try:
        p = pd.read_csv(PANEL_LONG_CSV, parse_dates=["date"])
    except FileNotFoundError:
        print(f"  NOTE: {PANEL_LONG_CSV} not found — run build_panel.py first.")
        return None

    p = p.dropna(subset=["spread", "dln_supply", "liq_buffer"])
    p["usdt"] = (p["issuer"] == "USDT").astype(int)

    # ΔSpread_t: first-difference of the common spread (same for both issuers per month)
    spread_ts = p.groupby("date")["spread"].first().sort_index()
    d_spread  = spread_ts.diff().rename("d_spread")
    p = p.merge(d_spread.reset_index(), on="date", how="left")

    controls = ["vix", "dln_row_equity", "usdt"]
    results_text = []
    summary_rows = []

    for c in thresholds:
        tag     = f"{int(c * 100)}pct"
        low_col = f"low_buf_{tag}"
        int_col = f"low_buf_{tag}_x_dlns"
        p[low_col] = (p["liq_buffer"] < c).astype(int)
        p[int_col] = p[low_col] * p["dln_supply"]

        n_low          = int(p[low_col].sum())
        issuers_in_low = p[p[low_col] == 1]["issuer"].value_counts().to_dict()

        vars_ = ["dln_supply", low_col, int_col] + controls

        for dv_label, dv_col in [("Spread_t (levels)", "spread"),
                                  ("ΔSpread_t (first-diff)", "d_spread")]:
            sub = p.dropna(subset=[dv_col] + vars_)
            if len(sub) < 20:
                print(f"  SKIP c={c:.0%} {dv_label}: only {len(sub)} obs after dropna")
                continue

            X      = sm.add_constant(sub[vars_])
            y      = sub[dv_col]
            groups = sub["date"].astype("int64")
            res    = sm.OLS(y, X).fit(cov_type="cluster", cov_kwds={"groups": groups})

            b1, p1 = res.params["dln_supply"], res.pvalues["dln_supply"]
            b2, p2 = res.params[low_col],      res.pvalues[low_col]
            b3, p3 = res.params[int_col],      res.pvalues[int_col]
            sig = lambda pv: "***" if pv < 0.01 else "**" if pv < 0.05 else "*" if pv < 0.1 else ""

            header = (f"\nTHRESHOLD c={c:.0%}  |  DV={dv_label}"
                      f"  |  N={len(sub)} ({n_low} low-buf rows: {issuers_in_low})")
            eq = (f"  {dv_col} = α + β₁·ΔlnS + β₂·1[L<{c:.0%}]"
                  f" + β₃·1[L<{c:.0%}]·ΔlnS + controls + δ·USDT")
            print(f"\n{'='*65}")
            print(header)
            print(eq)
            print(f"{'='*65}")
            print(res.summary())
            print(f"  β₁ (ΔlnS)              = {b1:+.4f}  p={p1:.4f} {sig(p1)}")
            print(f"  β₂ (1[L<{c:.0%}])          = {b2:+.4f}  p={p2:.4f} {sig(p2)}")
            print(f"  β₃ (1[L<{c:.0%}]×ΔlnS)     = {b3:+.4f}  p={p3:.4f} {sig(p3)}  ← key")

            results_text.append(f"\n{'='*65}\n{header}\n{eq}\n{'='*65}\n")
            results_text.append(str(res.summary()))
            results_text.append(
                f"\nβ₁={b1:+.4f}(p={p1:.3f}{sig(p1)})  "
                f"β₂={b2:+.4f}(p={p2:.3f}{sig(p2)})  "
                f"β₃={b3:+.4f}(p={p3:.3f}{sig(p3)})\n"
            )
            summary_rows.append({
                "threshold_c": c, "DV": dv_col, "N": len(sub),
                "n_low_buf": n_low, "low_buf_issuers": str(issuers_in_low),
                "beta1_dlns": round(b1, 4), "p1": round(p1, 4), "sig1": sig(p1),
                "beta2_lowbuf": round(b2, 4), "p2": round(p2, 4), "sig2": sig(p2),
                "beta3_inter": round(b3, 4), "p3": round(p3, 4), "sig3": sig(p3),
                "R2": round(res.rsquared, 4),
            })

    with open(outfile, "w") as f:
        f.write("THRESHOLD PANEL REGRESSIONS — Low-Buffer Nonlinear Specs\n")
        f.write("Spec: DV = α + β₁·ΔlnS + β₂·1[L<c] + β₃·1[L<c]·ΔlnS + controls + USDT_FE\n")
        f.write("SE clustered by month. Issuer FE = USDT dummy (baseline USDC).\n")
        f.write("WARNING: low-buffer obs are few and mostly late-2025/2026 USDT.\n")
        f.write("Verify Dec-2025 USDT cash entry before citing these results.\n")
        f.write("=" * 65 + "\n")
        f.writelines(results_text)

    summary_df = pd.DataFrame(summary_rows)
    summary_csv = outfile.replace(".txt", "_summary.csv")
    summary_df.to_csv(summary_csv, index=False)

    print(f"\n  Full results → {outfile}")
    print(f"  Summary table → {summary_csv}")
    print("\n--- THRESHOLD SUMMARY ---")
    for _, row in summary_df.iterrows():
        print(f"  c={row['threshold_c']:.0%}  DV={row['DV']:25s}  "
              f"β₃={row['beta3_inter']:+.3f}(p={row['p3']:.3f}{row['sig3']})  "
              f"N={row['N']}  n_low={row['n_low_buf']}")

    return summary_df


def run_asymmetric_panel(outfile: str, thresholds: list = None):
    """
    Asymmetric panel regression (professor's revised baseline specification).

    Theory: the fragility mechanism is one-sided. Supply increases let issuers
    accumulate T-bills gradually — the liquid buffer need not matter much. Supply
    decreases (redemptions) force T-bill sales when the liquid buffer is depleted.

    Spec:
        ΔSpread_t = α + β1·Inflow_it + β2·Outflow_it
                    + β3·Low_it
                    + β4·Low_it × Inflow_it
                    + β5·Low_it × Outflow_it   ← key: predicted positive
                    + γ·controls + δ·USDT_i + ε_it

    where:
        Inflow_it  = max(ΔlnS_it, 0)
        Outflow_it = max(-ΔlnS_it, 0)
        Low_it     = 1[L_it < c]   for c ∈ thresholds

    DV is ΔSpread (first-differenced) to address non-stationarity.
    SE clustered by month. Issuer FE via USDT dummy.
    """
    if thresholds is None:
        thresholds = [0.10, 0.12]

    try:
        p = pd.read_csv(PANEL_LONG_CSV, parse_dates=["date"])
    except FileNotFoundError:
        print(f"  NOTE: {PANEL_LONG_CSV} not found — run build_panel.py first.")
        return None

    p = p.sort_values(["issuer", "date"]).reset_index(drop=True)
    p["usdt"]    = (p["issuer"] == "USDT").astype(int)
    p["dspread"] = p.groupby("issuer")["spread"].diff()

    # Asymmetric supply decomposition (using DeFiLlama supply via dln_supply)
    p["inflow"]  = p["dln_supply"].clip(lower=0)
    p["outflow"] = (-p["dln_supply"]).clip(lower=0)

    controls = ["vix", "dln_row_equity", "usdt"]
    results_text = []
    summary_rows = []
    sig = lambda pv: "***" if pv < 0.01 else "**" if pv < 0.05 else "*" if pv < 0.1 else ""

    for c in thresholds:
        tpct = int(c * 100)
        p[f"low{tpct}"]      = (p["liq_buffer"] < c).astype(int)
        p[f"low_in_{tpct}"]  = p[f"low{tpct}"] * p["inflow"]
        p[f"low_out_{tpct}"] = p[f"low{tpct}"] * p["outflow"]

        reg_cols = ["inflow", "outflow", f"low{tpct}",
                    f"low_in_{tpct}", f"low_out_{tpct}"] + controls

        sub = p.dropna(subset=["dspread"] + reg_cols).copy().reset_index(drop=True)

        n_low          = int(sub[f"low{tpct}"].sum())
        n_low_out      = int(((sub[f"low{tpct}"] == 1) & (sub["outflow"] > 0)).sum())
        issuers_in_low = sorted(sub[sub[f"low{tpct}"] == 1]["issuer"].unique().tolist())

        X      = sm.add_constant(sub[reg_cols])
        y      = sub["dspread"]
        groups = sub["date"].astype("int64")
        res    = sm.OLS(y, X).fit(cov_type="cluster", cov_kwds={"groups": groups})

        b1, p1 = res.params["inflow"],           res.pvalues["inflow"]
        b2, p2 = res.params["outflow"],          res.pvalues["outflow"]
        b3, p3 = res.params[f"low{tpct}"],       res.pvalues[f"low{tpct}"]
        b4, p4 = res.params[f"low_in_{tpct}"],   res.pvalues[f"low_in_{tpct}"]
        b5, p5 = res.params[f"low_out_{tpct}"],  res.pvalues[f"low_out_{tpct}"]

        header = (f"\nASYMMETRIC PANEL  L<{tpct}%  |  DV=ΔSpread"
                  f"  |  N={len(sub)}  low-buf obs={n_low}"
                  f"  low-buf outflow>0={n_low_out}  issuers={issuers_in_low}")
        print(f"\n{'='*65}")
        print(header)
        print(f"{'='*65}")
        print(res.summary())
        print(f"\n  β1 (Inflow)           = {b1:+.4f}  p={p1:.4f} {sig(p1)}")
        print(f"  β2 (Outflow)          = {b2:+.4f}  p={p2:.4f} {sig(p2)}")
        print(f"  β3 (Low{tpct})           = {b3:+.4f}  p={p3:.4f} {sig(p3)}")
        print(f"  β4 (Low{tpct}×Inflow)   = {b4:+.4f}  p={p4:.4f} {sig(p4)}")
        print(f"  β5 (Low{tpct}×Outflow)  = {b5:+.4f}  p={p5:.4f} {sig(p5)}  ← key")
        print(f"  R² = {res.rsquared:.4f}")

        results_text.append(f"\n{'='*65}\n{header}\n{'='*65}\n")
        results_text.append(str(res.summary()))
        results_text.append(
            f"\nβ5 (Low{tpct}×Outflow) = {b5:+.4f}  p={p5:.4f} {sig(p5)}  ← key\n"
        )
        summary_rows.append({
            "threshold_c": c, "N": len(sub),
            "n_low_buf": n_low, "n_low_outflow_pos": n_low_out,
            "issuers_in_low": str(issuers_in_low),
            "beta1_inflow":  round(b1, 4), "p1": round(p1, 4), "sig1": sig(p1),
            "beta2_outflow": round(b2, 4), "p2": round(p2, 4), "sig2": sig(p2),
            "beta3_low":     round(b3, 4), "p3": round(p3, 4), "sig3": sig(p3),
            "beta4_low_in":  round(b4, 4), "p4": round(p4, 4), "sig4": sig(p4),
            "beta5_low_out": round(b5, 4), "p5": round(p5, 4), "sig5": sig(p5),
            "R2": round(res.rsquared, 4),
        })

    with open(outfile, "w") as f:
        f.write("ASYMMETRIC PANEL REGRESSION — Professor's Revised Baseline Specification\n")
        f.write("Spec: ΔSpread = α + β1·Inflow + β2·Outflow + β3·Low + β4·Low×Inflow\n")
        f.write("             + β5·Low×Outflow + controls + USDT_FE\n")
        f.write("Inflow=max(ΔlnS,0), Outflow=max(-ΔlnS,0), Low=1[L<c]\n")
        f.write("DV=ΔSpread (first-differenced). SE clustered by month.\n")
        f.write("Key coef: β5 (Low×Outflow) — predicted positive (forced-sale channel).\n")
        f.write("=" * 65 + "\n")
        f.writelines(results_text)

    summary_df = pd.DataFrame(summary_rows)
    summary_csv = outfile.replace(".txt", "_summary.csv")
    summary_df.to_csv(summary_csv, index=False)

    print(f"\n  Full results  → {outfile}")
    print(f"  Summary table → {summary_csv}")
    print("\n--- ASYMMETRIC PANEL SUMMARY ---")
    for _, row in summary_df.iterrows():
        print(f"  L<{int(row['threshold_c']*100)}%  "
              f"β5={row['beta5_low_out']:+.4f}(p={row['p5']:.4f}{row['sig5']})  "
              f"N={row['N']}  n_low_outflow={row['n_low_outflow_pos']}  "
              f"issuers={row['issuers_in_low']}")

    return summary_df


def main():
    df = load_panel()
    print(f"Loaded monthly panel: {len(df)} observations ({df.index[0].date()} – {df.index[-1].date()})")

    y = df["spread"]
    has_buffer = df["liq_buffer"].notna().sum() > 10

    # ── Main specification (prof's equation) ────────────────────────────────
    # Spread = α + β₁·ΔlnS + β₃·L + β₄·(L×ΔlnS) + controls
    # Per prof feedback (#1): theta is DROPPED (θ+L≈1 by construction → linear
    # dependence) and no combined treasury+liquid variable is used. The story is
    # about the LIQUID buffer, so the interaction is L×ΔlnS directly. β₄ is the
    # coefficient of interest (#6).
    base_controls = ["vix", "dln_row_equity"]
    supply_vars   = ["dln_supply", "velocity"]
    VARS_NO_THETA = ["dln_supply", "liq_buffer", "L_x_dlns", "velocity"] + base_controls
    VARS_THETA    = ["dln_supply", "theta", "liq_buffer", "L_x_dlns", "velocity"] + base_controls
    MAIN_VARS     = VARS_THETA if INCLUDE_THETA_MAIN else VARS_NO_THETA

    if has_buffer:
        # Spec C — prof's equation, theta dropped
        res_noth = run_ols(y, df[VARS_NO_THETA],
                           "Spec C (prof): Spread = α + β₁ΔlnS + β₃L + β₄(L×ΔlnS) + controls  [NO theta]")
        # Spec B — theta retained (θ+L≠1 empirically, so not collinear). Kept as a
        # side-by-side because θ is significant and improves fit; the team chooses.
        res_th = None
        if "theta" in df.columns and df["theta"].notna().sum() > 10:
            res_th = run_ols(y, df[VARS_THETA],
                             "Spec B (theta kept): + β₂θ  [robustness — θ+L≈0.72, VIF<2, θ significant]")
        # main = whichever the toggle selects
        res_main = res_th if INCLUDE_THETA_MAIN else res_noth
        res_rob  = res_noth if INCLUDE_THETA_MAIN else res_th
    else:
        print("\n  NOTE: liq_buffer not available — running without buffer.")
        X_main = df[supply_vars + base_controls]
        res_main = run_ols(y, X_main, "Main: without buffer (attestation data missing)")
        res_rob = None

    # ── Panel regression: each issuer a separate observation (#2) ────────────
    # Run both: prof spec (no theta) and theta-retained robustness.
    res_panel    = run_panel(f"{RESULTS_DIR}/panel_regression.txt", include_theta=False)
    res_panel_th = run_panel(f"{RESULTS_DIR}/panel_regression_theta.txt", include_theta=True)

    # ── Robustness: alternative DV (bid-cover ratio) ────────────────────────
    if "bid_cover_ratio" in df.columns and df["bid_cover_ratio"].notna().sum() > 10:
        y_alt = df["bid_cover_ratio"]
        X_alt = df[supply_vars + (["liq_buffer", "L_x_dlns"] if has_buffer else []) + base_controls]
        run_ols(y_alt, X_alt, "Robustness: bid-cover ratio as DV")

    # ── Save ────────────────────────────────────────────────────────────────
    save_results(res_main, res_rob, f"{RESULTS_DIR}/regression_main.txt")

    # ── Post-2023 subsample (best attestation coverage, N=39) ──────────────
    df_post = df[df.index >= "2023-01-01"].copy()
    print(f"\n{'='*60}")
    print(f"  POST-2023 SUBSAMPLE  (Jan 2023 – Mar 2026, N={len(df_post)})")
    print(f"{'='*60}")
    if has_buffer and len(df_post) >= 20:
        y_post = df_post["spread"]
        X_post = df_post[MAIN_VARS]
        res_post = run_ols(y_post, X_post,
                           f"Post-2023 subsample: N={len(df_post)} (comprehensive attestations)",
                           lags=3)
        with open(f"{RESULTS_DIR}/post2023_regression.txt", "w") as f:
            f.write(f"POST-2023 SUBSAMPLE REGRESSION  (Jan 2023 – Mar 2026, N={len(df_post)})\n")
            f.write("Motivation: reserve attestations only became comprehensive after 2023.\n")
            f.write("=" * 60 + "\n")
            f.write(str(res_post.summary()))
        b1  = res_post.params.get("dln_supply", float("nan"))
        b4  = res_post.params.get("L_x_dlns",  float("nan"))
        p1  = res_post.pvalues.get("dln_supply", float("nan"))
        p4  = res_post.pvalues.get("L_x_dlns",  float("nan"))
        print(f"\n  Key post-2023 results:")
        print(f"    β₁ (ΔlnS)    = {b1:+.3f}  p={p1:.4f}")
        print(f"    β₄ (L×ΔlnS) = {b4:+.3f}  p={p4:.4f}")
        print(f"  Results saved to {RESULTS_DIR}/post2023_regression.txt")
    else:
        print("  NOTE: insufficient post-2023 observations or buffer data missing.")

    # ── Asymmetric growth vs. contraction regressions ──────────────────────
    if "dln_supply_pos" in df.columns:
        run_asymmetric(df, f"{RESULTS_DIR}/asymmetric_regression.txt")
    else:
        print("\n  NOTE: dln_supply_pos not found — rebuild panel first.")

    # ── Threshold panel: 1[L < 4%] and 1[L < 6%] × ΔlnS ───────────────────
    run_threshold_panel(f"{RESULTS_DIR}/threshold_panel.txt", thresholds=[0.04, 0.06])

    # ── Asymmetric panel: professor's revised baseline (L<10% and L<12%) ─────
    run_asymmetric_panel(
        f"{RESULTS_DIR}/asymmetric_panel.txt",
        thresholds=[0.10, 0.12],
    )

    # ── Granger causality ───────────────────────────────────────────────────
    granger_test(df)

    # ── Key coefficient table — all 4 specs (theta in/out × TS/panel) ────────
    print("\n--- Key coefficient summary (theta-out vs theta-in, TS & panel) ---")
    rows = []
    spec_list = [
        ("Time series, NO theta (prof)", res_noth),
        ("Time series, WITH theta",      res_th),
        ("Panel, NO theta (prof)",       res_panel),
        ("Panel, WITH theta",            res_panel_th),
    ]
    for label, res in spec_list:
        for var in ["dln_supply", "theta", "liq_buffer", "L_x_dlns", "usdt"]:
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
