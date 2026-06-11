# Prof Feedback — Changes & New Results (for the team)

This documents the code changes made in response to Prof. Hur's feedback and the
**new numbers they produce**. Read this before touching the paper/slides — the old
hardcoded numbers (β₁ = −7.57, q* = 0.13, etc.) are no longer what the code produces.

Only files inside this `for_claudecode_...` folder were changed. Backups: `*.py.bak`.

---

## What the prof asked (his exact points)

**Written summary (3 lines):**
1. Try using each issuer as a separate observation (exploit the panel dimension).
2. In either the panel or time series analysis, do not combine treasury and liquid reserves.
3. If anything, just drop the treasury (theta).

**Plus from the oral feedback:**
- B×ΔlnS "makes no sense… you cannot run that" → removed.
- "drop theta… θ+L by construction = 1" → removed.
- Forward-fill → "I would just do a moving average" → interpolation.
- Event study: keep LUNA as motivation; SVB is confounded, "you cannot use this".
- "Show the estimating equation" on every result.
- "β₄ is the important one. You want that one to be significant."

---

## The equation we now estimate (same for time series and panel)

```
Spread = α + β₁·ΔlnS + β₃·L + β₄·(L × ΔlnS) + controls
```
- **No theta. No B (combined treasury+liquid). Interaction uses L directly.**
- controls = velocity (time series only), VIX, ΔlnN*.
- β₄ on `L_x_dlns` is the coefficient of interest.

---

## Code changes

### build_panel.py  (#2 panel, #3 moving average, #1 drop B/theta combos)
- `load_attestations()` now interpolates **issuer by issuer** on a month-end grid,
  then aggregates with the prof's formula `θ=(T₁+T₂)/(S₁+S₂)`, `L=(cash₁+cash₂)/(S₁+S₂)`.
- Interpolation is selectable via `INTERP_METHOD` (default `"time"`):
  - `time`  — time-weighted linear interpolation (≡ prof's ⅔/⅓ blend)
  - `prof`  — the ⅔/⅓ weighting written out explicitly
  - `rolling` — centred 3-month rolling mean
  - `ffill` — old behaviour (kept only for comparison)
- New output **`data/panel_long.csv`** — one row per (month, issuer), 102 rows.
- Removed `buffer_ratio`, `buf_x_dlns`, `theta_x_dlns`.

### regression.py  (#1 spec, #2 panel, #6 β₄)
- Main spec dropped theta; removed the old "B-spec robustness" block entirely.
- New `run_panel()` runs the issuer-month panel (N=102), SE clustered by month.
- `coefficients.csv` now reports **both** time series and panel.

---

## New results (interpolation = time, the default)

### Time series (aggregate, N = 51)
| coef | value | p | sig |
|---|---|---|---|
| β₁ (ΔlnS) | +2.74 | 0.228 | ns |
| β₃ (L) | +8.09 | <0.001 | *** |
| **β₄ (L×ΔlnS)** | **−35.89** | **0.032** | ** |
| R² | 0.858 | | |

### Panel (issuer-month, N = 102)
| coef | value | p | sig |
|---|---|---|---|
| β₁ (ΔlnS) | +0.01 | 0.988 | ns |
| β₃ (L) | +3.85 | <0.001 | *** |
| β₄ (L×ΔlnS) | −7.45 | 0.293 | ns |

### Threshold (Hansen, on interpolated L)
- q* = **0.0664** (was 0.1301), bootstrap p = 0.208, 90% CI [0.066, 0.190].

### Granger (ΔlnS → Spread): lag-3 F p = 0.028 *

---

## ⚠️ Open issues the team must decide (NOT decided yet)

1. **β₄ sign flipped vs. the old story.** Old paper hypothesised β₄ > 0 ("buffer
   dampens transmission"). Actual estimate is **β₄ < 0** and significant in the time
   series. The economic interpretation of the negative sign is **not yet settled** —
   needs discussion (and ideally the prof's read).

2. **β₄ significant in time series (p=0.032) but NOT in panel (p=0.293).** Both are
   reported. The prof asked for the panel; the panel halves the per-issuer signal and
   β₄ loses significance. Which is the headline result is a team call.

3. **β₁ is now positive and insignificant** (was −7.57***). Dropping theta/B changed
   this. The "privilege amplification via β₁" framing needs rewriting.

4. **q* moved 13% → 6.6%.** Driven by the new interpolation. Any "13% reserve floor"
   policy claim in the paper/slides must be updated.

## Interpolation sensitivity (why "time" is the default)

| method | β₄ (time series) | p | β₄ (panel) | p |
|---|---|---|---|---|
| time | −35.89 | **0.032** | −7.45 | 0.293 |
| prof (⅔/⅓) | −35.89 | **0.032** | −7.45 | 0.293 |
| rolling | +5.25 | 0.873 | −1.91 | 0.858 |
| ffill (old) | −26.26 | 0.563 | −2.87 | 0.440 |

`time` and `prof` are mathematically identical. The prof's "moving average" advice is
what makes β₄ significant; the old forward-fill left it insignificant.

---

## ⚠️⚠️ DEEPER PROBLEM FOUND — the level regression is likely SPURIOUS

While investigating *why the signs are opposite to the paper's predictions*, we ran a
full diagnostic. The conclusion is serious and the team must see it.

### The slide-5 equation, run exactly as written (θ + L + L×ΔlnS + full controls):
| coef | predicted (slide 5) | actual (time series) | match? |
|---|---|---|---|
| β₁ ΔlnS | < 0 | **+4.11** (p=0.066) | ❌ opposite |
| β₂ θ | > 0 | **−1.10** (p=0.011) | ❌ opposite |
| β₄ L×ΔlnS | > 0 | **−44.39** (p=0.011) | ❌ opposite |

All three predicted signs are wrong. R²=0.88 — but that is the red flag, not reassurance.

### Why: the regression is spurious (trends, not causation)
1. **Non-stationarity (ADF unit-root test):** spread (p=0.49), liq_buffer (p=0.90),
   theta (p=0.46) are all NON-stationary. Only dln_supply is stationary.
2. **No cointegration (Engle-Granger):** spread~L p=0.120, spread~θ p=0.733,
   spread~ΔlnS p=0.139 — none cointegrate. Non-stationary + not cointegrated =
   textbook spurious regression.
3. **β₁ was negative until L entered.** Building up one variable at a time:
   `dln_supply` alone → β₁=−7.45***; add VIX/ΔlnN* → −5.31***; **add liq_buffer → −2.03 (ns);
   add theta+velocity → +4.11**. L (which is 0.89-correlated with spread by trend) flips it.
4. **Common driver = Fed funds.** corr(spread, fedfunds)=−0.48, corr(L, fedfunds)=−0.57.
   The 2022 hiking cycle moves spread AND reserve composition together.
5. **First-differencing kills it.** Δspread = β₁ΔlnS + ...: β₁=−0.06 (p=0.97),
   β₄=+5.36 (p=0.68) — both vanish. Only **ΔL survives (β₃=+9.5, p<0.001)**.

### What this means
- The paper's two headline claims — **β₁ (privilege amplification)** and
  **β₄ (threshold/fragility)** — are significant only in levels, do not cointegrate,
  and disappear under first-differencing. They are likely **spurious**.
- The one robust relationship is **β₃: higher L ↔ higher spread** (survives levels and
  differencing). But its sign/story does not match the original "buffer absorbs shocks"
  narrative — more likely both L and spread react to the same macro regime (rates/crises).
- The 6/9 deck's β₁=−7.57 (B-spec) was probably exploiting the same spurious trend
  correlation. This may be part of what the prof meant by "that regression makes no sense."

### Diagnostic spread snapshot (shows the shared downtrend)
```
spread:     2022=+0.85 → 2023=+0.21 → 2024=−0.30 → 2025=−0.29  (falling)
liq_buffer: 2022= 0.19 → ........................ → 2025= 0.06  (falling)
```
Two series falling together → high correlation by trend, not by mechanism.

### Options for the team (NOT decided)
1. Make first-difference the main spec (kills spurious; but β₁/β₄ then weak/insignificant).
2. Lean on the event study / daily data (less non-stationary) — but prof criticised it too.
3. Report this honestly: "level results carry spurious risk; only β₃(L) is robust."
4. Rethink whether the spread (even DGS3MO−SOFR) is the right stationary-enough DV.

This is a research-level problem, not a coding bug. It should be raised with the prof —
he will almost certainly ask about stationarity/cointegration, so flagging it first is
the stronger position.

---

## Still TODO (paper/slides — STEP 5, not done yet)
- Sync write_paper.py / make_slides.py to these numbers.
- Put the estimating equation on every result (#5).
- Demote the event study to motivation; drop/flag SVB (#4).
- Reframe around β₄ (#6); fix the β₄-sign interpretation once the team agrees.
