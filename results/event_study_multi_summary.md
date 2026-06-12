# Multi-Event Study — Crypto-Native Stress Episodes

**Rebuild of the event study per Prof. Hur:** SVB dropped (confounded by the banking channel); LUNA kept as the anchor; more crypto-native crises added. Dropping SVB removes the only high-buffer event, so the old low-vs-high design is replaced by a pooled test of whether crypto-native stress moves the spread.

**Selection rule:** crypto-native stress with no simultaneous banking/macro shock to Treasuries — the principled reason SVB is out and these are in.

**Method:** first-difference normal model (Δspread ~ ΔVIX + Δln equity) over (-120,-6); CAR over (0,+h) with the *estimation-window* residual σ; cross-event CAAR with events as the unit of observation. spread = DTB3 − OIS, in bps.

## Per-event CAR (bps)

| Event | Independent? | CAR[0,+5] | CAR[0,+10] | CAR[0,+20] |
|---|---|---:|---:|---:|
| LUNA / UST collapse | yes | +8.3 | +4.5 | -4.1 |
| Celsius freeze | no (LUNA chain) | +15.9* | +6.5 | +0.3 |
| FTX collapse | yes | -12.8 | -22.6 | -27.6 |
| BUSD shutdown (NYDFS) | yes | +2.2 | +0.0 | +5.2 |

## Pooled cross-event CAAR (events = unit of observation)

| Horizon | mean CAR (bps) | t | p | sign consistency |
|---|---:|---:|---:|---|
| +5d | +3.40 | +0.56 | 0.616 | 3/4 positive |
| +10d | -2.90 | -0.43 | 0.694 | 3/4 positive |
| +20d | -6.55 | -0.90 | 0.434 | 2/4 positive |

At +20 days the average crypto-native stress episode is associated with a **-6.5 bps** abnormal spread move — i.e. compression (flight to T-bills) — with p=0.434 across 4 events (2/4 share the sign).

## Honest caveats
- **Independence:** LUNA and Celsius are one 2022 deleveraging chain; their windows overlap, so the effective number of independent episodes is ~3, not 4. The independent-only pooled test is reported alongside.
- **Power:** with a handful of events the cross-event test has low power; treat this as **motivation / suggestive pattern**, not identification — which is exactly the role Prof. Hur assigned the event study.
- **Overlapping estimation windows:** Celsius's pre-event estimation window contains the LUNA shock, mildly contaminating its normal model. FTX and BUSD are clean.
