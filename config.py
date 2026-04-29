"""
config.py — shared constants for the stablecoin-exorbitant-privilege study.
Set FRED_API_KEY as an environment variable before running:
    export FRED_API_KEY="your_key_here"
Free keys available at https://fred.stlouisfed.org/docs/api/api_key.html
"""

import os

# ── Date range ─────────────────────────────────────────────────────────────
START_DATE = "2020-01-01"
END_DATE   = "2026-03-31"

# ── API keys ───────────────────────────────────────────────────────────────
FRED_API_KEY = os.getenv("FRED_API_KEY", "")

# ── FRED series codes ──────────────────────────────────────────────────────
# DTB3    : 3-month T-bill secondary market yield (daily, %)
# SOFR    : Secured Overnight Financing Rate — OIS proxy (daily, %)
# FEDFUNDS: Effective Fed Funds Rate — OIS fallback (monthly, %)
# VIXCLS  : CBOE VIX (daily)
FRED_TBILL    = "DTB3"
FRED_SOFR90   = "SOFR90DAYAVG"   # 90-day SOFR avg — 3-month OIS proxy (starts 2020-02-04)
FRED_SOFR     = "SOFR"            # overnight SOFR fallback
FRED_FF       = "FEDFUNDS"        # Fed Funds monthly fallback
FRED_VIX      = "VIXCLS"

# ── DeFiLlama ──────────────────────────────────────────────────────────────
# Stablecoin symbols to track individually (others roll into "rest")
TRACK_COINS  = {"USDT", "USDC"}

# ── Event study ────────────────────────────────────────────────────────────
# (event_key, calendar date, buffer regime)
EVENTS = {
    "LUNA_UST":   {"date": "2022-05-09", "buffer": "low",  "label": "LUNA/UST Collapse"},
    "USDT_depeg": {"date": "2022-05-12", "buffer": "low",  "label": "USDT Partial Depeg"},
    "USDC_SVB":   {"date": "2023-03-11", "buffer": "high", "label": "USDC / SVB Failure"},
}

# Event-study windows (trading days relative to event date τ = 0)
EST_WINDOW   = (-120, -6)    # estimation window for normal-spread model
EVENT_WINDOW = (-5,   20)    # event window for abnormal-spread measurement

# ── Paths ──────────────────────────────────────────────────────────────────
DATA_DIR    = "data"
RESULTS_DIR = "results"
ATTESTATION_CSV = f"{DATA_DIR}/reserve_attestations.csv"
AUCTION_CSV     = f"{DATA_DIR}/auction_bid_cover.csv"
MONTHLY_CSV     = f"{DATA_DIR}/monthly_panel.csv"
DAILY_CSV       = f"{DATA_DIR}/daily_panel.csv"
