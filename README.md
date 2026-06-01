# Stablecoins and the Exorbitant Privilege: Safe-Asset Demand and Its Systemic Fragility

**Mireu Kim · Sara Ambre Chekroune · Oybek Ibragimov**  
Yonsei GSIS — Topics in International Finance, Spring 2026

> **Replication repository** for the course paper submitted June 2026.  
> All code, data, and output are publicly available at this repository.

---

## Abstract

Large-scale USD-pegged stablecoins have emerged as significant buyers of U.S. Treasury bills, creating a new structural channel for safe-asset demand that amplifies America's exorbitant privilege. We extend Maggiori (2017) to incorporate stablecoin supply *S*, Treasury exposure *θ* (T-bill holdings / supply), and liquid buffer *L* (cash reserves / supply), showing that the relationship is two-sided: in normal times, stablecoin issuance compresses OIS–Treasury spreads; when the liquid buffer falls below a critical threshold, forced liquidation reverses the benefit and activates a Cole–Kehoe (2000) crisis zone — a *New Triffin Dilemma*.

Using 51 monthly observations (January 2022 – March 2026), we find **β₁ = −6.02** (p = 0.006), confirming privilege amplification. A Hansen (2000) threshold regression identifies **q\* = 13.0%** as the liquid buffer tipping point (bootstrap 90% CI: [2.6%, 14.5%]). Convergent validity is confirmed by a logistic smooth-transition regression (LSTAR) with transition midpoint **c\* = 13.1%** and near-discrete sharpness (γ\* = 2,768). A buffer-conditioned event study, corrected for Fed hiking cycle contamination, yields insignificant CARs (−15 to −2 bps) and serves as qualitative directional context only.

---

## Key Results

| Finding | Method | Estimate | Significance |
|---|---|---|---|
| Privilege amplification | OLS, Newey–West (1 lag) | β₁ = −6.02 bps/σ | p = 0.006 ✓ |
| Reserve threshold | Hansen (2000) grid search | q\* = 13.0% | p = 0.260 (suggestive) |
| Threshold stability | TRIM 15 / 20 / 25% | q\* = 0.1301 at all values | Robust ✓ |
| Smooth-transition check | LSTAR (nonlinear LS) | c\* = 13.1%, γ\* = 2,768 | Convergent ✓ |
| Event study | First-diff normal model | CARs −15 to −2 bps | All n.s. — qualitative only |

---

## Repository Structure

### Core pipeline

| Script | Purpose |
|---|---|
| `config.py` | Central configuration (dates, FRED series IDs, file paths) |
| `collect_data.py` | Fetch FRED, DeFiLlama stablecoins API, Yahoo Finance (ACWX) |
| `build_panel.py` | Merge raw sources into daily and monthly panels |
| `regression.py` | OLS with Newey–West HAC standard errors (1 lag) |
| `threshold.py` | Hansen (2000) threshold regression — grid search, bootstrap CI, TRIM sensitivity, two-threshold test |
| `star.py` | LSTAR smooth-transition regression — NLS estimation, bootstrap CI for c\* |
| `event_study.py` | Buffer-conditioned event study — first-difference normal model, CARs |
| `placebo_test.py` | Placebo test — pseudo-events from quiet periods, null distribution |
| `diagnostics.py` | ADF unit root tests, VIF, summary statistics |
| `robustness.py` | Engle–Granger cointegration, first-differenced spec, post-2023 sub-sample |

### Output and presentation

| Script | Purpose |
|---|---|
| `write_paper.py` | Generates `presentations/Stablecoins_Exorbitant_Privilege.docx` |
| `make_slides_0602.py` | Generates the June 2026 presentation deck |
| `add_notes.py` | Adds presenter notes to slide decks |

---

## Data Sources

| Variable | Definition | Source |
|---|---|---|
| OIS–Treasury spread | DTB3 − SOFR90DAYAVG (3-month) | FRED (no API key required) |
| Stablecoin supply *S* | USDT + USDC market cap | DeFiLlama stablecoins API (free) |
| Treasury exposure *θ* | T-bill holdings / supply | Tether/BDO + Circle/Deloitte attestations (manual) |
| Liquid buffer *L* | Cash reserves / supply | Tether/BDO + Circle/Deloitte attestations (manual) |
| Velocity *V* | 7-day rolling SD of daily Δ supply | Computed from DeFiLlama |
| VIX | CBOE VIX index | FRED |
| ΔlnN\* (RoW equity) | ACWX ETF log-return | Yahoo Finance |

> `data/reserve_attestations.csv` is manually populated from Tether (BDO Cayman, quarterly) and Circle (Grant Thornton / Deloitte, monthly) public attestation reports. Sample starts January 2022 when both issuers have formal attestation coverage.

---

## How to Reproduce

```bash
pip install -r requirements.txt

python collect_data.py      # downloads raw data → data/
python build_panel.py       # builds daily_panel.csv and monthly_panel.csv

python regression.py        # main OLS results → results/regression_main.txt
python threshold.py         # Hansen threshold + bootstrap + TRIM → results/threshold_results.txt
python star.py              # LSTAR smooth-transition → results/star_results.txt
python event_study.py       # event study CARs → results/event_study_table.csv
python placebo_test.py      # placebo test → results/placebo_table.csv
python diagnostics.py       # unit roots, VIF, summary stats
python robustness.py        # robustness checks → results/robustness.txt

python write_paper.py       # generates presentations/Stablecoins_Exorbitant_Privilege.docx
python make_slides_0602.py  # generates presentations/0602_Stablecoin_Exorbitant_Privilege.pptx
```

---

## Output Files

| File | Description |
|---|---|
| `presentations/Stablecoins_Exorbitant_Privilege.docx` | Final research paper |
| `presentations/0602_Stablecoin_Exorbitant_Privilege.pptx` | June 2026 presentation |
| `results/fig_timeseries.png` | Figure 1 — key time-series (spread, supply, buffer) |
| `results/threshold_ssr.png` | Figure 2 — Hansen SSR profile |
| `results/threshold_trim_sensitivity.png` | Figure 3 — TRIM sensitivity |
| `results/star_transition.png` | Figure 4 — LSTAR transition fit |
| `results/car_comparison.png` | Figure 5 — level vs. first-diff CAR comparison |
| `results/event_study_cars.png` | Figure 6 — corrected event study CARs |
| `results/placebo_cars.png` | Figure 7 — placebo test |
| `results/regression_main.txt` | OLS regression output |
| `results/threshold_results.txt` | Threshold regression + robustness |
| `results/star_results.txt` | LSTAR estimation output |
| `results/diagnostics.txt` | ADF tests, VIF, summary statistics |

---

## References

- Maggiori, M. (2017). Financial intermediation, international risk sharing, and reserve currencies. *AER*, 107(10).
- Cole, H.L. & Kehoe, T.J. (2000). Self-fulfilling debt crises. *Review of Economic Studies*, 67(1).
- Hansen, B.E. (2000). Sample splitting and threshold estimation. *Econometrica*, 68(3).
- Gourinchas, P.-O. & Rey, H. (2007). International financial adjustment. *JPE*, 115(4).
- Jeanne, O. & Rancière, R. (2011). The optimal level of international reserves. *Economic Journal*, 121(555).
- Obstfeld, M., Shambaugh, J.C. & Taylor, A.M. (2010). Financial stability, the trilemma, and international reserves. *AEJ: Macro*, 2(2).
- Gorton, G.B. & Zhang, J. (2021). Taming wildcat stablecoins. *U. Chicago Law Review*, 90(3).
- MacKinlay, A.C. (1997). Event studies in economics and finance. *Journal of Economic Literature*, 35(1).
- Duffie, D. (2022). Digital currencies and fast payment systems. Working Paper, Stanford University.
- Triffin, R. (1960). *Gold and the Dollar Crisis*. Yale University Press.
