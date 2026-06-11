# Auction-Level Bid-Cover Robustness

**Contribution.** Moves the bid-cover test from monthly-averaged (N≈51, no auction-size control) to the individual auction (N≈1,094) with the offering size, maturity fixed effects, VIX, and a linear time trend as controls. Standard errors clustered by month.

Pre-auction supply growth = log issuer supply growth over the 21 calendar days ending the day **before** each auction (strictly pre-auction).

## Estimating equation
```
bid_cover_{t,m} = α + β_USDT·Δln S^USDT_pre + β_USDC·Δln S^USDC_pre
                    + γ·ln(offering_{t,m}) + maturity FE + δ·VIX_t + θ·trend + ε
```

## Results

| Spec | N | β_USDT | p | β_USDC | p | Wald p (USDT=USDC) |
|---|---:|---:|---:|---:|---:|---:|
| (1) supply only | 1094 | +0.307 | 0.498 | +1.423*** | 0.000 | 0.088 |
| (2) + ln(offering) | 1094 | +0.113 | 0.832 | +1.085*** | 0.000 | 0.181 |
| (3) + maturity FE | 1094 | +0.114 | 0.830 | +1.088*** | 0.000 | 0.179 |
| (4) + VIX | 1094 | -0.054 | 0.901 | +1.095*** | 0.000 | 0.069 |
| (5) + linear time trend | 1094 | +0.322 | 0.499 | +1.279*** | 0.000 | 0.123 |
| per-maturity 4-Week | 273 | +0.762 | 0.224 | +1.491*** | 0.000 | 0.318 |
| per-maturity 8-Week | 273 | +0.357 | 0.562 | +1.440*** | 0.000 | 0.190 |
| per-maturity 13-Week | 274 | -0.729 | 0.181 | +0.754*** | 0.008 | 0.043 |
| per-maturity 26-Week | 274 | -0.633 | 0.198 | +0.275 | 0.330 | 0.150 |
| window=10d | 1094 | +1.394* | 0.061 | +1.851*** | 0.000 | 0.607 |
| window=21d | 1094 | +0.322 | 0.499 | +1.279*** | 0.000 | 0.123 |
| window=42d | 1094 | +0.099 | 0.762 | +0.884*** | 0.000 | 0.087 |
| FALSIFICATION future-supply | 1082 | +0.274 | 0.499 | +1.502*** | 0.000 | 0.025 |
| subsample: drop 2022 crisis year | 886 | -1.060** | 0.024 | +1.346*** | 0.000 | 0.000 |
| subsample: post-2023 only | 678 | -0.742 | 0.114 | +0.395** | 0.031 | 0.016 |

## Verdict

**The USDT bid-cover channel does NOT survive the auction-level rebuild.** In the fully-controlled pooled spec (5), β_USDT = +0.322 (p=0.499, not significant, and the sign is positive — opposite the hypothesis). It is null from spec (1) onward, so this is not an artifact of over-controlling.

β_USDC is the coefficient that is consistently significant (β=+1.279, p=0.000) — but **positive**, the opposite of a T-bill demand story, and the falsification test shows that *future* USDC growth also 'predicts' bid-cover (p=0.000, significant). A relationship that runs both forward and backward in time is a shared trend, not a causal channel.

The only place the predicted negative USDT sign appears significantly is the *drop-2022* subsample — an isolated, fragile result, not robust evidence.

## Why the original monthly result looked clean: it was the interpolated controls

Re-running the **monthly** design (N=51) two ways isolates the driver:

| Maturity | Original spec (8 controls incl. interpolated θ, L) | Clean controls (supply + VIX) |
|---|---|---|
| 4-Week | β_USDT=-1.14** (p=0.012) | β_USDT=-0.26 (p=0.628) |
| 8-Week | β_USDT=-1.54** (p=0.016) | β_USDT=-0.91 (p=0.110) |
| 13-Week | β_USDT=-1.47*** (p=0.000) | β_USDT=-0.80* (p=0.094) |
| 26-Week | β_USDT=-1.68*** (p=0.000) | β_USDT=-0.82* (p=0.065) |

Stripping the interpolated θ and liquid-buffer controls — the same manufactured quarterly reserve data flagged in the teardown — collapses the USDT coefficient from strongly significant (p<0.01) to marginal-or-null at every maturity. The 2,000-shuffle placebo test validated the *time ordering* of the coefficient, but the coefficient itself only exists *conditional on the interpolated regressors*. The placebo never tested that.

## Bottom line

The bid-cover result — previously billed as the paper's cleanest, placebo-validated causal evidence — does **not** hold up. It depended on (i) collapsing ~1,094 auctions to 51 monthly means, (ii) omitting auction offering size, and (iii) conditioning on interpolated reserve controls. At the auction level with offering controlled, the USDT channel is absent. This needs to be reported honestly, not led with.
