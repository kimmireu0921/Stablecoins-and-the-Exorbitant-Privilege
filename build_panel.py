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

# Issuer-level long panel output (#2). Defined here rather than in config.py
# so config.py is left untouched.
PANEL_LONG_CSV = f"{DATA_DIR}/panel_long.csv"


# ── Load raw sources ────────────────────────────────────────────────────────

def load_fred() -> pd.DataFrame:
    df = pd.read_csv(f"{DATA_DIR}/fred_raw.csv", index_col=0, parse_dates=True)
    # OIS proxy: prefer 90-day SOFR avg; fill with overnight SOFR where missing
    df["ois"] = df[FRED_SOFR90].combine_first(df[FRED_SOFR])
    df["spread"] = df[FRED_TBILL] - df["ois"]   # OIS-Treasury spread (%)
    # Forward-fill monthly FEDFUNDS to daily; captures Fed hiking cycle for normal model
    df["fedfunds"] = df["FEDFUNDS"].ffill()
    return df[["spread", FRED_VIX, "fedfunds"]].rename(columns={FRED_VIX: "vix"})


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


# Interpolation method for filling between attestation dates.
# Prof's feedback: "I would just do a moving average" instead of forward-fill,
# so a quarterly value (e.g. Q1 covering Jan-Mar) is blended with the neighbouring
# quarters rather than repeated as a flat step for three months.
#   "time"    — time-weighted linear interpolation on the month-end grid.
#               Mathematically equivalent to the prof's ⅔/⅓ blend
#               (Jan = ⅔·Q1 + ⅓·Q4_prev, Mar = ⅔·Q1 + ⅓·Q2).  [recommended]
#   "prof"    — the ⅔/⅓ weighting written out explicitly (anchored on the
#               attestation month, blended toward the adjacent attestation).
#   "rolling" — centred 3-month rolling mean of the forward-filled series.
#   "ffill"   — original behaviour, kept only for back-comparison.
INTERP_METHOD = "time"


def _interp_issuer(s: pd.Series, method: str) -> pd.Series:
    """Fill gaps in one issuer's month-end series by the chosen method."""
    if method == "ffill":
        return s.ffill()
    if method == "time":
        # time-weighted linear interpolation between known attestation points
        return s.interpolate(method="time", limit_direction="both")
    if method == "rolling":
        # forward-fill first (to have a value every month), then smooth
        return s.ffill().rolling(3, min_periods=1, center=True).mean()
    if method == "prof":
        # Explicit ⅔/⅓ blend toward the nearest *forward* attestation.
        # For a month m between attestation a (this quarter) and b (next quarter),
        # weight = distance to b, so the month adjacent to b leans ⅓ toward b.
        known = s.dropna()
        if len(known) < 2:
            return s.ffill()
        out = s.copy()
        anchors = known.index
        for i in range(len(anchors) - 1):
            a, b = anchors[i], anchors[i + 1]
            span = (b - a).days
            mask = (s.index > a) & (s.index < b)
            for m in s.index[mask]:
                w = (m - a).days / span          # 0 at a, →1 at b
                out.loc[m] = (1 - w) * known[a] + w * known[b]
        return out.ffill().bfill()
    raise ValueError(f"unknown INTERP_METHOD: {method}")


def load_attestations(method: str = None) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Reserve attestations (quarterly for Tether, monthly for Circle).
    Columns: date, issuer, treasury_holdings_bn, total_supply_bn, cash_reserves_bn, source, cash_source

    Per prof feedback (#2, #3) we interpolate *issuer by issuer* on a month-end grid
    before aggregating, instead of forward-filling the already-summed series.

    Returns:
      panel_long  — one row per (date, issuer) with theta_i, liq_buffer_i, supply_i
                    (#2: "each issuer as a separate observation").
      agg         — aggregate time series with
                      theta      = (T_USDT + T_USDC) / (S_USDT + S_USDC)
                      liq_buffer = (cash_USDT + cash_USDC) / (S_USDT + S_USDC)
                    (#2 prof aggregation formula).  No combined treasury+liquid
                    variable is built (#1: "do not combine treasury and liquid").
    """
    method = method or INTERP_METHOD
    try:
        att = pd.read_csv(ATTESTATION_CSV, parse_dates=["date"])
    except FileNotFoundError:
        print(f"  WARNING: {ATTESTATION_CSV} not found. Theta and liq_buffer will be NaN.")
        empty = pd.DataFrame(columns=["theta", "liq_buffer"])
        return pd.DataFrame(columns=["issuer", "theta", "liq_buffer", "supply"]), empty

    att = att.sort_values("date")
    # Scraping artifacts produce near-zero placeholders (e.g. 1.1e-08) for unreported
    # treasury/cash. Treat anything below 1e-6 bn as missing so interpolation fills it.
    for col in ["treasury_holdings_bn", "cash_reserves_bn"]:
        att[col] = att[col].where(att[col].isna() | (att[col] >= 1e-6), other=np.nan)

    # Month-end grid spanning the full attestation range
    grid = pd.date_range(att["date"].min(), att["date"].max(), freq="ME")

    cols = ["treasury_holdings_bn", "total_supply_bn", "cash_reserves_bn"]
    issuer_frames = []
    for iss, g in att.groupby("issuer"):
        g = g.set_index("date")[cols]
        # collapse any duplicate month-ends, then reindex to the full grid
        g = g[~g.index.duplicated(keep="last")].reindex(grid)
        for c in cols:
            g[c] = _interp_issuer(g[c], method)
        g["issuer"] = iss
        issuer_frames.append(g)

    long = pd.concat(issuer_frames).reset_index().rename(columns={"index": "date"})
    long = long.dropna(subset=["total_supply_bn"])

    # Per-issuer ratios (#2 panel: theta_i, L_i for each company)
    long["theta"]      = long["treasury_holdings_bn"] / long["total_supply_bn"]
    long["liq_buffer"] = long["cash_reserves_bn"]     / long["total_supply_bn"]
    panel_long = long.rename(columns={"total_supply_bn": "supply"})[
        ["date", "issuer", "theta", "liq_buffer", "supply",
         "treasury_holdings_bn", "cash_reserves_bn"]
    ].set_index("date")

    # Aggregate with the prof's formula: sum numerators and denominators first.
    agg = long.groupby("date")[cols].sum(min_count=1)
    agg["theta"]      = agg["treasury_holdings_bn"] / agg["total_supply_bn"]
    agg["liq_buffer"] = agg["cash_reserves_bn"]     / agg["total_supply_bn"]

    return panel_long, agg[["theta", "liq_buffer"]]


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

    # Join the already-interpolated aggregate theta / liq_buffer (#3: interpolation
    # is done issuer-by-issuer inside load_attestations, NOT forward-filled here).
    if not attestations.empty:
        att_monthly = attestations.resample("ME").last()
        monthly = monthly.join(att_monthly, how="left")
    else:
        monthly["theta"] = float("nan")
        monthly["liq_buffer"] = float("nan")

    # Asymmetric supply splits (buying T-bills is gradual; selling is forced)
    monthly["dln_supply_pos"] = monthly["dln_supply"].clip(lower=0)
    monthly["dln_supply_neg"] = monthly["dln_supply"].clip(upper=0)

    # Interaction term on the LIQUID buffer only (#1: keep L and L×ΔlnS directly;
    # theta and any combined treasury+liquid variable are dropped).
    monthly["L_x_dlns"] = monthly["liq_buffer"] * monthly["dln_supply"]      # L × Δln S
    monthly["L_x_dlns_pos"] = monthly["liq_buffer"] * monthly["dln_supply_pos"]
    monthly["L_x_dlns_neg"] = monthly["liq_buffer"] * monthly["dln_supply_neg"]

    monthly.index.name = "date"
    monthly = monthly.dropna(subset=["spread", "dln_supply"])
    # Restrict to sample period where attestation data is reliable
    monthly = monthly[monthly.index >= pd.Timestamp(START_DATE)]
    return monthly


def build_panel_long(monthly: pd.DataFrame, panel_long: pd.DataFrame,
                     coins: pd.DataFrame) -> pd.DataFrame:
    """
    Stack issuers into one long panel (#2): each row = one issuer in one month.
      - liq_buffer_i, theta_i  : issuer-specific (from attestations, interpolated)
      - dln_supply_i           : issuer-specific monthly log supply growth from
                                 DeFiLlama circulating supply — NOT attestation
                                 total_supply_bn (prof's correction: attestation
                                 supply is quarterly and smoothed by interpolation,
                                 so it mismeasures actual monthly supply changes)
      - spread, vix, dln_row_equity : macro, identical on both issuer rows per month
    L_x_dlns is the issuer-level interaction L_i × ΔlnS_i.
    """
    macro = monthly[["spread", "vix", "dln_row_equity"]].copy()

    p = panel_long.copy()
    p.index = p.index.to_period("M").to_timestamp("M")   # snap to month-end
    p = p.reset_index().rename(columns={"index": "date"})

    # DeFiLlama month-end supply for dln_supply (prof's correction)
    dl_monthly = coins[["supply_USDT", "supply_USDC"]].resample("ME").last()
    dl_monthly = dl_monthly.rename(columns={"supply_USDT": "USDT", "supply_USDC": "USDC"})
    dl_long = dl_monthly.stack().rename("supply_dl").reset_index()
    dl_long.columns = ["date", "issuer", "supply_dl"]

    p = p.merge(dl_long, on=["date", "issuer"], how="left")
    p = p.sort_values(["issuer", "date"])
    p["dln_supply"] = p.groupby("issuer")["supply_dl"].transform(
        lambda s: np.log(s).diff()
    )

    # attach macro vars (same value for every issuer in that month)
    p = p.set_index("date").join(macro, how="inner").reset_index()

    p["L_x_dlns"] = p["liq_buffer"] * p["dln_supply"]
    p = p.dropna(subset=["spread", "dln_supply", "liq_buffer"])
    p = p[p["date"] >= pd.Timestamp(START_DATE)]
    return p.set_index("date")


# ── Main ────────────────────────────────────────────────────────────────────

def main():
    print("Loading raw data...")
    fred  = load_fred()
    coins = load_stablecoins()
    row   = load_row_equity()
    panel_long, att = load_attestations()
    print(f"  Attestation interpolation method: {INTERP_METHOD}")

    print("Building daily panel...")
    daily = build_daily(fred, coins, row)
    daily.to_csv(DAILY_CSV)
    print(f"  -> {DAILY_CSV} ({len(daily)} rows, {daily.columns.tolist()})")

    print("Building monthly (aggregate time-series) panel...")
    monthly = build_monthly(daily, att)
    monthly.to_csv(MONTHLY_CSV)
    print(f"  -> {MONTHLY_CSV} ({len(monthly)} rows, theta+L non-null: "
          f"{monthly['liq_buffer'].notna().sum()})")

    print("Building issuer-level long panel (#2)...")
    panel = build_panel_long(monthly, panel_long, coins)
    panel.to_csv(PANEL_LONG_CSV)
    print(f"  -> {PANEL_LONG_CSV} ({len(panel)} issuer-month rows; "
          f"issuers: {sorted(panel['issuer'].unique())})")


if __name__ == "__main__":
    main()
