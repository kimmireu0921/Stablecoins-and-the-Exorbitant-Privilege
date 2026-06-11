# Bid-Cover Mechanism Validation

## What This Adds

The original main regression shows a price-side result:

```text
stablecoin supply growth -> lower OIS-Treasury spread
```

That is useful, but it does not by itself show the mechanism. A reviewer can still ask whether the spread compression is really coming from T-bill demand by stablecoin issuers.

The bid-cover analysis checks that mechanism more directly.

## Logic

The mechanism is:

```text
USDT supply growth
-> Tether increases T-bill exposure
-> secondary-market T-bill demand rises
-> T-bill prices rise and yields fall
-> OIS-Treasury spread compresses
```

At the auction level, if T-bills are already relatively expensive because of secondary-market demand, competitive bidders may have less incentive to bid aggressively in primary auctions. That can show up as lower bid-cover ratios.

So the expected issuer pattern is:

```text
USDT: should show a bid-cover pattern because it is more T-bill-heavy.
USDC: should not show the same consistent pattern.
```

## Correct Calculation

Issuer supply growth should be calculated from the daily source panel using true month-end supplies:

```text
dln_supply_USDT = log(month-end USDT supply) - log(previous month-end USDT supply)
dln_supply_USDC = log(month-end USDC supply) - log(previous month-end USDC supply)
```

Do not calculate monthly issuer growth by taking the last observation from a Friday-ending weekly panel. That uses the last Friday of the month, not necessarily the actual month-end.

## Result

Using the correct daily month-end construction:

```text
USDT: negative and statistically significant across 4 tested maturities.
USDC: statistically insignificant across 4 tested maturities.
```

This is a good result for the paper because it supports the reserve-composition story:

```text
The T-bill-heavy issuer shows the auction-side pattern.
The non-T-bill-heavy issuer does not show a consistent auction-side pattern.
```

## How To Phrase It

Use:

> USDT supply growth is consistently and significantly associated with lower bid-cover ratios across the short-term maturities we test, while USDC shows no consistent significant pattern. This provides more direct evidence consistent with a reserve-composition-driven T-bill demand channel.

Avoid:

```text
This directly identifies the causal mechanism.
```

That is too strong. Bid-cover is strong supporting evidence, not definitive causal identification.

## How To Run

From the project root:

```bash
python3 Minjin_6.1_codex/bidcover_mechanism_validation.py
```

Outputs:

```text
Minjin_6.1_codex/results/bidcover_mechanism_validation_results.csv
Minjin_6.1_codex/results/bidcover_growth_construction_check.csv
Minjin_6.1_codex/results/bidcover_mechanism_validation_summary.md
```
