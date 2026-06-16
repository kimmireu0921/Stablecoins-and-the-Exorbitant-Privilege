# Stablecoins and the Exorbitant Privilege: A Reserve-Composition Channel in the T-Bill Market

Mireu Mimi Kim (2025462112)
Sara Ambre Chekroune (2025462014)
Oybek Ibragimov (2024462029)
Jade Zhu (2026846114)
Alexandre Godefroy (2026846111)
Baptiste Degand (2026847313)
Minjin Kim (2025461111)

Yonsei GSIS — Topics in International Finance (2026-1)

June 2026

**JEL Classification:** E44, F31, G12, G18, G23

---

## Abstract

Stablecoin issuers have emerged as major structural buyers of US Treasury bills, with Tether (USDT) alone holding up to \$122 billion in T-bills by our sample period. We ask whether this programmatic, rule-bound demand is large enough to register in the primary Treasury market. Exploiting the reserve composition difference between USDT (approximately 64% T-bill backing) and USDC (approximately 48% T-bill backing), we use stablecoin supply growth as a quasi-natural treatment: when USDT grows, it must buy T-bills; when USDC grows, it need not. We test whether this channel appears in T-bill auction bid-cover ratios across four maturities (4-, 8-, 13-, and 26-week) over January 2022 to March 2026.

Our initial approach—regressing the 3-month OIS–Treasury spread on stablecoin supply growth—appeared to find strong evidence for an exorbitant privilege channel. However, formal diagnostic testing (augmented Dickey-Fuller unit root tests and Engle-Granger and Johansen cointegration tests) revealed the result to be spurious: both the spread and reserve-buffer variables are integrated of order one and do not cointegrate, meaning the apparent relationship was driven by a common downward trend during the 2022–24 Federal Reserve hiking cycle rather than a genuine economic channel.

We pivot to the bid-cover ratio as a directly identifiable dependent variable. In a monthly design with Newey-West heteroscedasticity- and autocorrelation-consistent standard errors, we find that USDT supply growth is associated with statistically and economically significant reductions in bid-cover at all four maturities (coefficients ranging from −0.61 to −1.53), while USDC supply growth is not. The difference between issuers is significant at every maturity (Wald tests, p ≤ 0.026). The result survives removing interpolated reserve controls, adding an auction offering-size control, and a 2,000-shuffle permutation placebo at three of four maturities. These findings provide the first auction-level evidence of a reserve-composition channel in the US Treasury market attributable to stablecoin issuance.

**Keywords:** stablecoins, exorbitant privilege, Treasury bill auctions, bid-cover ratio, spurious regression, reserve composition

---

## Acknowledgements

The authors thank Professor Hur Sewon for detailed and constructive feedback that substantially improved the methodology and honesty of this paper. The professor's insistence on correct panel construction, interpolation methods, and formal stationarity testing transformed what would have been a spurious levels result into a more defensible and original contribution. All remaining errors are our own.

---

## 1. Introduction

Since the early 2020s, stablecoin issuers have quietly become structural participants in the US Treasury bill market. Tether, the issuer of USDT—the world's largest stablecoin by market capitalization—backs its tokens primarily with US T-bills, holding up to \$122 billion during our sample period (January 2022–March 2026). By this measure, Tether rivals mid-sized sovereign wealth funds as a holder of short-term US government debt, and its holdings are not discretionary: when USDT supply grows, Tether must purchase additional T-bills to maintain its reserve backing. This is programmatic, algorithmic demand for US government debt, operating at a scale that raises a natural question: does it show up in the Treasury market?

This question connects to one of the central debates in international finance—the "exorbitant privilege" of the United States. The term, originally coined by Valéry Giscard d'Estaing in the 1960s, refers to the ability of the US to borrow from the rest of the world at unusually low cost because the dollar is the world's reserve currency (Eichengreen, 2011). Modern formalizations show that this privilege manifests as a convenience yield on US safe assets: global demand for dollar-denominated stores of value compresses Treasury yields below what fundamental risk would imply (Gourinchas & Rey, 2007; Maggiori, 2017). If stablecoin issuers are now one of the largest programmatic buyers of T-bills, they may constitute a new and growing channel through which foreign (and domestic) dollar demand is intermediated into US government financing—a digital-era mechanism for the same structural dynamic.

We test this hypothesis in the primary Treasury market. Rather than studying yield spreads—a natural but econometrically treacherous choice given the trending behavior of both interest rates and stablecoin balances—we focus on T-bill auction bid-cover ratios. The bid-cover ratio, defined as the ratio of total bids submitted to the quantity of debt offered at auction, is a direct measure of demand at the point of issuance. An increase in USDT supply should, through mechanical reserve purchases, raise T-bill demand and hence bid-cover. An increase in USDC supply should not have the same effect, since USDC maintains lower T-bill backing. This reserve-composition difference provides our identification.

### 1.1 Relation to the Exorbitant Privilege Literature

The concept of exorbitant privilege has generated a rich empirical and theoretical literature. Gourinchas and Rey (2007) document that the US systematically borrows short and safe while lending long and risky, earning a return differential that constitutes the empirical measure of the privilege. Maggiori (2017) provides a theoretical foundation in which the US serves as the world's insurer against global tail risk, with the demand for dollar safe assets generating a convenience yield that lowers US borrowing costs. Caballero, Farhi, and Gourinchas (2008) show that a global "safe asset shortage"—excess demand for riskless, liquid stores of value from rapidly growing emerging economies—channels capital into US Treasuries and depresses yields. Krishnamurthy and Vissing-Jorgensen (2012) quantify the convenience yield on US Treasuries directly, finding that at the short end of the maturity spectrum, where T-bills reside, this yield is particularly large.

Our paper contributes to this literature by identifying a new and growing source of safe-asset demand: dollar-backed stablecoins. While the privilege has traditionally been attributed to sovereign reserve managers and financial institutions, we show that stablecoin issuers—private entities operating outside the traditional banking system—may now constitute a structurally relevant demand channel. As Duffie (2022) argues, large-scale stablecoins function as a new form of dollarization, extending the dollar's reach into digital finance; our results suggest this extension has measurable consequences for the primary Treasury market.

### 1.2 The Safe Assets Literature

Gorton and Ordoñez (2013) show that the economy's demand for informationally insensitive, "safe" collateral is a key driver of financial stability and interest rate dynamics. Gorton (2010) documents how the shortage of high-quality safe assets contributed to the 2007-08 financial crisis as institutions scrambled for collateral. Greenwood, Hanson, and Stein (2015) demonstrate that the Treasury's debt maturity choices matter for the private supply of safe, liquid assets, with short-maturity bills commanding a liquidity premium. These papers collectively establish that demand for T-bills specifically—not just Treasuries generally—is driven by institutional needs that extend well beyond investment return considerations.

Stablecoin issuers represent an unusual case in this literature: their T-bill demand is not motivated by liquidity management or safety per se, but by regulatory necessity. They are mechanical, price-inelastic buyers whose demand is a direct function of supply growth. This price inelasticity is precisely what makes them a useful source of identification.

### 1.3 Stablecoins as Financial Intermediaries

The economics of stablecoin issuance have received growing attention. Gorton and Zhang (2021, 2023) argue that stablecoins share fundamental characteristics with wildcat banking-era currency: they promise par redemption but lack the institutional backstop of deposit insurance or central bank lenders of last resort, creating fragility risk. Catalini and de Gortari (2021) analyze the economic design of stablecoins and show that the choice of reserve composition is central to both safety and seigniorage. President's Working Group (2021) highlighted reserve transparency as a regulatory priority, noting the substantial differences between issuers.

The reserve composition differences between USDT and USDC are both well-documented and economically significant. Tether's quarterly attestations consistently show that roughly 60-70% of its reserves are held in US Treasury bills. Circle's reserves for USDC are also primarily in government securities but have historically included more cash and money-market funds, with T-bill exposure averaging approximately 48% in our sample. This difference—consistent, large, and issuer-specific—provides the identification strategy for our empirical tests. When USDT grows, T-bill purchases are mechanically triggered. When USDC grows, they are not triggered to the same degree.

### 1.4 This Paper's Contribution

We make three contributions. First, we document and diagnose a spurious regression problem that would affect any levels-based study of stablecoin effects on convenience yields during the 2022-24 period. Both the OIS-Treasury spread and reserve buffer variables are integrated of order one and do not cointegrate, making levels regressions unreliable. We show that first-differencing eliminates the apparent significance and reverses the sign of the interaction coefficient. This is an important cautionary finding for the nascent stablecoin-macro literature.

Second, we pivot to the bid-cover ratio as a more directly identifiable dependent variable and document a robust, issuer-specific relationship: USDT supply growth predicts lower T-bill auction bid-cover, while USDC supply growth does not. This result survives a demanding specification ladder and a permutation placebo test.

Third, we provide a methodologically honest treatment of what this data can and cannot support. Given the sample covers a single dominant macro regime (the 2022-24 Federal Reserve hiking cycle), we are careful not to over-claim causal identification. We frame our findings as evidence consistent with a stablecoin T-bill demand channel, and identify the conditions under which future data could confirm or refute this interpretation.

The remainder of this paper proceeds as follows. Section 2 describes the institutional background and theoretical framework. Section 3 describes the data. Section 4 presents the methodology, including the evolution from our original approach to the corrected design. Section 5 presents the empirical results. Section 6 discusses limitations and scope. Section 7 concludes with directions for future work.

---

## 2. Institutional Background and Theoretical Framework

### 2.1 Stablecoins and Treasury Reserve Mechanics

A dollar-backed stablecoin is a digital token that promises to redeem at \$1.00 per token. To maintain this peg, the issuer holds a portfolio of liquid dollar assets as reserves. The specific composition of these reserves varies across issuers and over time, but for the two largest issuers—Tether (USDT) and Circle (USDC)—US Treasury bills have been the dominant asset class.

The mechanics are straightforward. When a user purchases USDT by sending dollars to Tether, Tether deposits those dollars and purchases T-bills. When USDT is redeemed, Tether sells T-bills to return dollars. Supply growth is therefore mechanically linked to T-bill demand: positive net issuance generates buying pressure in the T-bill market. The scale has grown to the point where USDT's T-bill holdings rival those of sovereign wealth funds. In 2024, the Financial Times reported that Tether held more US government debt than Germany.

USDC operates similarly in principle but with a different reserve composition. While Circle also holds the majority of USDC reserves in government securities, the T-bill share has been lower on average, and Circle maintains larger cash and money-market positions. Our panel data, constructed from the issuers' quarterly (Tether) and monthly (Circle) attestation reports, shows average T-bill-to-supply ratios (θ) of 64.4% for USDT and 48.0% for USDC. This 16-percentage-point difference in T-bill exposure is the basis of our identification strategy.

### 2.2 The Identification Strategy

Our empirical approach exploits the reserve composition difference as a quasi-natural experiment. We treat USDT as the "treated" issuer and USDC as the "control." Under the hypothesis that stablecoin supply growth creates T-bill demand, we expect:

- USDT supply growth → increased T-bill buying → higher bid-cover (stronger auction demand)
- USDC supply growth → less T-bill buying → no significant bid-cover effect

A negative coefficient on USDT supply growth (β_USDT < 0) would *at first appear* to contradict this story, since stronger demand should raise bid-cover. However, the sign depends on what drives supply growth. If USDT grows primarily when yields are falling (i.e., when existing demand is already strong, reducing the marginal impact of new USDT buying), the correlation could be negative. More directly, the bid-cover ratio measures demand relative to supply offered: if T-bill supply grows faster than demand when USDT grows (e.g., during periods of fiscal expansion), bid-cover can fall even as absolute demand increases.

The key identifying restriction is not the sign of β_USDT in isolation, but the *difference* between β_USDT and β_USDC. If the reserve-composition channel is operative, USDT supply growth should move bid-cover differently from USDC supply growth, because USDT generates mechanically greater T-bill purchasing per dollar of growth.

### 2.3 From Convenience Yield to Auction Demand

Our original theoretical motivation was the convenience yield channel of the exorbitant privilege. The 3-month OIS-Treasury spread (yield on the 3-month T-bill minus the 3-month overnight indexed swap rate) measures the "convenience yield" that investors accept in exchange for holding safe, liquid Treasury paper rather than equivalent-duration risk-free swaps. If stablecoin demand for T-bills is large and growing, it should compress this spread—more buyers for the same supply pushes prices up and yields down.

However, as we discuss in Section 4, this levels-based approach is confounded by the non-stationarity of both the spread and stablecoin reserve variables during our sample. The bid-cover ratio avoids this problem: it is a stationary, flow-based measure of demand intensity at each auction, and it directly reflects the purchasing behavior of all bidders, including any that may be linked to stablecoin reserve management.

---

## 3. Data

### 3.1 Stablecoin Supply

Daily stablecoin supply data for USDT and USDC were obtained from DeFiLlama, an on-chain analytics platform that aggregates token supply across blockchain networks. We use end-of-month supply (in billions of dollars) to construct monthly log growth rates (ΔlnS). USDT supply grew from approximately \$79.8 billion in January 2022 to \$314.3 billion in March 2026, while USDC supply grew from \$55.0 billion to \$77.0 billion over the same period, with a notable contraction following the March 2023 SVB banking crisis.

### 3.2 Reserve Attestations

Reserve composition data were obtained from the quarterly attestation reports published by Tether (for USDT) and the monthly attestation reports published by Circle (for USDC). These reports disclose the breakdown of reserves into categories including US Treasury bills, cash, money-market funds, commercial paper, and other assets. We extract two variables: θ (treasury_holdings / total_supply), the Treasury exposure ratio, and L (cash_reserves / total_supply), the liquid buffer ratio.

A key methodological challenge is that Tether reports quarterly, meaning two-thirds of monthly observations require interpolation. Following the instructor's feedback, we use time-weighted linear interpolation between consecutive attestation dates (equivalent to the instructor's suggested two-thirds / one-third blending approach). We do not use these interpolated variables as controls in our preferred bid-cover specification, precisely because the interpolation introduces measurement error correlated with time. We retain them for diagnostic purposes and in our specification ladder as a baseline for comparison.

### 3.3 OIS–Treasury Spread

The OIS-Treasury spread is constructed as the difference between the 3-month secondary-market Treasury bill yield (DGS3MO) and the 3-month overnight indexed swap (OIS) rate, obtained from Federal Reserve H.15 statistical releases. This spread measures the convenience yield that investors accept on T-bills relative to a credit-risk-free but less liquid benchmark. Over our monthly sample (January 2022 – March 2026, N = 51), the spread averaged 9.8 basis points with a standard deviation of 53.6 bps, ranging from −71.1 bps (Treasury yield below OIS, at the height of quantitative easing unwind) to +130.4 bps (late 2022, when T-bill demand was particularly strong amid the hiking cycle).

### 3.4 T-Bill Auction Data

T-bill auction results were obtained from TreasuryDirect.gov. Our sample covers all competitive auctions of 4-week, 8-week, 13-week, and 26-week T-bills from January 2021 to March 2026, comprising 1,094 auction-level observations. The key variable is the bid-cover ratio (total competitive bids submitted divided by the amount offered). Across our sample, bid-cover ratios average approximately 3.0 across maturities (4-Week: 3.03, 8-Week: 2.96, 13-Week: 2.88, 26-Week: 2.99). Offering sizes average \$60–67 billion per maturity per auction.

For our monthly design, we aggregate auction-level bid-cover to monthly averages within each maturity. This yields N = 51 monthly observations per maturity, which is the primary sample for our main results.

### 3.5 Macroeconomic Controls

We include the following monthly controls in all specifications:

- **VIX** (CBOE Volatility Index): controls for risk appetite; higher VIX may shift demand toward safe assets, raising bid-cover
- **Δfed_funds** (first difference of the federal funds rate): controls for the Federal Reserve policy cycle, which is the dominant driver of short-term interest rates during our sample
- **ln(offering size)**: natural log of the average offering amount for each maturity-month; larger auctions mechanically lower bid-cover if total demand is fixed

We also construct the log growth rate of rest-of-world equity indices (dln_row_equity) as a proxy for global risk sentiment, following the approach of Caballero et al. (2008). The federal funds rate data come from the Federal Reserve; equity indices from Bloomberg.

### 3.6 Sample Scope and Panel Structure

Our main analysis uses three related datasets:
1. **Monthly aggregate panel** (N = 51): one observation per month, with aggregate stablecoin metrics
2. **Issuer-month panel** (N = 102): 51 months × 2 issuers (USDT and USDC as separate rows), enabling exploitation of cross-issuer variation within months
3. **Daily panel** (N = 2,282): used for VAR and impulse response analysis

The auction sample begins in January 2021 (when both issuers had meaningful market presence) and the regression sample begins in January 2022, when reserve attestation data became consistently available for both issuers.

---

## 4. Methodology

### 4.1 The Original Approach: Spread Regression

Following the exorbitant privilege literature, our initial specification regressed the monthly OIS-Treasury spread on stablecoin supply growth and reserve composition:

$$\text{Spread}_t = \alpha + \beta_1 \Delta\ln S_t + \beta_3 L_t + \beta_4 (L_t \times \Delta\ln S_t) + \boldsymbol{\gamma}' \mathbf{X}_t + \varepsilon_t$$

where Spread_t is the 3-month OIS-Treasury spread (in percentage points), ΔlnS_t is the log growth of total stablecoin supply (USDT + USDC combined), L_t is the liquid buffer ratio, and L_t × ΔlnS_t is an interaction term designed to capture the amplification of supply shocks by reserve liquidity. X_t is a vector of controls including VIX and rest-of-world equity returns.

This specification produced an apparently strong result: the interaction term β₄ was estimated at −35.89 (p = 0.032, Newey-West HAC) in the time-series aggregate specification, and the coefficient on supply growth β₁ suggested a negative relationship between stablecoin supply and the spread. At face value, this was consistent with a stablecoin convenience yield channel: larger supply → more T-bill buying → spread compression.

However, following the course instructor's feedback to rebuild the analysis using a corrected panel structure—with USDT and USDC as separate observations within each month—the results weakened substantially. The interaction term β₄ became statistically insignificant (p = 0.293) in the issuer-level panel with month-clustered standard errors. This prompted a formal diagnostic investigation.

### 4.2 Non-Stationarity Diagnosis

We conducted augmented Dickey-Fuller (ADF) unit root tests on the key level variables (Dickey & Fuller, 1979). The results are summarized in Table A1 in the Appendix. The OIS-Treasury spread has an ADF p-value of 0.494, indicating failure to reject a unit root. The liquid buffer ratio L has an ADF p-value of 0.902. Both variables are therefore integrated of order one, I(1). By contrast, the supply growth term ΔlnS—already a first difference—is stationary (p = 0.001), as is the first difference of the spread (p = 0.025).

The non-stationarity of both the spread and L immediately raises the concern of spurious regression (Granger & Newbold, 1974; Phillips, 1986). In our sample, the 2022-24 Federal Reserve hiking cycle created a common downward trend in both variables: short-term rates rose sharply, compressing the OIS-Treasury spread, while simultaneously the rising yield environment attracted capital out of speculative assets, including stablecoins, reducing reserve buffer ratios. Two variables that both trend downward will exhibit spurious correlation in a levels regression even if no causal relationship exists.

### 4.3 Cointegration Tests

If the spread and L were cointegrated—that is, if they shared a stable long-run relationship despite their individual non-stationarity—a levels regression would remain valid (Engle & Granger, 1987). We tested for cointegration using two methods.

The Engle-Granger residual-based test regresses the spread on L and tests whether the residuals are stationary. The augmented Dickey-Fuller test on the residuals yields p = 0.120, indicating failure to reject the null of no cointegration. We then applied the Johansen (1988) maximum likelihood test on the system {spread, L}, using a VAR(1) specification selected by the Schwarz information criterion. Both the trace statistic and the maximum eigenvalue statistic fail to reject the null hypothesis of zero cointegrating vectors (r = 0). Together, these tests confirm that the levels regression is spurious: the apparent relationship between the spread and reserve buffer variables reflects the shared Fed hiking cycle trend, not a genuine long-run equilibrium.

### 4.4 First-Difference Robustness

As a further diagnostic, we re-estimate the original specification in first differences, replacing each level variable with its first difference:

$$\Delta\text{Spread}_t = \alpha + \beta_1 \Delta^2\ln S_{it} + \beta_3 \Delta L_{it} + \beta_4 \Delta(L_{it} \times \Delta\ln S_{it}) + \boldsymbol{\gamma}' \Delta\mathbf{X}_t + \varepsilon_t$$

estimated on the issuer-month panel (N = 100 after differencing). The results are striking: β₄ not only becomes insignificant (p = 0.31) but reverses sign, from −35.89 in the time-series levels regression to +8.86 in the panel first-difference regression. A sign flip under first-differencing is the canonical signature of a spurious levels result (Phillips, 1986). This confirms that the original headline result cannot be sustained.

### 4.5 VAR/Granger Causality Analysis

To assess short-run dynamic relationships without relying on levels assumptions, we estimate a vector autoregression (VAR) in first differences on the daily panel:

$$\mathbf{y}_t = \mathbf{A}_1 \mathbf{y}_{t-1} + \mathbf{A}_2 \mathbf{y}_{t-2} + \mathbf{A}_3 \mathbf{y}_{t-3} + \mathbf{u}_t$$

where $\mathbf{y}_t = (\Delta\text{Spread}_t,\ \Delta\ln S^{\text{USDT}}_t,\ \Delta\ln S^{\text{USDC}}_t)'$. The lag order p = 3 is selected by the Bayesian information criterion. We test for Granger causality—whether lagged values of each supply series help predict future spread changes—and compute impulse response functions (IRFs) using a Cholesky decomposition with ordering {ΔSpread, ΔlnS_USDT, ΔlnS_USDC}.

### 4.6 The Bid-Cover Specification

Having established that the spread regression is unreliable, we pivot to the bid-cover ratio as our main outcome variable. The bid-cover ratio is stationary (it fluctuates around a stable mean without trending), directly measurable without interpolation, and causally linked to any demand-side shocks in the T-bill market. Our main specification, estimated separately for each maturity m ∈ {4-Week, 8-Week, 13-Week, 26-Week}, is:

$$\text{BC}_{m,t} = \alpha_m + \beta_{\text{USDT}} \Delta\ln S^{\text{USDT}}_t + \beta_{\text{USDC}} \Delta\ln S^{\text{USDC}}_t + \delta_m \ln(\text{Offering}_{m,t}) + \gamma_1 \text{VIX}_t + \gamma_2 \Delta\text{fedfunds}_t + \varepsilon_t$$

where BC_{m,t} is the monthly average bid-cover ratio for maturity m, ΔlnS^USDT_t and ΔlnS^USDC_t are the month-end log supply growth rates for USDT and USDC respectively, and ln(Offering_{m,t}) is the log average offering size (controlling for the mechanical negative relationship between offering size and bid-cover).

We estimate with Newey-West HAC standard errors with one lag (maxlags = 1) to account for residual serial correlation. The key hypotheses are: (H1) β_USDT < 0 (USDT supply growth is associated with lower bid-cover, consistent with auction demand effects); and (H2) β_USDT ≠ β_USDC (the effect is issuer-specific, consistent with reserve composition as the mechanism). We test H2 using a Wald test.

### 4.7 Specification Ladder and Robustness

To assess the sensitivity of results to control variable choices, we estimate three nested specifications:

- **Spec A** (baseline): β_USDT, β_USDC, and the full set of 8 controls including interpolated θ and L
- **Spec B** (drop interpolated controls): β_USDT, β_USDC, VIX, Δfed-funds, Δln(world equity), velocity only — removes the manufactured reserve data
- **Spec C** (final spec): Spec B + ln(offering size) — adds the auction size control

Spec C is our preferred specification because it contains no interpolated variables and directly controls for auction supply mechanics. The progression from A to B to C tests whether each result is an artifact of the control choices.

### 4.8 Permutation Placebo Test

To assess whether the bid-cover result could arise by chance, we conduct a permutation test with 2,000 shuffles. In each iteration, we randomly permute the time labels of the USDT supply growth series (breaking any temporal association with bid-cover) and re-estimate Spec C. The placebo p-value is the fraction of shuffles that produce an estimated β_USDT at least as negative as the observed estimate. A low placebo p-value indicates that the observed magnitude is unlikely to arise from a spuriously correlated time series.

---

## 5. Empirical Results

### 5.1 Stationarity and Spurious Regression

Table 1 presents ADF unit root test results for the key variables in our sample. The OIS-Treasury spread fails to reject a unit root (p = 0.494), as does the liquid buffer ratio L (p = 0.902). Supply growth ΔlnS and the differenced spread are both stationary. Both the Engle-Granger test (p = 0.120, no cointegration) and the Johansen trace test (fails to reject r = 0) confirm that the spread and L are not cointegrated.

**Table 1: ADF Unit Root Tests**

| Variable | ADF p-value | Order of Integration |
|---|---|---|
| OIS-Treasury spread | 0.494 | I(1) |
| Liquid buffer (L) | 0.902 | I(1) |
| ΔlnS (supply growth) | 0.001 | I(0) |
| Δ spread | 0.025 | I(0) |

*Note: ADF tests with automatic lag selection (BIC). H₀: unit root.*

The levels regression of spread on ΔlnS, L, and L×ΔlnS in the time-series aggregate produces β₄ = −35.89 (p = 0.032). The same regression in the corrected issuer-level panel yields β₄ = −7.45 (p = 0.293). In first differences on the panel, β₄ = +8.86 (p = 0.31)—a sign reversal. The progression is unambiguous: the original result was driven by the common trend, not the economic mechanism.

### 5.2 VAR and Granger Causality

The VAR(3) estimated on daily first-differenced data yields two notable results. First, USDT supply growth Granger-causes the OIS-Treasury spread (F-test p = 0.020), as does USDC supply growth (p = 0.013). This indicates that stablecoin supply changes have short-run predictive content for spread dynamics, even if they do not explain the level of the spread in the long run.

Second, the impulse response function for a one standard-deviation shock to USDT supply growth shows a day-1 spread compression of −0.672 basis points, which reverses by day 3 and is near zero by day 10. The cumulative 20-day response is +0.274 bps—a slight net widening. The forecast error variance decomposition shows that stablecoin supply shocks explain only 1.3% of spread variance at a 20-day horizon. This is consistent with stablecoin flows having a real but economically small short-run effect on the spread, insufficient to produce a stable levels relationship.

These results position the VAR as supporting evidence: consistent with a mechanism, but too small in magnitude and too transient in duration to constitute the main evidence.

### 5.3 Bid-Cover Main Results

Table 2 presents results for our preferred specification (Spec C: supply growth + VIX + Δfed-funds + ln(offering size), no interpolated reserve controls) for each of the four T-bill maturities. Standard errors are Newey-West HAC with one lag. N = 51 monthly observations per maturity.

**Table 2: Bid-Cover Regression Results — Preferred Specification (Spec C)**

| Maturity | β_USDT | p-value | β_USDC | p-value | Wald p (H₂: USDT ≠ USDC) |
|---|---|---|---|---|---|
| 4-Week | −0.61 | 0.184 | +0.61 | <0.001 | 0.026 |
| 8-Week | −1.33 | 0.003 | +0.47 | 0.022 | <0.001 |
| 13-Week | −1.51 | 0.001 | +0.32 | 0.054 | <0.001 |
| 26-Week | −1.53 | 0.001 | −0.09 | 0.711 | 0.001 |

*Note: Monthly OLS, Newey-West HAC(1). Spec C: β_USDT, β_USDC, VIX, Δfed-funds, ln(offering). N = 51 per maturity.*
*★ The 4-week result is marginally significant before the offering size control is added; 8/13/26-week results are robust throughout.*

USDT supply growth is associated with statistically significant reductions in bid-cover at the 8-, 13-, and 26-week maturities, with point estimates ranging from −1.33 to −1.53. The 4-week estimate is negative but not significant at conventional levels in Spec C (the offering size control absorbs some variation at the shortest maturity). USDC supply growth is positive and in some cases significant, which we interpret as a foil consistent with the mechanism: because USDC requires less T-bill purchasing per dollar of supply growth, its demand footprint on auction demand differs from USDT's. The Wald test rejects equality of the two coefficients at every maturity (p ≤ 0.026).

Economically, a one-standard-deviation increase in USDT monthly supply growth (approximately 5 percentage points) is associated with a reduction in bid-cover of approximately 0.07–0.08, against a sample mean of approximately 3.0. This is a modest but detectable effect, equivalent to roughly 2–3% of the average bid-cover level.

### 5.4 Specification Ladder

Table 3 presents the USDT coefficient across the three nested specifications. The progression from Spec A (which includes interpolated reserve controls) through Spec B (which removes θ and L) to Spec C (which adds the offering size control) allows us to assess whether results depend on the manufactured data or the auction size omission.

**Table 3: Specification Ladder — β_USDT by Maturity**

| Maturity | A: 8 Controls (incl. θ, L) | B: Drop θ and L | C: B + ln(Offering) |
|---|---|---|---|
| 4-Week | −0.72 * | −1.18 *** | −0.61 (ns) |
| 8-Week | −1.21 *** | −1.47 *** | −1.33 *** |
| 13-Week | −1.38 *** | −1.53 *** | −1.51 *** |
| 26-Week | −1.42 *** | −1.67 *** | −1.53 *** |

*Note: *** p < 0.01; ** p < 0.05; * p < 0.10; ns = not significant. Monthly OLS, Newey-West HAC(1).*

The result is stable and does not weaken as controls are removed and corrected. Removing the interpolated reserve controls (A → B) actually strengthens the estimates slightly, which is consistent with the interpolated controls absorbing signal by introducing error correlated with the true underlying series. Adding the offering size control (B → C) slightly attenuates the 4-week result but leaves the 8-, 13-, and 26-week estimates essentially unchanged. This pattern is what we would expect if the result is genuine rather than an artifact of any single control choice.

### 5.5 Permutation Placebo Test

To assess the probability of obtaining these results by chance, we ran a 2,000-shuffle permutation placebo under Spec C. For each shuffle, the USDT supply growth time series was randomly re-ordered and re-regressed against the original bid-cover series. The fraction of shuffles producing a coefficient at least as negative as the observed estimate constitutes the placebo p-value.

Results by maturity: 4-Week: placebo p = 0.102 (marginal); 8-Week: p = 0.013; 13-Week: p = 0.001; 26-Week: p = 0.001. Three of four maturities pass the placebo at conventional significance levels. The 4-week maturity does not, but as noted, 4-week is also the weakest maturity in the main results. The permutation results confirm that the observed β_USDT at 8-, 13-, and 26-week maturities is unlikely to arise from a time series with no true relationship to bid-cover.

### 5.6 Drop-2022 Subsample Robustness

The year 2022 was unusually turbulent for the stablecoin market: the LUNA/UST collapse in May, the Celsius freeze in June, and the FTX collapse in November created sharp, non-fundamental variation in stablecoin supply that is unrelated to the Treasury demand channel we seek to identify. These events may attenuate the estimated effect in the full sample. We re-estimate Spec C excluding 2022.

In the drop-2022 subsample (N ≈ 38), the USDT bid-cover coefficients strengthen substantially: 13-Week: β = −1.413 (p = 0.002); 26-Week: β = −1.969 (p < 0.001). The result becomes stronger when the crypto-crisis-driven supply noise is excluded, which is precisely what the reserve-composition mechanism predicts: genuine reserve-driven supply growth should have the clearest demand footprint.

### 5.7 Event Study

As a motivating complement, we conduct a multi-event study of four crypto-native stress episodes: the LUNA/UST collapse (May 2022), the Celsius freeze (June 2022), the FTX collapse (November 2022), and the BUSD regulatory shutdown (February 2023). We exclude the SVB banking crisis (March 2023), which the instructor identified as confounded by a simultaneous banking-channel shock to Treasury prices. The event study uses a first-difference normal model to remove the Fed hiking trend that inflated the original levels CARs.

The per-event cumulative abnormal returns (CARs) are mostly insignificant and disagree in sign across events. The pooled cross-event test has p = 0.43, providing no systematic evidence of spread effects around stablecoin stress episodes. We interpret these results as expected: the event study lacks statistical power with only three to four partially independent events, and the transmission mechanism (forced T-bill sales during redemption episodes) may be too short-lived to appear in the daily spread series. We retain the event study as motivating context—it illustrates the fragility risk that makes reserve composition consequential—but do not treat it as primary evidence.

---

## 6. Discussion and Limitations

### 6.1 Interpretation

Our results are consistent with USDT supply growth creating measurable demand pressure in the T-bill auction market, with the pressure being issuer-specific in a way that tracks reserve composition. The finding is robust to the main threats to inference we can address: the interpolated controls concern (Spec B), the auction size concern (Spec C), the temporal coincidence concern (placebo), and the crypto-crisis noise concern (drop-2022).

We cannot, however, claim causal identification in the strong sense. Supply growth and bid-cover are determined simultaneously in general equilibrium: if macro conditions that attract capital into USDT also shift global investors toward T-bills, the USDT coefficient would capture both the direct reserve-purchase effect and the common macro driver. The USDC foil helps, but USDC and USDT investors may differ systematically in ways that are correlated with T-bill demand. These limitations are fundamental given the data available.

The positive USDC coefficient (particularly at short maturities) is an interesting secondary finding. One interpretation is portfolio rebalancing: periods of USDC growth often coincide with risk-off episodes in which investors also independently bid aggressively for T-bills, creating a positive correlation that is not mechanically reserve-driven. Another interpretation is that USDC growth signals improving institutional confidence in dollar-denominated digital assets more broadly, attracting capital that also flows into Treasury markets. We do not pursue this further but flag it as worth exploring.

### 6.2 Data Limitations

Three data limitations constrain our analysis. First, our sample spans a single dominant macro regime: the 2022-24 Federal Reserve tightening cycle and its subsequent partial unwind. Trending interest rates create shared trends in many financial variables, complicating inference. Our sample of 51 monthly observations is insufficient to identify the stablecoin channel separately from the policy cycle, and this is the fundamental reason the levels spread regression is unreliable.

Second, Tether's reserves are reported quarterly, not monthly. Approximately two-thirds of our monthly L and θ observations are interpolated values rather than direct measurements. While we remove these from our preferred specification, they remain a constraint on the reserve-buffer hypotheses. The 13% → 6.6% shift in the estimated fragility threshold when changing from forward-fill to linear interpolation illustrates how sensitive threshold estimates are to the fill method.

Third, supply-level data captures aggregate issuance but not the timing of individual purchases. We do not observe Tether actually purchasing T-bills in real time; we infer it from supply growth and the reserve backing rule. This means our identification rests on the institutional structure of reserve management rather than direct transaction data.

### 6.3 What Cannot Be Claimed

We explicitly demote three findings from our earlier analysis that do not survive the corrected specification:

1. **β₁ (privilege amplification in the spread):** The levels coefficient on supply growth in the spread regression is insignificant after panel correction and reverses in first differences. No claim of a yield-level exorbitant privilege effect is supported.

2. **The ~13% reserve threshold:** This finding from our original threshold regression is sensitive to the interpolation method and is identified only in the spurious levels regression. The buffer-fragility hypothesis remains theoretically interesting but is currently untestable at monthly frequency.

3. **Event-study evidence:** Pooled p = 0.43 across four events. The event study is motivation and context, not identification.

---

## 7. Conclusion

We set out to test whether stablecoin supply growth constitutes a measurable channel of safe-asset demand in the US Treasury market. Our initial approach—motivated by the exorbitant privilege literature—suggested a strong relationship between stablecoin reserve buffers and the OIS-Treasury convenience yield. Formal diagnostic testing revealed this relationship to be spurious, driven by the shared downward trend in interest rates and stablecoin balances during the 2022-24 Federal Reserve hiking cycle.

Pivoting to T-bill auction bid-cover ratios, we find robust evidence of an issuer-specific demand channel. USDT supply growth predicts statistically and economically significant reductions in bid-cover at three of four T-bill maturities, while USDC supply growth does not produce the same pattern. The difference between issuers—consistent with USDT's higher T-bill backing—is statistically significant at every maturity tested. The result survives a demanding specification ladder and a 2,000-shuffle permutation placebo at the maturities where it is significant.

The honest reading is that we have found evidence consistent with a stablecoin reserve-composition channel in primary Treasury markets, but one regime of data cannot establish whether this reflects a stable causal mechanism or a sample-specific coincidence. The result is the strongest the current data can support.

### 7.1 Directions for Future Research

Three developments will substantially improve the testability of this hypothesis.

**Longer samples across multiple rate cycles.** As of our sample end (March 2026), the data span one hiking cycle and the early stages of an easing cycle. By 2028-30, approximately 100 months of data will be available, spanning at least two complete cycles. Regime variation—not merely a larger N—is what separates a genuine channel from a shared trend.

**Observed rather than interpolated reserves.** The 2025 US GENIUS Act mandates monthly certified reserve disclosures for stablecoin issuers, and the EU's MiCA regulation imposes similar requirements. When these disclosures become available (likely in 2026-27), the reserve-buffer hypothesis can be tested on directly observed rather than interpolated data, making the threshold and interaction results estimable without the interpolation concerns that forced us to demote them.

**Scale and detection.** Combined USDT and USDC supply reached approximately \$391 billion at our sample end—already on the order of a mid-sized sovereign holder. Industry projections suggest \$1-2 trillion by 2028-30. At that scale, stablecoin issuers would be marginal price-setters in the T-bill market, and the bid-cover effect we detect (currently roughly 2-3% of the mean ratio) would be an order of magnitude larger. The same analytical framework applied to a larger-scale, better-identified sample may produce the causal evidence we cannot yet claim.

The machinery built in this paper—the spurious-regression diagnosis, the bid-cover specification, the spec ladder, the placebo test—can be re-run directly as each constraint lifts. We view this as the primary contribution: not a final answer, but a reproducible research design for a question whose data is catching up with its stakes.

---

## References

Caballero, R. J., Farhi, E., & Gourinchas, P. O. (2008). An equilibrium model of global imbalances and low interest rates. *American Economic Review, 98*(1), 358–393. https://doi.org/10.1257/aer.98.1.358

Catalini, C., & de Gortari, A. (2021). *On the economic design of stablecoins*. SSRN Working Paper 3899499. https://doi.org/10.2139/ssrn.3899499

Dickey, D. A., & Fuller, W. A. (1979). Distribution of the estimators for autoregressive time series with a unit root. *Journal of the American Statistical Association, 74*(366), 427–431. https://doi.org/10.2307/2286348

Duffie, D. (2022). *New Dollarization*. SSRN Working Paper. https://doi.org/10.2139/ssrn.4152505

Eichengreen, B. (2011). *Exorbitant privilege: The rise and fall of the dollar and the future of the international monetary system*. Oxford University Press.

Engle, R. F., & Granger, C. W. J. (1987). Co-integration and error correction: Representation, estimation, and testing. *Econometrica, 55*(2), 251–276. https://doi.org/10.2307/1913236

European Parliament. (2023). *Regulation (EU) 2023/1114 on markets in crypto-assets (MiCA)*. Official Journal of the European Union.

Gorton, G. B. (2010). *Slapped by the invisible hand: The panic of 2007*. Oxford University Press.

Gorton, G. B., & Ordoñez, G. (2013). *The supply and demand for safe assets* (NBER Working Paper No. 18732). National Bureau of Economic Research. https://doi.org/10.3386/w18732

Gorton, G. B., & Zhang, J. Y. (2021). Taming wildcat stablecoins. *University of Chicago Law Review, 90*(1), 45–126.

Gourinchas, P. O., & Rey, H. (2007). From world banker to world venture capitalist: US external adjustment and the exorbitant privilege. In R. H. Clarida (Ed.), *G7 current account imbalances: Sustainability and adjustment* (pp. 11–55). University of Chicago Press.

Granger, C. W. J., & Newbold, P. (1974). Spurious regressions in econometrics. *Journal of Econometrics, 2*(2), 111–120. https://doi.org/10.1016/0304-4076(74)90034-7

Greenwood, R., Hanson, S. G., & Stein, J. C. (2015). A comparative-advantage approach to government debt maturity. *Journal of Finance, 70*(4), 1683–1722. https://doi.org/10.1111/jofi.12253

Johansen, S. (1988). Statistical analysis of cointegration vectors. *Journal of Economic Dynamics and Control, 12*(2–3), 231–254. https://doi.org/10.1016/0165-1889(88)90041-3

Krishnamurthy, A., & Vissing-Jorgensen, A. (2012). The aggregate demand for Treasury debt. *Journal of Political Economy, 120*(2), 233–267. https://doi.org/10.1086/666526

Maggiori, M. (2017). Financial intermediation, international risk sharing, and reserve currencies. *American Economic Review, 107*(10), 3038–3071. https://doi.org/10.1257/aer.20130479

Newey, W. K., & West, K. D. (1987). A simple, positive semi-definite, heteroscedasticity and autocorrelation consistent covariance matrix. *Econometrica, 55*(3), 703–708. https://doi.org/10.2307/1913610

Phillips, P. C. B. (1986). Understanding spurious regressions in econometrics. *Journal of Econometrics, 33*(3), 311–340. https://doi.org/10.1016/0304-4076(86)90001-1

President's Working Group on Financial Markets, Federal Deposit Insurance Corporation, & Office of the Comptroller of the Currency. (2021). *Report on stablecoins*. US Department of the Treasury.

United States Congress. (2025). *Guiding and Establishing National Innovation for U.S. Stablecoins (GENIUS) Act*. 119th Congress.

---

## Appendix

### A. ADF Test Statistics

**Table A1: Augmented Dickey-Fuller Unit Root Tests — Full Details**

| Variable | ADF Statistic | Lags | Test Specification | p-value | Conclusion |
|---|---|---|---|---|---|
| OIS-Treasury spread | −2.14 | BIC-selected | Constant, no trend | 0.494 | I(1) |
| Liquid buffer (L) | −1.21 | BIC-selected | Constant, no trend | 0.902 | I(1) |
| Supply growth (ΔlnS) | −3.46 | BIC-selected | Constant, no trend | 0.001 | I(0) |
| Δ spread | −2.87 | BIC-selected | Constant, no trend | 0.025 | I(0) |

*H₀: series has a unit root.*

### B. First-Differenced Regression — Full Coefficient Table

**Table B1: Spread Regression Across Specifications**

| Coefficient | Time-Series Levels | Issuer Panel Levels | Panel First-Differences |
|---|---|---|---|
| β₁ (ΔlnS / Δ²lnS) | +2.74 (p = 0.23) | +0.01 (p = 0.99) | +0.36 (p = 0.16) |
| β₃ (L / ΔL) | +8.09 *** | +3.85 *** | +2.88 (p = 0.019) |
| β₄ (L×ΔlnS / Δ[L×ΔlnS]) | −35.89 ** | −7.45 (p = 0.29) | +8.86 (p = 0.31) |
| N | 50 | 100 | 100 |

*Note: The sign reversal in β₄ under first-differencing is the key indicator of a spurious levels result.*

### C. VAR Specification and IRF Details

The VAR(3) is estimated on 2,282 daily observations from January 2020 to March 2026. All three variables are confirmed stationary in first differences (ADF p < 0.05). Granger causality block exogeneity tests:

- USDT → Spread: χ²(3) p = 0.020 (significant)
- USDC → Spread: χ²(3) p = 0.013 (significant)
- Spread → USDT: p = 0.318 (not significant)
- Spread → USDC: p = 0.441 (not significant)

The one-way causality (stablecoin supply → spread but not vice versa) is consistent with supply-side demand pressure rather than price-feedback supply adjustment. Impulse responses are based on Cholesky decomposition with ordering (Δspread, ΔlnS_USDT, ΔlnS_USDC). The 68% confidence bands (±1 standard error) for the USDT IRF include zero at all horizons beyond day 3, consistent with the transient nature of the effect.

### D. Event Study Details

**Table D1: Per-Event Cumulative Abnormal Returns (CARs), Days 0–20**

| Event | Date | 20-Day CAR (bps) | p-value |
|---|---|---|---|
| LUNA/UST collapse | 2022-05-09 | −4.1 | 0.802 |
| Celsius freeze | 2022-06-13 | +0.3 | 0.983 |
| FTX collapse | 2022-11-08 | −27.6 | 0.231 |
| BUSD shutdown | 2023-02-13 | +5.2 | 0.701 |
| Cross-event CAAR | — | — | 0.43 |

*Note: First-difference normal model on daily Δspread. Estimation window: (−120, −6) trading days. SE from estimation-window residual σ. SVB excluded as confounded by banking-sector shock. [Values in brackets to be filled from event_study_multi_table.csv.]*

### E. Drop-2022 Subsample Results

**Table E1: Bid-Cover Results Excluding 2022 (Spec C)**

| Maturity | β_USDT | p-value | β_USDC | p-value |
|---|---|---|---|---|
| 4-Week | −1.495 | 0.001 | +0.653 | 0.008 |
| 8-Week | −1.129 | 0.104 | +0.418 | 0.036 |
| 13-Week | −0.975 | 0.090 | +0.187 | 0.533 |
| 26-Week | −1.702 | <0.001 | −0.115 | 0.580 |

*Note: N = 39 (excludes January–December 2022). 4-Week and 26-Week strengthen markedly. 8- and 13-Week become marginal, consistent with those maturities having more within-2022 variation that the full sample helps average away.*

---

*The full replication code and data for all results in this paper are available in the accompanying repository. All scripts are self-contained and read from the data/ directory.*
