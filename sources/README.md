# Data Sources

All data used in the analysis, with reproduction instructions.

---

## Programmatic sources (auto-fetched by `collect_data.py`)

Run `python collect_data.py` to refresh all of these.

| Output file | Source | Series / endpoint |
|---|---|---|
| `data/fred_raw.csv` | FRED (St. Louis Fed) | DTB3, SOFR90DAYAVG, SOFR, FEDFUNDS, VIXCLS |
| `data/defillama_raw.csv` | DeFiLlama API | Total stablecoin supply + USDT + USDC daily circulating |
| `data/row_equity_raw.csv` | Yahoo Finance (yfinance) | ACWX — iShares MSCI ACWI ex-US ETF (RoW equity proxy) |

No API keys required. FRED data is free and public.

---

## Manual sources (PDFs — must download by hand)

| Output file | Source | Instructions |
|---|---|---|
| `data/reserve_attestations.csv` | Tether BDO attestations + Circle Deloitte/Grant Thornton attestations | See `attestation_pdfs/README.md` |

PDF files should be saved to `sources/attestation_pdfs/` following the naming convention
in that folder's README. They are not committed to the repo (too large; added to .gitignore).

---

## Key variable definitions

| Variable | Definition | Source |
|---|---|---|
| `spread` | DGS3MO − overnight SOFR (convenience yield proxy, %) | FRED |
| `supply_USDT` / `supply_USDC` | Daily circulating supply (USD) | DeFiLlama |
| `dln_supply` | Monthly log change in circulating supply | DeFiLlama (month-end) |
| `liq_buffer` (L) | Cash & Bank Deposits / total supply | Tether/Circle attestation PDFs |
| `theta` | U.S. Treasury Bills / total supply | Tether/Circle attestation PDFs |
| `vix` | CBOE Volatility Index | FRED (VIXCLS) |
| `fedfunds` | Effective federal funds rate | FRED (FEDFUNDS) |
| `dln_row_equity` | Monthly log change in ACWX close price | Yahoo Finance |
