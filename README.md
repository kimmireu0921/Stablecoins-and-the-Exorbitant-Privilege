# Stablecoins and the Exorbitant Privilege
## A Reserve-Composition Channel in the T-Bill Market

Mireu Mimi Kim (2025462112) · Sara Ambre Chekroune (2025462014) · Oybek Ibragimov (2024462029)
Jade Zhu (2026846114) · Alexandre Godefroy (2026846111) · Baptiste Degand (2026847313) · Minjin Kim (2025461111)

**Yonsei GSIS — Topics in International Finance (2026-1) · Professor Hur Sewon · June 2026**

> Replication repository for the course paper submitted June 2026.

---

## What This Paper Finds

USDT supply growth is associated with statistically significant reductions in T-bill auction bid-cover ratios across all four maturities (4-, 8-, 13-, 26-week), while USDC supply growth is not. The difference between issuers is significant at every maturity (Wald p ≤ 0.026), consistent with USDT's higher Treasury-bill reserve backing (~64%) versus USDC (~48%).

| Maturity | β_USDT | p-value | β_USDC | Wald p (USDT ≠ USDC) |
|---|---|---|---|---|
| 4-Week  | −0.61 | 0.184 | +0.61*** | 0.026 |
| 8-Week  | −1.33*** | 0.003 | +0.47** | <0.001 |
| 13-Week | −1.51*** | 0.001 | +0.32* | <0.001 |
| 26-Week | −1.53*** | 0.001 | −0.09 | 0.001 |

*Monthly OLS, Newey–West HAC(1). Spec: supply growth + VIX + Δfed-funds + ln(offering size). N = 51.*

The original spread-regression result (β₁ = −7.57, p = 0.004) was found to be **spurious**: both the OIS–Treasury spread and the reserve-buffer variable are I(1) and do not cointegrate (Engle-Granger p = 0.120; Johansen fails to reject r = 0). See §Research Evolution below.

---

## Research Evolution

This repository reflects a full research cycle — from initial hypothesis through diagnosis to a corrected final analysis. The professor's mid-semester feedback was the turning point.

### Phase 1 — Original Analysis (January–June 9, 2026)

**Hypothesis:** Stablecoin supply growth compresses the OIS–Treasury spread (convenience yield) and amplifies the exorbitant privilege.

**Specification:**
```
Spreadₜ = α + β₁·ΔlnSₜ + β₃·Lₜ + β₄·(Lₜ × ΔlnSₜ) + controls + εₜ
```

**Results at the time:** β₁ = −7.57 (p = 0.004), β₄ = −35.89 (p = 0.032); reserve threshold at L* ≈ 13%; LSTAR transition midpoint c* = 14.9%.

**Scripts (Phase 1):** `regression.py` (original version), `threshold.py`, `star.py`, `event_study.py`, `robustness.py`

**Presentations:** `presentations/DONE_0421_*.pptx` → `DONE_0512_*.pptx` → `DONE_0519_*.pptx` → `DONE_0526_*.pptx` → `DONE_0602_*.pptx`

---

### Phase 2 — Professor's Feedback and Spurious Regression Diagnosis (June 10–12, 2026)

**Professor Hur's corrections:**
- Exploit the issuer panel (USDT and USDC as separate rows, N: 51 → 102)
- Replace forward-fill with time-weighted interpolation for quarterly attestations
- Drop collinear θ; keep L and L×ΔlnS
- Show the estimating equation on every result slide

**What the re-run revealed:** After applying the corrected panel structure, β₁ became insignificant and β₄ flipped sign under first-differencing (+8.86, p = 0.31 vs. −35.89 in levels). Formal tests confirmed the cause:

| Test | Result |
|---|---|
| ADF — spread | p = 0.494 (unit root, I(1)) |
| ADF — liquid buffer L | p = 0.902 (unit root, I(1)) |
| Engle-Granger cointegration | p = 0.120 (no cointegration) |
| Johansen cointegration | Fails to reject r = 0 |
| β₄ in first-differences | +8.86 (sign flip — spurious signature) |

Both the spread and L trended down together during the 2022–24 Fed hiking cycle. The original result was a textbook spurious regression, not a genuine channel.

**Scripts (Phase 2):** `build_panel.py` (updated: interpolation + `panel_long.csv`), `regression.py` (updated: panel regression), `diagnostics.py` (updated: formal ADF/cointegration), `bidcover_mechanism_validation.py`, `bidcover_defense.py`, `bidcover_final.py`, `claims_assessment.py`

**Documentation:** `PROF_FEEDBACK_CHANGES.md` — exact record of what changed and why

**Presentation:** `presentations/0609_FINAL_merged_Stablecoin_Privilege.pptx` (June 9 team deck)

---

### Phase 3 — Final Analysis: Bid-Cover Approach (June 12–16, 2026)

**Response:** Changed the dependent variable from the (non-stationary) OIS–Treasury spread to the T-bill auction bid-cover ratio — a stationary, flow-based, directly observable measure of demand at auction.

**Final specification (per maturity m):**
```
BC_{m,t} = α + β_USDT·ΔlnS^USDT_t + β_USDC·ΔlnS^USDC_t
           + δ·ln(Offering_{m,t}) + γ₁·VIX_t + γ₂·Δfedfunds_t + εₜ
```

**Robustness checks performed:**
- Spec A/B/C ladder: dropping interpolated θ/L does not kill the result; adding offering-size control does not kill it
- 2,000-shuffle permutation placebo: 3 of 4 maturities pass (p < 0.05)
- Drop-2022 subsample: 4-Week and 26-Week strengthen markedly (β ≈ −1.5 to −1.7)
- Daily VAR(3): USDT Granger-causes spread (p = 0.020), explaining ~1.3% of spread variance

**Scripts (Phase 3):** `bidcover_robustness.py` (spec ladder A/B/C), `event_study_multi.py` (multi-event rebuild dropping SVB), `placebo_test.py`, `make_final_deck.py`

**Presentation:** `presentations/0616_Stablecoin_Exorbitant_Privilege.pptx` — **final deck**

**Paper:** `PAPER_DRAFT.md` — full paper draft (submit-ready; fill in professor's name on acknowledgements line)

---

## Repository Structure

```
.
├── config.py          # central configuration (paths, FRED series IDs, event dates)
├── collect_data.py    # fetches FRED, DeFiLlama, Yahoo Finance → data/
├── build_panel.py     # builds daily_panel, monthly_panel, panel_long → data/
├── requirements.txt
├── README.md
├── PAPER_DRAFT.md                 # ★ final paper (7 sections + appendix)
├── PROF_FEEDBACK_CHANGES.md       # exact record of professor's corrections
│
├── analysis/                      # all analytical scripts
│   │
│   │  ── Phase 1: Original Analysis (pre-feedback) ──
│   ├── regression.py              # OLS spread regression + panel (Newey-West HAC)
│   ├── diagnostics.py             # ADF, VIF, cointegration tests, summary stats
│   ├── robustness.py              # Engle-Granger, first-differenced spec
│   ├── threshold.py               # Hansen (2000) threshold regression [demoted]
│   ├── star.py                    # LSTAR smooth-transition regression [demoted]
│   ├── event_study.py             # original buffer-conditioned event study [demoted]
│   ├── placebo_test.py            # permutation placebo test
│   │
│   │  ── Phase 2: Feedback & Diagnosis (June 10–12) ──
│   ├── bidcover_mechanism_validation.py  # bid-cover channel validation
│   ├── bidcover_defense.py               # auction-level robustness follow-up
│   ├── claims_assessment.py             # point-by-point claim verification
│   │
│   │  ── Phase 3: Final Analysis ──
│   ├── bidcover_robustness.py     # ★ main spec ladder A/B/C (final result)
│   ├── bidcover_final.py          # ★ final spec + placebo
│   └── event_study_multi.py       # ★ multi-event rebuild (LUNA/Celsius/FTX/BUSD)
│
├── data/
│   ├── daily_panel.csv            # daily: spread, supply_USDT, supply_USDC, VIX, fedfunds
│   ├── monthly_panel.csv          # monthly aggregate panel (N=51, Jan 2022–Mar 2026)
│   ├── panel_long.csv             # issuer-month panel (N=102: USDT+USDC × 51 months)
│   ├── reserve_attestations.csv   # manual: Tether/Circle quarterly/monthly attestations
│   ├── fred_raw.csv               # raw FRED pulls (DGS3MO, SOFR, fedfunds)
│   ├── defillama_raw.csv          # raw DeFiLlama stablecoin supply
│   └── row_equity_raw.csv         # ACWX rest-of-world equity index
│
├── results/
│   ├── CLEAN_RESULTS_SUMMARY.md         # full 6-step analysis results
│   ├── CLAIMS_ASSESSMENT.md             # point-by-point claim verification
│   ├── bidcover_robustness.csv/.md      # spec ladder A/B/C output
│   ├── event_study_multi_*.csv/.png     # multi-event study output
│   ├── bidcover_auction_raw_rebuilt.csv # 1,094 individual auction observations
│   ├── irf_usdt_usdc.png               # VAR impulse response figure
│   └── [regression outputs and figures]
│
└── presentations/                 # ← semester progression visible here
    ├── DONE_0421_*.pptx           # April 21 — initial pitch
    ├── DONE_0512_*.pptx           # May 12
    ├── DONE_0519_*.pptx           # May 19
    ├── DONE_0526_*.pptx           # May 26
    ├── DONE_0602_*.pptx           # June 2
    ├── 0609_FINAL_merged_*.pptx   # June 9 — last pre-feedback team deck
    ├── 0616_*.pptx                # June 16 — FINAL DECK ★
    ├── Stablecoins_Exorbitant_Privilege.docx  # original paper draft
    └── TEAM_MEMO_regression_update.docx       # internal memo on regression fix
```

---

## How to Reproduce the Final Results

```bash
pip install -r requirements.txt

# 1. Build the data panels (run from project root)
python collect_data.py                       # downloads raw data → data/
python build_panel.py                        # builds all three panels

# 2. Confirm non-stationarity and spurious regression (Phase 2 diagnosis)
python analysis/diagnostics.py               # ADF tests, cointegration → results/diagnostics.txt
python analysis/regression.py               # panel regression (N=102) → results/panel_regression.txt

# 3. Run the final bid-cover analysis (Phase 3)
python analysis/bidcover_robustness.py       # spec ladder A/B/C → results/bidcover_robustness.csv
python analysis/bidcover_final.py            # final spec + placebo → results/bidcover_final_results.csv
python analysis/event_study_multi.py         # multi-event study → results/event_study_multi_*.csv

# 4. Supporting evidence (VAR/IRF)
python analysis/robustness.py                # VAR, Granger causality, IRF → results/robustness.txt
```

To reproduce Phase 1 (original — now understood to be spurious):
```bash
python analysis/threshold.py                 # Hansen threshold → results/threshold_results.txt
python analysis/star.py                      # LSTAR → results/star_results.txt
```

---

## Data Sources

| Variable | Definition | Source |
|---|---|---|
| OIS–Treasury spread | DGS3MO − overnight SOFR | FRED (no API key required) |
| USDT supply | USDT market cap (daily) | DeFiLlama stablecoins API |
| USDC supply | USDC market cap (daily) | DeFiLlama stablecoins API |
| Treasury exposure θ | T-bill holdings / total supply | Tether (BDO, quarterly) + Circle (monthly) attestations |
| Liquid buffer L | Cash reserves / total supply | Same attestations |
| T-bill auction data | Bid-cover, offering size by maturity | TreasuryDirect.gov |
| VIX | CBOE Volatility Index | FRED |
| Federal funds rate | Effective fed funds rate | FRED |
| RoW equity (ΔlnN*) | ACWX ETF log-return | Yahoo Finance |

> `data/reserve_attestations.csv` is manually populated from public attestation reports.
> Tether reports quarterly (Cayman BDO); Circle reports monthly (Grant Thornton / Deloitte).

---

## What Was Demoted and Why

| Original Result | Status | Reason |
|---|---|---|
| β₁ = −7.57 (spread compression) | **Spurious** | Spread and L both I(1), no cointegration; driven by 2022–24 Fed hiking trend |
| Reserve threshold L* ≈ 13% | **Untestable** | Identified only in spurious levels regression; threshold shifts with interpolation method |
| LSTAR smooth-transition | **Demoted** | Same identification problem; c* = 14.9% not robust |
| Event-study CAR significance | **Qualitative only** | Pooled p = 0.43; insufficient power with 3–4 partially independent events |

---

## References

Caballero, R. J., Farhi, E., & Gourinchas, P. O. (2008). An equilibrium model of global imbalances and low interest rates. *American Economic Review*, 98(1), 358–393.

Engle, R. F., & Granger, C. W. J. (1987). Co-integration and error correction. *Econometrica*, 55(2), 251–276.

Gorton, G. B., & Zhang, J. Y. (2021). Taming wildcat stablecoins. *University of Chicago Law Review*, 90(1), 45–126.

Gourinchas, P. O., & Rey, H. (2007). From world banker to world venture capitalist. In *G7 Current Account Imbalances* (pp. 11–55). University of Chicago Press.

Granger, C. W. J., & Newbold, P. (1974). Spurious regressions in econometrics. *Journal of Econometrics*, 2(2), 111–120.

Johansen, S. (1988). Statistical analysis of cointegration vectors. *Journal of Economic Dynamics and Control*, 12(2–3), 231–254.

Krishnamurthy, A., & Vissing-Jorgensen, A. (2012). The aggregate demand for Treasury debt. *Journal of Political Economy*, 120(2), 233–267.

Maggiori, M. (2017). Financial intermediation, international risk sharing, and reserve currencies. *American Economic Review*, 107(10), 3038–3071.

Newey, W. K., & West, K. D. (1987). A simple, positive semi-definite, heteroscedasticity and autocorrelation consistent covariance matrix. *Econometrica*, 55(3), 703–708.

Phillips, P. C. B. (1986). Understanding spurious regressions in econometrics. *Journal of Econometrics*, 33(3), 311–340.
