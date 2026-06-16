# Collaboration Note — Professor Hur Sewon

This file is written for Professor Hur. It summarizes where the research stands after applying your June feedback, why the results became insignificant, and what the open question is for potential collaboration.

---

## What We Applied from Your Feedback

From your written and oral feedback in June:

1. Treat each issuer as a separate observation — exploit the panel dimension (N: 51 → 102)
2. Do not combine treasury and liquid reserves (drop θ)
3. Keep L and L×ΔlnS; drop B×ΔlnS ("makes no sense")
4. Replace forward-fill with time-weighted linear interpolation for quarterly attestations
5. Show the estimating equation on every result slide

The estimating equation we now use:

```
Spreadₜ = α + β₁·ΔlnSₜ + β₃·Lₜ + β₄·(Lₜ × ΔlnSₜ) + γ·controls + εₜ
```

No theta. No B. Interaction uses L directly. The full record of code changes is in `0609_PROF_FEEDBACK_CHANGES.md`.

---

## Results After Applying Your Corrections

### Time series (N = 51)

| Coefficient | Value | p |
|---|---|---|
| β₁ (ΔlnS) | +2.74 | 0.228 |
| β₃ (L) | +8.09 | <0.001 *** |
| **β₄ (L × ΔlnS)** | **−35.89** | **0.032 **|

### Panel — issuer × month (N = 102)

| Coefficient | Value | p |
|---|---|---|
| β₁ (ΔlnS) | +0.01 | 0.988 |
| β₃ (L) | +3.85 | <0.001 *** |
| β₄ (L × ΔlnS) | −7.45 | 0.293 |

β₄ is significant in the time series but loses significance in the panel. β₁ is no longer negative.

---

## Why We Think the Results Are Insignificant — Spurious Regression

While investigating the sign reversals, we ran formal stationarity and cointegration tests. The conclusion is serious.

### Unit root tests (ADF)

| Variable | ADF p-value | Verdict |
|---|---|---|
| Spread (DGS3MO − SOFR) | 0.494 | I(1) — non-stationary |
| Liquid buffer L | 0.902 | I(1) — non-stationary |
| ΔlnS (supply growth) | 0.001 | I(0) — stationary |

### Cointegration (Engle-Granger)

| Pair | p-value | Verdict |
|---|---|---|
| Spread ~ L | 0.120 | No cointegration |
| Spread ~ θ | 0.733 | No cointegration |

Both the spread and L are I(1) and do not cointegrate. Regressing one on the other in levels is a textbook spurious regression.

### The smoking gun — first-differencing

Under Δspread = β·ΔlnS + ..., β₄ becomes **−107 (p = 0.46)** — collapses to insignificance. The level result was driven by a shared downward trend during the 2022–24 Fed hiking cycle, not a structural relationship.

```
spread:      2022 = +0.85 → 2024 = −0.30   (falling)
liq_buffer:  2022 =  0.19 → 2025 =  0.06   (falling)
```

Two trending series, same driver (Fed funds rate), high spurious correlation.

---

## Open Question for Collaboration

The buffer L hypothesis is still economically compelling — but it cannot be tested in a levels regression with the spread as the dependent variable.

**One viable path:** use the T-bill auction bid-cover ratio as the dependent variable instead. Bid-cover is stationary (mean-reverting around ~3.0), directly observable from Treasury auction data, and not affected by the spurious regression problem. The threshold interaction then becomes testable:

```
BC_{m,t} = αₘ + β_USDT·ΔlnS^USDT_t + β_USDC·ΔlnS^USDC_t
              + δₘ·ln(Offering_{m,t}) + γ₁·VIX_t + γ₂·Δfedfunds_t + εₜ
```

Separating USDT and USDC as distinct regressors allows us to test whether the effect is specific to Tether's reserve structure or common to all stablecoins. Maturity fixed effects (αₘ) absorb the level differences across the four auction maturities (4-, 8-, 13-, 26-week). The GENIUS Act's monthly disclosure requirement will also improve the quarterly attestation data going forward.

---

## How to Run the Code

```bash
git clone <repo URL>
cd stablecoin_research
pip install -r requirements.txt

# Rebuild the panel (time-weighted interpolation, your ⅔/⅓ correction)
python build_panel.py

# Main regression + panel
python analysis/regression.py        # → results/regression_main.txt, panel_regression.txt

# Stationarity and cointegration tests
python analysis/diagnostics.py       # → results/diagnostics.txt

# Hansen threshold on L
python analysis/threshold.py         # → results/threshold_results.txt

# LSTAR robustness
python analysis/star.py              # → results/star_results.txt
```

All raw outputs are already in `results/` from the team's last run. The full research evolution (Phase 1 → 2 → 3) is documented in `README.md`.
