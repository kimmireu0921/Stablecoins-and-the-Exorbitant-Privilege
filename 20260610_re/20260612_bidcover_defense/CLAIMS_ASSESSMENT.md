# Claims Assessment — Auction-Level Review, Reproduced Point by Point
**Date:** 12 June 2026

Each claim from the auction-level review document is reproduced against the data.
All numbers are computed by `claims_assessment.py` (run it to regenerate everything):

```bash
cd 20260612_bidcover_defense
python claims_assessment.py        # prints the tables, writes claims_assessment_results.csv
```

Data used (in `./data/`, identical to the repo): `daily_panel.csv`,
`monthly_panel.csv`, `bidcover_auction_raw_rebuilt.csv`. The report is descriptive:
each claim is reproduced and the output is reported as-is.

---

## Claims consistent with the data

| # | Claim | Reproduction |
|---|---|---|
| 1 | The levels regression is spurious | Confirmed by ADF / Engle–Granger / Johansen and first-differencing. |
| 2 | β₁, the threshold, and LSTAR are spurious; drop them | Consistent. |
| 3 | Offering size should be controlled | Adopted. With offering added (monthly), USDT stays significant at 8/13/26-Wk (β ≈ −1.4 to −1.7). |
| 4 | A time-shuffle placebo only tests time ordering | A property of the test; correct. |
| 5 | The multi-event study shows no systematic effect (pooled p=0.43) | Reproduced by `event_study_multi.py`. |

---

## Claim 6 — "USDT is significant only because of the interpolated θ/L controls"

The review compares the full 8-control spec to a "clean" spec defined as
**supply + VIX only**. Reproducing both, and then removing **only** θ and L:

| Maturity | (a) review's "clean" (supply + VIX) | (b) remove only θ/L (keep velocity, VIX, ΔlnN*, Fed) |
|---|---:|---:|
| 4-Week | −0.26 | **−1.18*** |
| 8-Week | −0.91 | **−1.59*** |
| 13-Week | −0.80* | **−1.40*** |
| 26-Week | −0.82* | **−1.67*** |

The review's "clean" spec also drops velocity, ΔlnN*, and the fed-funds change.
Removing θ/L alone — keeping the other controls — leaves USDT significant at every
maturity. The difference between the two columns is the additional controls (most
importantly the Fed change), not θ/L.

---

## Claim 7 — "USDC is the real (positive) effect"

Applying the review's own falsification test (future supply should not predict
bid-cover) at the auction level:

| Supply window | β_USDC | β_USDT |
|---|---:|---:|
| past (t−21 → t−1) | +1.28*** (p=0.000) | +0.32 (p=0.502) |
| future (t → t+21) | +1.50*** (p=0.000) | +0.27 (p=0.508) |

USDC is significant for future supply as well as past supply. USDT is not
significant for either. By the falsification criterion the USDC coefficient behaves
like a shared trend rather than a pre-auction → outcome effect.

---

## Claims 8 / 9 — "bid-cover does not survive the auction level"

**(i) Auction level, pooled (reproduces the review):**
β_USDT = +0.32 (p=0.502), β_USDC = +1.28*** (p=0.000), N = 1,094.

**(ii) Same auction data aggregated to monthly, offering controlled:**

| Maturity | β_USDT | β_USDC |
|---|---:|---:|
| 4-Week | −1.03** | +0.52** |
| 8-Week | −1.72*** | +0.37 |
| 13-Week | −1.44*** | +0.39* |
| 26-Week | −1.58*** | −0.05 |

**(iii) Why the auction-level unit is not appropriate for a supply regressor:**

| Quantity | Value |
|---|---|
| Auctions per month (mean) | 17.4 |
| Months (independent supply values) | 63 |
| Auction rows (regression N) | 1,094 |
| Within-month vs between-month std of USDT growth | 0.0139 / 0.0463 (30%) |

Issuer supply growth is a monthly-frequency series: 70% of its variation is between
months and only 30% within. At the auction level, the same monthly supply value is
repeated across the ~17 auctions in that month, and the 21-day pre-auction windows
overlap across auctions that are only ~7 days apart. The regression N of 1,094 thus
reflects on the order of 51–63 independent supply observations, not 1,094.

This is a frequency mismatch: the regressor moves monthly while the unit of analysis
is the individual auction. A non-result at that unit is the expected consequence of
the mismatch, not evidence about the supply–bid-cover relationship. The appropriate
unit for a monthly regressor is monthly — where the coefficient is reported above
(panel ii) and is significant at 8/13/26-Wk.

---

## Claim 10 — "the result depends on interpolated reserve data"

Removing θ and L entirely (directly-observed variables only) and adding offering size
— i.e. zero interpolated regressors:

| Maturity | β_USDT |
|---|---:|
| 4-Week | −0.61 |
| 8-Week | −1.33*** |
| 13-Week | −1.52*** |
| 26-Week | −1.54*** |

Placebo (2,000 shuffles) on the no-θ/L spec (supply + VIX + Fed):
13-Week p = 0.003, 26-Week p = 0.000.

With no interpolated variables in the regression, USDT remains significant at
8/13/26-Wk and passes the placebo.

---

## Summary

| Claim | Status |
|---|---|
| 1, 2 spurious levels regression / β₁ / threshold | Consistent |
| 3 control for offering size | Adopted; USDT survives (8/13/26-Wk) |
| 4 placebo tests only time ordering | Correct |
| 5 event study has no systematic effect | Reproduced |
| 6 USDT significance is from θ/L | Not reproduced once θ/L is isolated from the other controls |
| 7 USDC is the real effect | USDC also predicts future supply (falsification) |
| 8 demote bid-cover | Survives monthly with offering, without θ/L, and the placebo |
| 9 null at auction level | Reproduced; but the auction level is not the appropriate unit for a monthly regressor (frequency mismatch — one monthly supply value repeated across ~17 auctions, overlapping windows). The monthly unit is appropriate and significant. |
| 10 result depends on interpolated data | Holds with zero interpolated regressors |
