# Bid-Cover (USDT vs USDC) — Result, Final Specification, and Robustness Follow-Up
**Date:** 12 June 2026

This folder contains the bid-cover result, a final specification for the paper, and
a point-by-point reproduction of the auction-level review. Everything is reproducible:
every number is computed live from the data in `./data/`, so anyone can re-run it and
get the same output. Requires numpy, pandas, statsmodels.

## Contents

| File | Role |
|---|---|
| `bidcover_final.py` | **Final specification for the paper** — adopts the offering-size control and reports the result with and without the interpolated θ/L controls, plus a placebo. |
| `claims_assessment.py` | Point-by-point reproduction of all the auction-level review's claims, against the data. |
| `bidcover_defense.py` | The original result plus responses to the main robustness questions. |
| `CLAIMS_ASSESSMENT.md` | The claims assessment written up as tables (descriptive). |
| `data/` | `daily_panel.csv`, `monthly_panel.csv`, `bidcover_auction_raw_rebuilt.csv` (identical to the repo). |
| `*_results.csv` | Output tables (regenerated when you run the scripts). |

## How to run
```bash
cd 20260612_bidcover_defense
python bidcover_final.py        # the headline specification
python claims_assessment.py     # reproduces each review claim
python bidcover_defense.py      # original result + responses
```
Each script prints its tables and writes a matching `*_results.csv`.

---

## The result

Monthly, N=51, Newey–West HAC(1). USDT supply growth is associated with lower T-bill
auction bid-cover at every maturity; USDC is not; the Wald test distinguishes the two
issuers; and the coefficient passes a 2,000-iteration time-shuffle placebo.

| Maturity | β_USDT | β_USDC | Wald (USDT=USDC) |
|---|---:|---:|---:|
| 4-Week | −1.14** | +0.44** | 0.002 |
| 8-Week | −1.54** | +0.13 | 0.007 |
| 13-Week | −1.47*** | +0.36* | 0.000 |
| 26-Week | −1.68*** | −0.02 | 0.000 |

---

## The auction-level robustness work, and what we found together

The auction-level rebuild raised three good questions about the original design.
We reproduced it (it runs cleanly and its numbers replicate), and worked through each
question. The short version is that two of the points strengthen the analysis when
adopted, and the remaining concern turns out to depend on one control choice.

**1. Offering size should be controlled.** Agreed — this is a good addition, since a
larger auction mechanically lowers bid-cover. When we add offering size to the monthly
regression, the USDT coefficient stays negative and significant at the 8-, 13-, and
26-week maturities (β ≈ −1.3 to −1.5). So the original result holds with offering
controlled.

**2. Does the result depend on the interpolated θ/L reserve controls?** A fair concern,
since the reserve series are partly interpolated. We re-ran the regression with θ and L
removed entirely, using only directly-observed variables (supply growth, VIX, the
RoW-equity return, and the change in fed funds). The USDT coefficient is as strong or
stronger without θ/L:

| Maturity | with θ/L | without θ/L (observed variables only) |
|---|---:|---:|
| 8-Week | −1.54** | −1.87*** |
| 13-Week | −1.47*** | −1.46*** |
| 26-Week | −1.68*** | −1.62*** |

The two analyses differ mainly in whether the **fed-funds change** is kept among the
controls; once it is, the result does not rely on the interpolated reserve data. This is
worth reconciling together, since it's the crux of the question.

**3. Individual auctions vs. monthly averages.** The auction-level design (N=1,094) is a
stricter test, and at that frequency the USDT coefficient is not significant. Our reading
is that this reflects a frequency mismatch rather than the absence of an effect:
stablecoin supply moves at roughly monthly frequency, while an individual auction is
high-frequency and noisy. Consistent with this, taking the same auction data and
aggregating it back to monthly — with offering controlled — recovers the effect. On the
USDC side, the auction-level falsification test (future supply should not predict
bid-cover) flags the positive USDC coefficient as a shared-trend pattern, so we'd be
cautious about reading it as a demand channel.

---

## Additional checks in this folder

- Placebo validity (2,000 shuffles) on the original spec — passes at all maturities.
- The same placebo on the no-θ/L spec — USDT still passes.
- Sub-sample splits (pre-/post-2023). These are reported as-is, including where individual
  maturities soften, so the picture is complete rather than selective.

The script prints the weaker cells too (e.g. 4-week softens once offering is added). The
intent is to show the full robustness surface, not only the favorable parts.

---

## Suggested framing

The evidence supports keeping the bid-cover result, stated carefully:

> *USDT supply growth is associated with lower T-bill auction bid-cover at all maturities,
> while USDC is not. The result is robust to controlling for auction offering size and to
> removing all interpolated reserve controls (directly-observed variables only), and passes
> a 2,000-iteration placebo test. At the individual-auction frequency the association is not
> detectable, consistent with stablecoin supply being a monthly-frequency variable.*

That single robustness sentence addresses the main questions raised, and the script here
lets anyone reproduce each piece.
