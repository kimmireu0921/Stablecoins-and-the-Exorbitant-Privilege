# Bid-Cover Mechanism Validation

## Purpose

The original spread regression shows a price-side relationship: stablecoin supply growth is associated with lower OIS-Treasury spreads. This check asks whether the result is also consistent with a T-bill demand channel.

The key comparison is issuer-level:

- USDT: more directly tied to T-bill reserve holdings.
- USDC: no consistent T-bill auction pattern should appear if the channel is reserve-composition driven.

## Construction

Issuer growth is calculated from the daily source panel using true month-end supplies:

```text
dln_supply_issuer = log(month-end issuer supply) - log(previous month-end issuer supply)
```

This avoids using the weekly panel's last Friday observation as a substitute for the actual month-end value.

## Results

| Maturity | N | beta_USDT | p_USDT | beta_USDC | p_USDC | Wald p | DW |
|---|---:|---:|---:|---:|---:|---:|---:|
| 4-Week | 51 | -1.225 | 0.010 | 0.452 | 0.060 | 0.001 | 1.396 |
| 8-Week | 51 | -1.553 | 0.007 | 0.145 | 0.516 | 0.003 | 1.294 |
| 13-Week | 51 | -1.366 | 0.003 | 0.338 | 0.131 | 0.000 | 1.481 |
| 26-Week | 51 | -1.587 | 0.000 | -0.016 | 0.937 | 0.001 | 1.784 |

## Interpretation

- USDT is negative and significant across all four tested maturities: yes.
- USDC is insignificant across all four tested maturities: yes.
- This is good supporting evidence for the paper because it moves closer to the claimed mechanism: the spread result is consistent with T-bill demand coming from the T-bill-heavy issuer.
- This should be described as mechanism-consistent evidence, not definitive causal identification.

Suggested wording:

> USDT supply growth is consistently and significantly associated with lower bid-cover ratios across the short-term maturities we test, while USDC shows no consistent significant pattern. This provides more direct evidence consistent with a reserve-composition-driven T-bill demand channel.

## Growth-Construction Check

Weekly panel was not found, so no weekly-derived comparison was run.
