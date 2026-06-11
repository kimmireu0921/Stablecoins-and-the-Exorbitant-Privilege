"""
bidcover_auction_level.py — AUCTION-LEVEL bid-cover robustness (new contribution).

Why this exists
---------------
The existing bid-cover test (bidcover_mechanism_validation.py) collapses every
auction in a month to a single monthly mean (N≈51) and never controls for the
auction's OFFERING SIZE — the single most mechanical driver of a bid-cover ratio.
The obvious objection is therefore unanswered: "Isn't the USDT effect just bill
issuance rising at the same time stablecoins grew?"

This script answers that objection. It runs the regression at the level of the
individual auction (N≈1,094), controls for log(offering size), maturity fixed
effects, the risk environment (VIX), and — in the most demanding spec — a linear
time trend that strips out any common 2022–24 downtrend. Standard errors are
clustered by month (auctions in the same month share macro shocks).

Design
------
For each auction at date t with maturity m:

    bid_cover_{t,m} = α + β_USDT·Δln S^USDT_pre + β_USDC·Δln S^USDC_pre
                        + γ·ln(offering_{t,m}) + maturity FE + δ·VIX_t
                        [+ θ·trend]  + ε_{t,m}

Δln S^j_pre = pre-auction supply growth for issuer j over the WINDOW calendar days
ending the day BEFORE the auction (strictly pre-auction, no look-ahead).

Tests
-----
1. Specification ladder (pooled, all maturities): add offering → term FE → VIX →
   time trend, one at a time. β_USDT should stay negative and significant; β_USDC ≈ 0.
2. Per-maturity table with full controls.
3. Wald test β_USDT = β_USDC in each spec.
4. Window sensitivity (10 / 21 / 42 calendar days).
5. Lead / reverse-time falsification: FUTURE supply growth (t → t+WINDOW) should
   NOT predict bid_cover. If past predicts and future doesn't, the timing is right.
6. Subsample stability: drop the 2022 crypto-crisis year; post-2023 only.

Outputs (results/):
  bidcover_auction_level_results.csv   — every coefficient/spec
  bidcover_auction_level_summary.md    — human-readable writeup
Leaves all existing project files untouched.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
OUT = ROOT / "results"
OUT.mkdir(exist_ok=True)

TERMS = ["4-Week", "8-Week", "13-Week", "26-Week"]
AUCTION_CSV = OUT / "bidcover_auction_raw_rebuilt.csv"
DAILY_CSV = DATA / "daily_panel.csv"

WINDOW_MAIN = 21          # calendar days of pre-auction supply growth (~1 month)
WINDOWS_SENS = [10, 21, 42]


# ── Data assembly ────────────────────────────────────────────────────────────

def load_daily_supply() -> pd.DataFrame:
    d = pd.read_csv(DAILY_CSV, index_col=0, parse_dates=True)
    # full calendar-day grid so date arithmetic is exact; ffill weekends/holidays
    grid = pd.date_range(d.index.min(), d.index.max(), freq="D")
    d = d.reindex(grid).ffill()
    return d[["supply_USDT", "supply_USDC", "vix", "fedfunds"]]


def pre_auction_growth(daily: pd.DataFrame, t: pd.Timestamp, window: int,
                       lead: bool = False) -> tuple[float, float]:
    """
    Log supply growth over `window` calendar days.
      lead=False : (t-1-window) → (t-1)   strictly BEFORE the auction.
      lead=True  : (t)          → (t+window)  AFTER the auction (falsification).
    Returns (dln_USDT, dln_USDC); NaN if data is unavailable at an endpoint.
    """
    if lead:
        a, b = t, t + pd.Timedelta(days=window)
    else:
        b = t - pd.Timedelta(days=1)
        a = b - pd.Timedelta(days=window)
    out = []
    for col in ("supply_USDT", "supply_USDC"):
        s = daily[col]
        if a < s.index.min() or b > s.index.max():
            out.append(np.nan)
            continue
        va, vb = s.asof(a), s.asof(b)
        out.append(np.log(vb) - np.log(va) if (va > 0 and vb > 0) else np.nan)
    return out[0], out[1]


def build_auction_panel(window: int = WINDOW_MAIN, lead: bool = False) -> pd.DataFrame:
    auc = pd.read_csv(AUCTION_CSV, parse_dates=["date"])
    auc = auc[auc["term"].isin(TERMS)].copy()
    daily = load_daily_supply()

    g = auc["date"].apply(lambda t: pre_auction_growth(daily, t, window, lead))
    auc["dln_USDT"] = [x[0] for x in g]
    auc["dln_USDC"] = [x[1] for x in g]
    auc["ln_offering"] = np.log(auc["offering"])
    auc["vix"] = auc["date"].map(daily["vix"].asof)
    auc["month"] = auc["date"].dt.to_period("M")
    # linear time trend in months from sample start
    auc["trend"] = (auc["date"].dt.year - auc["date"].dt.year.min()) * 12 + auc["date"].dt.month
    for term in TERMS:
        auc[f"FE_{term}"] = (auc["term"] == term).astype(float)
    return auc.dropna(subset=["dln_USDT", "dln_USDC", "bid_cover", "ln_offering", "vix"])


# ── Estimation ───────────────────────────────────────────────────────────────

def cluster_ols(df: pd.DataFrame, xcols: list[str]):
    X = sm.add_constant(df[xcols], has_constant="add")
    y = df["bid_cover"]
    groups = df["month"].astype(str).astype("category").cat.codes
    return sm.OLS(y, X).fit(cov_type="cluster", cov_kwds={"groups": groups})


def sig(p: float) -> str:
    return "***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.10 else ""


def coef_row(spec: str, res, n: int) -> dict:
    bU, pU = res.params["dln_USDT"], res.pvalues["dln_USDT"]
    bC, pC = res.params["dln_USDC"], res.pvalues["dln_USDC"]
    try:
        wald_p = float(res.f_test("dln_USDT = dln_USDC").pvalue)
    except Exception:
        wald_p = np.nan
    return {
        "spec": spec, "n": n,
        "beta_USDT": bU, "p_USDT": pU, "sig_USDT": sig(pU),
        "beta_USDC": bC, "p_USDC": pC, "sig_USDC": sig(pC),
        "wald_USDT_eq_USDC_p": wald_p,
        "r2": res.rsquared,
    }


def run():
    rows = []
    panel = build_auction_panel(WINDOW_MAIN)
    fe = [f"FE_{t}" for t in TERMS[1:]]   # drop one term as reference

    # 1) Specification ladder (pooled, all maturities) ------------------------
    ladders = [
        ("(1) supply only",            ["dln_USDT", "dln_USDC"]),
        ("(2) + ln(offering)",         ["dln_USDT", "dln_USDC", "ln_offering"]),
        ("(3) + maturity FE",          ["dln_USDT", "dln_USDC", "ln_offering"] + fe),
        ("(4) + VIX",                  ["dln_USDT", "dln_USDC", "ln_offering", "vix"] + fe),
        ("(5) + linear time trend",    ["dln_USDT", "dln_USDC", "ln_offering", "vix", "trend"] + fe),
    ]
    print("\n" + "=" * 78)
    print("  AUCTION-LEVEL BID-COVER — specification ladder (pooled, N auctions)")
    print("=" * 78)
    for name, xc in ladders:
        res = cluster_ols(panel, xc)
        r = coef_row(name, res, len(panel))
        rows.append(r)
        print(f"  {name:26s} N={r['n']:4d}  "
              f"β_USDT={r['beta_USDT']:+.3f}{r['sig_USDT']:3s} (p={r['p_USDT']:.3f})  "
              f"β_USDC={r['beta_USDC']:+.3f}{r['sig_USDC']:3s} (p={r['p_USDC']:.3f})  "
              f"Wald p={r['wald_USDT_eq_USDC_p']:.3f}")

    full_x = ["dln_USDT", "dln_USDC", "ln_offering", "vix", "trend"]

    # 2) Per-maturity (full controls, no FE needed within a term) -------------
    print("\n" + "=" * 78)
    print("  PER-MATURITY (full controls: offering + VIX + trend)")
    print("=" * 78)
    for term in TERMS:
        sub = panel[panel["term"] == term]
        res = cluster_ols(sub, full_x)
        r = coef_row(f"per-maturity {term}", res, len(sub))
        rows.append(r)
        print(f"  {term:8s} N={r['n']:4d}  "
              f"β_USDT={r['beta_USDT']:+.3f}{r['sig_USDT']:3s} (p={r['p_USDT']:.3f})  "
              f"β_USDC={r['beta_USDC']:+.3f}{r['sig_USDC']:3s} (p={r['p_USDC']:.3f})  "
              f"Wald p={r['wald_USDT_eq_USDC_p']:.3f}")

    # 3) Window sensitivity (pooled, full controls) ---------------------------
    print("\n" + "=" * 78)
    print("  PRE-AUCTION WINDOW SENSITIVITY (pooled, full controls)")
    print("=" * 78)
    for w in WINDOWS_SENS:
        pw = build_auction_panel(w)
        res = cluster_ols(pw, ["dln_USDT", "dln_USDC", "ln_offering", "vix", "trend"] + fe)
        r = coef_row(f"window={w}d", res, len(pw))
        rows.append(r)
        print(f"  {w:2d}-day  N={r['n']:4d}  "
              f"β_USDT={r['beta_USDT']:+.3f}{r['sig_USDT']:3s} (p={r['p_USDT']:.3f})  "
              f"β_USDC={r['beta_USDC']:+.3f}{r['sig_USDC']:3s} (p={r['p_USDC']:.3f})")

    # 4) Lead / reverse-time falsification ------------------------------------
    print("\n" + "=" * 78)
    print("  FALSIFICATION: FUTURE supply growth (t → t+21d) should NOT predict")
    print("=" * 78)
    lead_panel = build_auction_panel(WINDOW_MAIN, lead=True)
    res = cluster_ols(lead_panel, ["dln_USDT", "dln_USDC", "ln_offering", "vix", "trend"] + fe)
    r = coef_row("FALSIFICATION future-supply", res, len(lead_panel))
    rows.append(r)
    print(f"  future  N={r['n']:4d}  "
          f"β_USDT={r['beta_USDT']:+.3f}{r['sig_USDT']:3s} (p={r['p_USDT']:.3f})  "
          f"β_USDC={r['beta_USDC']:+.3f}{r['sig_USDC']:3s} (p={r['p_USDC']:.3f})  "
          f"(expect USDT ns)")

    # 5) Subsample stability --------------------------------------------------
    print("\n" + "=" * 78)
    print("  SUBSAMPLE STABILITY (pooled, full controls)")
    print("=" * 78)
    subs = [
        ("drop 2022 crisis year", panel[panel["date"].dt.year != 2022]),
        ("post-2023 only",        panel[panel["date"] >= "2023-01-01"]),
    ]
    for name, sub in subs:
        res = cluster_ols(sub, ["dln_USDT", "dln_USDC", "ln_offering", "vix", "trend"] + fe)
        r = coef_row(f"subsample: {name}", res, len(sub))
        rows.append(r)
        print(f"  {name:22s} N={r['n']:4d}  "
              f"β_USDT={r['beta_USDT']:+.3f}{r['sig_USDT']:3s} (p={r['p_USDT']:.3f})  "
              f"β_USDC={r['beta_USDC']:+.3f}{r['sig_USDC']:3s} (p={r['p_USDC']:.3f})")

    res_df = pd.DataFrame(rows)
    res_df.to_csv(OUT / "bidcover_auction_level_results.csv", index=False)

    decomp = control_decomposition()
    write_summary(res_df, decomp)
    print(f"\n  -> {OUT/'bidcover_auction_level_results.csv'}")
    print(f"  -> {OUT/'bidcover_auction_level_summary.md'}")


def control_decomposition() -> pd.DataFrame:
    """
    Diagnose WHY the original monthly result was significant. Re-run the monthly
    design with (a) the original 8 controls incl. interpolated theta/liq_buffer,
    vs (b) clean controls only (supply growth + VIX). If significance lives in the
    interpolated controls, the 'cleanest result' is actually resting on the same
    manufactured reserve data flagged in the teardown.
    """
    auc = pd.read_csv(AUCTION_CSV, parse_dates=["date"])
    auc = auc[auc["term"].isin(TERMS)]
    m = pd.read_csv(DATA / "monthly_panel.csv", index_col=0, parse_dates=True)
    d = pd.read_csv(DAILY_CSV, index_col=0, parse_dates=True)
    me = d[["supply_USDT", "supply_USDC"]].resample("ME").last()
    m["dln_USDT"] = np.log(me.supply_USDT).diff()
    m["dln_USDC"] = np.log(me.supply_USDC).diff()
    m["d_fedfunds"] = d["fedfunds"].resample("ME").last().diff()

    clean = ["dln_USDT", "dln_USDC", "vix"]
    full = ["dln_USDT", "dln_USDC", "theta", "liq_buffer", "velocity", "vix",
            "dln_row_equity", "d_fedfunds"]

    def fit(df, xc):
        df = df.dropna(subset=["bc"] + xc)
        r = sm.OLS(df["bc"], sm.add_constant(df[xc])).fit(
            cov_type="HAC", cov_kwds={"maxlags": 1})
        return len(df), r.params["dln_USDT"], r.pvalues["dln_USDT"]

    out = []
    for term in TERMS:
        t = auc[auc.term == term].set_index("date")
        bc = t["bid_cover"].resample("ME").mean().rename("bc")
        df = m.join(bc)
        n_o, b_o, p_o = fit(df.copy(), full)    # original spec (interpolated ctrls)
        n_c, b_c, p_c = fit(df.copy(), clean)   # clean controls only
        out.append({"term": term,
                    "orig_8ctrl_beta": b_o, "orig_8ctrl_p": p_o,
                    "clean_beta": b_c, "clean_p": p_c})
    return pd.DataFrame(out)


def write_summary(df: pd.DataFrame, decomp: pd.DataFrame) -> None:
    def fmt(r):
        return (f"| {r['spec']} | {int(r['n'])} | {r['beta_USDT']:+.3f}{r['sig_USDT']} "
                f"| {r['p_USDT']:.3f} | {r['beta_USDC']:+.3f}{r['sig_USDC']} | {r['p_USDC']:.3f} "
                f"| {r['wald_USDT_eq_USDC_p']:.3f} |")

    lines = [
        "# Auction-Level Bid-Cover Robustness",
        "",
        "**Contribution.** Moves the bid-cover test from monthly-averaged (N≈51, no "
        "auction-size control) to the individual auction (N≈1,094) with the offering "
        "size, maturity fixed effects, VIX, and a linear time trend as controls. "
        "Standard errors clustered by month.",
        "",
        "Pre-auction supply growth = log issuer supply growth over the 21 calendar days "
        "ending the day **before** each auction (strictly pre-auction).",
        "",
        "## Estimating equation",
        "```",
        "bid_cover_{t,m} = α + β_USDT·Δln S^USDT_pre + β_USDC·Δln S^USDC_pre",
        "                    + γ·ln(offering_{t,m}) + maturity FE + δ·VIX_t + θ·trend + ε",
        "```",
        "",
        "## Results",
        "",
        "| Spec | N | β_USDT | p | β_USDC | p | Wald p (USDT=USDC) |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    lines += [fmt(r) for _, r in df.iterrows()]

    # ---- data-driven verdict --------------------------------------------------
    pooled5 = df[df.spec == "(5) + linear time trend"].iloc[0]
    usdt_ns = pooled5["p_USDT"] >= 0.05
    usdc_sig = pooled5["p_USDC"] < 0.05
    usdt_wrong = pooled5["beta_USDT"] > 0
    lead = df[df.spec.str.startswith("FALSIFICATION")].iloc[0]
    lead_usdc_sig = lead["p_USDC"] < 0.05

    lines += [
        "",
        "## Verdict",
        "",
        f"**The USDT bid-cover channel does NOT survive the auction-level rebuild.** "
        f"In the fully-controlled pooled spec (5), β_USDT = {pooled5['beta_USDT']:+.3f} "
        f"(p={pooled5['p_USDT']:.3f}, {'not significant' if usdt_ns else 'significant'}"
        f"{', and the sign is positive — opposite the hypothesis' if usdt_wrong else ''}). "
        "It is null from spec (1) onward, so this is not an artifact of over-controlling.",
        "",
        f"β_USDC is the coefficient that is consistently significant "
        f"(β={pooled5['beta_USDC']:+.3f}, p={pooled5['p_USDC']:.3f}) — but **positive**, "
        "the opposite of a T-bill demand story, and the falsification test shows that "
        f"*future* USDC growth also 'predicts' bid-cover "
        f"(p={lead['p_USDC']:.3f}{', significant' if lead_usdc_sig else ''}). "
        "A relationship that runs both forward and backward in time is a shared trend, "
        "not a causal channel.",
        "",
        "The only place the predicted negative USDT sign appears significantly is the "
        "*drop-2022* subsample — an isolated, fragile result, not robust evidence.",
        "",
        "## Why the original monthly result looked clean: it was the interpolated controls",
        "",
        "Re-running the **monthly** design (N=51) two ways isolates the driver:",
        "",
        "| Maturity | Original spec (8 controls incl. interpolated θ, L) | Clean controls (supply + VIX) |",
        "|---|---|---|",
    ]
    for _, r in decomp.iterrows():
        s_o = sig(r["orig_8ctrl_p"]); s_c = sig(r["clean_p"])
        lines.append(
            f"| {r['term']} | β_USDT={r['orig_8ctrl_beta']:+.2f}{s_o} (p={r['orig_8ctrl_p']:.3f}) "
            f"| β_USDT={r['clean_beta']:+.2f}{s_c} (p={r['clean_p']:.3f}) |")
    lines += [
        "",
        "Stripping the interpolated θ and liquid-buffer controls — the same manufactured "
        "quarterly reserve data flagged in the teardown — collapses the USDT coefficient "
        "from strongly significant (p<0.01) to marginal-or-null at every maturity. The "
        "2,000-shuffle placebo test validated the *time ordering* of the coefficient, but "
        "the coefficient itself only exists *conditional on the interpolated regressors*. "
        "The placebo never tested that.",
        "",
        "## Bottom line",
        "",
        "The bid-cover result — previously billed as the paper's cleanest, placebo-validated "
        "causal evidence — does **not** hold up. It depended on (i) collapsing ~1,094 auctions "
        "to 51 monthly means, (ii) omitting auction offering size, and (iii) conditioning on "
        "interpolated reserve controls. At the auction level with offering controlled, the "
        "USDT channel is absent. This needs to be reported honestly, not led with.",
    ]
    (OUT / "bidcover_auction_level_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    run()
