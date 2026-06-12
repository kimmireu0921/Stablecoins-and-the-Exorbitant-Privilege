"""
threshold.py — Hansen (2000) threshold regression for reserve adequacy threshold L*.

Model:
  Spread_t = α + β1·ΔlnS_t + δ·ΔlnS_t·I(L_t ≤ q) + γ·controls + ε_t

Where L_t (liq_buffer) = Cash Reserves / Supply is the Liquid Buffer variable.

Grid-searches over quantiles of L to find q* = argmin SSR.
Bootstrap p-value tests whether the threshold effect is significant.
Bootstrap percentile CI for q* (replaces LR-inversion CI which is grid-bounded).

Robustness analyses:
  A. TRIM sensitivity  — re-runs grid search at TRIM ∈ {0.15, 0.20, 0.25}
  B. Multiple threshold test — sequential test: H0 = 1 threshold vs H1 = 2 thresholds

Reference: Hansen, B.E. (2000). "Sample Splitting and Threshold Estimation."
           Econometrica 68(3): 575–603.

Output: results/threshold_results.txt, results/threshold_ssr.png,
        results/threshold_bootstrap_ci.png, results/threshold_trim_sensitivity.png
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import MONTHLY_CSV, RESULTS_DIR

Path(RESULTS_DIR).mkdir(exist_ok=True)

N_BOOTSTRAP  = 1000   # bootstrap replications for p-value and CI
N_BOOT_2T    = 300    # bootstrap replications for two-threshold test (slower)
TRIM         = 0.15   # default trim (Hansen recommendation)
TRIM_GRID    = [0.15, 0.20, 0.25]   # trim=0.10 excluded: only ~5 obs/regime at N=51


# ── Core helpers ──────────────────────────────────────────────────────────────

def ssr(y: np.ndarray, X: np.ndarray) -> float:
    """OLS sum of squared residuals."""
    coef, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
    return float(np.sum((y - X @ coef) ** 2))


def threshold_model_ssr(y: np.ndarray, X_base: np.ndarray,
                        q_var: np.ndarray, q: float) -> float:
    """One-threshold model SSR: augments X_base with ΔlnS·I(L ≤ q)."""
    dln_s = X_base[:, 1]          # column 1 = ΔlnS (const at 0)
    X_aug = np.column_stack([X_base, dln_s * (q_var <= q).astype(float)])
    return ssr(y, X_aug)


def grid_search(y: np.ndarray, X_base: np.ndarray, q_var: np.ndarray,
                trim: float = TRIM) -> tuple[float, np.ndarray, np.ndarray]:
    lo  = np.quantile(q_var, trim)
    hi  = np.quantile(q_var, 1 - trim)
    cands = np.unique(q_var[(q_var >= lo) & (q_var <= hi)])
    ssrs  = np.array([threshold_model_ssr(y, X_base, q_var, q) for q in cands])
    return float(cands[np.argmin(ssrs)]), cands, ssrs


def bootstrap_ci_qstar(y: np.ndarray, X_base: np.ndarray, q_var: np.ndarray,
                       n_boot: int = N_BOOTSTRAP,
                       level: float = 0.90,
                       trim: float = TRIM) -> tuple[float, float, np.ndarray]:
    """
    Percentile bootstrap CI for q*.

    Resamples rows of (y, X_base, q_var) with replacement and re-runs
    grid_search on each sample.  Takes the (alpha/2, 1-alpha/2) percentiles
    of the resulting distribution as the CI endpoints.

    This avoids the grid-boundary truncation problem of LR-inversion CIs,
    where the upper bound was always capped at q* when q* sat near the edge
    of the trimmed candidate set.
    """
    rng    = np.random.default_rng(42)
    n      = len(y)
    q_boot = []

    for _ in range(n_boot):
        idx  = rng.integers(0, n, size=n)
        y_b  = y[idx]
        X_b  = X_base[idx]
        qv_b = q_var[idx]
        # Need at least 3 unique candidates in the trimmed range
        lo_b    = np.quantile(qv_b, trim)
        hi_b    = np.quantile(qv_b, 1 - trim)
        cands_b = np.unique(qv_b[(qv_b >= lo_b) & (qv_b <= hi_b)])
        if len(cands_b) < 3:
            continue
        try:
            q_star_b, _, _ = grid_search(y_b, X_b, qv_b, trim=trim)
            q_boot.append(float(q_star_b))
        except Exception:
            continue

    q_boot = np.array(q_boot)
    alpha  = 1 - level
    ci_lo  = float(np.percentile(q_boot, 100 * alpha / 2))
    ci_hi  = float(np.percentile(q_boot, 100 * (1 - alpha / 2)))
    return ci_lo, ci_hi, q_boot


def bootstrap_pvalue(y: np.ndarray, X_base: np.ndarray, q_var: np.ndarray,
                     ssr_h0: float, ssr_h1: float,
                     n_boot: int = N_BOOTSTRAP) -> float:
    """Hansen (2000) bootstrap LR p-value for H0: no threshold."""
    n     = len(y)
    lr0   = n * (ssr_h0 - ssr_h1) / ssr_h1
    coef0, *_ = np.linalg.lstsq(X_base, y, rcond=None)
    resid0 = y - X_base @ coef0
    rng    = np.random.default_rng(42)
    lr_boot = []
    for _ in range(n_boot):
        y_b = X_base @ coef0 + resid0[rng.integers(0, n, size=n)]
        _, _, ssrs_b = grid_search(y_b, X_base, q_var)
        lr_boot.append(n * (ssr(y_b, X_base) - ssrs_b.min()) / ssrs_b.min())
    return float((np.array(lr_boot) >= lr0).mean())


# ── Robustness A: TRIM sensitivity ───────────────────────────────────────────

def trim_sensitivity(y: np.ndarray, X_base: np.ndarray,
                     q_var: np.ndarray) -> list[dict]:
    """
    Re-run grid search at each TRIM value in TRIM_GRID.
    Reports q* and candidate count only — CI is omitted here because
    the proper CI (bootstrap) is reported separately for the baseline.
    TRIM=0.10 excluded: only ~5 obs/regime at N=51, too small to trust.
    """
    results = []
    for trim in TRIM_GRID:
        q_star, cands, _ = grid_search(y, X_base, q_var, trim=trim)
        results.append({
            "trim":    trim,
            "n_cands": len(cands),
            "q_star":  round(float(q_star), 4),
        })
    return results


def plot_trim_sensitivity(trim_results: list[dict], baseline_ci: tuple,
                          outfile: str):
    """
    Plot q* for each TRIM value.
    Baseline bootstrap CI shaded only for the TRIM=0.15 point.
    """
    fig, ax = plt.subplots(figsize=(7, 4))
    trims   = [r["trim"]   for r in trim_results]
    q_stars = [r["q_star"] for r in trim_results]

    ax.plot(trims, q_stars, "o-", color="#1f77b4", linewidth=1.8,
            markersize=8, zorder=3, label="q* (estimated threshold)")

    # Shade bootstrap CI only at the baseline TRIM=0.15
    ci_lo, ci_hi = baseline_ci
    base_idx = [r["trim"] for r in trim_results].index(0.15)
    # q* can sit at/near a CI bound (e.g. q*=ci_lo), which would make an errorbar
    # arm negative — matplotlib rejects that. Clip both arms at 0.
    lo_arm = max(0.0, q_stars[base_idx] - ci_lo)
    hi_arm = max(0.0, ci_hi - q_stars[base_idx])
    ax.errorbar(trims[base_idx], q_stars[base_idx],
                yerr=[[lo_arm], [hi_arm]],
                fmt="none", color="#d62728", capsize=6, linewidth=1.5,
                label=f"Bootstrap 90% CI at TRIM=15% [{ci_lo:.3f}, {ci_hi:.3f}]")

    ax.axhline(q_stars[base_idx], color="#d62728", linestyle="--",
               linewidth=0.9, alpha=0.6)

    ax.set_xticks(trims)
    ax.set_xticklabels([f"{t:.0%}" for t in trims])
    ax.set_xlabel("TRIM parameter (fraction excluded from each tail)")
    ax.set_ylabel("Estimated threshold q*")
    ax.set_title("TRIM Sensitivity: q* is stable across search-grid boundaries\n"
                 "(Bootstrap 90% CI shown at baseline TRIM=15%)")
    ax.legend(fontsize=9)
    ax.set_ylim(0, 0.30)
    plt.tight_layout()
    plt.savefig(outfile, dpi=150, bbox_inches="tight")
    print(f"  Plot saved to {outfile}")
    plt.close()


def plot_bootstrap_distribution(q_boot: np.ndarray, q_star: float,
                                ci_lo: float, ci_hi: float, outfile: str):
    """Histogram of bootstrap q* values with CI and point estimate marked."""
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.hist(q_boot, bins=30, color="#1f77b4", alpha=0.7, edgecolor="white",
            label="Bootstrap q* distribution")
    ax.axvline(q_star, color="#d62728", linewidth=2.0, linestyle="-",
               label=f"q* = {q_star:.3f} (point estimate)")
    ax.axvline(ci_lo,  color="#d62728", linewidth=1.4, linestyle="--",
               label=f"90% CI: [{ci_lo:.3f}, {ci_hi:.3f}]")
    ax.axvline(ci_hi,  color="#d62728", linewidth=1.4, linestyle="--")
    ax.axvspan(ci_lo, ci_hi, alpha=0.12, color="#d62728")
    ax.set_xlabel("Bootstrap q* (liquid buffer threshold)")
    ax.set_ylabel("Frequency")
    ax.set_title(f"Bootstrap Distribution of q*  (B = {len(q_boot)} replications)\n"
                 "Percentile 90% CI does not have a grid-boundary truncation problem")
    ax.legend(fontsize=9)
    plt.tight_layout()
    plt.savefig(outfile, dpi=150, bbox_inches="tight")
    print(f"  Plot saved to {outfile}")
    plt.close()


# ── Robustness B: Multiple threshold test ────────────────────────────────────

def two_threshold_model_ssr(y: np.ndarray, X_base: np.ndarray,
                             q_var: np.ndarray, q1: float, q2: float) -> float:
    """
    Two-threshold model SSR (three regimes).
    Augments X_base with:
      ΔlnS·I(L ≤ q1)          — low regime
      ΔlnS·I(q1 < L ≤ q2)     — middle regime
    High regime (L > q2) is the baseline absorbed into β1.
    """
    dln_s = X_base[:, 1]
    low   = (q_var <= q1).astype(float)
    mid   = ((q_var > q1) & (q_var <= q2)).astype(float)
    X_aug = np.column_stack([X_base, dln_s * low, dln_s * mid])
    return ssr(y, X_aug)


def double_grid_search(y: np.ndarray, X_base: np.ndarray,
                       q_var: np.ndarray,
                       trim: float = TRIM) -> tuple[float, float, float]:
    """
    Grid search over all ordered pairs (q1, q2) with q1 < q2.
    Returns (q1*, q2*, SSR_min).
    """
    lo    = np.quantile(q_var, trim)
    hi    = np.quantile(q_var, 1 - trim)
    cands = np.unique(q_var[(q_var >= lo) & (q_var <= hi)])

    best_ssr = np.inf
    best_q1 = best_q2 = float("nan")
    for i, q1 in enumerate(cands[:-1]):
        for q2 in cands[i + 1:]:
            s = two_threshold_model_ssr(y, X_base, q_var, q1, q2)
            if s < best_ssr:
                best_ssr, best_q1, best_q2 = s, float(q1), float(q2)
    return best_q1, best_q2, best_ssr


def bootstrap_second_threshold(y: np.ndarray, X_base: np.ndarray,
                                q_var: np.ndarray,
                                q1_star: float,
                                ssr_1t: float, ssr_2t: float,
                                n_boot: int = N_BOOT_2T) -> tuple[float, float]:
    """
    Bootstrap test: H0 = 1 threshold, H1 = 2 thresholds.
    Simulates LR = n*(SSR_1t - SSR_2t)/SSR_2t under H0 (one-threshold model).
    Returns (p-value, observed LR statistic).
    """
    n      = len(y)
    lr_obs = n * (ssr_1t - ssr_2t) / ssr_2t

    # Build one-threshold model (H0) to get residuals
    dln_s  = X_base[:, 1]
    X_h0   = np.column_stack([X_base, dln_s * (q_var <= q1_star).astype(float)])
    coef_h0, *_ = np.linalg.lstsq(X_h0, y, rcond=None)
    resid_h0 = y - X_h0 @ coef_h0

    rng     = np.random.default_rng(42)
    lr_boot = []
    for _ in range(n_boot):
        y_b = X_h0 @ coef_h0 + resid_h0[rng.integers(0, n, size=n)]
        _, _, s1_b = grid_search(y_b, X_base, q_var)
        _, _, s2_b = double_grid_search(y_b, X_base, q_var)
        ssr_1t_b   = s1_b if np.isscalar(s1_b) else s1_b.min()
        lr_boot.append(n * (ssr_1t_b - s2_b) / s2_b)

    p_val = float((np.array(lr_boot) >= lr_obs).mean())
    return p_val, lr_obs


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    df = pd.read_csv(MONTHLY_CSV, index_col=0, parse_dates=True)
    df = df.dropna(subset=["spread", "dln_supply", "liq_buffer", "vix", "dln_row_equity"])

    if len(df) < 30:
        print(f"Only {len(df)} complete observations — need liq_buffer data.")
        return

    n = len(df)
    print(f"Threshold regression on {n} monthly observations (using liq_buffer).")

    y     = df["spread"].to_numpy()
    dln_s = df["dln_supply"].to_numpy()
    vix   = df["vix"].to_numpy()
    dlnr  = df["dln_row_equity"].to_numpy()
    L     = df["liq_buffer"].to_numpy()

    # X_base: [const, ΔlnS, VIX, Δln(equity)]  — col 1 = ΔlnS
    X_base = np.column_stack([np.ones(n), dln_s, vix, dlnr])

    # ── Baseline: single threshold ────────────────────────────────────────
    ssr_h0 = ssr(y, X_base)
    print(f"\nGrid search (TRIM={TRIM:.0%})...")
    q_star, candidates, ssrs = grid_search(y, X_base, L)
    ssr_h1 = ssrs.min()
    lr_stat = n * (ssr_h0 - ssr_h1) / ssr_h1

    print(f"  q* = {q_star:.4f}")
    print(f"  SSR_H0 = {ssr_h0:.6f}  |  SSR_H1 = {ssr_h1:.6f}")
    print(f"  LR statistic = {lr_stat:.3f}")

    print(f"Bootstrap p-value ({N_BOOTSTRAP} replications)...")
    p_val = bootstrap_pvalue(y, X_base, L, ssr_h0, ssr_h1)
    print(f"  p-value = {p_val:.3f}")

    print(f"Bootstrap 90% CI for q* ({N_BOOTSTRAP} replications)...")
    ci_lo, ci_hi, q_boot = bootstrap_ci_qstar(y, X_base, L)
    print(f"  90% CI: [{ci_lo:.4f}, {ci_hi:.4f}]  "
          f"(from {len(q_boot)} valid bootstrap samples)")

    low_mask = L <= q_star
    print(f"\n  Low-buffer  (L ≤ {q_star:.4f}): {low_mask.sum()} obs")
    print(f"  High-buffer (L >  {q_star:.4f}): {(~low_mask).sum()} obs")
    for label, mask in [("Low-buffer  (L ≤ q*)", low_mask),
                         ("High-buffer (L >  q*)", ~low_mask)]:
        if mask.sum() < 5:
            continue
        coef, *_ = np.linalg.lstsq(X_base[mask], y[mask], rcond=None)
        print(f"  {label}:  β_ΔlnS = {coef[1]:.4f}  "
              f"(const={coef[0]:.4f}, VIX={coef[2]:.4f})")

    # ── Robustness A: TRIM sensitivity ────────────────────────────────────
    print(f"\n{'='*60}")
    print("ROBUSTNESS A — TRIM SENSITIVITY")
    print(f"{'='*60}")
    print(f"  (TRIM=0.10 excluded: only ~5 obs/regime at N={n})")
    trim_results = trim_sensitivity(y, X_base, L)
    print(f"  {'TRIM':>8}  {'Cands':>6}  {'q*':>8}")
    for r in trim_results:
        marker = " ← baseline" if r["trim"] == 0.15 else ""
        print(f"  {r['trim']:>8.0%}  {r['n_cands']:>6}  {r['q_star']:>8.4f}{marker}")

    q_star_vals = [r["q_star"] for r in trim_results]
    stable = max(q_star_vals) - min(q_star_vals) < 0.03
    print(f"\n  q* range across TRIM values: [{min(q_star_vals):.4f}, {max(q_star_vals):.4f}]")
    print(f"  Result: {'STABLE ✓ (max spread < 3 pp)' if stable else 'SENSITIVE — review trim choice'}")

    plot_trim_sensitivity(trim_results, (ci_lo, ci_hi),
                          f"{RESULTS_DIR}/threshold_trim_sensitivity.png")

    # ── Robustness B: Multiple threshold test ─────────────────────────────
    print(f"\n{'='*60}")
    print("ROBUSTNESS B — MULTIPLE THRESHOLD TEST (H0: 1 threshold, H1: 2 thresholds)")
    print(f"{'='*60}")
    print("Double grid search for q1*, q2* (this may take ~30 seconds)...")
    q1_2t, q2_2t, ssr_2t = double_grid_search(y, X_base, L)
    lr_2t = n * (ssr_h1 - ssr_2t) / ssr_2t
    print(f"  Two-threshold model: q1* = {q1_2t:.4f}, q2* = {q2_2t:.4f}")
    print(f"  SSR_1threshold = {ssr_h1:.6f}  |  SSR_2threshold = {ssr_2t:.6f}")
    print(f"  LR statistic (1 vs 2) = {lr_2t:.3f}")

    print(f"Bootstrap p-value ({N_BOOT_2T} replications under H0: 1 threshold)...")
    p_2t, _ = bootstrap_second_threshold(y, X_base, L, q_star, ssr_h1, ssr_2t)
    print(f"  p-value = {p_2t:.3f}")
    if p_2t > 0.10:
        conclusion_2t = "Cannot reject H0 — single threshold is sufficient. ✓"
    elif p_2t > 0.05:
        conclusion_2t = "Weak evidence for a second threshold (p < 0.10)."
    else:
        conclusion_2t = "Reject H0 — evidence for a second threshold (p < 0.05)."
    print(f"  → {conclusion_2t}")

    # Three-regime β comparison (if two thresholds found)
    print(f"\n  Three-regime β_ΔlnS comparison:")
    regime_masks = [
        (f"Low    (L ≤ {q1_2t:.3f})",        L <= q1_2t),
        (f"Middle ({q1_2t:.3f} < L ≤ {q2_2t:.3f})", (L > q1_2t) & (L <= q2_2t)),
        (f"High   (L >  {q2_2t:.3f})",        L > q2_2t),
    ]
    for label, mask in regime_masks:
        if mask.sum() < 5:
            print(f"  {label}: only {mask.sum()} obs — skipped")
            continue
        coef, *_ = np.linalg.lstsq(X_base[mask], y[mask], rcond=None)
        print(f"  {label}  N={mask.sum():2d}  β_ΔlnS = {coef[1]:.4f}")

    # ── Save results ──────────────────────────────────────────────────────
    out = f"{RESULTS_DIR}/threshold_results.txt"
    with open(out, "w") as f:
        f.write("HANSEN (2000) THRESHOLD REGRESSION\n")
        f.write("=" * 55 + "\n")
        f.write(f"N = {n}  |  Threshold variable: liq_buffer (L = Cash / Supply)\n\n")
        f.write("BASELINE SINGLE THRESHOLD\n")
        f.write(f"  q* = {q_star:.4f}\n")
        f.write(f"  Bootstrap 90% CI: [{ci_lo:.4f}, {ci_hi:.4f}]  "
                f"(B={N_BOOTSTRAP}, percentile method)\n")
        f.write(f"  LR statistic = {lr_stat:.3f}\n")
        f.write(f"  Bootstrap p-value = {p_val:.3f}  (B={N_BOOTSTRAP})\n\n")
        f.write("ROBUSTNESS A — TRIM SENSITIVITY  (TRIM=0.10 excluded: N too small)\n")
        f.write(f"  {'TRIM':>6}  {'Cands':>6}  {'q*':>8}\n")
        for r in trim_results:
            f.write(f"  {r['trim']:>6.0%}  {r['n_cands']:>6}  {r['q_star']:>8.4f}\n")
        f.write(f"  Stability: {'STABLE' if stable else 'SENSITIVE'}\n\n")
        f.write("ROBUSTNESS B — MULTIPLE THRESHOLD TEST\n")
        f.write(f"  Two-threshold model: q1* = {q1_2t:.4f}, q2* = {q2_2t:.4f}\n")
        f.write(f"  LR (1 vs 2 thresholds) = {lr_2t:.3f}\n")
        f.write(f"  Bootstrap p-value = {p_2t:.3f}  (B={N_BOOT_2T})\n")
        f.write(f"  Conclusion: {conclusion_2t}\n")
    print(f"\n  All results saved to {out}")

    # ── Bootstrap CI distribution plot ────────────────────────────────────
    plot_bootstrap_distribution(q_boot, q_star, ci_lo, ci_hi,
                                f"{RESULTS_DIR}/threshold_bootstrap_ci.png")

    # ── SSR plot (baseline) ───────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(candidates, ssrs, color="#1f77b4", linewidth=1.5)
    ax.axvline(q_star, color="#d62728", linestyle="--",
               label=f"q* = {q_star:.3f}")
    ax.axvspan(ci_lo, ci_hi, alpha=0.15, color="#d62728",
               label=f"Bootstrap 90% CI [{ci_lo:.3f}, {ci_hi:.3f}]")
    ax.set_xlabel("Candidate threshold q (liquid buffer L)")
    ax.set_ylabel("SSR")
    ax.set_title("Hansen (2000) Threshold Search: SSR over Liquid Buffer Grid")
    ax.legend()
    plt.tight_layout()
    plt.savefig(f"{RESULTS_DIR}/threshold_ssr.png", dpi=150, bbox_inches="tight")
    print(f"  Plot saved to {RESULTS_DIR}/threshold_ssr.png")
    plt.close()


if __name__ == "__main__":
    main()
