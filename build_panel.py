"""
build_panel.py — merge raw data into daily and monthly analysis panels.

Inputs:  data/fred_raw.csv, data/defillama_raw.csv, data/row_equity_raw.csv,
         data/reserve_attestations.csv  (fill manually from Tether/Circle PDFs)
Outputs: data/daily_panel.csv, data/monthly_panel.csv
"""

import numpy as np
import pandas as pd

from config import (
    DATA_DIR, DAILY_CSV, MONTHLY_CSV, ATTESTATION_CSV,
    FRED_TBILL, FRED_SOFR90, FRED_SOFR, FRED_VIX,
    START_DATE,
)


# ── Load raw sources ────────────────────────────────────────────────────────

def load_fred() -> pd.DataFrame:
    df = pd.read_csv(f"{DATA_DIR}/fred_raw.csv", index_col=0, parse_dates=True)
    # OIS proxy: prefer 90-day SOFR avg; fill with overnight SOFR where missing
    df["ois"] = df[FRED_SOFR90].combine_first(df[FRED_SOFR])
    df["spread"] = df[FRED_TBILL] - df["ois"]   # OIS-Treasury spread (%)
    return df[["spread", FRED_VIX]].rename(columns={FRED_VIX: "vix"})


def load_stablecoins() -> pd.DataFrame:
    df = pd.read_csv(f"{DATA_DIR}/defillama_raw.csv", index_col=0, parse_dates=True)
    # Ensure we have total supply in billions for readability
    if df["total_supply"].max() > 1e9:
        df = df / 1e9   # convert from raw USD to billions
    df.columns = [f"supply_{c}" if c != "total_supply" else "supply_total" for c in df.columns]
    return df


def load_row_equity() -> pd.Series:
    df = pd.read_csv(f"{DATA_DIR}/row_equity_raw.csv", index_col=0, parse_dates=True)
    return df.iloc[:, 0].rename("row_equity")


def load_attestations() -> pd.DataFrame:
    """
    Reserve attestations (quarterly for Tether, monthly for Circle).
    Columns: date, issuer, treasury_holdings_bn, total_supply_bn, cash_reserves_bn, source, cash_source
    
    Computes:
    - theta = treasury_holdings_bn / total_supply_bn (Treasury Exposure)
    - liq_buffer = cash_reserves_bn / total_supply_bn (Liquid Buffer)
    - buffer_ratio = (treasury_holdings_bn - total_supply_bn) / total_supply_bn (Old measure, kept for comparison)
    
    Returns monthly forward-filled values.
    """
    try:
        att = pd.read_csv(ATTESTATION_CSV, parse_dates=["date"])
    except FileNotFoundError:
        print(f"  WARNING: {ATTESTATION_CSV} not found. Theta and liq_buffer will be NaN.")
        return pd.DataFrame(columns=["theta", "liq_buffer", "buffer_ratio"])

    att = att.sort_values("date")
    # Aggregate across issuers: sum holdings, supply, and cash reserves
    agg = att.groupby("date")[["treasury_holdings_bn", "total_supply_bn", "cash_reserves_bn"]].sum()
    
    # Compute decomposed buffer variables
    agg["theta"] = agg["treasury_holdings_bn"] / agg["total_supply_bn"]  # Treasury exposure
    agg["liq_buffer"] = agg["cash_reserves_bn"] / agg["total_supply_bn"]  # Liquid buffer
    
    # Keep buffer_ratio for comparison
    agg["buffer_ratio"] = (agg["treasury_holdings_bn"] - agg["total_supply_bn"]) / agg["total_supply_bn"]
    
    return agg[["theta", "liq_buffer", "buffer_ratio"]]


# ── Derived variables ───────────────────────────────────────────────────────

def compute_velocity(supply: pd.Series, window: int = 7) -> pd.Series:
    """7-day rolling std of daily log-changes — redemption velocity V."""
    log_chg = np.log(supply).diff()
    return log_chg.rolling(window, min_periods=3).std().rename("velocity")


# ── Build panels ────────────────────────────────────────────────────────────

def build_daily(fred: pd.DataFrame, coins: pd.DataFrame, row: pd.Series) -> pd.DataFrame:
    supply = coins["supply_total"]
    dlns   = np.log(supply).diff().rename("dln_supply")   # Δln S
    vel    = compute_velocity(supply)
    dlnrow = np.log(row).diff().rename("dln_row_equity")

    daily = pd.concat([fred, coins, dlns, vel, dlnrow], axis=1)
    daily = daily.ffill(limit=3)   # fill weekends / bank holidays (max 3 days)
    daily.index.name = "date"
    return daily


def build_monthly(daily: pd.DataFrame, attestations: pd.DataFrame) -> pd.DataFrame:
    # Resample to month-end
    agg = {
        "spread":       "mean",
        "vix":          "mean",
        "supply_total": "last",
        "dln_supply":   "sum",     # monthly log-change = sum of daily
        "velocity":     "mean",
        "dln_row_equity": "sum",
    }
    monthly = daily.resample("ME").agg({k: v for k, v in agg.items() if k in daily.columns})

    # Forward-fill theta, liq_buffer, and buffer_ratio from attestation dates to every month-end
    if not attestations.empty:
        att_monthly = attestations.resample("ME").last().ffill()
        monthly = monthly.join(att_monthly, how="left")
        # Forward-fill all buffer variables
        monthly["theta"] = monthly["theta"].ffill()
        monthly["liq_buffer"] = monthly["liq_buffer"].ffill()
        monthly["buffer_ratio"] = monthly["buffer_ratio"].ffill()
    else:
        monthly["theta"] = float("nan")
        monthly["liq_buffer"] = float("nan")
        monthly["buffer_ratio"] = float("nan")

    # Asymmetric supply splits (buying T-bills is gradual; selling is forced)
    monthly["dln_supply_pos"] = monthly["dln_supply"].clip(lower=0)
    monthly["dln_supply_neg"] = monthly["dln_supply"].clip(upper=0)

    # Interaction terms for decomposed buffer variables
    monthly["theta_x_dlns"] = monthly["theta"] * monthly["dln_supply"]       # theta × Δln S
    monthly["L_x_dlns"] = monthly["liq_buffer"] * monthly["dln_supply"]      # L × Δln S
    monthly["L_x_dlns_pos"] = monthly["liq_buffer"] * monthly["dln_supply_pos"]
    monthly["L_x_dlns_neg"] = monthly["liq_buffer"] * monthly["dln_supply_neg"]

    # Keep old interaction term for comparison
    monthly["buf_x_dlns"] = monthly["buffer_ratio"] * monthly["dln_supply"]

    monthly.index.name = "date"
    monthly = monthly.dropna(subset=["spread", "dln_supply"])
    # Restrict to sample period where attestation data is reliable
    monthly = monthly[monthly.index >= pd.Timestamp(START_DATE)]
    return monthly


# ── Main ────────────────────────────────────────────────────────────────────

def main():
    print("Loading raw data...")
    fred  = load_fred()
    coins = load_stablecoins()
    row   = load_row_equity()
    att   = load_attestations()

    print("Building daily panel...")
    daily = build_daily(fred, coins, row)
    daily.to_csv(DAILY_CSV)
    print(f"  -> {DAILY_CSV} ({len(daily)} rows, {daily.columns.tolist()})")

    print("Building monthly panel...")
    monthly = build_monthly(daily, att)
    monthly.to_csv(MONTHLY_CSV)
    print(f"  -> {MONTHLY_CSV} ({len(monthly)} rows)")
    print(f"\nColumn summary:\n{monthly.describe().round(4)}")

    missing = monthly["buffer_ratio"].isna().sum()
    if missing > 0:
        print(f"\n  NOTE: buffer_ratio missing for {missing} months."
              f" Fill data/reserve_attestations.csv to enable regression with B.")


if __name__ == "__main__":
    main()
