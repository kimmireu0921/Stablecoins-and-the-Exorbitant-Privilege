# Stablecoins and the Exorbitant Privilege:
## A New Channel for Safe-Asset Demand and Its Systemic Fragility

Mireu Mimi Kim (2025462112) · Sara Ambre Chekroune (2025462014) · Oybek Ibragimov (2024462029)
Jade Zhu (2026846114) · Alexandre Godefroy (2026846111) · Baptiste Degand (2026847313) · Minjin Kim (2025461111)

**Yonsei GSIS — Topics in International Finance (2026-1) · Professor Hur Sewon · June 2026**

**JEL Classification:** E44, F31, G12, G18, G23

---

## Abstract

We examine whether large-scale USD-pegged stablecoins introduce a novel, two-sided form of systemic fragility — a "New Triffin Dilemma" — and whether the severity of downside risk depends critically on the adequacy of issuers' liquid reserve buffers. Extending Maggiori's (2017) two-country continuous-time framework to incorporate stablecoin supply *S*, Treasury exposure *θ* (T-bill holdings / supply), and liquid buffer *L* (cash and near-cash reserves / supply), we derive a testable reserve adequacy threshold below which forced Treasury liquidation generates measurable sovereign spillovers. Using an issuer-level panel of 102 observations (USDT and USDC, January 2022 – March 2026, with supply growth measured from DeFiLlama daily circulating supply), we estimate the main specification

*Spread_t = α + β₁·ΔlnS_it + β₃·L_it + β₄·(L_it × ΔlnS_it) + controls + issuer FE + ε_it*

The continuous-L interaction β₄ is not significant in the issuer panel (β₄ = −4.35, p = 0.68), consistent with the linear relationship being weak once supply growth is measured correctly and issuer fixed effects are included. However, focusing on nonlinear effects at very low buffer levels — consistent with the theory's prediction that the mechanism should concentrate near depletion — a threshold specification with ΔSpread as the dependent variable finds that the interaction term 1[L_it < 4%] × ΔlnS_it is significant (β₃ = −4.39, p = 0.001). This result does not appear at the 6% threshold (p = 0.64), suggesting the effect concentrates specifically at very low buffer states. We interpret this as suggestive evidence for a nonlinear liquidity-buffer channel: when Tether's liquid reserves fall below 4% of outstanding supply, supply growth is associated with significantly larger spread changes. These estimates should be interpreted cautiously, as all nine low-buffer observations come from USDT between mid-2025 and early 2026. A buffer-conditioned event study confirms the directional mechanism qualitatively. Liquid buffer *L* is constructed as Cash & Bank Deposits plus Money Market Funds (or Term Reverse Repos where MMF are absent) from BDO ISAE 3000R quarterly attestations, verified against source PDFs.

**Keywords:** stablecoins, exorbitant privilege, safe-asset demand, reserve adequacy, Triffin dilemma, OIS–Treasury spread, threshold regression, liquidity buffer

---

## 1. Introduction

The rapid ascent of USD-pegged stablecoins from under $50 billion in market capitalization in 2021 to over $300 billion by early 2026 has created a new class of large-scale, rule-bound buyers of short-term U.S. Treasuries. Tether (USDT) and USD Coin (USDC) together back their liabilities approximately 1:1 with short-duration dollar assets, making their combined Treasury holdings comparable in scale to those of mid-sized sovereign reserve managers. This structural T-bill demand creates a channel through which stablecoin supply dynamics may affect the short-term U.S. government securities market — what we call the *stablecoin exorbitant privilege channel*.

The core tension is a "New Triffin Dilemma." In normal times, stablecoin issuance increases demand for T-bills, compressing the OIS–Treasury spread and amplifying the U.S. convenience yield — the privilege side. But the same reserve structure creates systemic fragility: in a redemption run, stablecoin issuers must liquidate T-bills to meet dollar outflows, generating forced selling that widens spreads and potentially destabilizes the very market whose demand they ordinarily support.

Whether this fragility channel activates depends critically on how much *liquid* reserve buffer the issuer holds. An issuer holding 100% T-bills absorbs redemptions through forced sales; an issuer holding substantial cash or near-cash equivalents can meet redemptions without touching its T-bill portfolio. The liquid buffer *L* — cash and near-cash / outstanding supply — is therefore the key reserve-adequacy variable. Below some critical threshold *L**, the fragility channel switches on.

This paper provides empirical evidence for this mechanism. Our main contribution is to document that the relationship between stablecoin supply growth and OIS–Treasury spread changes is nonlinear, concentrating at very low buffer states. We find a significant threshold interaction at L < 4% in the differenced-spread specification (β₃ = −4.39, p = 0.001), consistent with the theory's prediction that buffer effects are negligible until reserves are nearly depleted.

We are transparent about three important limitations. First, the level-spread regression faces a spurious-regression concern: both the spread and the liquid buffer variable *L* are non-stationary (ADF p = 0.49 and 0.90, respectively) and do not cointegrate (Engle-Granger p = 0.12). We therefore present the differenced-spread specification as primary. Second, the significant threshold result is identified from nine USDT observations between mid-2025 and early 2026; the estimates are sensitive to this narrow window. Third, the continuous-L interaction is not significant in the panel, consistent with the linear mechanism being weak. We frame all results accordingly.

The paper is organized as follows. Section 2 develops the theoretical framework. Section 3 describes the data and variable construction. Section 4 presents the continuous-L panel regression. Section 5 presents the threshold panel specification. Section 6 describes the event study. Section 7 concludes.

---

## 2. Theoretical Framework

We extend Maggiori's (2017) two-country continuous-time framework by incorporating stablecoin issuers as a third class of safe-asset intermediary operating alongside the U.S. banking system.

### 2.1 Setup

Let *S_t* denote the aggregate supply of USD-pegged stablecoins (in dollars). Stablecoin issuers hold reserves *R_t = θ_t · S_t + L_t · S_t + other_t*, where *θ_t* is the Treasury exposure ratio (T-bill holdings / supply) and *L_t* is the liquid buffer ratio (cash and near-cash / supply). Normal issuance of *ΔS > 0* units requires purchasing *θ · ΔS* in T-bills, increasing demand for government paper and compressing the convenience yield (spread). This is the **privilege amplification** channel: each additional dollar of stablecoin supply mechanically increases Treasury demand by *θ* dollars.

### 2.2 The Fragility Channel and the Reserve Threshold

During a redemption run, stablecoin holders demand dollar redemptions at par. The issuer can meet *ΔS < 0* redemptions from either (a) the liquid buffer *L · |ΔS|* without T-bill sales, or (b) forced T-bill liquidation for any shortfall beyond *L*. Define the *critical buffer* as the level *L** below which T-bill sales are forced for any non-trivial run. Below *L***, forced selling generates spread widening — reversing the normal privilege channel. This motivates the estimating equation:

For *L > L**: *∂Spread / ∂ΔlnS ≈ β₁ < 0* (privilege dominates)

For *L < L**: *∂Spread / ∂ΔlnS ≈ β₁ + β₃ ≠ β₁* (forced liquidation modifies the relationship)

### 2.3 Equilibrium and Testable Implications

In the Maggiori (2017) framework, the safe-asset premium depends on the asset-holder's ability to absorb global risk. Stablecoin issuers operating as large T-bill buyers compress the U.S. convenience yield when expanding but amplify volatility in the T-bill market when they face forced liquidations. The testable implications are:

**H1 (Privilege Amplification):** Stablecoin supply growth compresses OIS–Treasury spreads in the aggregate.

**H2 (Fragility Threshold):** The relationship between supply growth and spreads is nonlinear, with the buffer-mediated regime change concentrated at very low *L*.

---

## 3. Data

### 3.1 Dependent Variable

The OIS–Treasury spread is constructed as DGS3MO (3-month constant-maturity T-bill yield, FRED) minus overnight SOFR (SOFR, FRED). The 3-month T-bill yield is used on the bond-equivalent basis rather than the discount basis (DTB3) to avoid a systematic 5–10 bps downward bias. Overnight SOFR is the best available proxy for the OIS leg given data constraints; the ideal instrument, CME Term SOFR 3M, is not available on FRED for our full sample. The spread is measured in percentage points and is reported monthly as the within-month mean of daily values. Sample: January 2022 – March 2026 (51 months).

### 3.2 Stablecoin Supply and Supply Growth

Daily circulating supply for USDT and USDC is obtained from the DeFiLlama stablecoins API. Monthly supply growth *ΔlnS_it* is constructed as the log-difference of month-end values for each issuer separately:

*ΔlnS_it = log(supply_i,t) − log(supply_i,t−1)*

This construction uses DeFiLlama's daily circulating supply — the actual tokens in active circulation across all chains — rather than the total_supply_bn figures from reserve attestations. The attestation supply figures are reported quarterly for USDT and reflect total outstanding tokens rather than circulating supply; they also smooth through the interpolation scheme applied to fill quarterly gaps. Using DeFiLlama supply ensures that month-to-month supply growth reflects actual redemption and issuance activity at monthly frequency.

### 3.3 Liquid Buffer (*L*)

The liquid buffer *L_it* = liquid reserves / outstanding supply is the key reserve-adequacy variable. For USDT, we construct *L* from BDO ISAE 3000R quarterly attestation PDFs downloaded from tether.to. The numerator is **Cash & Bank Deposits plus Money Market Funds** from the BDO-attested reserves breakdown. Starting in Q4 2025, Tether replaced MMF with **Term Reverse Repurchase Agreements** (maturity < 90 days, fully collateralized by US Treasuries) — we include the Term Repo figure in *L* for those quarters to maintain a consistent "immediately-liquid-or-near-liquid" definition across the sample.

Rationale: Cash & Bank Deposits is immediately liquid (T+0). Money Market Funds invest in highly liquid short-term instruments and typically redeem at T+1. Term Repos collateralized by US Treasuries with maturity under 90 days are near-cash by any reasonable definition. All three components are immediately available to meet redemptions without T-bill liquidation, which is the economic content of the fragility buffer. U.S. Treasury Bills (even those with residual maturity < 90 days) are not included in *L* because their sale in a run scenario is the forced-liquidation mechanism the paper studies.

All 2024 and 2025 USDT *L* values are verified directly against BDO PDF source documents. The 2025 reports reflect a corporate restructuring: starting Q1 2025, BDO attestations cover **Tether International, S.A. de C.V.** only (not the consolidated Tether Holdings group). Treasury and cash figures for 2025+ reflect this single entity; prior quarters covered Tether Holdings Limited (consolidated).

For USDC, *L* is constructed from Circle's monthly attestation reports (Grant Thornton / Deloitte) using the reported cash and cash-equivalent holdings. USDC attestations are available monthly, so no quarterly interpolation is required.

Between quarterly USDT attestation dates, *L* is interpolated using time-weighted linear interpolation (equivalent to the ⅔/⅓ blend discussed in our internal documentation), applied issuer-by-issuer on a month-end grid before aggregating.

### 3.4 Controls

- **VIX:** CBOE Volatility Index (FRED: VIXCLS), monthly mean.
- **ΔlnN*:** Log-change in the ACWX ETF (Yahoo Finance), proxying rest-of-world equity flows (Maggiori 2017).
- **Velocity (V):** 7-day rolling standard deviation of daily supply log-changes, measuring short-term redemption intensity. Used in the aggregate time-series model only.
- **Issuer FE:** A USDT dummy (baseline = USDC) absorbing time-invariant level differences between the two issuers (reserve composition, reporting conventions).

### 3.5 Sample and Panel Construction

The issuer-level long panel contains 102 observations: 51 months × 2 issuers (USDT and USDC), from January 2022 to March 2026. The spread is the same macro variable for both issuers in a given month; issuer-level variation enters through *ΔlnS_it*, *L_it*, and the issuer fixed effect. Month fixed effects are not included — with two issuers sharing the same monthly spread, month FE would absorb all variation in the dependent variable.

---

## 4. Continuous-L Panel Regression

### 4.1 Specification

The primary estimating equation follows the professor's specification:

*Spread_t = α + β₁·ΔlnS_it + β₃·L_it + β₄·(L_it × ΔlnS_it) + γ₁·VIX_t + γ₂·ΔlnN*_t + δ·USDT_i + ε_it*

Standard errors are clustered by month (shared macro shock within a month). θ (Treasury exposure) is excluded — once *L* enters, the separate identification of *θ* and *L* is weak at N = 51, and the theoretical variable of interest is the liquid buffer, not total reserve exposure.

### 4.2 Results

**Table 1. Continuous-L Issuer-Panel Regression (N = 102)**

| Coefficient | Variable | Estimate | p-value | |
|---|---|---|---|---|
| β₁ | ΔlnS_it | −0.122 | 0.947 | |
| β₃ | L_it | +7.192 | <0.001 | *** |
| β₄ | L_it × ΔlnS_it | −4.349 | 0.682 | |
| γ₁ | VIX | +0.011 | 0.220 | |
| γ₂ | ΔlnN* | +0.373 | 0.387 | |
| δ | USDT FE | −0.193 | 0.000 | *** |

*N = 102 issuer-month observations. SE clustered by month. Issuer FE: USDT dummy (baseline = USDC). No month FE. R² = 0.712.*

The continuous interaction β₄ is not significant (p = 0.68), consistent with the professor's expectation that "the interaction L_it × ΔlnS_it was not significant" once supply growth is measured correctly from DeFiLlama. Supply growth alone (β₁) is also not significant (p = 0.95). The level of *L* (β₃) is positive and highly significant, but this likely reflects the common trend in both series — the non-stationarity concern discussed below — rather than a causal mechanism.

### 4.3 Stationarity and Spurious Regression Caution

Formal ADF tests confirm that both the OIS–Treasury spread (ADF p = 0.49) and the liquid buffer *L* (ADF p = 0.90) are non-stationary at the monthly frequency. Engle-Granger cointegration tests find no long-run relationship (Engle-Granger p = 0.12). The significant β₃ in the levels specification should therefore be interpreted with caution: the spread and *L* declined together during the 2022–2024 Fed hiking cycle (common macro driver), and this co-movement produces high apparent correlation without causal content.

The aggregate time-series model (N = 51) shows a significant L × ΔlnS interaction in levels (β₄ = −49.78, p = 0.004, R² = 0.874), but this result faces the same spurious regression concern. The implied break-even threshold — the level of L at which the total effect of supply growth on spread changes sign — is approximately L* ≈ 10.7% (= 5.31 / 49.78), consistent with the economic prior that the buffer effect matters most at low buffer levels. However, given the non-stationarity, we do not emphasize this figure as a regulatory benchmark.

We therefore turn to the differenced-spread specification, which avoids the non-stationarity problem and is theoretically motivated by the theory's focus on dynamic transmission.

---

## 5. Threshold Panel Specification

### 5.1 Motivation

The theory does not predict a linear relationship between *L* and the spread transmission coefficient. Rather, the fragility mechanism should be dormant when *L* is high (buffers absorb redemptions without T-bill sales) and active only when *L* approaches depletion. This motivates a threshold specification:

*DV_t = α + β₁·ΔlnS_it + β₂·1[L_it < c] + β₃·1[L_it < c]·ΔlnS_it + γ·controls + δ·USDT_i + ε_it*

where DV ∈ {Spread_t, ΔSpread_t} and c ∈ {4%, 6%}. β₃ is the coefficient of interest: a significant negative β₃ in the ΔSpread specification would indicate that, in low-buffer states, supply growth is associated with larger spread changes — consistent with the theory's fragility channel.

We use ΔSpread as the primary dependent variable because (a) first-differencing renders the left-hand side stationary, avoiding the spurious regression concern from Section 4.3, and (b) the theory predicts dynamic transmission (how supply changes affect spread changes), not a level relationship.

### 5.2 Low-Buffer Observations

Of the 102 panel observations, **23 have L < 6%** and **9 have L < 4%** — all from USDT, concentrated between mid-2025 and early 2026. The decline in USDT's liquid buffer reflects supply growth outpacing the dollar value of the MMF/Term Repo buffer: USDT outstanding supply grew from approximately $104 billion (Q1 2024) to $186 billion (Q4 2025) while MMF holdings remained roughly flat at $5–7 billion, mechanically compressing *L*.

**USDT Liquid Buffer (L), Selected Dates:**

| Quarter | L (%) | Supply (bn) | Cash+MMF/Repo (bn) |
|---|---|---|---|
| 2024-Q1 | 6.1% | 104.0 | 6.38 |
| 2024-Q2 | 5.7% | 112.4 | 6.47 |
| 2024-Q4 | 4.8% | 136.6 | 6.62 |
| 2025-Q1 | 4.4% | 143.7 | 6.35 |
| 2025-Q2 | 4.1% | 157.0 | 6.38 |
| 2025-Q3 | 3.7% | 174.4 | 6.44 |
| 2025-Q4 | 3.0% | 186.5 | 5.58 |
| 2026-Q1 | 2.6% | 184.2 | 4.85 |

*L = (Cash & Bank Deposits + MMF or Term Repos <90d) / total_supply_bn. Source: BDO ISAE 3000R attestation PDFs, verified.*

### 5.3 Threshold Regression Results

**Table 2. Threshold Panel Regression Results**

| Threshold | DV | β₁ (ΔlnS) | β₂ (1[L<c]) | β₃ (1[L<c]×ΔlnS) | N | N_low |
|---|---|---|---|---|---|---|
| L < 4% | ΔSpread_t | +0.003 | +0.094*** | **−4.385***  (p=0.001)** | 100 | 9 |
| L < 4% | Spread_t | +2.024 | −0.480*** | +3.224  (p=0.309) | 102 | 9 |
| L < 6% | ΔSpread_t | −0.093 | +0.036 | −0.561  (p=0.639) | 100 | 23 |
| L < 6% | Spread_t | +1.618 | −0.643*** | +0.561  (p=0.620) | 102 | 23 |

*SE clustered by month. Controls: VIX, ΔlnN*, USDT dummy. ΔSpread specifications lose 2 obs from first-differencing. *** p < 0.01.*

The **L < 4% threshold in ΔSpread** yields a significant interaction (β₃ = −4.385, p = 0.001). The negative sign indicates that in low-buffer states, supply growth is associated with a larger decrease in the spread change. In the nine low-buffer observations (all USDT, mid-2025 to early 2026), USDT supply was expanding while spreads were compressing — so the negative β₃ captures: "when the buffer is thin and supply is growing, spreads fall faster." This is consistent with a period of strong USDT demand that simultaneously tightened the buffer (supply grew faster than MMF holdings) and compressed spreads.

The 6% threshold yields no significant interaction at either DV (p > 0.62), and the levels specification at 4% is also insignificant (p = 0.31). The significant result is specific to the 4% threshold in the differenced specification.

### 5.4 Interpretation and Caveats

The threshold result is suggestive but not robust in the sense that the professor specified. Three caveats apply:

**Caveat 1 — Small sample.** All nine low-buffer observations are from the same issuer (USDT) in the same 9-month window (mid-2025 to early 2026). The threshold dummy effectively interacts with a period dummy; the estimate cannot rule out that the result reflects a USDT-specific or macro-regime factor in that window rather than a buffer mechanism.

**Caveat 2 — Sign interpretation.** The negative β₃ in ΔSpread does not straightforwardly confirm the "fragility" channel as originally hypothesized. The raw co-movement during low-buffer episodes was supply growth (ΔlnS > 0) accompanied by spread compression (ΔSpread < 0). Both are consistent with a strong-USDT-demand regime in late 2025, which may reflect macro factors beyond the buffer mechanism.

**Caveat 3 — Threshold not significant at 6%.** The absence of significance at L < 6% means the result does not generalize to a broader set of observations. It is concentrated in the deepest low-buffer tail of the sample.

In the professor's framing: "The low-buffer estimates should be interpreted cautiously because they are identified from a small number of USDT observations, but they provide suggestive evidence for a nonlinear liquidity-buffer channel."

---

## 6. Event Study

### 6.1 Design

We classify three historical stress episodes by buffer state at the time of the event:

| Event | Date | Buffer State | L at Event |
|---|---|---|---|
| LUNA/UST Collapse | 2022-05-09 | Low (USDT) | ~15% |
| USDT Partial Depeg | 2022-05-12 | Low (USDT) | ~15% |
| USDC / SVB Failure | 2023-03-11 | High (USDC) | ~22% |

The normal model is estimated in first differences (Δspread = f(ΔVIX, ΔlnN*)) over a pre-event window of [−120, −6] trading days, removing low-frequency trends that contaminated the original level-model specification. The event window is [−5, +20] trading days.

### 6.2 Results

**Table 3. Buffer-Conditioned Event Study**

| Event | Buffer | CAR[−5,+20] | t-stat | p-value |
|---|---|---|---|---|
| LUNA/UST Collapse | Low | −15.3 bps | −1.07 | 0.295 |
| USDT Partial Depeg | Low | −4.3 bps | −0.31 | 0.759 |
| USDC / SVB Failure | High | −2.4 bps | −0.04 | 0.967 |
| Low vs. High (diff) | — | — | −0.13 | 0.898 |

All CARs are statistically insignificant. A placebo test using three quiet-period pseudo-events yields mean |CAR| = 4.8 bps versus 7.3 bps for actual events (ratio 1.5×), confirming the actual CARs are indistinguishable from noise. The event study cannot serve as the paper's primary quantitative evidence.

The directional pattern — negative CARs for low-buffer events and near-zero for the high-buffer event — is consistent with the regression framework. For the USDC/SVB episode, Circle's $3.3B frozen at SVB represented approximately 8% of its $41B supply. The government deposit guarantee within 72 hours prevented forced T-bill liquidation, consistent with a high-buffer event leaving spreads largely unaffected. The event study provides qualitative directional context for the mechanism; the quantitative evidence rests on the threshold regression in Section 5.

---

## 7. Conclusion

This paper provides suggestive empirical evidence that large-scale USD-pegged stablecoins introduce a two-sided "New Triffin Dilemma" into the short-term U.S. government securities market. The privilege and fragility channels are both theoretically grounded in Maggiori (2017), but the empirical identification of the fragility channel is challenging: the key variable — the liquid buffer *L* — is non-stationary, and the significant threshold result is identified from nine USDT observations in a single macroeconomic window.

The main finding is that the linear buffer-interaction is weak (β₄ = −4.35, p = 0.68 in the issuer panel), consistent with the effect being nonlinear rather than proportional. A threshold specification at L < 4% finds a significant interaction with ΔSpread (β₃ = −4.39, p = 0.001), consistent with the theory's prediction that buffer effects concentrate near depletion. The result does not generalize to the L < 6% threshold and disappears in the levels specification.

We follow the professor's suggested framing: "the linear buffer interaction is weak once issuer supply growth is measured correctly. However, consistent with the theory, the relationship appears concentrated in very low-buffer states." The evidence is suggestive rather than conclusive, and we recommend future work obtain a longer panel — as USDT's buffer continues to decline relative to supply, additional low-buffer observations will sharpen identification — and test robustness by exploiting quasi-exogenous variation in reserve composition rather than relying on the time-series of a single issuer.

For regulators considering stablecoin reserve legislation, our results highlight the importance of distinguishing liquid reserves (cash, MMF, short-dated repos) from total reserve exposure (T-bill holdings). The relevant buffer for systemic risk is the former — assets that can absorb redemptions without forced T-bill selling — not the latter. Our data show that USDT's liquid buffer has declined from approximately 15% in 2022 to below 3% by early 2026, driven by supply growth outpacing the MMF/Repo buffer in absolute terms. Whether this trajectory poses systemic risk depends on the scale of any future run and the pace at which the buffer can be rebuilt — questions our results cannot answer definitively but motivate studying.

---

## Acknowledgments

The authors thank Professor Hur Sewon and participants at the Yonsei GSIS Topics in International Finance seminar (2026-1) for valuable comments and suggestions. All errors are our own. Replication code and data are available at the project repository.

---

## References

Caballero, R.J., Farhi, E., and Gourinchas, P.-O. (2008). An equilibrium model of "global imbalances" and low interest rates. *American Economic Review*, 98(1), 358–393.

Cole, H.L. and Kehoe, T.J. (2000). Self-fulfilling debt crises. *Review of Economic Studies*, 67(1), 91–116.

Duffie, D. (2022). Digital currencies and fast payment systems: Disruption is coming. Working Paper, Stanford University.

Engle, R.F. and Granger, C.W.J. (1987). Co-integration and error correction. *Econometrica*, 55(2), 251–276.

Ghamami, S., Glasserman, P., and Young, H.P. (2023). Stablecoins and macroprudential regulation. Working Paper.

Gorton, G.B. and Zhang, J. (2021). Taming wildcat stablecoins. *University of Chicago Law Review*, 90(3), 909–956.

Gourinchas, P.-O. and Rey, H. (2007). International financial adjustment. *Journal of Political Economy*, 115(4), 665–703.

Granger, C.W.J. and Newbold, P. (1974). Spurious regressions in econometrics. *Journal of Econometrics*, 2(2), 111–120.

Hansen, B.E. (2000). Sample splitting and threshold estimation. *Econometrica*, 68(3), 575–603.

MacKinlay, A.C. (1997). Event studies in economics and finance. *Journal of Economic Literature*, 35(1), 13–39.

Maggiori, M. (2017). Financial intermediation, international risk sharing, and reserve currencies. *American Economic Review*, 107(10), 3038–3071.

Obstfeld, M., Shambaugh, J.C., and Taylor, A.M. (2010). Financial stability, the trilemma, and international reserves. *American Economic Journal: Macroeconomics*, 2(2), 57–94.

Phillips, P.C.B. (1986). Understanding spurious regressions in econometrics. *Journal of Econometrics*, 33(3), 311–340.

Triffin, R. (1960). *Gold and the Dollar Crisis: The Future of Convertibility*. Yale University Press.

---

## Appendix

### A.1 Liquid Buffer Variable Construction

**L_it = (Cash & Bank Deposits + Money Market Funds) / total_supply_bn**

For quarters where MMF is absent from the BDO report (Q4 2025 and Q1 2026), Term Reverse Repurchase Agreements (maturity < 90 days, fully collateralized by US Treasuries) replace MMF in the numerator. All values are verified against BDO ISAE 3000R PDF attestations.

**USDT verified L values (from BDO PDFs):**

| Date | Cash ($M) | MMF or Term Repo ($bn) | L (%) |
|---|---|---|---|
| 2024-03-31 | 100.3 | 6.28 (MMF) | 6.1% |
| 2024-06-30 | 109.9 | 6.36 (MMF) | 5.7% |
| 2024-12-31 | 108.8 | 6.51 (MMF) | 4.8% |
| 2025-03-31 | 64.3 | 6.29 (MMF) | 4.4% |
| 2025-06-30 | 32.4 | 6.35 (MMF) | 4.1% |
| 2025-09-30 | 30.1 | 6.41 (MMF) | 3.7% |
| 2025-12-31 | 34.0 | 5.55 (Term Repo) | 3.0% |
| 2026-03-31 | 107.0 | 4.75 (Term Repo) | 2.6% |

*Note: 2025+ reports cover Tether International, S.A. de C.V. only (entity restructuring); prior quarters covered Tether Holdings Limited consolidated.*

### A.2 Stationarity and Cointegration Tests

| Test | Variable | Statistic | p-value | Verdict |
|---|---|---|---|---|
| ADF | OIS–Treasury spread | −1.580 | 0.494 | I(1) — non-stationary |
| ADF | ΔlnS (supply growth) | −4.007 | 0.001 | I(0) — stationary ✓ |
| ADF | L (liquid buffer) | −2.529 | 0.108 | I(1) — non-stationary |
| ADF | VIX | −2.618 | 0.089 | Borderline |
| ADF | ΔlnN* | −4.701 | 0.000 | I(0) — stationary ✓ |
| Engle-Granger | spread ~ ΔlnS | −2.888 | 0.139 | Not cointegrated |
| Engle-Granger | spread ~ L | −1.611 | 0.716 | Not cointegrated |

*ADF tests use AIC lag selection. N = 51 monthly observations.*

### A.3 Aggregate Time-Series Regression (Reference)

The aggregate monthly time-series regression (N = 51) is reported for reference. Given the non-stationarity of both spread and L, these results carry spurious regression risk and are not the paper's primary evidence.

| Coefficient | Estimate | p-value | |
|---|---|---|---|
| β₁ (ΔlnS) | +5.313 | 0.031 | * |
| β₃ (L) | +9.247 | <0.001 | *** |
| β₄ (L × ΔlnS) | −49.784 | 0.004 | ** |
| Velocity | −104.744 | <0.001 | *** |
| VIX | +0.011 | 0.098 | |
| ΔlnN* | +0.557 | 0.232 | |

*HAC standard errors (1 lag). R² = 0.874. The implied break-even L (where total effect of ΔlnS on spread = 0) is L* ≈ 5.31 / 49.78 ≈ 10.7%. Not cited as a regulatory benchmark given spurious regression concerns.*

### A.4 Methodological Notes on OIS–Treasury Spread Construction

The OIS–Treasury spread measures the T-bill convenience yield: the premium investors accept to hold risk-free government paper relative to an uncollateralized overnight-indexed swap. We use DGS3MO (bond-equivalent yield basis) rather than DTB3 (discount basis): discount-basis yields understate the true return by approximately 5–10 bps. Overnight SOFR is used as the OIS proxy rather than the 90-day trailing average (SOFR90DAYAVG), which lagged overnight SOFR by up to 119 bps during the 2022 hiking cycle and inflated mean spreads to 84 bps — a Fed-policy artifact. Overnight SOFR reduces the mean to approximately 17 bps, which is a more economically plausible convenience yield.

### A.5 Event Study: First-Difference Normal Model

The normal model is estimated as Δspread = f(ΔVIX, ΔlnN*) over the pre-event window [−120, −6]. First-differencing removes the trending behavior that inflated original level-model CARs approximately 120-fold during the 2022 hiking cycle estimation window. Event window: [−5, +20] trading days. Pre-event window: [−120, −6]. Placebo events drawn from three quiet periods (October 2022, June 2023, September 2024).
