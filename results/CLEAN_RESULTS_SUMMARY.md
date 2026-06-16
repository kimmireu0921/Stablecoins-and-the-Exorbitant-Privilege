> ⚠️ Historical snapshot — June 11, 2026. Numbers reflect Spec B (pre-offering-size control). Current final results are in README.md.

# Clean Results Summary — Stablecoins and the Exorbitant Privilege
**Date:** 2026-06-11  
**Prepared by:** Analysis pipeline (Steps 1–6)  
**Status:** All 6 steps completed. Reviewed against PROF_FEEDBACK_CHANGES.md.

---

## What we settled (no longer in dispute)

### Cointegration framework (Step 1)

The earlier Johansen result showing 2 cointegrating vectors was an artifact of including ΔlnS — which is already I(0) — in the Johansen system. Running Johansen correctly on only the two I(1) variables (spread and L) gives:

| Test | Statistic | CV 95% | Decision |
|---|---|---|---|
| Trace (r≤0) | 14.076 | 15.494 | Fail to reject |
| Max-eigenvalue (r≤0) | 13.612 | 14.264 | Fail to reject |

**Verdict: No cointegration.** This agrees with Engle-Granger (p=0.12). The levels regression is spurious. VAR in first differences is the correct framework — not VECM.

---

## Main regression (professor's corrected spec)

**Estimating equation:**
```
Spread_t = α + β₁·ΔlnS_t + β₃·L_t + β₄·(L_t × ΔlnS_t) + VIX + ΔlnN*
```

### Time series (N = 51)
| Coef | Variable | Estimate | p | Sig |
|---|---|---|---|---|
| β₁ | ΔlnS | +2.74 | 0.228 | ns |
| β₃ | L | +8.09 | <0.001 | *** |
| **β₄** | **L × ΔlnS** | **−35.89** | **0.032** | ** |
| R² | | 0.858 | | |

### Panel (issuer-month, N = 102)
| Coef | Variable | Estimate | p | Sig |
|---|---|---|---|---|
| β₁ | ΔlnS | +0.01 | 0.988 | ns |
| β₃ | L | +3.85 | <0.001 | *** |
| β₄ | L × ΔlnS | −7.45 | 0.293 | ns |

**Key open issue:** β₄ is significant in the time series but not in the panel. Also, β₄ < 0 is opposite to the original theoretical prediction (β₄ > 0 was predicted). Economic re-interpretation needed.

---

## Step 3: Does β₄ survive first-differencing?

**Estimating equation (first-difference):**
```
Δspread_it = β₁·ΔlnS_it + β₃·ΔL_it + β₄·(ΔL_it × ΔlnS_it) + ΔVIX + Δln_equity
```
Run on the issuer-level panel (N=100, 50 per issuer after first-differencing). SE clustered by month per professor's construction.

| Coef | Levels time-series | Levels panel | First-diff panel N=100 |
|---|---|---|---|
| β₁ | +2.74 (p=0.23) | +0.01 (p=0.99) | **+0.36 (p=0.16)** |
| β₃ | +8.09*** | +3.85*** | **+2.88 (p=0.019)** |
| β₄ | −35.89** | −7.45 (ns) | **+8.86 (p=0.31)** |

Note: the aggregate first-difference (N=50, single time series) gives β₄ = −48.97 (p=0.25). The panel (N=100) gives β₄ = +8.86 (p=0.31). **The sign flips between aggregate and panel.** Both are insignificant, but the instability itself is evidence that β₄ is meaningless.

**Verdict:**
- β₁ (privilege amplification): **spurious**. Vanishes after first-differencing regardless of specification.
- β₃ (liquid buffer): **robust**. Significant in levels (p<0.001) and in the panel first-diff (p=0.019). This is the only reliable result from the monthly regression.
- β₄ (interaction): **spurious and unstable**. Significant only in the levels time-series; vanishes and changes sign after first-differencing. The levels result (−35.89**) cannot be attributed to the buffer mechanism.

---

## Step 2: VAR / Granger / IRF (daily, N = 1,550)

**System:** [Δspread, dln_USDT, dln_USDC], all I(0), VAR(3) by BIC

### Granger causality
| Cause | Effect | VAR Wald χ² | df | p |
|---|---|---|---|---|
| dln_USDT | Δspread | 9.88 | 3 | **0.020** |
| dln_USDC | Δspread | 10.73 | 3 | **0.013** |

Both USDT and USDC Granger-cause spread changes. However, the USDC effect is at least as strong as USDT at short lags — which cuts against USDT-specific identification.

### Impulse response (VAR Cholesky, 1-std shock)
| | Day 1 | Cumulative (Day 20) | Direction |
|---|---|---|---|
| USDT → spread | −0.672 | +0.274 | Initial compression, then reversal |
| USDC → spread | +0.344 | +0.417 | Persistent widening |

**Interpretation:**
- USDT: day-1 response is consistent with the privilege story (supply growth → spread compression). But the cumulative 20-day effect is positive (spread widening) due to reversal at day 3.
- USDC: spread widening on impact, opposite of T-bill demand channel.
- Forecast Error Variance Decomposition: supply shocks explain only ~1.3% of spread variance (USDT=0.6%, USDC=0.7%). Economic magnitude is small.

**Verdict:** The IRF confirms a short-lived USDT compression channel, but the cumulative effect is ambiguous and the magnitude is very small. Use as suggestive evidence only.

---

## Step 4: Pre-auction window bid-cover

Testing whether supply growth in 3/5/10 days before each auction predicts bid-cover.

| Term | Window | β_USDT | p_USDT | β_USDC | p_USDC | Wald p |
|---|---|---|---|---|---|---|
| 13-Week | 10-day | −1.35 | 0.041** | +0.48 | 0.373 | 0.077* |
| 4-Week | 3/5/10-day | Positive (wrong direction) | — | — | — | — |
| 8-Week | All | Insignificant | — | — | — | — |
| 26-Week | All | Insignificant | — | — | — | — |

**Verdict:** Pre-auction window is noisier than the monthly design. Only 13-week at 10-day shows the correct sign. The existing monthly-averaged bid-cover regression remains the stronger design and should stay as the primary evidence. The pre-auction result is weak support for the mechanism channel.

---

## Step 5: Bid-cover placebo test (N = 2,000 shuffles)

The placebo shuffles the time index of USDT/USDC supply growth, breaking any genuine time-series relationship while preserving the distribution.

### β_USDT placebo p-values
| Maturity | Observed β | Placebo mean | p (one-sided) | Significant? |
|---|---|---|---|---|
| 4-Week | −1.14 | +0.00 | 0.027 | YES** |
| 8-Week | −1.54 | −0.00 | 0.003 | YES*** |
| 13-Week | −1.47 | −0.02 | 0.001 | YES*** |
| 26-Week | −1.68 | +0.01 | 0.001 | YES*** |

### Wald F-statistic placebo p-values (USDT ≠ USDC)
| Maturity | Observed F | Placebo p |
|---|---|---|
| 4-Week | 11.49 | 0.021** |
| 8-Week | 8.16 | 0.049** |
| 13-Week | 21.17 | 0.003*** |
| 26-Week | 16.58 | 0.015** |

**Verdict: The bid-cover result is not spurious.** The observed USDT effect sits far in the left tail of the null distribution at all 4 maturities. This is the paper's cleanest causal evidence.

---

## Summary table: what is and is not robust

| Claim | Method | Verdict |
|---|---|---|
| β₁ < 0: supply growth compresses spread | Monthly OLS (levels) | **SPURIOUS** — fails first-diff, spurious regression |
| β₄ interaction: buffer dampens transmission | Monthly OLS (levels) | **SPURIOUS** — fails first-diff |
| β₃: L level correlated with spread | Monthly OLS (levels + FD) | **ROBUST** — survives both specs; but may reflect common macro driver |
| USDT Granger-causes spread | Daily VAR(3) | **SUPPORTED** — p=0.020; but USDC also significant |
| USDT compresses spread short-run | IRF day-1 | **SUPPORTED** — but cumulative reversal; 1.3% FEVD |
| USDT suppresses T-bill bid-cover | Monthly bid-cover OLS | **ROBUST + PLACEBO-VALIDATED** — all 4 maturities, p<0.05 in placebo |
| USDT ≠ USDC for bid-cover | Wald test + placebo | **ROBUST** — all 4 maturities pass placebo |

---

## Recommended paper structure given these results

### Main argument (restructured)
The OIS–Treasury convenience yield is associated with stablecoin growth — but the mechanism runs through T-bill market microstructure, not the levels regression.

### Evidence hierarchy (strongest to weakest)
1. **Lead evidence (keep):** Bid-cover suppression. USDT supply growth → lower T-bill auction bid-cover at all 4 maturities (p<0.01). Wald: USDT ≠ USDC (p<0.004). Placebo-validated.
2. **Supporting (use cautiously):** Short-run USDT IRF. Day-1 compression of −0.67 pp per 1-std USDT shock. Small cumulative magnitude.
3. **Demote or report as robustness:** Monthly regression β₃ (L robustly correlated with spread, but likely macro-driven). Do not lead with this.
4. **Drop from main claims:** β₁ and β₄ from levels regression. Both spurious.

### Threshold model (Hansen / LSTAR)
The threshold result (q* moved from 13.0% → 6.6% after professor's corrections) is now fragile. Demote to appendix if β₄ itself is dropped from main evidence.

---

## Open team decisions (still unresolved)

1. **β₄ sign:** Why is β₄ < 0? If buffer dampens transmission, we predicted β₄ > 0. One interpretation: when L is high, supply growth occurs during already-strong reserve periods → spread is already compressed → marginal effect of growth is smaller (concave). But this needs a written economic argument.

2. **Panel vs. time series as headline:** Panel β₄ is not significant. The professor asked for panel. Which result leads the paper?

3. **USDC as a foil:** Granger causality shows USDC is at least as strong as USDT at short lags, which weakens the USDT-specific identification in the VAR. The bid-cover design preserves the USDT ≠ USDC distinction cleanly.

4. **Bid-cover as main evidence:** Given that β₁ and β₄ are spurious, should bid-cover become the primary result rather than supporting evidence? This is now the strongest thing in the paper.

---

## Files referenced
- [data/monthly_panel.csv](../data/monthly_panel.csv) — N=51 monthly observations
- [data/daily_panel.csv](../data/daily_panel.csv) — N=1,550 daily observations (Jan 2022–Mar 2026)
- [results/bidcover_auction_raw_rebuilt.csv](bidcover_auction_raw_rebuilt.csv) — raw auction data
- [results/bidcover_mechanism_validation_results.csv](bidcover_mechanism_validation_results.csv) — existing monthly bid-cover results
- [results/bidcover_preauction_window.csv](bidcover_preauction_window.csv) — Step 4 pre-auction results (NEW)
- [20260610_re/PROF_FEEDBACK_CHANGES.md](../20260610_re/PROF_FEEDBACK_CHANGES.md) — professor's corrections and deep-problem finding
