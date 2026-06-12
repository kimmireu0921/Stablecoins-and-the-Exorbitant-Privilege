"""
bidcover_final.py
===================================================================
Final bid-cover specification (USDT vs USDC).

Builds on the original monthly design and folds in the auction-level
review's one adopted point — controlling for offering size — and reports
the result both with and without the interpolated reserve controls (theta, L),
plus a placebo. This is the version intended for the paper.

Run:
    python bidcover_final.py

Reads from ./data/ :  daily_panel.csv, monthly_panel.csv,
                      bidcover_auction_raw_rebuilt.csv
Writes ./bidcover_final_results.csv and prints the tables.

All numbers are computed live from the data. Nothing is hand-typed.

Specification (per maturity m, monthly, N=51):
    bid_cover_t = a + b_USDT dlnS^USDT_t + b_USDC dlnS^USDC_t
                    + g ln(offering_t)            [offering size, adopted control]
                    + controls + e_t
    Newey-West HAC(1) SE. Issuer supply growth = month-end log-difference.

Two control sets are reported:
    MAIN  : offering + VIX + dlnN* + d_fedfunds          (no interpolated theta/L)
    +RES  : MAIN + theta + L + velocity                  (adds reserve controls)
===================================================================
"""
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.stattools import durbin_watson
from pathlib import Path
import warnings
warnings.filterwarnings("ignore")

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
AUCTION_CSV = HERE / "results" / "bidcover_auction_raw_rebuilt.csv"
TERMS = ["4-Week", "8-Week", "13-Week", "26-Week"]
ROWS = []

# Control sets
MAIN_CTRL = ["ln_offering", "vix", "dln_row_equity", "d_ff"]            # no theta/L
RES_CTRL = ["ln_offering", "vix", "dln_row_equity", "d_ff",
            "theta", "liq_buffer", "velocity"]                          # + reserves


def sig(p):
    return "***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.10 else ""


def hr(t):
    print("\n" + "=" * 78)
    print("  " + t)
    print("=" * 78)


def load():
    m = pd.read_csv(DATA / "monthly_panel.csv", index_col=0, parse_dates=True)
    d = pd.read_csv(DATA / "daily_panel.csv", index_col=0, parse_dates=True)
    me = d[["supply_USDT", "supply_USDC"]].resample("ME").last()
    m["dlnU"] = np.log(me["supply_USDT"]).diff()
    m["dlnC"] = np.log(me["supply_USDC"]).diff()
    m["d_ff"] = d["fedfunds"].resample("ME").last().diff()
    a = pd.read_csv(AUCTION_CSV, parse_dates=["date"])
    a = a[a["term"].isin(TERMS)].copy()
    return m, d, a


def fit(m, a, term, controls):
    t = a[a["term"] == term].set_index("date").sort_index()
    bc = t["bid_cover"].resample("ME").mean().rename("bid_cover")
    off = np.log(t["offering"].resample("ME").mean()).rename("ln_offering")
    df = m.join(bc, how="left").join(off, how="left")
    xc = ["dlnU", "dlnC"] + controls
    use = df[["bid_cover"] + xc].replace([np.inf, -np.inf], np.nan).dropna()
    r = sm.OLS(use["bid_cover"], sm.add_constant(use[xc])).fit(
        cov_type="HAC", cov_kwds={"maxlags": 1})
    wald = float(r.f_test("dlnU = dlnC").pvalue)
    return dict(term=term, n=len(use),
                bU=r.params["dlnU"], pU=r.pvalues["dlnU"],
                bC=r.params["dlnC"], pC=r.pvalues["dlnC"],
                wald=wald, r2=r.rsquared, dw=durbin_watson(r.resid))


def table(m, a, controls, label, tag):
    print(f"\n  {label}")
    print(f"  {'Maturity':9} {'b_USDT':>11} {'b_USDC':>11} {'Wald U=C':>10} {'R2':>6} {'DW':>5}")
    print("  " + "-" * 62)
    for term in TERMS:
        r = fit(m, a, term, controls)
        print(f"  {term:9} {r['bU']:+8.3f}{sig(r['pU']):3} {r['bC']:+8.3f}{sig(r['pC']):3} "
              f"{r['wald']:>9.4f}{sig(r['wald'])} {r['r2']:>6.3f} {r['dw']:>5.2f}")
        ROWS.append({"spec": tag, **r})


def placebo(m, a, controls, term, n_boot=2000, seed=42):
    t = a[a["term"] == term].set_index("date").sort_index()
    bc = t["bid_cover"].resample("ME").mean().rename("bid_cover")
    off = np.log(t["offering"].resample("ME").mean()).rename("ln_offering")
    df = m.join(bc, how="left").join(off, how="left")
    xc = ["dlnU", "dlnC"] + controls
    use = df[["bid_cover"] + xc].replace([np.inf, -np.inf], np.nan).dropna()
    y = use["bid_cover"].values
    obs = np.linalg.lstsq(sm.add_constant(use[xc]).values, y, rcond=None)[0][1]
    rng = np.random.default_rng(seed); cnt = 0; base = use[xc].copy()
    for _ in range(n_boot):
        bb = base.copy(); perm = rng.permutation(len(bb))
        bb["dlnU"] = base["dlnU"].values[perm]; bb["dlnC"] = base["dlnC"].values[perm]
        bp = np.linalg.lstsq(sm.add_constant(bb).values, y, rcond=None)[0][1]
        if bp <= obs:
            cnt += 1
    return obs, cnt / n_boot


def main():
    m, d, a = load()

    print("#" * 78)
    print("#  BID-COVER — FINAL SPECIFICATION (USDT vs USDC)")
    print("#  Monthly, N=51, Newey-West HAC(1). Computed live from ./data/.")
    print("#" * 78)

    hr("MAIN — supply + offering + VIX + dlnN* + Fed  (no interpolated theta/L)")
    print("  This is the recommended headline spec: it adopts the offering-size")
    print("  control and uses only directly-observed regressors.")
    table(m, a, MAIN_CTRL, "Result:", "main_no_thetaL")

    hr("ROBUSTNESS — MAIN + theta + L + velocity  (adds reserve controls)")
    print("  Same spec with the reserve controls added back, for comparison.")
    table(m, a, RES_CTRL, "Result:", "with_reserves")

    hr("PLACEBO — 2,000 time-shuffles on the MAIN spec")
    for term in TERMS:
        obs, p = placebo(m, a, MAIN_CTRL, term)
        print(f"  {term:9} b_USDT={obs:+.3f}  placebo p(one-sided)={p:.3f}{sig(p)}")

    hr("NOTES")
    print("""  - b_USDT is the coefficient of interest: a higher monthly supply growth for
    the T-bill-heavy issuer (USDT) is associated with a lower bid-cover ratio.
  - b_USDC is reported alongside; the Wald test is for b_USDT = b_USDC.
  - The MAIN spec contains no interpolated reserve variables; the ROBUSTNESS spec
    adds theta and L and gives similar coefficients.
  - SE: Newey-West HAC with 1 lag. Issuer supply growth is the month-end
    log-difference of circulating supply. Offering size enters in logs, averaged
    to the month.""")

    pd.DataFrame(ROWS).to_csv(HERE / "results" / "bidcover_final_results.csv", index=False)
    print("\n  Saved: bidcover_final_results.csv")
    print("=" * 78)


if __name__ == "__main__":
    main()
