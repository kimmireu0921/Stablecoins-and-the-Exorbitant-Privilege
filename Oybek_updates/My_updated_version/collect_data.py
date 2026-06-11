"""
collect_data.py — pull raw data from FRED (no API key), DeFiLlama, yfinance, TreasuryDirect.

Outputs:
  data/fred_raw.csv          — DTB3, SOFR90DAYAVG, SOFR, FEDFUNDS, VIXCLS (daily/monthly)
  data/defillama_raw.csv     — total stablecoin supply + USDT + USDC (daily, USD)
  data/row_equity_raw.csv    — ACWX close price as RoW equity proxy (daily)
  data/auction_raw.csv       — 13-week T-bill bid-cover ratios from TreasuryDirect
"""

import json
import requests
import pandas as pd
import yfinance as yf
from io import StringIO

from config import START_DATE, END_DATE, DATA_DIR, TRACK_COINS
from config import FRED_TBILL, FRED_SOFR90, FRED_SOFR, FRED_FF, FRED_VIX

FRED_CSV_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={}"
DEFILLAMA_TOTAL = "https://stablecoins.llama.fi/stablecoincharts/all"
DEFILLAMA_LIST  = "https://stablecoins.llama.fi/stablecoins"
TREASURYDIRECT_URL = (
    "https://www.treasurydirect.gov/TA_WS/securities/search"
    "?type=Bill&term=13-Week"
    "&dateFieldName=auctionDate"
    "&startDate={start}&endDate={end}"
    "&format=json&pagesize=2000"
)


def fetch_fred(series_id: str) -> pd.Series:
    url = FRED_CSV_URL.format(series_id)
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    df = pd.read_csv(StringIO(r.text), index_col=0, parse_dates=True, na_values=".")
    s = df.iloc[:, 0].astype(float)
    s.name = series_id
    return s.loc[START_DATE:END_DATE]


def fetch_defillama() -> pd.DataFrame:
    # Total USD-pegged stablecoin market cap
    r = requests.get(DEFILLAMA_TOTAL, timeout=60)
    r.raise_for_status()
    raw = r.json()
    dates = [pd.Timestamp(int(d["date"]), unit="s") for d in raw]
    total = [d.get("totalCirculating", {}).get("peggedUSD", float("nan")) for d in raw]
    series = {"total_supply": pd.Series(total, index=dates)}

    # Individual coin supply
    r2 = requests.get(DEFILLAMA_LIST, timeout=30)
    r2.raise_for_status()
    payload   = r2.json()
    coin_list = payload.get("peggedAssets", payload) if isinstance(payload, dict) else payload

    seen = set()
    for coin in coin_list:
        sym = coin.get("symbol", "")
        if sym not in TRACK_COINS or sym in seen:
            continue
        seen.add(sym)
        cid = coin["id"]
        rc = requests.get(f"{DEFILLAMA_TOTAL}?stablecoin={cid}", timeout=60)
        rc.raise_for_status()
        craw = rc.json()
        cdates = [pd.Timestamp(int(d["date"]), unit="s") for d in craw]
        cmcap  = [d.get("totalCirculating", {}).get("peggedUSD", float("nan")) for d in craw]
        series[sym] = pd.Series(cmcap, index=cdates)
        print(f"    {sym}: {len(cdates)} observations")

    df = pd.DataFrame(series)
    df.index.name = "date"
    return df.loc[START_DATE:END_DATE]


def fetch_row_equity() -> pd.Series:
    # iShares MSCI ACWI ex-US ETF as RoW financial net worth proxy
    hist = yf.Ticker("ACWX").history(start=START_DATE, end=END_DATE)
    s = hist["Close"].rename("row_equity")
    s.index = s.index.tz_localize(None)
    return s


def fetch_auction_data() -> pd.DataFrame:
    url = TREASURYDIRECT_URL.format(start=START_DATE, end=END_DATE)
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    data = r.json()
    records = []
    for item in data:
        try:
            bcr = item.get("bidToCoverRatio") or item.get("bidToCoverRatio2")
            hy  = item.get("highYield") or item.get("highDiscountRate")
            if bcr is None:
                continue
            records.append({
                "date": pd.Timestamp(item["auctionDate"]),
                "bid_cover_ratio": float(bcr),
                "high_yield": float(hy) if hy else float("nan"),
            })
        except (KeyError, ValueError, TypeError):
            continue
    if not records:
        print("  TreasuryDirect returned no parseable records.")
        return pd.DataFrame()
    df = pd.DataFrame(records).set_index("date").sort_index()
    return df.loc[START_DATE:END_DATE]


def main():
    print("=== Fetching FRED series (no API key required) ===")
    fred_series = {
        FRED_TBILL:  fetch_fred(FRED_TBILL),
        FRED_SOFR90: fetch_fred(FRED_SOFR90),
        FRED_SOFR:   fetch_fred(FRED_SOFR),
        FRED_FF:     fetch_fred(FRED_FF),
        FRED_VIX:    fetch_fred(FRED_VIX),
    }
    for name, s in fred_series.items():
        print(f"  {name}: {s.notna().sum()} non-null observations")
    fred_df = pd.concat(fred_series.values(), axis=1)
    fred_df.to_csv(f"{DATA_DIR}/fred_raw.csv")
    print(f"  -> data/fred_raw.csv ({len(fred_df)} rows)\n")

    print("=== Fetching DeFiLlama stablecoin supply ===")
    dl_df = fetch_defillama()
    dl_df.to_csv(f"{DATA_DIR}/defillama_raw.csv")
    print(f"  -> data/defillama_raw.csv ({len(dl_df)} rows)\n")

    print("=== Fetching RoW equity (ACWX via yfinance) ===")
    row = fetch_row_equity()
    row.to_frame().to_csv(f"{DATA_DIR}/row_equity_raw.csv")
    print(f"  -> data/row_equity_raw.csv ({len(row)} rows)\n")

    print("=== Fetching TreasuryDirect 13-week auction data ===")
    try:
        auctions = fetch_auction_data()
        auctions.to_csv(f"{DATA_DIR}/auction_raw.csv")
        print(f"  -> data/auction_raw.csv ({len(auctions)} rows)\n")
    except Exception as e:
        print(f"  WARNING: TreasuryDirect fetch failed ({e}). Fill data/auction_bid_cover.csv manually.\n")

    print("=== Done. ===")
    print("Next: fill data/reserve_attestations.csv from Tether/Circle PDFs, then run build_panel.py")


if __name__ == "__main__":
    main()
