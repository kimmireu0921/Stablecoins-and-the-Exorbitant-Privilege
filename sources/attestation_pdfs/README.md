# Attestation PDFs

These PDFs are the primary source for `data/reserve_attestations.csv`.
Download each one manually and save it here using the filename convention below.
All reports are publicly available — no login required.

---

## Tether (USDT) — BDO Italia
**Website:** https://tether.to/en/transparency (scroll to "Past Reports")

For each report, look for the table titled "Financials Figures and Reserves Report."
Extract: **U.S. Treasury Bills**, **Cash & Bank Deposits**, **total USDT in circulation** (from the liabilities section).

| Date | Filename to save as | Status |
|---|---|---|
| 2026-03-31 | `USDT_2026Q1_BDO.pdf` | ☐ |
| **2025-12-31** | `USDT_2025Q4_BDO.pdf` | ✅ verified (Cash & Bank Deposits = $33,952,735) |
| 2025-09-30 | `USDT_2025Q3_BDO.pdf` | ☐ |
| 2025-06-30 | `USDT_2025Q2_BDO.pdf` | ☐ |
| 2025-03-31 | `USDT_2025Q1_BDO.pdf` | ☐ |
| 2024-12-31 | `USDT_2024Q4_BDO.pdf` | ☐ |
| 2024-09-30 | `USDT_2024Q3_BDO.pdf` | ☐ |
| 2024-06-30 | `USDT_2024Q2_BDO.pdf` | ☐ |
| 2024-03-31 | `USDT_2024Q1_BDO.pdf` | ☐ |
| 2023-12-31 | `USDT_2023Q4_BDO.pdf` | ☐ |
| 2023-09-30 | `USDT_2023Q3_BDO.pdf` | ☐ |
| 2023-06-30 | `USDT_2023Q2_BDO.pdf` | ☐ |
| 2023-03-31 | `USDT_2023Q1_BDO.pdf` | ☐ |
| 2022-12-31 | `USDT_2022Q4_BDO.pdf` | ☐ |
| 2022-09-30 | `USDT_2022Q3_BDO.pdf` | ☐ |
| 2022-06-30 | `USDT_2022Q2_BDO.pdf` | ☐ |
| 2022-03-31 | `USDT_2022Q1_BDO.pdf` | ☐ |

**Priority:** Download 2024-03-31, 2024-06-30, 2024-12-31 first — these quarters have
`cash_reserves_bn` as NaN in the CSV (values were near-zero scraping artifacts treated as
missing and interpolated). The PDFs will tell you the real Cash & Bank Deposits figure.

---

## Circle (USDC) — Deloitte / Grant Thornton
**Website:** https://www.circle.com/en/transparency

Circle publishes monthly. Look for the "Reserve Report" — extract:
**U.S. Treasury Bills**, **Cash**, **total USDC in circulation**.

Circle's reports have comprehensive monthly data from mid-2022 onward.
The CSV already has good coverage from web-extracted values for most months.
Download only if you need to verify a specific entry.

| Priority quarters | Filename |
|---|---|
| 2022-06-30 (first detailed report) | `USDC_2022Q2_GrantThornton.pdf` |
| 2023-12-31 (estimated entry in CSV) | `USDC_2023Q4_Deloitte.pdf` |

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
