# Stablecoins and the Exorbitant Privilege: Reserve Buffer Adequacy and OIS–Treasury Spread Dynamics

Mireu Mimi Kim · Sara Ambre Chekroune · Oybek Ibragimov · Jade Zhu · Alexandre Godefroy · Baptiste Degand · Minjin Kim

Yonsei Graduate School of International Studies · Topics in International Finance (2026-1) · Professor Hur Sewon

**JEL Classification:** E44, F31, G12, G18, G23

---

## Abstract

Large-scale USD-pegged stablecoins now hold Treasury bills at a scale comparable to mid-sized sovereign reserve managers, creating a structural channel through which stablecoin supply dynamics may affect the short-term U.S. government securities market. We document a "New Triffin Dilemma": in normal times, stablecoin issuance compresses the OIS–Treasury spread by increasing T-bill demand (the privilege channel), but an adequately thin liquid reserve buffer transforms expansion episodes into a fragility risk. We test this mechanism using an issuer-level panel of 102 observations covering USDT and USDC from January 2022 to March 2026. Supply growth is measured from DeFiLlama daily circulating supply; the liquid buffer *L* — Cash and Bank Deposits plus Money Market Funds — is constructed from BDO ISAE 3000R attestation PDFs verified quarter-by-quarter. The continuous buffer-interaction is not significant in the panel (β₄ = −4.35, *p* = 0.68), consistent with a nonlinear rather than proportional mechanism. Separating supply inflows from outflows, we find that supply contractions in low-buffer states (*L* < 12%) are associated with OIS–Treasury spread increases: the Low × Outflow coefficient β₅ = +7.55 (*p* = 0.065), identified by six low-buffer outflow observations spanning both issuers. The inflow coefficient is uniformly insignificant, consistent with the asymmetric theoretical prediction that only forced T-bill sales — triggered by outflows when buffers are depleted — generate spread pressure. We interpret this as suggestive evidence of a forced-sale channel and discuss implications for stablecoin reserve regulation.

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

**Asymmetric Threshold Specification.** To address non-stationarity and align with the theoretical mechanism, we use ΔSpread*_t* = Spread*_t* − Spread*_{t−1}* as the primary dependent variable, and decompose monthly supply growth into inflows and outflows:

Inflow*_it* = max(ΔlnS*_it*, 0); &ensp; Outflow*_it* = max(−ΔlnS*_it*, 0)

The theory predicts that only outflows in low-buffer states trigger forced T-bill sales; inflows (new T-bill purchases) are orderly by construction. We therefore estimate:

ΔSpread*_t* = α + β₁·Inflow*_it* + β₂·Outflow*_it* + β₃·**1**[*L_it* < *c*] + β₄·**1**[*L_it* < *c*]·Inflow*_it* + β₅·**1**[*L_it* < *c*]·Outflow*_it* + γ·controls + δ·USDT*_i* + ε*_it*

The key coefficient is β₅ (Low × Outflow): a positive and significant β₅ indicates that supply contractions in low-buffer states are associated with spread *increases*, consistent with the forced-sale channel. We evaluate this specification at *c* ∈ {10%, 12%}, reporting the *L* < 12% threshold as the primary result given its larger identification cell (six low-buffer outflow observations across both issuers), and *L* < 10% as a robustness check.

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

### 3.3 Asymmetric Threshold Specification

The symmetric threshold regression (reported in Appendix A.5) identifies an effect concentrated at very low *L*, but the sign — spread compression in low-buffer states as supply grows — does not directly confirm the fragility channel. Supply growth in low-buffer periods reflects high-demand conditions in which both supply and spreads are moving together, not the redemption-stress scenario the theory describes. This motivates the asymmetric decomposition described in Section 2.3: separating supply *inflows* (new issuance, requires T-bill purchases) from supply *outflows* (redemptions, may require T-bill sales) allows the data to distinguish the two regimes.

Table 3 reports the asymmetric specification at the two candidate thresholds. The key coefficient throughout is β₅ on the Low × Outflow interaction.

**Table 3. Asymmetric Threshold Panel: Low × Outflow Specification (DV = ΔSpread)**

| | *L* < 10% | *L* < 12% (primary) |
|---|---|---|
| β₁ Inflow | +0.507 | +0.518 |
| β₂ Outflow | −0.043 | −0.081 |
| β₃ Low | +0.035 | +0.008 |
| β₄ Low × Inflow | −0.923 | −0.335 |
| **β₅ Low × Outflow** | **+16.923*** (*p* < 0.001)** | **+7.552*** (*p* = 0.065)** |
| VIX | +0.010*** | +0.010*** |
| ΔlnN* | +0.050 | +0.084 |
| USDT fixed effect | −0.009 | +0.001 |
| *N* | 100 | 100 |
| Low-buffer outflow obs | 2 | 6 |
| *R*² | 0.141 | 0.119 |

*Note.* DV = ΔSpread (first-differenced). Standard errors clustered by month. Controls: VIX, ΔlnN*, USDT issuer dummy. Low-buffer outflow obs = observations with *L* < *c* and Outflow > 0 in the regression sample. ΔSpread loses 2 observations from first-differencing (N = 100 from 102). *** *p* < 0.01, ** *p* < 0.05, * *p* < 0.10.

At the *L* < 12% threshold — the primary specification — β₅ = +7.55 (*p* = 0.065), significant at the 10% level. This indicates that a one-unit increase in the monthly supply-contraction rate in a low-buffer state is associated with a 7.55 percentage-point increase in ΔSpread, consistent with the forced-sale channel: when liquid buffers are below 12%, stablecoin supply contractions are associated with increases in the T-bill-OIS spread.

The *L* < 10% threshold delivers a substantially larger coefficient (β₅ = +16.92, *p* < 0.001), but is identified by only two low-buffer outflow observations — both from USDT in early 2026. With a single issuer and only two data points, this result cannot rule out a USDT-specific or period-specific explanation and should be treated as exploratory. The *L* < 12% threshold uses six low-buffer outflow observations spanning both issuers (USDT and USDC) and multiple years (2023–2026), making it the more defensible identification basis.

Crucially, the inflow coefficients β₁ and β₄ are uniformly insignificant across both thresholds. Supply increases — which require issuers to *purchase* T-bills — do not generate significant spread effects regardless of the buffer level. The asymmetry is precisely what the forced-sale theory predicts: orderly T-bill purchases compress spreads smoothly; forced T-bill sales in depleted-buffer states generate pressure.

The evidence is strongest when we allow for asymmetry between stablecoin inflows and outflows. Supply contractions are associated with increases in the T-bill-OIS spread when issuers have low liquid buffers, consistent with a forced-sale channel.

As a robustness check, replacing the binary Low indicator with the continuous interaction *L* × Outflow yields β₅ = −18.58 (*p* = 0.120), consistent in sign with the forced-sale channel but less precisely estimated (Appendix A.6). The continuous specification implies that the outflow effect approaches zero as the buffer rises above approximately 20% — consistent with USDT's ability to absorb the May 2022 redemption wave ($10bn+) without T-bill sales when *L* ≈ 16%. The weaker statistical performance relative to the threshold specification is expected when the true relationship is concentrated at low buffer values rather than proportional across the full range of *L*.

![**Figure 3.** Supply growth (ΔlnS) versus spread change (ΔSpread), colored by buffer regime. The asymmetric pattern — outflows in low-buffer states coinciding with spread increases — is visible in the upper-left quadrant for low-buffer observations. High-buffer observations (blue circles) show no systematic relationship between supply changes and spread changes.](results/fig_paper_3_threshold_scatter.png){width=90%}

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

This paper provides suggestive empirical evidence that large-scale USD-pegged stablecoins have introduced a new source of potential fragility into the short-term U.S. government securities market, operating through the liquid reserve buffer. We extend Maggiori's (2017) framework to derive a testable threshold prediction and test it using a verified issuer-level panel of 102 observations. The linear buffer-interaction is weak (β₄ = −4.35, *p* = 0.68), consistent with the effect being nonlinear. An asymmetric threshold specification — separating supply inflows from outflows — finds that supply contractions in low-buffer states (*L* < 12%) are associated with spread *increases* (β₅ = +7.55, *p* = 0.065), identified by six low-buffer outflow observations spanning both issuers. The inflow coefficient is uniformly insignificant, consistent with the asymmetric prediction that only forced T-bill sales, triggered by outflows when buffers are depleted, generate spread pressure.

Two limitations constrain the strength of this conclusion. The significant result rests on only six identifying observations, and the non-stationarity of the level spread precludes straightforward inference from the continuous-*L* levels specification. The *L* < 10% robustness produces a larger coefficient (β₅ = +16.92) but is identified by only two observations, underscoring the need for additional data.

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

### A.5 Symmetric Threshold Specification (Exploratory)

For reference, the symmetric threshold specification — which does not distinguish inflows from outflows — is reported below. The main result (β₃ = −4.385 at *L* < 4%, *p* = 0.001) motivated the asymmetric decomposition in Section 3.3, but is interpretively limited: the negative sign reflects spread *compression* when supply is growing in low-buffer periods, not the spread *widening* the fragility channel predicts for a redemption scenario. All nine low-buffer observations are from USDT in a single window (mid-2025 to early 2026), and the result disappears at the 6% threshold (*p* = 0.64) and in the levels specification (*p* = 0.31).

| Threshold | Dep. Var. | β₁ (ΔlnS) | β₂ (**1**[*L*<*c*]) | β₃ (**1**[*L*<*c*]×ΔlnS) | *N* | *N*_low |
|---|---|---|---|---|---|---|
| *L* < 4% | ΔSpread | +0.003 | +0.094*** | −4.385*** (*p* = 0.001) | 100 | 9 |
| *L* < 4% | Spread | +2.024 | −0.480*** | +3.224 (*p* = 0.309) | 102 | 9 |
| *L* < 6% | ΔSpread | −0.093 | +0.036 | −0.561 (*p* = 0.639) | 100 | 23 |
| *L* < 6% | Spread | +1.618 | −0.643*** | +0.561 (*p* = 0.620) | 102 | 23 |

*Note.* SE clustered by month. Controls: VIX, ΔlnN*, USDT dummy. *** *p* < 0.01.

### A.6 Continuous-L Asymmetric Robustness Check

Replacing the binary Low indicator with a continuous *L* × Outflow interaction uses all 100 observations and avoids the sparse-cell concern raised by the threshold specification. The estimating equation is:

ΔSpread*_t* = α + β₁·Inflow*_it* + β₂·Outflow*_it* + β₃·*L_it* + β₄·*L_it* × Inflow*_it* + β₅·*L_it* × Outflow*_it* + γ·controls + δ·USDT*_i* + ε*_it*

The key coefficient is β₅ (*L* × Outflow): predicted negative — higher buffer dampens the outflow-spread link.

| Variable | Coefficient | *p*-value | |
|---|---|---|---|
| β₁ Inflow | −0.119 | 0.903 | |
| β₂ Outflow | +3.774 | 0.134 | |
| β₃ *L* | −0.132 | 0.797 | |
| β₄ *L* × Inflow | +3.307 | 0.642 | |
| **β₅ *L* × Outflow** | **−18.579** | **0.120** | |
| VIX | +0.009 | 0.003 | *** |
| ΔlnN* | +0.042 | 0.851 | |
| USDT fixed effect | −0.006 | 0.856 | |

*Note.* DV = ΔSpread. *N* = 100. SE clustered by month. R² = 0.120.

The sign of β₅ = −18.58 is in the predicted direction: higher liquid buffers reduce the spread impact of outflows. The total outflow effect at any buffer level is β₂ + β₅ × *L* = 3.774 − 18.579 × *L*, which approaches zero at *L* ≈ 20% (USDT's approximate buffer level in 2022) and reaches its maximum at *L* ≈ 0 (USDT's trajectory in early 2026). The coefficient is not significant at conventional levels (*p* = 0.12), reflecting the dilution of a nonlinear effect across the full range of *L*. The threshold specification, which concentrates the test at *L* < 12%, recovers greater statistical power precisely because the relationship is nonlinear. The two specifications are consistent in economic direction and implied break-even buffer level.

### A.7 Event Study: Normal Model and Placebo Design

The normal model is Δspread*_d* = α + γ₁·ΔVIX*_d* + γ₂·ΔlnN\**_d* + ε*_d*, estimated over the pre-event window [−120, −6] trading days via OLS. The original level-model specification inflated CARs approximately 120-fold by including the 2022 hiking trend in the estimation window; first-differencing corrects this. Event window: [−5, +20] trading days. Placebo pseudo-events: October 2022, June 2023, September 2024 — chosen as low-volatility periods with no major stablecoin or monetary policy news.
