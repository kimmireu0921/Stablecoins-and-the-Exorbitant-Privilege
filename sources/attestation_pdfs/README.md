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
| 2026-03-31 | ✅ verified (T-Bills = $117,035,732,050; Cash = $107,021,630) |
| **2025-12-31** | ✅ verified (T-Bills = $122,325,714,946; Cash = $33,952,735) |
| **2025-09-30** | ✅ verified (T-Bills = $112,417,034,272; Cash = $30,100,334) — file named `31-10-2025` (approval date) |
| **2025-06-30** | ✅ verified (T-Bills = $105,518,993,610; Cash = $32,430,726) — file named `RC187322025BD0201` |
| **2025-03-31** | ✅ verified (T-Bills = $98,523,657,338; Cash = $64,302,555) |
| **2024-12-31** | ✅ verified (T-Bills = $94,471,651,607; Cash = $108,844,601) |
| 2024-09-30 | ☐ missing — not yet downloaded |
| **2024-06-30** | ✅ verified (T-Bills = $80,948,647,984; Cash = $109,867,228) |
| **2024-03-31** | ✅ verified (T-Bills = $74,045,290,303; Cash = $100,264,024) |
| 2023-12-31 | ✅ downloaded |
| 2023-09-30 | ✅ downloaded |
| 2023-06-30 | ✅ downloaded |
| 2023-03-31 | ✅ downloaded |
| 2022-12-31 | ✅ downloaded |
| 2022-09-30 | ✅ downloaded |
| 2022-06-30 | ✅ downloaded |
| 2022-03-31 | ✅ downloaded |
| 2021-12-31 | ✅ downloaded |
| 2021-09-30 | ✅ downloaded |

**Still missing:** 2024-09-30 only. All other quarters are present.

**Note on file naming (2025+):** BDO report filenames reflect the approval date, not the
reporting date. `31-10-2025` = Q3 report as of 2025-09-30 (approved 31 Oct 2025).
`RC187322025BD0201` = Q2 report as of 2025-06-30 (approved 31 Jul 2025).

**Note on entity scope (2025+):** Starting Q1 2025, BDO attestations cover
**Tether International, S.A. de C.V.** only (not the consolidated Tether Holdings group).
Treasury and cash figures reflect this single entity. Prior quarters (≤ 2024-12-31) covered
Tether Holdings Limited (consolidated). All CSV values use the BDO-attested scope.

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

## Note on 2024–2025 USDT cash entries

Cash & Bank Deposits for USDT dropped sharply from billions (2021–2023, web-extracted
from tether.to) to tens-of-millions (2024+, BDO-attested). The tether.to website appears
to report a broader "cash" category than the BDO line item "Cash & Bank Deposits." All
2024+ entries in the CSV use the BDO-attested figures.
