# Stablecoins and the Exorbitant Privilege: Safe-Asset Demand and Its Systemic Fragility

**Mireu Kim · Sara Ambre Chekroune · Oybek Ibragimov**  
Yonsei GSIS — Topics in International Finance, Spring 2026

---

## Abstract

Large-scale USD-pegged stablecoins have emerged as significant buyers of U.S. Treasury bills, creating a new structural channel for safe-asset demand that amplifies America's exorbitant privilege. We extend Maggiori (2017) to incorporate stablecoin supply *S* and a reserve buffer *B*, showing that the relationship is asymmetric: when reserves are adequate (|ΔS| < B), stablecoin growth compresses OIS–Treasury spreads; when reserves fall below a critical threshold, forced liquidation reverses the benefit and activates a Cole–Kehoe (2000) crisis zone.

Using monthly data from January 2020 to March 2026 (N = 75), we find β₁ = −5.95*** (privilege amplification) and β₃ = −11.30*** (buffer-conditioned fragility). A Hansen (2000) threshold regression identifies q* = −0.524 (bootstrap p < 0.001), implying Treasury holdings must exceed 47.6% of outstanding supply to remain outside the crisis zone. A buffer-conditioned event study across three stress episodes confirms a 27 pp CAR swing between low- and high-buffer regimes (Welch t = 15.22***).

---

## Repository Structure

| File | Purpose |
|---|---|
| `config.py` | Central configuration (dates, FRED series, file paths) |
| `collect_data.py` | Fetch FRED, DeFiLlama stablecoins API, Yahoo Finance (ACWX) |
| `build_panel.py` | Merge raw sources into daily and monthly panels |
| `regression.py` | OLS with Newey–West HAC standard errors |
| `threshold.py` | Hansen (2000) threshold regression with bootstrap p-values |
| `event_study.py` | Buffer-conditioned event study (CAR, Welch test) |
| `diagnostics.py` | ADF unit root tests, VIF, Figure 1, summary statistics |
| `robustness.py` | Mean-centering, Engle–Granger cointegration, first-differenced spec |
| `write_paper.py` | Generate full research paper as `.docx` |
| `make_slides.py` | Generate presentation as `.pptx` |

---

## Data Sources

| Variable | Definition | Source |
|---|---|---|
| OIS–Treasury spread | DTB3 − SOFR90DAYAVG | FRED (public CSV, no API key required) |
| Stablecoin supply *S* | USDT + USDC market cap | DeFiLlama stablecoins API (free) |
| Reserve buffer *B* | T-bill holdings − supply / supply | Tether/BDO + Circle/Deloitte attestations (manual) |
| Velocity *V* | 7-day rolling SD of daily supply changes | Computed from DeFiLlama |
| VIX | CBOE VIX index | FRED |
| ΔlnN* (RoW equity) | ACWX ETF log-return | Yahoo Finance |

> **Note:** `data/reserve_attestations.csv` is manually populated from Tether (BDO Cayman, quarterly) and Circle (Grant Thornton / Deloitte, monthly) public attestation reports. Pre-attestation months (Jan 2020 – Feb 2021) are estimated at 2% of supply.

---

## How to Reproduce

```bash
pip install -r requirements.txt

python collect_data.py      # downloads raw data to data/
python build_panel.py       # builds daily_panel.csv and monthly_panel.csv
python regression.py        # main OLS results
python threshold.py         # Hansen threshold + bootstrap
python event_study.py       # event study CARs
python diagnostics.py       # unit roots, VIF, Figure 1
python robustness.py        # robustness checks
python write_paper.py       # generates Stablecoins_Exorbitant_Privilege.docx
python make_slides.py       # generates Stablecoins_Presentation.pptx
```

---

## Key Results

- **β₁ = −5.95\*\*\*** — a one-SD supply growth (9.9 pp) compresses the OIS–Treasury spread by ~59 bp, confirming privilege amplification.
- **q\* = −0.524** (bootstrap p < 0.001) — the reserve buffer threshold separating the privilege-amplification regime from the crisis zone; Treasury holdings must exceed 47.6% of supply.
- **27 pp CAR swing** — low-buffer runs yield CAR = +8.9 pp; high-buffer stress yields CAR = −18.0 pp (Welch t = 15.22***).

---

## Output Files

| File | Description |
|---|---|
| `Stablecoins_Exorbitant_Privilege.docx` | Draft for research paper |
| `Stablecoins_Presentation.pptx` | May 12, Class presentation |
| `results/fig_timeseries.png` | Figure 1 — key time series |
| `results/threshold_ssr.png` | Figure 2 — Hansen LR profile |
| `results/event_study_cars.png` | Figure 3 — CAR paths |
| `results/diagnostics.txt` | ADF, VIF, NW lag sensitivity |
| `results/robustness.txt` | Mean-centering, cointegration, first-diff |

---

## Theoretical Background

- **Maggiori (2017)** — safe-asset demand and the exorbitant privilege  
- **Cole & Kehoe (2000)** — self-fulfilling crisis zones and reserve adequacy  
- **Hansen (2000)** — threshold regression with bootstrap inference  
- **Triffin (1960)** — the original dilemma between reserve currency supply and confidence
