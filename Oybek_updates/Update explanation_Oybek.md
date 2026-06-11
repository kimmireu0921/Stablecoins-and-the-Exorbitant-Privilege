# Update Explanation — Oybek
**Date:** 12 June 2026
**For:** Mireu (Mimi), Sara — please read before we next meet
**Audience note:** written so it's followable even if you're newer to the econometrics.

---

## 0. How to read this & where the files are

I did **not** touch the main project. Everything I added lives in **one subfolder**:

```
Stablecoins-…-Fragility/
├── (the main project = MIMI'S LAST VERSION, unchanged) ────────────────┐
│                                                                        │  ← outside the
│   regression.py, threshold.py, bidcover_mechanism_validation.py …      │     subfolder is
│   results/, data/, 20260610_re/ …  (exactly as Mimi committed)         │     still Mimi's
│                                                                        │     last version
└── Oybek_updates/   ← EVERYTHING I DID IS IN HERE ──────────────────────┘
    ├── Update explanation_Oybek.html        ← this file (browser version)
    ├── Update explanation_Oybek.md          ← this file (markdown)
    ├── My_updated_version/                  ← full runnable copy WITH my additions
    └── README.md                            ← short folder guide + one honesty note (read it)
```

So: **outside `Oybek_updates/` = Mimi's last version. Inside `Oybek_updates/My_updated_version/` = the same project plus my work.** Mimi's version isn't duplicated inside this folder — it's the main project itself (and git commit `d34f0cc`), so you can diff `My_updated_version/` against the project root.

The deck is at `Oybek_updates/My_updated_version/presentations/FINAL_Stablecoin_Reassessment.pptx`.

> ⚠️ One honesty note (full detail in `README.md`): a small untracked work-in-progress file
> (`bidcover_auction_level.py`) already existed in the folder and was overwritten before it was
> read. It was never in git, so the original isn't recoverable here — check Time Machine / cloud
> sync / a teammate's copy if you had a version of it. Everything else is additive.

---

## 1. Where we were — Mimi's update (and what she got RIGHT)

Mimi's revision (commit *"Research Methodology Update"*) was a big, correct step forward. Credit
where it's due — she found the things that actually mattered:

- **She caught that the levels regression is spurious.** She ran the proper diagnostics
  (ADF unit-root tests, Engle–Granger and Johansen cointegration) and correctly concluded that
  `spread` and `L` (the liquid buffer) just trend together during the Fed hiking cycle — they
  are not causally linked. Right call.
- **She caught the Johansen artifact** (a stationary variable, ΔlnS, had been wrongly included
  in the cointegration test, faking a result). Right call.
- **She correctly flagged β₄ as meaningless** — it changes sign when you go from levels to
  first-differences. Right call.
- **Her conclusion:** demote β₁ (privilege amplification) and the 13% threshold; **lead the
  paper with the bid-cover result**, which she described as *"the paper's cleanest causal
  evidence… placebo-validated… significant at all 4 maturities."*

Her diagnosis was sound. The problem is **where she stopped.**

---

## 2. The core problem in Mimi's approach — a double standard

Here is the single most important point in this document.

Mimi applied **full rigor** to the regression that *failed* (stationarity → cointegration →
first-differencing → "it's spurious, drop it"). But she applied **almost no rigor** to the one
result she chose to *promote* — the bid-cover regression. The bid-cover model she elevated still:

1. uses the **same interpolated reserve data** (θ and L) as control variables — the very data she
   flagged as the problem everywhere else;
2. **collapses ~1,094 individual T-bill auctions into just 51 monthly averages**, throwing away
   almost all the data; and
3. **never controls for the auction's offering size** — which is the single most mechanical
   driver of a bid-cover ratio (bigger auction → lower bid-cover, automatically).

The only test she ran on it was a **time-shuffle placebo**. That placebo answers *"is this
coefficient different from random time-ordering?"* It does **not** answer *"does this coefficient
survive proper controls, or is it an artifact of the interpolated regressors and the missing
auction-size control?"* Omitted-variable problems are **invisible** to a time-shuffle placebo.

So "placebo-validated → not spurious" was an **over-claim**. The placebo never tested the thing
that actually breaks the result. **My job was simply to finish applying her own standard to the
result she kept.**

A second, related inconsistency: her own pre-auction-window test (Step 4) was the *cleaner*
design, and it **failed** ("noisier… only 13-week shows the right sign"). She read that as "use
the looser monthly design instead." But the cleaner design failing is **evidence against the
channel**, not a reason to prefer the messier design that gives the wanted answer.

---

## 3. What I did — two purpose-built rebuilds

### 3a. Bid-cover, done at the auction level — `bidcover_auction_level.py`

**The fix:** instead of 51 monthly averages, run the regression on each **individual auction**
(N = 1,094), and add the controls that were missing.

Estimating equation:
```
bid_cover(auction) = α + β_USDT·ΔlnS^USDT_pre + β_USDC·ΔlnS^USDC_pre
                       + γ·ln(offering size) + maturity fixed effects + δ·VIX + θ·time-trend + ε
```
- `ΔlnS_pre` = each issuer's supply growth in the **21 days before** the auction (strictly
  before — no "look-ahead", which the monthly design had).
- Standard errors clustered by month.
- Plus a **falsification test**: *future* supply growth should NOT predict the auction. If it
  does, the relationship is a shared trend, not a real pre-auction → outcome effect.
- Plus subsample checks (drop the 2022 crisis year; post-2023 only).

### 3b. Event study, rebuilt — `event_study_multi.py`

Per Prof. Hur's feedback:
- **Dropped SVB** — it's confounded (it hit Treasuries through the *banking* channel, not just
  the USDC depeg, so you can't isolate the stablecoin effect).
- **Kept LUNA** as the anchor and **added more crypto-native crises**: Celsius, FTX, BUSD.
- **Selection rule (our defense for "why these and not SVB"):** crypto-native stress with **no
  simultaneous banking/macro shock** to Treasuries.
- Fixed the statistics: first-difference normal model (removes the Fed trend), proper
  estimation-window standard errors, and a **cross-event test** that treats each event as one
  observation (robust to day-to-day autocorrelation).

> Note: dropping SVB removes the only "high-buffer" event, so the old "low vs high buffer"
> comparison no longer works. The event study is therefore reframed as a **pooled test of
> whether crypto-native stress moves the spread at all** — which is the "motivation only" role
> Prof. Hur assigned it.

---

## 4. Why the results changed — the numbers

### 4a. Bid-cover: the headline does **not** survive

**(i) At the auction level, with offering controlled, the USDT effect is gone:**

| Spec (pooled, N=1,094) | β_USDT | p | β_USDC | p |
|---|---:|---:|---:|---:|
| (1) supply only | +0.31 | 0.50 | +1.42 | 0.000 |
| (2) + offering size | +0.11 | 0.83 | +1.09 | 0.000 |
| (3) + maturity FE | +0.11 | 0.83 | +1.09 | 0.000 |
| (4) + VIX | −0.05 | 0.90 | +1.10 | 0.000 |
| (5) + time trend | +0.32 | 0.50 | +1.28 | 0.000 |

β_USDT is **null from the very first spec** — so this is not me "over-controlling" it to death.
And the only coefficient that *is* significant, β_USDC, is **positive** (the opposite of a T-bill
demand story) — and my **falsification test fails it**: *future* USDC growth also "predicts"
bid-cover (p<0.001). A relationship that runs both forwards and backwards in time is a trend, not
causation.

**(ii) Why Mimi's monthly version looked significant — it was the interpolated controls.**
Re-running her monthly design two ways, changing nothing but the control set:

| Maturity | Mimi's spec (8 controls incl. interpolated θ, L) | Clean controls (supply + VIX only) |
|---|---|---|
| 4-Week | β_USDT = −1.14 ** (p=0.012) | β_USDT = −0.26 (p=0.628) |
| 8-Week | β_USDT = −1.54 ** (p=0.016) | β_USDT = −0.91 (p=0.110) |
| 13-Week | β_USDT = −1.47 *** (p=0.000) | β_USDT = −0.80 * (p=0.094) |
| 26-Week | β_USDT = −1.68 *** (p=0.000) | β_USDT = −0.82 * (p=0.065) |

Strip the interpolated reserve controls — the data we already agreed is manufactured — and the
significance **collapses to marginal-or-nothing**. The result was leaning on those controls the
whole time. (The only place the predicted negative sign survives is the drop-2022 subsample,
β=−1.06, p=0.024 — one isolated, fragile result.)

### 4b. Event study: no systematic effect (motivation only)

| Event | CAR[0,+20] (bps) | Significant? |
|---|---:|---|
| LUNA / UST | −4.1 | no |
| Celsius | +0.3 | no |
| FTX | −27.6 | no |
| BUSD | +5.2 | no |
| **Pooled (all 4)** | **−6.6** | **no (p=0.43)** |

The events **disagree in sign** (FTX strongly negative, others positive/flat). There is no clean,
systematic spread response to crypto crises. Useful as narrative motivation — not as evidence.

---

## 5. Why this happened (the root cause, briefly)

Both Mimi and I keep running into the **same underlying problem: the reserve data (θ, L) is
largely manufactured.**

- Tether reports its T-bill holdings **quarterly**, so ~2 out of every 3 monthly data points are
  **straight-line interpolation** between two quarterly numbers.
- 2020 figures are literally labelled *"pre-attestation estimate, extrapolated"*; some 2021
  treasury figures are failed web-scrapes (≈0) that get interpolated over.
- **The interpolation method changes the answer:** β₄ is significant under one fill method
  (p=0.03) and insignificant under others (p=0.56–0.87). When a headline number depends on how
  you fill the *missing* data, it's describing the fill, not Tether.

This is why everything built on θ/L-levels keeps dissolving under scrutiny — the regression, the
13% threshold, and (now) the bid-cover result that depended on θ/L as controls.

---

## 6. What survives — the honest, defensible core

| What | Status |
|---|---|
| USDT is one of the largest **structural holders** of US T-bills | **Fact** (from attestations). The privilege *mechanism* exists by construction. |
| β₃ — liquid buffer correlates with the spread | **Survives** levels + first-differencing. But likely macro co-movement, report carefully. |
| Short-run USDT → spread (daily VAR, in differences) | **Weak** — day-1 effect, reverses by day 3, ~1.3% of variance. Suggestive only. |
| β₁ (privilege amplification), the 13% threshold, LSTAR | **Spurious** — drop from main claims. |
| **Bid-cover USDT suppression** | **Does not survive** auction-level + offering control. Demote. |
| Event study | **Motivation only** — no systematic effect. |

**The reframe I'd recommend:** lead with the *structural* fact (stablecoins are now programmatic
T-bill buyers — the privilege channel is real by construction), then present the **honest finding**
that its month-to-month causal footprint is small and swamped by the Fed cycle and our data
limits. Show the rigor — *"we stress-tested our own headline results and report what fails."*
This pre-empts every objection Prof. Hur can raise. **Owning the limitation is a stronger
position than defending a result he could dismantle with two questions** ("did you control for
auction size?" / "does it hold without the interpolated controls?").

---

## 7. What I'd suggest we do next (team decision)

1. **Agree on the reframe** in §6 — structural fact + honest null + β₃ as the one surviving
   correlation.
2. **Decide whether to lead with bid-cover.** My strong recommendation: no — it doesn't survive.
   If we still want to mention it, report it transparently as "did not survive auction-level
   robustness."
3. **Sync the paper & slides.** `write_paper.py` and `make_slides.py` still contain the old
   hardcoded numbers (β₁=−7.57, q*=13%). These need updating to the honest version.
4. **Raise the data-quality limit openly** with Prof. Hur — quarterly interpolation is a real
   constraint, and flagging it first is the stronger move.

Everything here is reproducible: the scripts are in `Oybek_updates/My_updated_version/`
(`bidcover_auction_level.py`, `event_study_multi.py`, `make_final_slides.py`), with full result
tables and figures in that copy's `results/` folder.

— Oybek
