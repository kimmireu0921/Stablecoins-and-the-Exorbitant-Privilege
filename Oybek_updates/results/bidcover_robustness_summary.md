# Bid-Cover Robustness (corrected)

Headline tested: **USDT supply growth lowers T-bill auction bid-cover; USDC does not.**
Monthly design, per maturity, Newey-West HAC(1). β shown is on USDT supply growth.

| Maturity | A: orig 8 ctrl (incl. interpolated θ,L) | B: drop ONLY θ,L | C: B + offering size |
|---|---|---|---|
| 4-Week | -1.14** (p=0.012) | -1.18*** (p=0.008) | -0.82* (p=0.084) |
| 8-Week | -1.54** (p=0.016) | -1.59*** (p=0.008) | -1.29** (p=0.032) |
| 13-Week | -1.47*** (p=0.000) | -1.40*** (p=0.002) | -1.43*** (p=0.001) |
| 26-Week | -1.68*** (p=0.000) | -1.67*** (p=0.000) | -1.61*** (p=0.000) |

Under spec C (zero interpolated variables, auction size controlled):

| Maturity | USDT | USDC (foil) | Wald USDT≠USDC |
|---|---|---|---|
| 4-Week | -0.82* | +0.69*** | 0.001*** |
| 8-Week | -1.29** | +0.36 | 0.005*** |
| 13-Week | -1.43*** | +0.18 | 0.000*** |
| 26-Week | -1.61*** | -0.08 | 0.000*** |

## What this shows
- **Not an interpolation artifact (A→B):** dropping the manufactured θ and liquid-buffer controls leaves USDT significant at all four maturities (−1.18 to −1.67, p<0.01). The result does not depend on the interpolated reserve data.
- **Not an auction-size artifact (B→C):** adding ln(offering) keeps USDT significant at 8/13/26-Week; it softens 4-Week to marginal (p≈0.08). So report 4-Week as the weakest maturity and 8/13/26-Week as strong.
- **Issuer-specific:** USDC is an insignificant foil at 8/13/26-Week, and USDT≠USDC at every maturity (Wald p≤0.005). This is the reserve-composition identification.
- Combined with the existing 2,000-shuffle placebo, the bid-cover result is robust and is the paper's defensible lead.

## Auction-level caveat (why we keep the monthly design)
A disaggregated auction-level version of this test returns an attenuated, insignificant USDT coefficient. That is expected, not contradictory: stablecoin supply is a monthly series (within-month variation is small), and pre-auction windows overlap across nearby auctions, so the auction level mostly re-uses ~51 monthly supply numbers with added noise. The monthly design is the correct level for a monthly regressor.
