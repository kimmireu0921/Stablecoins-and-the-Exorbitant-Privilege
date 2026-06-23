# Stablecoins and the Exorbitant Privilege
## Liquid Reserve Buffers and the OIS–Treasury Spread

Mireu Mimi Kim (2025462112) · Sara Ambre Chekroune (2025462014) · Oybek Ibragimov (2024462029)
Jade Zhu (2026846114) · Alexandre Godefroy (2026846111) · Baptiste Degand (2026847313) · Minjin Kim (2025461111)

**Yonsei GSIS — Topics in International Finance (2026-1) · Professor Hur Sewon · June 2026**

> Replication repository for the course paper submitted June 2026.

---

## What This Paper Finds

We draw on Maggiori (2017) to model stablecoin issuers as large-scale buyers of short-term U.S. Treasuries and derive a testable liquidity-buffer threshold below which forced Treasury liquidation creates measurable sovereign spillovers (the "New Triffin Dilemma").

Using an issuer-level panel of 102 observations (USDT + USDC, January 2022 – March 2026), the continuous-L interaction is not significant (β₄ = −4.35, p = 0.68), consistent with a nonlinear rather than proportional effect. A threshold specification at L < 4% finds a significant interaction with ΔSpread:

**Table: Threshold Panel Results (primary specification)**

| Threshold | DV | β₃ (1[L<c] × ΔlnS) | p-value | N_low |
|---|---|---|---|---|
| L < 4% | **ΔSpread_t** | **−4.385** | **0.001 ***  ← main result** | 9 |
| L < 4% | Spread_t | +3.224 | 0.309 | 9 |
| L < 6% | ΔSpread_t | −0.561 | 0.639 | 23 |
| L < 6% | Spread_t | +0.561 | 0.620 | 23 |

*SE clustered by month. Controls: VIX, ΔlnN*, USDT issuer dummy. N=100 for ΔSpread (2 obs lost in differencing).*

**Caveat:** All 9 low-buffer observations are from USDT between mid-2025 and early 2026; the result cannot rule out a USDT-specific or macroeconomic-regime factor in that window. We interpret this as **suggestive evidence for a nonlinear liquidity-buffer channel**, per the professor's framing.

Liquid buffer *L* = (Cash & Bank Deposits + Money Market Funds) / total supply, per BDO ISAE 3000R attestation PDFs (Term Repos < 90d replace MMF starting Q4 2025). All values PDF-verified.

---

## Research Evolution

This repository reflects a full research cycle — from initial hypothesis through spurious-regression diagnosis to a corrected final analysis.

### Phase 1 — Original Analysis (January–June 9, 2026)

**Hypothesis:** Stablecoin supply growth compresses the OIS–Treasury spread and reserve buffers moderate this relationship.

**Specification:**
```
Spreadₜ = α + β₁·ΔlnSₜ + β₃·Lₜ + β₄·(Lₜ × ΔlnSₜ) + controls + εₜ
```

**Results at the time:** β₁ = −7.57 (p = 0.004); β₄ = −35.89 (p = 0.032); L* ≈ 13%; LSTAR c* = 14.9%.

**Scripts (Phase 1):** `regression.py`, `threshold.py`, `star.py`, `event_study.py`, `robustness.py`

**To reproduce Phase 1 exactly:** Set `INTERP_METHOD = "ffill"` in `build_panel.py` (~line 35). The current default is `"time"` (professor's correction).

---

### Phase 2 — Spurious Regression Diagnosis (June 10–12, 2026)

**Professor's corrections:**
- Exploit the issuer panel (USDT and USDC as separate rows, N: 51 → 102)
- Use DeFiLlama circulating supply for ΔlnS (not attestation totals)
- Replace forward-fill with time-weighted interpolation for quarterly attestations
- Drop collinear θ; keep L and L×ΔlnS

**What the re-run revealed:** Both the OIS–Treasury spread and L are I(1) and do not cointegrate. The original result was a textbook spurious regression.

| Test | Result |
|---|---|
| ADF — spread | p = 0.494 (unit root, I(1)) |
| ADF — liquid buffer L | p = 0.902 (unit root, I(1)) |
| Engle-Granger cointegration | p = 0.120 (no cointegration) |
| β₄ in ΔSpread spec | −107 (p = 0.46) — collapses to insignificance |

**Documentation:** `README_PROF_HUR.md`, `0609_PROF_FEEDBACK_CHANGES.md`

---

### Phase 3 — Final Analysis: Buffer/Spread Approach (June 12–21, 2026)

**Response:** Rather than abandoning the spread approach, the spuriousness is addressed by:
1. Using **ΔSpread** (first difference) as the primary DV — stationary by construction
2. Replacing the continuous-L interaction with a **threshold indicator** 1[L < c%]
3. Redefining L precisely from BDO PDF attestations (Cash + MMF, not web-extracted aggregates)
4. Using DeFiLlama circulating supply for monthly ΔlnS

**Main finding:** The 1[L < 4%] × ΔlnS interaction is significant in ΔSpread (β₃ = −4.385, p = 0.001). The result concentrates at the deepest low-buffer tail of the sample; it does not generalize to L < 6%.

**Data correction this phase:** Tether's USDT liquid buffer was redefined as Cash & Bank Deposits + Money Market Funds (verified against BDO PDFs quarter by quarter), correcting earlier entries that incorrectly used only the "Cash & Bank Deposits" BDO line item. The full correct values are in `data/reserve_attestations.csv` (cash_source = `pdf_verified (Cash + MMF)`).

**Scripts (Phase 3):**
- `build_panel.py` — builds `panel_long.csv` (102 rows, issuer-month); uses DeFiLlama supply for ΔlnS
- `analysis/regression.py` — panel regression + threshold specs (Spec D–G); cluster-robust SE by month
- `analysis/diagnostics.py` — ADF, VIF, Engle-Granger tests

**Paper:** `0621_Final_Draft_for_Submission.md` — **submit-ready**

---

## Repository Structure

```
.
├── config.py                          # central configuration
├── collect_data.py                    # fetches FRED, DeFiLlama, Yahoo Finance → data/
├── build_panel.py                     # builds daily_panel, monthly_panel, panel_long → data/
├── requirements.txt
├── README.md
├── 0621_Final_Draft_for_Submission.md  # ★ FINAL PAPER (submit-ready)
├── README_PROF_HUR.md                 # Phase 2 diagnosis memo (for professor)
├── 0609_PROF_FEEDBACK_CHANGES.md      # exact record of professor's corrections
│
├── analysis/                          # all analytical scripts
│   ├── regression.py                  # ★ panel regression + threshold specs (Phase 2/3)
│   ├── diagnostics.py                 # ADF, VIF, cointegration tests
│   ├── robustness.py                  # Engle-Granger, first-differenced spec, VAR
│   ├── threshold.py                   # Hansen (2000) threshold [Phase 1 — demoted]
│   ├── star.py                        # LSTAR smooth-transition [Phase 1 — demoted]
│   ├── event_study.py                 # buffer-conditioned event study (first-diff model)
│   └── placebo_test.py                # permutation placebo
│
├── data/
│   ├── daily_panel.csv                # daily: spread, supply_USDT, supply_USDC, VIX
│   ├── monthly_panel.csv              # monthly aggregate panel (N=51)
│   ├── panel_long.csv                 # ★ issuer-month panel (N=102: USDT+USDC × 51 months)
│   ├── reserve_attestations.csv       # ★ manual: BDO/Circle quarterly attestations (PDF-verified)
│   ├── fred_raw.csv                   # raw FRED pulls (DGS3MO, SOFR, fedfunds)
│   ├── defillama_raw.csv              # raw DeFiLlama stablecoin supply
│   └── row_equity_raw.csv             # ACWX rest-of-world equity index
│
├── sources/
│   └── attestation_pdfs/              # BDO ISAE 3000R PDFs (Tether quarterly)
│       └── README.md                  # PDF inventory, verification status, file-naming notes
│
├── results/
│   └── [regression outputs and figures]
│
└── presentations/
    ├── DONE_0421_*.pptx               # April 21 — initial pitch
    ├── DONE_0512_*.pptx               # May 12
    ├── DONE_0519_*.pptx               # May 19
    ├── DONE_0526_*.pptx               # May 26
    ├── DONE_0602_*.pptx               # June 2
    ├── 0609_FINAL_merged_*.pptx       # June 9 — last pre-feedback team deck
    └── 0616_*.pptx                    # June 16 deck (bid-cover, superseded by paper)
```

---

## How to Reproduce the Final Results

```bash
pip install -r requirements.txt

# 1. Build the data panels
python collect_data.py              # downloads raw data → data/
python build_panel.py               # builds panel_long.csv (N=102) using DeFiLlama supply

# 2. Run stationarity / cointegration checks
python analysis/diagnostics.py     # ADF, Engle-Granger → results/diagnostics.txt

# 3. Run the main regressions (Phase 3)
python analysis/regression.py      # continuous-L panel + threshold specs → results/

# 4. Event study (qualitative context)
python analysis/event_study.py     # first-diff normal model → results/event_study_*.csv
```

To reproduce Phase 1 (original — spurious):
```bash
# In build_panel.py, set INTERP_METHOD = "ffill" (~line 35), then rebuild
python analysis/threshold.py       # Hansen threshold → results/threshold_results.txt
python analysis/star.py            # LSTAR → results/star_results.txt
```

---

## Data Sources

| Variable | Definition | Source |
|---|---|---|
| OIS–Treasury spread | DGS3MO (bond-equiv.) − overnight SOFR | FRED |
| USDT / USDC supply (ΔlnS) | Daily circulating supply, log-differenced | DeFiLlama stablecoins API |
| Treasury exposure θ | T-bill holdings / total supply | BDO/Circle attestations |
| **Liquid buffer L** | **(Cash & Bank Deposits + MMF or Term Repo <90d) / supply** | **BDO ISAE 3000R PDFs (Tether); Circle monthly reports (USDC)** |
| VIX | CBOE Volatility Index | FRED |
| Federal funds rate | Effective fed funds rate | FRED |
| RoW equity (ΔlnN*) | ACWX ETF log-return | Yahoo Finance |

> `data/reserve_attestations.csv` is manually populated from public attestation PDFs.
> Tether: BDO Italia, quarterly (2024+ entries are `pdf_verified`).
> Circle: Grant Thornton / Deloitte, monthly.
>
> **L definition note:** Cash & Bank Deposits is the "Cash" BDO line item only (tens of millions),
> not the broader tether.to website "cash" aggregate. Money Market Funds ($6–7bn) are the dominant
> liquid component. Starting Q4 2025, MMF is replaced by Term Reverse Repurchase Agreements (<90d).
> See `sources/attestation_pdfs/README.md` for exact PDF-verified figures.

---

## What Was Demoted and Why

| Result | Status | Reason |
|---|---|---|
| β₁ = −7.57 in levels (Phase 1) | **Spurious** | Spread and L both I(1), no cointegration |
| Hansen threshold L* ≈ 13% | **Spurious** | Identified only in non-stationary levels regression |
| LSTAR c* = 14.9% | **Spurious** | Same identification problem |
| Bid-cover regression (Phase 3 interim) | **Superseded** | Professor's latest feedback directed revival of buffer/spread approach |
| Event study CARs | **Qualitative only** | All CARs statistically insignificant; pooled p >> 0.05 |

---

## References

Caballero, R. J., Farhi, E., & Gourinchas, P. O. (2008). An equilibrium model of global imbalances and low interest rates. *American Economic Review*, 98(1), 358–393.

Engle, R. F., & Granger, C. W. J. (1987). Co-integration and error correction. *Econometrica*, 55(2), 251–276.

Gorton, G. B., & Zhang, J. Y. (2021). Taming wildcat stablecoins. *University of Chicago Law Review*, 90(1), 45–126.

Gourinchas, P. O., & Rey, H. (2007). From world banker to world venture capitalist. In *G7 Current Account Imbalances*. University of Chicago Press.

Granger, C. W. J., & Newbold, P. (1974). Spurious regressions in econometrics. *Journal of Econometrics*, 2(2), 111–120.

Hansen, B. E. (2000). Sample splitting and threshold estimation. *Econometrica*, 68(3), 575–603.

Maggiori, M. (2017). Financial intermediation, international risk sharing, and reserve currencies. *American Economic Review*, 107(10), 3038–3071.

Phillips, P. C. B. (1986). Understanding spurious regressions in econometrics. *Journal of Econometrics*, 33(3), 311–340.

Triffin, R. (1960). *Gold and the Dollar Crisis: The Future of Convertibility*. Yale University Press.
