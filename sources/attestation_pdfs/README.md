# Attestation PDFs

These PDFs are the primary source for `data/reserve_attestations.csv`.
Download each one manually and save it here. Keep the original filename from the website — no renaming needed.
All reports are publicly available — no login required.

---

## Tether (USDT) — BDO Italia
**Website:** https://tether.to/en/transparency (scroll to "Past Reports")

For each report, look for the table titled "Financials Figures and Reserves Report."
Extract: **U.S. Treasury Bills**, **Cash & Bank Deposits**, **total USDT in circulation** (from the liabilities section).

| Date | Status |
|---|---|
| 2026-03-31 | ✅ downloaded |
| **2025-12-31** | ✅ verified (Cash & Bank Deposits = $33,952,735) |
| 2025-09-30 | ☐ missing — not yet downloaded |
| **2025-06-30** | ✅ verified (Cash & Bank Deposits = $32,430,726) |
| 2025-03-31 | ✅ downloaded |
| 2024-12-31 | ✅ downloaded |
| 2024-09-30 | ☐ missing — not yet downloaded |
| 2024-06-30 | ✅ downloaded |
| 2024-03-31 | ✅ downloaded |
| 2023-12-31 | ✅ downloaded |
| 2023-09-30 | ✅ downloaded |
| 2023-06-30 | ✅ downloaded |
| 2023-03-31 | ✅ downloaded |
| 2022-12-31 | ✅ downloaded |
| 2022-09-30 | ✅ downloaded |
| 2022-06-30 | ✅ downloaded |
| 2022-03-31 | ✅ downloaded |

**Still missing:** 2025-09-30 and 2024-09-30. All other quarters are present.

**Note on 2025-10-31 file:** An extra file (`31-10-2025`) is present — this appears to be a
monthly attestation, not the Q3 quarterly report. The Q3 (2025-09-30) report is still needed.

**Note on 2024 priority quarters:** PDFs for 2024-03-31, 2024-06-30, and 2024-12-31 are now
downloaded. Extract Cash & Bank Deposits from each and update `data/reserve_attestations.csv`
to replace the NaN placeholders (2.1e-08, 2.3e-08 artifacts).

---

## Circle (USDC) — Deloitte / Grant Thornton

Circle attestation PDFs are **not included** in this folder. The USDC entries in
`data/reserve_attestations.csv` were verified to be accurate through web extraction
and no suspicious entries were found that required PDF confirmation. USDC's liquid
buffer (L) stays consistently between 10–25% throughout the sample and never
approaches the threshold levels relevant to the analysis.

USDT PDFs were downloaded specifically because the Q4 2025 cash entry appeared
suspicious and required direct verification against the BDO source document.

---

## What the CSV fields mean (mapped to PDF line items)

| CSV column | PDF line item |
|---|---|
| `treasury_holdings_bn` | "U.S. Treasury Bills" (in billions) |
| `cash_reserves_bn` | "Cash & Bank Deposits" or "Cash" (in billions) |
| `total_supply_bn` | Total USDT/USDC in circulation (liabilities section) |

---

## Note on 2024 USDT cash entries

Quarters 2024-Q1, 2024-Q2, 2024-Q4 have near-zero placeholder values (2.1e-08, 2.3e-08)
in the raw CSV, which the pipeline treats as NaN and interpolates. The actual Cash & Bank
Deposits for those quarters may be small but nonzero — verify from the PDFs if the
threshold analysis results are being cited.
