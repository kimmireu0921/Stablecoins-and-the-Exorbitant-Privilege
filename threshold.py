"""
threshold.py — Hansen (2000) threshold regression for reserve adequacy threshold B*.

Model:
  Spread_t = α + β1·ΔlnS_t + δ·ΔlnS_t·I(B_t ≤ q) + γ·controls + ε_t

Grid-searches over quantiles of B to find q* = argmin SSR.
Bootstrap p-value tests whether the threshold effect is significant.

Reference: Hansen, B.E. (2000). "Sample Splitting and Threshold Estimation."
           Econometrica 68(3): 575–603.

Output: results/threshold_results.txt, results/threshold_ssr.png
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from pathlib import Path

from config import MONTHLY_CSV, RESULTS_DIR

Path(RESULTS_DIR).mkdir(exist_ok=True)

N_BOOTSTRAP = 1000
TRIM        = 0.15     # trim 15% from each tail (Hansen recommendation)


def ssr(y: np.ndarray, X: np.ndarray) -> float:
    """OLS sum of squared residuals."""
    coef, res, _, _ = np.linalg.lstsq(X, y, rcond=None)
    fitted = X @ coef
    return float(np.sum((y - fitted) ** 2))


def threshold_model_ssr(y: np.ndarray, X_base: np.ndarray, q_var: np.ndarray, q: float) -> float:
    """
    For candidate threshold q, augment X with the split interaction ΔlnS·I(B≤q)
    and return SSR.
    """
    regime_low = (q_var <= q).astype(float)
    # First column of X_base assumed to be ΔlnS; add regime-interaction
    dln_s = X_base[:, 1]   # column index depends on build below
    X_aug = np.column_stack([X_base, dln_s * regime_low])
    return ssr(y, X_aug)


def grid_search(y: np.ndarray, X_base: np.ndarray, q_var: np.ndarray,
                trim: float = TRIM) -> tuple[float, np.ndarray, np.ndarray]:
    lo = np.quantile(q_var, trim)
    hi = np.quantile(q_var, 1 - trim)
    candidates = np.unique(q_var[(q_var >= lo) & (q_var <= hi)])
    ssrs = np.array([threshold_model_ssr(y, X_base, q_var, q) for q in candidates])
    q_star = candidates[np.argmin(ssrs)]
    return q_star, candidates, ssrs


def bootstrap_pvalue(y: np.ndarray, X_base: np.ndarray, q_var: np.ndarray,
                     ssr_h0: float, ssr_h1: float, n_boot: int = N_BOOTSTRAP) -> float:
    """
    Hansen (2000) bootstrap of the likelihood-ratio statistic
    LR = n*(SSR_H0 - SSR_H1) / SSR_H1
    under the null of no threshold effect.
    """
    n    = len(y)
    lr0  = n * (ssr_h0 - ssr_h1) / ssr_h1
    # Residuals under H0
    coef0, *_ = np.linalg.lstsq(X_base, y, rcond=None)
    resid0 = y - X_base @ coef0

    lr_boot = []
    rng = np.random.default_rng(42)
    for _ in range(n_boot):
        y_b   = X_base @ coef0 + resid0[rng.integers(0, n, size=n)]
        _, cands_b, ssrs_b = grid_search(y_b, X_base, q_var)
        ssr_h0_b = ssr(y_b, X_base)
        ssr_h1_b = ssrs_b.min()
        lr_boot.append(n * (ssr_h0_b - ssr_h1_b) / ssr_h1_b)

    lr_boot = np.array(lr_boot)
    p_val = float((lr_boot >= lr0).mean())
    return p_val


def confidence_interval(candidates: np.ndarray, ssrs: np.ndarray,
                        ssr_h1: float, n: int, level: float = 0.90) -> tuple[float, float]:
    """
    Approximate CI for q* via inversion of the LR statistic.
    Reject H0: q = q0 when LR(q0) > χ²(level) critical value.
    """
    from scipy.stats import chi2
    crit  = chi2.ppf(level, df=1)
    lr_q  = n * (ssrs - ssr_h1) / ssr_h1
    in_ci = candidates[lr_q <= crit]
    if len(in_ci) == 0:
        return float("nan"), float("nan")
    return float(in_ci.min()), float(in_ci.max())


def main():
    df = pd.read_csv(MONTHLY_CSV, index_col=0, parse_dates=True)
    df = df.dropna(subset=["spread", "dln_supply", "buffer_ratio", "vix", "dln_row_equity"])

    if len(df) < 30:
        print(f"Only {len(df)} complete observations after dropping NaN — need buffer_ratio data.")
        print("Fill data/reserve_attestations.csv first.")
        return

    print(f"Threshold regression on {len(df)} monthly observations.")

    # Variable arrays
    y     = df["spread"].to_numpy()
    dln_s = df["dln_supply"].to_numpy()
    vix   = df["vix"].to_numpy()
    dlnr  = df["dln_row_equity"].to_numpy()
    B     = df["buffer_ratio"].to_numpy()   # threshold variable

    # X_base: constant, ΔlnS, VIX, ΔlnN* (no split interaction)
    # Column order: const, dln_s, vix, dlnr — index 1 = dln_s (used in threshold_model_ssr)
    X_base = np.column_stack([np.ones(len(y)), dln_s, vix, dlnr])

    # ── H0: no threshold ───────────────────────────────────────────────────
    ssr_h0 = ssr(y, X_base)

    # ── Grid search for q* ─────────────────────────────────────────────────
    print(f"Grid search over buffer quantiles [{TRIM:.0%}, {1-TRIM:.0%}]...")
    q_star, candidates, ssrs = grid_search(y, X_base, B)
    ssr_h1 = ssrs.min()
    n = len(y)

    print(f"  q* = {q_star:.4f}  (buffer ratio)")
    print(f"  SSR_H0 = {ssr_h0:.6f}  |  SSR_H1 = {ssr_h1:.6f}")
    print(f"  LR statistic = {n * (ssr_h0 - ssr_h1) / ssr_h1:.3f}")

    # ── Bootstrap p-value ──────────────────────────────────────────────────
    print(f"Bootstrap p-value ({N_BOOTSTRAP} replications)...")
    p_val = bootstrap_pvalue(y, X_base, B, ssr_h0, ssr_h1)
    print(f"  p-value = {p_val:.3f}")

    # ── Confidence interval ────────────────────────────────────────────────
    ci_lo, ci_hi = confidence_interval(candidates, ssrs, ssr_h1, n)
    print(f"  90% CI for q*: [{ci_lo:.4f}, {ci_hi:.4f}]")

    # ── Regime-specific coefficients ──────────────────────────────────────
    low_mask  = B <= q_star
    high_mask = ~low_mask
    print(f"\n  Low-buffer regime (B ≤ {q_star:.4f}): {low_mask.sum()} obs")
    print(f"  High-buffer regime (B >  {q_star:.4f}): {high_mask.sum()} obs")

    for label, mask in [("Low-buffer (B ≤ q*)", low_mask), ("High-buffer (B > q*)", high_mask)]:
        if mask.sum() < 5:
            continue
        coef, *_ = np.linalg.lstsq(X_base[mask], y[mask], rcond=None)
        print(f"\n  {label}:  β_ΔlnS = {coef[1]:.4f}  (const={coef[0]:.4f}, VIX={coef[2]:.4f})")

    # ── Save results ───────────────────────────────────────────────────────
    out = f"{RESULTS_DIR}/threshold_results.txt"
    with open(out, "w") as f:
        f.write("HANSEN (2000) THRESHOLD REGRESSION\n")
        f.write("=" * 50 + "\n")
        f.write(f"Threshold variable: buffer_ratio (B)\n")
        f.write(f"N = {n}\n\n")
        f.write(f"Optimal threshold q* = {q_star:.4f}\n")
        f.write(f"90% CI: [{ci_lo:.4f}, {ci_hi:.4f}]\n")
        f.write(f"LR statistic = {n * (ssr_h0 - ssr_h1) / ssr_h1:.3f}\n")
        f.write(f"Bootstrap p-value = {p_val:.3f}  (B={N_BOOTSTRAP} replications)\n")
    print(f"\n  Results saved to {out}")

    # ── SSR plot ───────────────────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(candidates, ssrs, color="#1f77b4", linewidth=1.5)
    ax.axvline(q_star, color="#d62728", linestyle="--", label=f"q* = {q_star:.3f}")
    ax.axvspan(ci_lo, ci_hi, alpha=0.15, color="#d62728", label="90% CI")
    ax.set_xlabel("Candidate threshold q (buffer ratio B)")
    ax.set_ylabel("SSR")
    ax.set_title("Hansen (2000) Threshold Search: SSR over Buffer Ratio Grid")
    ax.legend()
    plt.tight_layout()
    png = f"{RESULTS_DIR}/threshold_ssr.png"
    plt.savefig(png, dpi=150, bbox_inches="tight")
    print(f"  Plot saved to {png}")


if __name__ == "__main__":
    main()
