"""
star.py — Logistic Smooth Transition Regression (LSTAR) robustness check.

Hansen (2000) assumes the regime switch at q* is sharp (binary: in or out).
LSTAR replaces that binary indicator with a smooth logistic transition function:

  G(L; γ, c) = 1 / (1 + exp(γ · (L − c)))       [inverted logistic]

  → G → 1  when L << c  (deep in the low-buffer regime)
  → G = 0.5 exactly at L = c  (transition midpoint)
  → G → 0  when L >> c  (deep in the high-buffer regime)

So the full LSTAR model is:

  Spread_t = α + β₁·ΔlnS_t + δ·ΔlnS_t·G(L_t; γ, c) + β_ctrl·controls + ε_t

Parameters:
  c  — transition midpoint (analogous to q* in Hansen)
  γ  — sharpness (γ → ∞ recovers the Hansen sharp switch; small γ = gradual)

γ is estimated in units of 1/std(L) so it is scale-free and interpretable:
  γ = 1  → transition spans roughly one full std(L) — very gradual
  γ = 5  → moderate sharpness
  γ = 20 → sharp, close to Hansen

Convergent validity: if c* ≈ q* = 0.130, the 13% threshold is robust to
the sharp-switch assumption.

Reference: Teräsvirta, T. (1994). "Specification, Estimation, and Evaluation
           of Smooth Transition Autoregressive Models." JASA 89(425): 208-218.

Outputs: results/star_results.txt, results/star_transition.png
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from pathlib import Path

from config import MONTHLY_CSV, RESULTS_DIR

Path(RESULTS_DIR).mkdir(exist_ok=True)

HANSEN_Q_STAR = 0.1301    # from threshold.py — for comparison
N_BOOT        = 500       # bootstrap replications for CI on c*
TRIM          = 0.15


# ── Helpers ───────────────────────────────────────────────────────────────────

def ssr(y: np.ndarray, X: np.ndarray) -> float:
    coef, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
    return float(np.sum((y - X @ coef) ** 2))


def logistic_G(L: np.ndarray, gamma: float, c: float,
               L_std: float) -> np.ndarray:
    """
    Inverted logistic: G → 1 at L << c, G → 0 at L >> c.
    gamma is in units of 1/std(L) (scale-free).
    """
    return 1.0 / (1.0 + np.exp(gamma * (L - c) / L_std))


def star_ssr(gamma: float, c: float,
             y: np.ndarray, X_base: np.ndarray,
             L: np.ndarray, L_std: float) -> float:
    """SSR of the LSTAR model at given (gamma, c)."""
    G     = logistic_G(L, gamma, c, L_std)
    dln_s = X_base[:, 1]
    X_aug = np.column_stack([X_base, dln_s * G])
    return ssr(y, X_aug)


# ── Profile likelihood grid search ────────────────────────────────────────────

def profile_grid_search(y: np.ndarray, X_base: np.ndarray,
                        L: np.ndarray, L_std: float,
                        trim: float = TRIM
                        ) -> tuple[float, float, float]:
    """
    Search over a grid of (gamma, c) pairs.
    gamma_grid: scale-free values (1/std units) from gradual to near-sharp.
    c_grid: trimmed interior of L's distribution.
    Returns (gamma*, c*, min_SSR).
    """
    gamma_grid = np.array([1, 2, 5, 10, 20, 50])
    c_lo  = np.quantile(L, trim)
    c_hi  = np.quantile(L, 1 - trim)
    # Use unique observed L values in the trimmed range as c candidates
    # (matches Hansen's approach so comparison is fair)
    c_grid = np.unique(L[(L >= c_lo) & (L <= c_hi)])
    if len(c_grid) < 3:
        c_grid = np.linspace(c_lo, c_hi, 20)

    best_ssr_val = np.inf
    best_gamma = best_c = float("nan")

    for gamma in gamma_grid:
        for c in c_grid:
            s = star_ssr(gamma, c, y, X_base, L, L_std)
            if s < best_ssr_val:
                best_ssr_val = s
                best_gamma, best_c = float(gamma), float(c)

    return best_gamma, best_c, best_ssr_val


def refine_with_nlls(gamma0: float, c0: float,
                     y: np.ndarray, X_base: np.ndarray,
                     L: np.ndarray, L_std: float) -> tuple[float, float, float]:
    """
    Refine grid-search estimates with Nelder-Mead NLLS optimisation.
    Returns (gamma*, c*, min_SSR).
    """
    def obj(params):
        g, c = params
        if g <= 0:          # gamma must be positive
            return 1e10
        return star_ssr(g, c, y, X_base, L, L_std)

    res = minimize(obj, x0=[gamma0, c0], method="Nelder-Mead",
                   options={"xatol": 1e-6, "fatol": 1e-8, "maxiter": 5000})
    gamma_star, c_star = res.x
    return float(gamma_star), float(c_star), float(res.fun)


# ── Regime-specific β at the optimum ─────────────────────────────────────────

def regime_betas(gamma: float, c: float,
                 y: np.ndarray, X_base: np.ndarray,
                 L: np.ndarray, L_std: float) -> dict:
    """
    Return OLS coefficients from the LSTAR model at (gamma*, c*).
    Also computes the effective β_ΔlnS at L=0 (pure low-buffer)
    and L=max (pure high-buffer).
    """
    G     = logistic_G(L, gamma, c, L_std)
    dln_s = X_base[:, 1]
    X_aug = np.column_stack([X_base, dln_s * G])
    coef, _, _, _ = np.linalg.lstsq(X_aug, y, rcond=None)
    beta1 = coef[1]   # coefficient on ΔlnS (high-buffer baseline, G→0)
    delta = coef[-1]  # coefficient on ΔlnS·G (extra low-buffer effect)

    # Effective β at G=1 (L<<c, low buffer) and G=0 (L>>c, high buffer)
    beta_low  = beta1 + delta   # G=1
    beta_high = beta1           # G=0
    return {"beta1": beta1, "delta": delta,
            "beta_low": beta_low, "beta_high": beta_high,
            "coef_full": coef}


# ── Bootstrap CI for c* ───────────────────────────────────────────────────────

def bootstrap_ci_c(gamma_star: float,
                   y: np.ndarray, X_base: np.ndarray,
                   L: np.ndarray, L_std: float,
                   n_boot: int = N_BOOT) -> tuple[float, float, np.ndarray]:
    """
    Percentile bootstrap 90% CI for c*.
    Fixes gamma at gamma_star (profile bootstrap) and re-estimates c only,
    keeping the grid search efficient.
    """
    rng    = np.random.default_rng(42)
    n      = len(y)
    c_boot = []

    for _ in range(n_boot):
        idx  = rng.integers(0, n, size=n)
        y_b  = y[idx]
        X_b  = X_base[idx]
        L_b  = L[idx]

        # Grid search over c only (gamma fixed at gamma_star)
        c_lo  = np.quantile(L_b, TRIM)
        c_hi  = np.quantile(L_b, 1 - TRIM)
        cands = np.unique(L_b[(L_b >= c_lo) & (L_b <= c_hi)])
        if len(cands) < 3:
            continue

        best_s = np.inf
        best_c = float("nan")
        for c in cands:
            s = star_ssr(gamma_star, c, y_b, X_b, L_b, L_std)
            if s < best_s:
                best_s, best_c = s, float(c)
        c_boot.append(best_c)

    c_boot = np.array(c_boot)
    ci_lo  = float(np.percentile(c_boot, 5))
    ci_hi  = float(np.percentile(c_boot, 95))
    return ci_lo, ci_hi, c_boot


# ── Plots ─────────────────────────────────────────────────────────────────────

def plot_star(gamma_star: float, c_star: float,
              beta1: float, delta: float,
              L: np.ndarray, L_std: float,
              ci_lo: float, ci_hi: float,
              outfile: str):
    """
    Two-panel figure:
      Left:  G(L; γ*, c*) — the smooth transition function
      Right: Effective β_ΔlnS(L) = β₁ + δ·G(L) — how the effect varies with buffer
    """
    L_grid = np.linspace(0, L.max() + 0.02, 300)
    G_grid = logistic_G(L_grid, gamma_star, c_star, L_std)
    beta_grid = beta1 + delta * G_grid

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))

    # ── Left: transition function ──────────────────────────────────────────
    ax1.plot(L_grid, G_grid, color="#1f77b4", linewidth=2.0,
             label=f"G(L; γ*={gamma_star:.1f}, c*={c_star:.3f})")
    ax1.axvline(c_star, color="#d62728", linestyle="--", linewidth=1.4,
                label=f"c* = {c_star:.3f}  (LSTAR midpoint)")
    ax1.axvline(HANSEN_Q_STAR, color="darkorange", linestyle=":",
                linewidth=1.4, label=f"q* = {HANSEN_Q_STAR:.3f}  (Hansen sharp)")
    ax1.axvspan(ci_lo, ci_hi, alpha=0.12, color="#d62728",
                label=f"Bootstrap 90% CI c* [{ci_lo:.3f}, {ci_hi:.3f}]")
    ax1.axhline(0.5, color="gray", linewidth=0.7, linestyle="--", alpha=0.5)
    ax1.scatter(L, np.zeros_like(L) - 0.04, color="#1f77b4",
                alpha=0.4, s=20, zorder=3, label="Observed L values")
    ax1.set_xlabel("Liquid buffer L = Cash / Supply")
    ax1.set_ylabel("G(L)  — regime weight  [0 = high-buffer, 1 = low-buffer]")
    ax1.set_title("LSTAR Transition Function")
    ax1.set_ylim(-0.12, 1.08)
    ax1.legend(fontsize=8)

    # ── Right: effective β_ΔlnS ───────────────────────────────────────────
    ax2.plot(L_grid, beta_grid, color="#2ca02c", linewidth=2.0,
             label="Effective β_ΔlnS(L) = β₁ + δ·G(L)")
    ax2.axvline(c_star, color="#d62728", linestyle="--", linewidth=1.4,
                label=f"c* = {c_star:.3f}")
    ax2.axvline(HANSEN_Q_STAR, color="darkorange", linestyle=":",
                linewidth=1.4, label=f"q* = {HANSEN_Q_STAR:.3f}  (Hansen)")
    ax2.axhline(0, color="black", linewidth=0.6, alpha=0.5)
    ax2.fill_between(L_grid, beta_grid, 0,
                     where=(beta_grid < 0), alpha=0.08, color="#2ca02c",
                     label="Privilege amplification zone (β < 0)")
    ax2.set_xlabel("Liquid buffer L = Cash / Supply")
    ax2.set_ylabel("Effective β_ΔlnS (bps per σ supply growth)")
    ax2.set_title("Effective Supply Effect Across Buffer Levels")
    ax2.legend(fontsize=8)

    plt.suptitle(
        f"LSTAR Robustness Check  |  γ* = {gamma_star:.1f}  ·  c* = {c_star:.3f}  "
        f"(Hansen q* = {HANSEN_Q_STAR:.3f})",
        fontsize=11, fontweight="bold"
    )
    plt.tight_layout()
    plt.savefig(outfile, dpi=150, bbox_inches="tight")
    print(f"  Plot saved to {outfile}")
    plt.close()


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    df = pd.read_csv(MONTHLY_CSV, index_col=0, parse_dates=True)
    df = df.dropna(subset=["spread", "dln_supply", "liq_buffer", "vix", "dln_row_equity"])

    if len(df) < 30:
        print("Insufficient observations — fill liq_buffer data first.")
        return

    n = len(df)
    print(f"LSTAR regression on {n} monthly observations.\n")

    y     = df["spread"].to_numpy()
    dln_s = df["dln_supply"].to_numpy()
    vix   = df["vix"].to_numpy()
    dlnr  = df["dln_row_equity"].to_numpy()
    L     = df["liq_buffer"].to_numpy()
    L_std = float(L.std())

    X_base = np.column_stack([np.ones(n), dln_s, vix, dlnr])

    print(f"L summary:  mean={L.mean():.4f}  std={L_std:.4f}  "
          f"min={L.min():.4f}  max={L.max():.4f}")
    print(f"γ is scaled by std(L) = {L_std:.4f} — so γ=1 spans ~1 std in L\n")

    # ── Step 1: profile grid search ───────────────────────────────────────
    print("Profile grid search over (γ, c)...")
    gamma0, c0, ssr0 = profile_grid_search(y, X_base, L, L_std)
    print(f"  Grid best:  γ = {gamma0:.1f},  c = {c0:.4f},  SSR = {ssr0:.6f}")

    # ── Step 2: NLLS refinement ───────────────────────────────────────────
    print("Refining with Nelder-Mead NLLS...")
    gamma_star, c_star, ssr_star = refine_with_nlls(gamma0, c0, y, X_base, L, L_std)
    print(f"  Final:      γ* = {gamma_star:.4f},  c* = {c_star:.4f},  SSR = {ssr_star:.6f}")

    # ── Step 3: regime betas ──────────────────────────────────────────────
    res = regime_betas(gamma_star, c_star, y, X_base, L, L_std)
    print(f"\n  β₁ (high-buffer baseline, G→0):  {res['beta_high']:+.4f}")
    print(f"  δ  (transition effect):           {res['delta']:+.4f}")
    print(f"  Effective β_ΔlnS at G=1 (low L):  {res['beta_low']:+.4f}")
    print(f"  Effective β_ΔlnS at G=0 (high L): {res['beta_high']:+.4f}")

    # ── Step 4: bootstrap CI for c* ───────────────────────────────────────
    print(f"\nBootstrap 90% CI for c* ({N_BOOT} replications, γ fixed at γ*)...")
    ci_lo, ci_hi, c_boot = bootstrap_ci_c(gamma_star, y, X_base, L, L_std)
    print(f"  90% CI for c*: [{ci_lo:.4f}, {ci_hi:.4f}]")

    # ── Step 5: comparison with Hansen ────────────────────────────────────
    diff      = abs(c_star - HANSEN_Q_STAR)
    in_ci     = ci_lo <= HANSEN_Q_STAR <= ci_hi
    converges = diff < 0.03

    print(f"\n{'='*55}")
    print("COMPARISON: LSTAR  vs  Hansen (2000)")
    print(f"{'='*55}")
    print(f"  Hansen q*     = {HANSEN_Q_STAR:.4f}  (sharp threshold)")
    print(f"  LSTAR c*      = {c_star:.4f}  (smooth midpoint)")
    print(f"  Difference    = {diff:.4f}")
    print(f"  Hansen q* inside LSTAR 90% CI: {'YES ✓' if in_ci else 'NO'}")
    if gamma_star > 20:
        sharpness = "near-sharp (close to Hansen binary switch)"
    elif gamma_star > 5:
        sharpness = "moderate — meaningful smooth transition"
    else:
        sharpness = "gradual — regime switch spans a wide buffer range"
    print(f"  Transition sharpness (γ*={gamma_star:.2f}): {sharpness}")

    if converges and in_ci:
        verdict = "CONVERGENT VALIDITY ✓ — both models locate the threshold near 13%."
    elif in_ci:
        verdict = "BROADLY CONSISTENT — Hansen q* within LSTAR CI, slight location difference."
    else:
        verdict = "DIVERGENT — models disagree on threshold location; investigate further."
    print(f"\n  Verdict: {verdict}")

    # ── Save results ──────────────────────────────────────────────────────
    out = f"{RESULTS_DIR}/star_results.txt"
    with open(out, "w") as f:
        f.write("LSTAR SMOOTH TRANSITION REGRESSION\n")
        f.write("=" * 55 + "\n")
        f.write(f"N = {n}  |  Transition variable: liq_buffer (L)\n")
        f.write(f"std(L) = {L_std:.4f}  (γ scaled by this)\n\n")
        f.write(f"γ*  = {gamma_star:.4f}\n")
        f.write(f"c*  = {c_star:.4f}\n")
        f.write(f"Bootstrap 90% CI for c*: [{ci_lo:.4f}, {ci_hi:.4f}]\n")
        f.write(f"SSR = {ssr_star:.6f}\n\n")
        f.write(f"β₁  (high-buffer, G→0):  {res['beta_high']:+.4f}\n")
        f.write(f"δ   (transition effect): {res['delta']:+.4f}\n")
        f.write(f"Effective β at G=1 (low buffer):  {res['beta_low']:+.4f}\n\n")
        f.write("COMPARISON WITH HANSEN (2000)\n")
        f.write(f"  Hansen q* = {HANSEN_Q_STAR:.4f}\n")
        f.write(f"  LSTAR c*  = {c_star:.4f}  (diff = {diff:.4f})\n")
        f.write(f"  Hansen q* in LSTAR CI: {'YES' if in_ci else 'NO'}\n")
        f.write(f"  Verdict: {verdict}\n")
    print(f"\n  Results saved to {out}")

    # ── Plot ──────────────────────────────────────────────────────────────
    plot_star(gamma_star, c_star, res["beta1"], res["delta"],
              L, L_std, ci_lo, ci_hi,
              f"{RESULTS_DIR}/star_transition.png")


if __name__ == "__main__":
    main()
