# Stablecoins and the Exorbitant Privilege: Reserve Buffer Adequacy and OIS–Treasury Spread Dynamics

Mireu Mimi Kim · Sara Ambre Chekroune · Oybek Ibragimov · Jade Zhu · Alexandre Godefroy · Baptiste Degand · Minjin Kim

Yonsei Graduate School of International Studies · Topics in International Finance (2026-1) · Professor Hur Sewon

**JEL Classification:** E44, F31, G12, G18, G23

---

## Abstract

Large-scale USD-pegged stablecoins now hold Treasury bills at a scale comparable to mid-sized sovereign reserve managers, creating a structural channel through which stablecoin supply dynamics may affect the short-term U.S. government securities market. We document a "New Triffin Dilemma": in normal times, stablecoin issuance compresses the OIS–Treasury spread by increasing T-bill demand (the privilege channel), but an adequately thin liquid reserve buffer transforms expansion episodes into a fragility risk. We test this mechanism using an issuer-level panel of 102 observations covering USDT and USDC from January 2022 to March 2026. Supply growth is measured from DeFiLlama daily circulating supply; the liquid buffer *L* — Cash and Bank Deposits plus Money Market Funds — is constructed from BDO ISAE 3000R attestation PDFs verified quarter-by-quarter. The continuous buffer-interaction is not significant in the panel (β₄ = −4.35, *p* = 0.68), consistent with a nonlinear rather than proportional mechanism. A threshold specification at *L* < 4% using first-differenced spreads finds a significant interaction (β₃ = −4.39, *p* = 0.001), though all nine low-buffer observations are from USDT between mid-2025 and early 2026. We interpret this as suggestive evidence of a nonlinear liquidity-buffer channel and discuss implications for stablecoin reserve regulation.

**Keywords:** stablecoins, exorbitant privilege, safe-asset demand, reserve adequacy, Triffin dilemma, OIS–Treasury spread, threshold regression, liquidity buffer

---

## Acknowledgements

The authors thank Professor Hur Sewon for detailed feedback at multiple stages of this project. All errors are our own. Replication code and data are available at the project repository.

---

## 1. Introduction

Between 2021 and early 2026, the combined market capitalization of USD-pegged stablecoins grew from under $50 billion to over $300 billion, with Tether (USDT) and USD Coin (USDC) together accounting for more than 90% of outstanding supply. Both issuers maintain approximately 1:1 backing in short-duration dollar assets — predominantly U.S. Treasury bills — making their combined T-bill holdings comparable in scale to those of mid-sized sovereign reserve managers such as Norway or South Korea. This structural T-bill demand creates a novel channel through which stablecoin supply dynamics may affect the short-end of the U.S. government securities market. This paper asks whether that channel exists, and whether its sign depends critically on how much liquid reserve buffer the issuer holds.

The intellectual starting point is the concept of *exorbitant privilege*, the excess return the United States earns on its external liabilities relative to its assets by virtue of the dollar's reserve-currency role (Gourinchas & Rey, 2007). The mechanism, formalized by Caballero et al. (2008), operates through safe-asset demand: foreign investors and intermediaries bid up the price of U.S. Treasuries, compressing yields and reducing the government's borrowing cost. Krishnamurthy & Vissing-Jorgensen (2012) provide direct evidence that Treasury supply reductions widen corporate credit spreads, confirming that the marginal investor in Treasuries is highly inelastic — a property stablecoin issuers now exploit at scale. Maggiori (2017) provides the micro-founded general equilibrium framework we use: in his two-country continuous-time model, the country whose financial intermediaries absorb global risk issues the global safe asset, and the premium those intermediaries earn — the convenience yield — equals the wedge between the safe rate and the market clearing rate. We extend this framework to incorporate stablecoin issuers as a third class of safe-asset intermediary. Each dollar of new stablecoin issuance requires purchasing *θ* dollars of T-bills, mechanically compressing the convenience yield; each dollar of redemption requires the reverse. This is the *privilege amplification channel*.

The fragility dimension mirrors the original Triffin (1960) dilemma, in which the United States had to run current account deficits to supply dollars to the world, but those same deficits eventually undermined confidence in dollar convertibility. In our setting, stablecoin issuers supply dollar-denominated safe assets to crypto markets, but the T-bill portfolios they hold as backing create a systemic linkage: a large-scale redemption run forces T-bill liquidation, widening the OIS–Treasury spread and potentially destabilizing the very market the issuers ordinarily support. Obstfeld et al. (2010) and Cole & Kehoe (2000) provide theoretical precedents for how this kind of self-fulfilling fragility can materialize under reserve constraints.

The critical variable linking the privilege and fragility channels is the *liquid buffer* — cash and near-cash holdings relative to outstanding supply. An issuer with substantial cash, money market funds, or short-dated repos can absorb redemptions without touching its T-bill portfolio; an issuer whose liquid buffer approaches depletion must sell T-bills for any material redemption. This nonlinear threshold structure — buffer-adequacy determines which channel dominates — has not been empirically tested for stablecoins. Gorton & Zhang (2021) provide the closest antecedent, documenting that stablecoins share structural properties with pre-Federal Reserve private bank notes and are vulnerable to run dynamics. Duffie (2022) and Ghamami et al. (2023) argue for regulatory standards requiring minimum liquid reserve ratios precisely because of this fragility channel. Our contribution is to provide an empirical test of the threshold mechanism using directly verified attestation data.

Our empirical strategy addresses two challenges that previous informal treatments have ignored. First, the OIS–Treasury spread is non-stationary (ADF *p* = 0.49) and does not cointegrate with the liquid buffer variable (Engle-Granger *p* = 0.72; the Spread–ΔlnS pair also fails to cointegrate, *p* = 0.14), making level regressions spurious in the sense of Granger & Newbold (1974) and Phillips (1986). We address this by making the change in the spread the primary dependent variable in our threshold specification. Second, the threshold itself is not known *a priori*; we evaluate it at economically motivated candidate values (4% and 6%) and apply cluster-robust inference following Hansen (2000). We also present an issuer-specific event study (MacKinlay, 1997) around two USDT stress episodes as qualitative context.

The paper is organized as follows. Section 2 describes our data, theoretical framework, and estimation strategy. Section 3 presents the empirical results. Section 4 concludes with policy implications and directions for future research.

---

## 2. Methodology

### 2.1 Theoretical Framework

We extend Maggiori's (2017) two-country continuous-time model to incorporate stablecoin issuers as a third intermediary class. Let *S_t* denote aggregate USD-pegged stablecoin supply, *θ_t* the Treasury-exposure ratio (T-bill holdings / supply), and *L_t* the liquid-buffer ratio (cash and near-cash / supply). Normal issuance of Δ*S* > 0 requires purchasing *θ*·Δ*S* in T-bills, compressing the convenience yield — the spread between the T-bill rate and the overnight swap rate. In a redemption episode (Δ*S* < 0), the issuer can absorb the first *L*·|Δ*S*| from liquid reserves without T-bill sales; anything beyond that forces T-bill liquidation.

Define *L** as the critical buffer below which any non-trivial redemption triggers forced T-bill sales. This generates a regime-switch in the relationship between supply growth and spread dynamics:

For *L > L***: ∂Spread / ∂(ΔlnS) ≈ β₁ < 0 *(convenience yield compression dominates)*

For *L < L***: ∂Spread / ∂(ΔlnS) ≈ β₁ + β₃ *(forced liquidation modifies the transmission)*

This motivates two testable hypotheses. **H1** (*Privilege Amplification*): stablecoin supply growth compresses the OIS–Treasury spread in the aggregate. **H2** (*Fragility Threshold*): the relationship is nonlinear, with the buffer-mediated regime shift concentrated at very low *L*.

### 2.2 Data Sources and Variable Construction

**OIS–Treasury Spread.** We construct the spread as the 3-month constant-maturity T-bill yield (DGS3MO, FRED) minus the daily overnight SOFR rate (SOFR, FRED), converted to a monthly mean of daily values. We use DGS3MO on a bond-equivalent basis rather than the discount-basis series DTB3, which understates yields by 5–10 bps. We use overnight SOFR rather than the 90-day trailing average (SOFR90DAYAVG), which lagged overnight SOFR by up to 119 bps during the 2022 hiking cycle and inflated mean spreads to 84 bps — a policy artifact rather than a convenience yield signal. Overnight SOFR produces a sample mean of approximately 17 bps, which is economically plausible. Additional details on the spread construction are in Appendix A.4.

**Stablecoin Supply.** Daily circulating supply for USDT and USDC is obtained from the DeFiLlama stablecoins API. Monthly supply growth is ΔlnS*_it* = log(supply*_{i,t}*) − log(supply*_{i,t−1}*) for each issuer *i*. We use DeFiLlama circulating supply — tokens actively in circulation across all chains — rather than total outstanding supply from reserve attestations, which is available only quarterly for USDT and reflects non-circulating reserve tokens.

**Liquid Buffer (*L*).** The liquid buffer *L_it* = liquid reserves / outstanding supply is the key reserve-adequacy variable. For USDT, *L* is constructed from BDO ISAE 3000R quarterly attestation PDFs downloaded from tether.to and verified line-by-line. The numerator is *Cash & Bank Deposits plus Money Market Funds*. Starting in Q4 2025, Tether replaced MMF with Term Reverse Repurchase Agreements (maturity < 90 days, fully collateralized by U.S. Treasuries); we treat these equivalently as near-cash instruments that can absorb redemptions without T-bill sales. U.S. T-bills are explicitly excluded from *L* even when residual maturity is under 90 days, because their sale is the forced-liquidation mechanism under study. All 2024 and 2025 USDT values are PDF-verified (see Appendix A.1). Starting Q1 2025, BDO attestations cover Tether International, S.A. de C.V. only, following a corporate restructuring; prior quarters covered Tether Holdings Limited consolidated. For USDC, *L* is taken directly from Circle's monthly attestation reports (Grant Thornton / Deloitte), which report cash and cash-equivalents monthly, eliminating the need for interpolation. Between USDT quarterly attestation dates, *L* is interpolated using time-weighted linear interpolation, consistent with the professor's ⅔/⅓ blend recommendation.

![**Figure 1.** USDT and USDC circulating supply (Panel A, DeFiLlama) and OIS–Treasury spread (Panel B, DGS3MO − overnight SOFR, monthly mean) over the sample period. Dashed vertical lines mark the two issuer-specific USDT stress events used in Section 3.4 (USDT Partial Depeg, May 2022; USDT FTX-Era Stress, November 2022).](results/fig_paper_1_timeseries.png){width=95%}

**Controls.** The VIX (CBOE Volatility Index, FRED: VIXCLS) controls for aggregate risk appetite. The log-return on the ACWX ETF (ΔlnN*, Yahoo Finance) proxies rest-of-world equity flows following Maggiori (2017). In the aggregate time-series specification we also include a velocity measure (7-day rolling standard deviation of daily ΔlnS) to capture redemption intensity.

**Panel Construction.** The issuer-level long panel contains 102 observations: 51 months × 2 issuers (USDT and USDC), January 2022 – March 2026. The spread is a common macro variable for both issuers within a month; issuer-level variation enters through ΔlnS*_it*, *L_it*, and a USDT fixed effect (baseline = USDC). Month fixed effects are excluded — with two issuers sharing a common monthly spread, month FE would absorb all variation in the dependent variable.

### 2.3 Estimation Strategy

**Continuous-L Panel.** The baseline specification follows the professor's recommended form:

Spread*_t* = α + β₁·ΔlnS*_it* + β₃·*L_it* + β₄·(*L_it* × ΔlnS*_it*) + γ₁·VIX*_t* + γ₂·ΔlnN\**_t* + δ·USDT*_i* + ε*_it*

Standard errors are clustered by month to account for the shared macro shock within each month-period. We report this specification as a benchmark but note that level regressions carry spurious regression risk because both Spread*_t* and *L_it* are I(1) and do not cointegrate (see Section 3.1 and Appendix A.2).

**Threshold Specification.** To address non-stationarity, we use ΔSpread*_t* = Spread*_t* − Spread*_{t−1}* as the primary dependent variable in our threshold spec, which is stationary by construction. The estimating equation is:

ΔSpread*_t* = α + β₁·ΔlnS*_it* + β₂·**1**[*L_it* < *c*] + β₃·**1**[*L_it* < *c*]·ΔlnS*_it* + γ·controls + δ·USDT*_i* + ε*_it*

where **1**[·] is an indicator for the low-buffer regime and *c* ∈ {4%, 6%} are economically motivated candidate thresholds. β₃ is the coefficient of interest: a significant negative β₃ indicates that supply growth in the low-buffer regime is associated with larger spread changes than in the high-buffer regime. Both DV specifications (Spread and ΔSpread) are reported for transparency.

**Issuer-Specific Event Study.** We identify stress episodes where the stablecoin issuer itself was the source of concern, excluding events driven by external factors (bank failures, or the collapse of a different stablecoin protocol). This leaves two events: the USDT partial depeg on May 12, 2022 (when $10bn+ in redemptions broke the USDT peg to $0.945, driven by concerns about Tether's own backing), and the USDT FTX-era stress on November 9, 2022 (when FTX's collapse raised specific concerns about Tether's exposure to Alameda Research). We estimate a first-difference normal model Δspread = *f*(ΔVIX, ΔlnN\*) over the pre-event window [−120, −6] trading days; first-differencing removes the trend contamination that inflated level-model CARs approximately 120-fold. CARs are accumulated over the event window [−5, +20] trading days.

---

## 3. Results

### 3.1 Stationarity and Spuriousness Diagnostics

Before presenting regression results, we document that the OIS–Treasury spread and the liquid buffer *L* are both non-stationary and do not cointegrate (Table 1). The ADF test fails to reject a unit root for the spread (*p* = 0.49) and for *L* (*p* = 0.90), while supply growth ΔlnS is stationary (*p* = 0.001). Engle-Granger cointegration tests confirm there is no long-run relationship between the spread and either ΔlnS (*p* = 0.14) or *L* (*p* = 0.72). This means that any significant coefficient on *L_it* in a levels regression reflects shared macroeconomic trend rather than a structural relationship — both the spread and Tether's buffer declined together during the 2022–2024 Federal Reserve hiking cycle — and not a genuine causal mechanism.

**Table 1. Stationarity and Cointegration Tests**

| Test | Variable | Test Statistic | *p*-value | Verdict |
|---|---|---|---|---|
| ADF | OIS–Treasury Spread | −1.580 | 0.494 | I(1) — non-stationary |
| ADF | Liquid buffer *L* | −2.529 | 0.108 | I(1) — non-stationary |
| ADF | ΔlnS (supply growth) | −4.007 | 0.001 | I(0) — stationary |
| ADF | ΔlnN* | −4.701 | <0.001 | I(0) — stationary |
| Engle-Granger | Spread ~ ΔlnS | −2.888 | 0.139 | Not cointegrated |
| Engle-Granger | Spread ~ *L* | −1.611 | 0.716 | Not cointegrated |

*Note.* ADF tests use AIC lag selection. *N* = 51 monthly observations.

![**Figure 2.** USDT liquid buffer *L* (Cash & Bank Deposits + MMF or Term Repos <90d, as a share of outstanding supply), January 2022 – March 2026. Dots mark BDO-attested quarter-end values; the line is time-weighted interpolated monthly values. Shading marks the L < 4% low-buffer regime (red) and the 4%–6% moderate-buffer band (orange).](results/fig_paper_2_buffer.png){width=95%}

### 3.2 Continuous-L Panel Regression

Table 2 presents the baseline continuous-L panel regression (*N* = 102). The interaction coefficient β₄ is not significant (*p* = 0.68), consistent with the professor's prior that the linear buffer interaction is weak once supply growth is measured correctly from circulating supply and issuer fixed effects are included. Supply growth β₁ is also not significant (*p* = 0.95). The level of *L* (β₃ = +7.19, *p* < 0.001) is highly significant, but this reflects the spurious common trend identified in Table 1, not a causal relationship. The VIX coefficient is positive and significant (γ₁ = +0.025, *p* = 0.006), consistent with risk-off episodes widening the T-bill convenience yield. The USDT fixed effect is positive and significant (δ = +0.544, *p* < 0.001), indicating that USDT-issuer months are associated with a higher spread level than USDC months after conditioning on *L* and other controls; this likely reflects USDT's longer period of high Treasury exposure and the different timing of each issuer's reserve composition shifts across the sample.

**Table 2. Continuous-L Issuer-Panel Regression**

| | Coefficient | Estimate | *p*-value | |
|---|---|---|---|---|
| β₁ | ΔlnS*_it* | −0.122 | 0.947 | |
| β₃ | *L_it* | +7.192 | <0.001 | *** |
| β₄ | *L_it* × ΔlnS*_it* | −4.349 | 0.683 | |
| γ₁ | VIX | +0.025 | 0.006 | *** |
| γ₂ | ΔlnN* | +0.515 | 0.409 | |
| δ | USDT fixed effect | +0.544 | <0.001 | *** |

*Note.* *N* = 102 issuer-month observations. Standard errors clustered by month. Issuer FE: USDT dummy (baseline = USDC). No month fixed effects. R² = 0.712. *** *p* < 0.01.

### 3.3 Threshold Panel Specification

Table 3 presents the threshold results across two candidate thresholds (*c* = 4%, 6%) and two dependent variables (ΔSpread, Spread). The main result is in the first row: at the *L* < 4% threshold in the ΔSpread specification, the interaction β₃ = −4.385 is significant at *p* = 0.001.

**Table 3. Threshold Panel Regression Results**

| Threshold | Dep. Var. | β₁ (ΔlnS) | β₂ (**1**[*L*<*c*]) | β₃ (**1**[*L*<*c*]×ΔlnS) | *N* | *N*_low |
|---|---|---|---|---|---|---|
| *L* < 4% | **ΔSpread** | +0.003 | +0.094*** | **−4.385*** (*p* = 0.001)** | 100 | 9 |
| *L* < 4% | Spread | +2.024 | −0.480*** | +3.224 (*p* = 0.309) | 102 | 9 |
| *L* < 6% | ΔSpread | −0.093 | +0.036 | −0.561 (*p* = 0.639) | 100 | 23 |
| *L* < 6% | Spread | +1.618 | −0.643*** | +0.561 (*p* = 0.620) | 102 | 23 |

*Note.* Standard errors clustered by month. Controls: VIX, ΔlnN*, USDT dummy. ΔSpread specifications lose 2 observations from first-differencing. *** *p* < 0.01.

Of the 102 panel observations, 9 have *L* < 4% and 23 have *L* < 6%; all low-buffer observations are from USDT, concentrated between mid-2025 and early 2026. The decline in USDT's buffer reflects supply growth outpacing MMF holdings in dollar terms: supply grew from approximately $104 billion (Q1 2024) to $186 billion (Q4 2025) while the MMF/Term Repo buffer remained roughly flat at $5–7 billion, mechanically compressing *L* from 6.1% to below 3%.

![**Figure 3.** Threshold regime scatter: monthly supply growth ΔlnS vs. change in OIS–Treasury spread ΔSpread, colored by buffer regime. Red diamonds (L < 4%, n = 9) show a steeper negative fitted slope than blue circles (L ≥ 6%, n = 77), consistent with β₃ = −4.39 in the threshold panel regression. Orange triangles are the moderate-buffer band (4% ≤ L < 6%, n = 14). Note: n-counts reflect the ΔSpread sample (N = 100); two observations are lost to first-differencing.](results/fig_paper_3_threshold_scatter.png){width=90%}

The *L* < 4% ΔSpread result is interpretively nuanced. The negative β₃ indicates that in low-buffer states, supply growth is associated with larger spread *declines* — not the spread widening that the fragility channel predicts for a run scenario. During mid-2025 to early 2026, USDT supply was expanding rapidly while spreads were compressing, consistent with a period of strong stablecoin demand coinciding with declining T-bill rates. The buffer was simultaneously thinning because supply growth outpaced the buffer. The result therefore captures: "when the buffer is thin and supply is growing, spreads fall faster." This is consistent with a high-demand regime rather than a redemption-stress regime. Importantly, the 6% threshold is not significant (*p* = 0.64), and the 4% threshold disappears in the levels specification (*p* = 0.31), indicating the result is specific to the ΔSpread formulation at the deepest low-buffer tail.

Three caveats govern interpretation. First, all nine low-buffer observations are from a single issuer (USDT) in a single 9-month window; the threshold dummy is nearly collinear with a USDT-×-2025H2 period dummy, and the estimate cannot rule out a macro-regime or issuer-specific explanation. Second, the sign of β₃ reflects compression rather than widening, which does not straightforwardly confirm the original fragility hypothesis. Third, the continuous interaction β₄ is insignificant, suggesting the mechanism — if real — is strongly nonlinear rather than proportional. We characterize the result as *suggestive evidence for a nonlinear liquidity-buffer channel*, pending a longer sample with more variation in low-buffer episodes across issuers.

### 3.4 Issuer-Specific Event Study

We restrict the event study to episodes where the stablecoin issuer itself was the source of stress, excluding events caused by external factors. Two events are excluded on these grounds: the LUNA/UST collapse (May 9, 2022), which involved a *different protocol* (Terra's algorithmic stablecoin) rather than USDT or USDC; and the USDC/SVB failure (March 11, 2023), which was caused by an external bank failure unrelated to Circle's own reserve management. Two issuer-specific USDT events are retained.

**Table 4. Issuer-Specific Event Study: CARs[−5, +20]**

| Event | Date | Issuer Cause | USDT Buffer | CAR (bps) | *t*-stat | *p*-value |
|---|---|---|---|---|---|---|
| USDT Partial Depeg | 2022-05-12 | $10bn+ redemptions broke the USDT peg to $0.945; market concerned about Tether's backing | ~16% | −4.3 | −0.31 | 0.759 |
| USDT FTX-Era Stress | 2022-11-09 | FTX collapse raised concerns about Tether's exposure to Alameda Research; USDT hit $0.997 | ~19% | −2.1 | −0.18 | 0.858 |

*Note.* Normal model estimated as Δspread = *f*(ΔVIX, ΔlnN*) over pre-event window [−120, −6] trading days. Event window [−5, +20] trading days. Both events are USDT-specific. At both event dates USDT's liquid buffer was well above the 4% threshold identified in Section 3.3.

![**Figure 4.** Cumulative abnormal spread (CAR) paths for the two issuer-specific USDT stress episodes. Shaded bands are 95% confidence intervals. Neither CAR is statistically distinguishable from zero, consistent with the theory's prediction: both events occurred when USDT's liquid buffer was high (~16–19%), meaning Tether could absorb redemptions without forced T-bill liquidation and without generating measurable spread effects.](results/fig_paper_4_event_study.png){width=95%}

Both events occurred when USDT held buffers well above the 4% threshold, and in both cases the spread response is statistically indistinguishable from zero. This is actually consistent with the theory: the fragility channel requires a depleted buffer to activate. The event study cannot test what would happen with a sub-4% buffer because no major stress episode has yet occurred during the 2025–2026 low-buffer period — the most informative natural experiment has not yet arrived. The event study therefore serves as qualitative illustration of the mechanism under high-buffer conditions, not as independent evidence of the threshold effect.

---

## 4. Conclusion

This paper provides suggestive empirical evidence that large-scale USD-pegged stablecoins have introduced a new source of potential fragility into the short-term U.S. government securities market, operating through the liquid reserve buffer. We extend Maggiori's (2017) framework to derive a testable threshold prediction and test it using a verified issuer-level panel of 102 observations. The linear buffer-interaction is weak (β₄ = −4.35, *p* = 0.68), consistent with the effect being nonlinear. A threshold specification at *L* < 4% finds a significant interaction with ΔSpread (β₃ = −4.39, *p* = 0.001), concentrated in nine USDT observations in mid-2025 to early 2026.

Three limitations constrain the strength of this conclusion. The significant result is identified from a single issuer in a single macroeconomic window; the sign of the significant coefficient reflects spread compression rather than widening, making its interpretation as evidence of fragility indirect; and the non-stationarity of the level spread precludes straightforward inference from the continuous-L levels specification.

**Policy Implications.** Our data show that USDT's liquid buffer declined from approximately 15% in 2022 to below 3% by early 2026, driven by supply growth outpacing the absolute dollar value of the MMF/Term Repo holdings. The distinction between *liquid* reserves (cash, MMF, short-dated repos) and *total* reserves (primarily T-bills) is economically critical for regulatory purposes: the former absorbs redemptions without T-bill sales; the latter does not. Regulatory frameworks that focus solely on the T-bill backing ratio — ensuring 1:1 reserve coverage — may overlook the liquidity composition question that our results suggest is the operative variable for systemic risk.

**Directions for Future Research.** Three extensions would sharpen identification considerably. First, a longer panel will naturally produce more low-buffer episodes as USDT supply continues to grow faster than its buffer; even two additional years of data would roughly double the number of *L* < 4% observations, improving statistical power substantially. Second, exploiting quasi-exogenous variation in reserve composition — for instance, regulatory guidance that prompted Circle's shift toward exclusively cash and T-bill holdings — would provide cleaner identification than the current time-series variation. Third, a higher-frequency (daily or weekly) analysis using intraday T-bill quote data and on-chain supply flows would allow testing whether the mechanism operates at the transaction frequency implied by the theoretical model, rather than the monthly frequency forced by quarterly attestation availability.

---

## References

Caballero, R. J., Farhi, E., & Gourinchas, P.-O. (2008). An equilibrium model of "global imbalances" and low interest rates. *American Economic Review*, *98*(1), 358–393. https://doi.org/10.1257/aer.98.1.358

Cole, H. L., & Kehoe, T. J. (2000). Self-fulfilling debt crises. *Review of Economic Studies*, *67*(1), 91–116. https://doi.org/10.1111/1467-937X.00123

Duffie, D. (2022). *Digital currencies and fast payment systems: Disruption is coming*. Working Paper, Stanford University Graduate School of Business.

Engle, R. F., & Granger, C. W. J. (1987). Co-integration and error correction: Representation, estimation, and testing. *Econometrica*, *55*(2), 251–276. https://doi.org/10.2307/1913236

Ghamami, S., Glasserman, P., & Young, H. P. (2023). *Stablecoins and macroprudential regulation*. Working Paper.

Gorton, G. B., & Zhang, J. (2021). Taming wildcat stablecoins. *University of Chicago Law Review*, *90*(3), 909–956.

Gourinchas, P.-O., & Rey, H. (2007). International financial adjustment. *Journal of Political Economy*, *115*(4), 665–703. https://doi.org/10.1086/521966

Granger, C. W. J., & Newbold, P. (1974). Spurious regressions in econometrics. *Journal of Econometrics*, *2*(2), 111–120. https://doi.org/10.1016/0304-4076(74)90034-7

Hansen, B. E. (2000). Sample splitting and threshold estimation. *Econometrica*, *68*(3), 575–603. https://doi.org/10.1111/1468-0262.00124

Krishnamurthy, A., & Vissing-Jorgensen, A. (2012). The aggregate demand for Treasury debt. *Journal of Political Economy*, *120*(2), 233–267. https://doi.org/10.1086/666526

MacKinlay, A. C. (1997). Event studies in economics and finance. *Journal of Economic Literature*, *35*(1), 13–39.

Maggiori, M. (2017). Financial intermediation, international risk sharing, and reserve currencies. *American Economic Review*, *107*(10), 3038–3071. https://doi.org/10.1257/aer.20130479

Obstfeld, M., Shambaugh, J. C., & Taylor, A. M. (2010). Financial stability, the trilemma, and international reserves. *American Economic Journal: Macroeconomics*, *2*(2), 57–94. https://doi.org/10.1257/mac.2.2.57

Phillips, P. C. B. (1986). Understanding spurious regressions in econometrics. *Journal of Econometrics*, *33*(3), 311–340. https://doi.org/10.1016/0304-4076(86)90001-1

Triffin, R. (1960). *Gold and the dollar crisis: The future of convertibility*. Yale University Press.

---

## Appendix

### A.1 Verified USDT Liquid Buffer Values

All entries below are verified against BDO ISAE 3000R PDF attestations. For 2025+, BDO attests Tether International, S.A. de C.V. only (entity restructuring from Q1 2025; prior quarters: Tether Holdings Limited consolidated). Cash refers to the "Cash & Bank Deposits" BDO line item; MMF refers to "Money Market Funds"; Term Repo refers to "Term Reverse Repurchase Agreements (<90 days)."

| Date | Cash | Liquid Component | *L* (%) |
|---|---|---|---|
| 2024-03-31 | $100.3M | $6.28bn MMF | 6.1% |
| 2024-06-30 | $109.9M | $6.36bn MMF | 5.7% |
| 2024-12-31 | $108.8M | $6.51bn MMF | 4.8% |
| 2025-03-31 | $64.3M | $6.29bn MMF | 4.4% |
| 2025-06-30 | $32.4M | $6.35bn MMF | 4.1% |
| 2025-09-30 | $30.1M | $6.41bn MMF | 3.7% |
| 2025-12-31 | $34.0M | $5.55bn Term Repo | 3.0% |
| 2026-03-31 | $107.0M | $4.75bn Term Repo | 2.6% |

### A.2 Full Stationarity and Cointegration Test Output

| Test | Variable | Lags (AIC) | Statistic | *p*-value |
|---|---|---|---|---|
| ADF | OIS–Treasury Spread | 1 | −1.580 | 0.494 |
| ADF | ΔlnS | 0 | −4.007 | 0.001 |
| ADF | *L* (liquid buffer) | 1 | −2.529 | 0.108 |
| ADF | VIX | 1 | −2.618 | 0.089 |
| ADF | ΔlnN* | 0 | −4.701 | <0.001 |
| Engle-Granger | Spread ~ ΔlnS residual | — | −2.888 | 0.139 |
| Engle-Granger | Spread ~ *L* residual | — | −1.611 | 0.716 |

### A.3 Aggregate Time-Series Regression (Reference Only)

The aggregate monthly time-series regression (*N* = 51) is reported for reference. Given the non-stationarity of both Spread and *L*, these results carry spurious regression risk and are *not* the paper's primary evidence. The implied break-even buffer — the level of *L* at which the total effect of ΔlnS on Spread changes sign — is *L** ≈ 5.31 / 49.78 ≈ 10.7%; this is not cited as a regulatory benchmark.

| Coefficient | Estimate | *p*-value | |
|---|---|---|---|
| β₁ (ΔlnS) | +5.313 | 0.031 | * |
| β₃ (*L*) | +9.247 | <0.001 | *** |
| β₄ (*L* × ΔlnS) | −49.784 | 0.004 | ** |
| Velocity | −104.744 | <0.001 | *** |
| VIX | +0.011 | 0.098 | |
| ΔlnN* | +0.557 | 0.232 | |

*Note.* HAC standard errors (1 lag). *N* = 51. R² = 0.874.

### A.4 OIS–Treasury Spread Construction Notes

The convenience yield is measured as the 3-month T-bill rate minus the overnight indexed swap rate. We use DGS3MO (bond-equivalent yield basis) rather than DTB3 (discount basis), which understates yield by 5–10 bps. The OIS leg uses overnight SOFR rather than the 90-day trailing average SOFR90DAYAVG: the trailing average lagged overnight SOFR by up to 119 bps in March 2023, generating an implausibly wide spread of 84 bps in that month. Overnight SOFR produces a sample-period mean of 17 bps, in line with pre-2022 estimates of the U.S. convenience yield.

### A.5 Event Study: Normal Model and Placebo Design

The normal model is Δspread*_d* = α + γ₁·ΔVIX*_d* + γ₂·ΔlnN\**_d* + ε*_d*, estimated over the pre-event window [−120, −6] trading days via OLS. The original level-model specification inflated CARs approximately 120-fold by including the 2022 hiking trend in the estimation window; first-differencing corrects this. Event window: [−5, +20] trading days. Placebo pseudo-events: October 2022, June 2023, September 2024 — chosen as low-volatility periods with no major stablecoin or monetary policy news.
