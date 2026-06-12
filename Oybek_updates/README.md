# Oybek_updates/ — my contribution to the paper

This folder contains **only my actual new work** — no copies of anyone else's files.
Everything outside this folder is Mimi's last version, unchanged.

Two pieces, both supporting the paper's lead result
(**USDT supply growth lowers T-bill auction bid-cover; USDC does not**):

```
Oybek_updates/
├── bidcover_robustness.py      → robustness section for the bid-cover headline
├── event_study_multi.py        → multi-event study (motivation)
└── results/
    ├── bidcover_robustness.csv / _summary.md
    └── event_study_multi_{table.csv, caar.csv, summary.md, .png}
```

Run either from this folder (`python3 Oybek_updates/bidcover_robustness.py`); they read
data from the main project and write outputs into `Oybek_updates/results/`.

## 1. `bidcover_robustness.py` — the robustness section
Answers the two questions an examiner will ask about the bid-cover result:
- **Is it just the interpolated reserve controls (θ, L)?** No — drop θ/L and USDT stays
  significant at all four maturities (−1.18 to −1.67, p<0.01).
- **Is it just auction size?** No — add `ln(offering)` and USDT survives at 8/13/26-Week;
  it only softens 4-Week to marginal (p≈0.08). So **4-Week is the weak maturity; 8/13/26-Week
  are strong.** USDC stays an insignificant foil; USDT≠USDC at every maturity (Wald p≤0.005).

Net: the headline is **not** an artifact of the manufactured reserve data or of auction size.
Combined with the existing placebo test, it's the paper's defensible lead result.

## 2. `event_study_multi.py` — motivation
Per Prof. Hur: dropped SVB (banking-confounded), kept LUNA, added crypto-native crises
(Celsius, FTX, BUSD). Honest finding: per-event CARs are mostly insignificant and the events
disagree in sign (pooled p=0.43) — so this is **motivation/context only**, exactly the role
the prof assigned the event study.

## Note on my earlier auction-level analysis
An earlier version of this work disaggregated bid-cover to the auction level and concluded
the USDT effect was null. That conclusion was **wrong** — the auction level is the wrong unit
for a monthly supply variable (overlapping windows, tiny within-month variation), which
attenuates the estimate. Mimi caught this; the corrected `bidcover_robustness.py` above is the
honest version. The earlier auction-level files and the teardown deck were removed (they remain
in git history at commit `41895ef` if anyone needs them).
