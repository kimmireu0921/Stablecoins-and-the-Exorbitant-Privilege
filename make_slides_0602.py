"""
make_slides_0602.py — June 2026 update deck with graphs embedded.

Slides:
  1.  Title
  2.  Roadmap
  3.  CAR Correction (text + fig_timeseries.png showing the Fed-hiking contamination)
  4.  Before vs After — CAR Comparison (car_comparison.png, 2×3 grid)
  5.  Corrected Event Study (event_study_cars.png + per-event annotations)
  6.  Placebo Test — table + summary
  7.  Placebo Test — graph (placebo_cars.png)
  8.  What the Paper Proves (threshold_ssr.png + before/after comparison)
  9.  Thank You

Saves to: presentations/0602_Stablecoin_Exorbitant_Privilege.pptx
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pathlib import Path

RESULTS       = Path("results")
PRESENTATIONS = Path("presentations")
PRESENTATIONS.mkdir(exist_ok=True)

# ── Colours ───────────────────────────────────────────────────────────────────
DARK_NAVY  = RGBColor(0x0A, 0x1E, 0x5C)
MED_NAVY   = RGBColor(0x14, 0x30, 0x70)
HDR_NAVY   = RGBColor(0x1B, 0x3A, 0x72)
WHITE      = RGBColor(0xFF, 0xFF, 0xFF)
ORANGE     = RGBColor(0xD4, 0x63, 0x2A)
BODY_DARK  = RGBColor(0x1A, 0x1A, 0x2E)
LGRAY      = RGBColor(0xF0, 0xF4, 0xF8)
MIDGRAY    = RGBColor(0x55, 0x55, 0x66)
GREEN      = RGBColor(0x1A, 0x7A, 0x4A)
RED        = RGBColor(0xC0, 0x39, 0x2B)
LIGHT_RED  = RGBColor(0xFC, 0xEB, 0xE8)
LIGHT_GRN  = RGBColor(0xE6, 0xF4, 0xEA)
GOLD       = RGBColor(0xFF, 0xD7, 0x00)
AMBER      = RGBColor(0xE6, 0x7E, 0x22)

SW = Inches(13.33)
SH = Inches(7.5)


# ── Helpers ───────────────────────────────────────────────────────────────────

def blank(prs):
    return prs.slides.add_slide(prs.slide_layouts[6])


def box(sld, l, t, w, h, fill=None, line_color=None, line_width=Pt(0)):
    sh = sld.shapes.add_shape(1, l, t, w, h)
    sh.line.fill.background()
    if fill:
        sh.fill.solid()
        sh.fill.fore_color.rgb = fill
    else:
        sh.fill.background()
    if line_color:
        sh.line.color.rgb = line_color
        sh.line.width = line_width
    return sh


def txt(sld, text, l, t, w, h, size=18, bold=False, italic=False,
        color=BODY_DARK, align=PP_ALIGN.LEFT, font="Calibri", wrap=True):
    tb = sld.shapes.add_textbox(l, t, w, h)
    tb.word_wrap = wrap
    tf = tb.text_frame
    tf.word_wrap = wrap
    p = tf.paragraphs[0]
    p.alignment = align
    r = p.add_run()
    r.text = text
    r.font.name = font
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.italic = italic
    r.font.color.rgb = color
    return tb


def add_line(tf, text, size=18, bold=False, italic=False,
             color=BODY_DARK, align=PP_ALIGN.LEFT, space_before=4):
    p = tf.add_paragraph()
    p.alignment = align
    p.space_before = Pt(space_before)
    r = p.add_run()
    r.text = text
    r.font.name = "Calibri"
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.italic = italic
    r.font.color.rgb = color
    return p


def img(sld, path, l, t, w, h=None):
    p = Path(path)
    if p.exists():
        if h:
            sld.shapes.add_picture(str(p), l, t, w, h)
        else:
            sld.shapes.add_picture(str(p), l, t, w)
    else:
        # Placeholder box if image missing
        box(sld, l, t, w, h or Inches(2), fill=LGRAY, line_color=MIDGRAY, line_width=Pt(1))
        txt(sld, f"[image not found:\n{p.name}]", l + Inches(0.1), t + Inches(0.1),
            w - Inches(0.2), (h or Inches(2)) - Inches(0.2),
            size=11, italic=True, color=MIDGRAY)


def title_slide_bg(sld):
    box(sld, 0, 0, SW, SH, fill=DARK_NAVY)
    box(sld, 0, Inches(2.85), SW, Inches(1.15), fill=MED_NAVY)
    for shape_args in [
        (9, Inches(0.1),  Inches(0.0),  Inches(3.8), Inches(3.8), WHITE,     DARK_NAVY),
        (9, Inches(0.55), Inches(0.45), Inches(2.9), Inches(2.9), DARK_NAVY, None),
        (9, Inches(0.1),  Inches(4.4),  Inches(3.6), Inches(3.6), WHITE,     DARK_NAVY),
        (9, Inches(0.65), Inches(4.85), Inches(2.5), Inches(2.5), DARK_NAVY, None),
    ]:
        shape_type, sl, st, sw, sh_, fill_col, _ = shape_args
        sh = sld.shapes.add_shape(shape_type, sl, st, sw, sh_)
        sh.fill.solid(); sh.fill.fore_color.rgb = fill_col; sh.line.fill.background()
    box(sld, 0, Inches(2.55), Inches(3.8), Inches(0.6), fill=MIDGRAY)


def content_slide(prs, title_text):
    sld = blank(prs)
    box(sld, 0, 0, SW, SH, fill=WHITE)
    box(sld, 0, 0, SW, Inches(0.95), fill=HDR_NAVY)
    txt(sld, title_text,
        Inches(0.3), Inches(0.1), Inches(11.5), Inches(0.78),
        size=26, color=WHITE, align=PP_ALIGN.LEFT, font="Calibri")
    return sld


def slide_number(sld, num):
    txt(sld, str(num),
        SW - Inches(0.55), SH - Inches(0.42), Inches(0.45), Inches(0.35),
        size=13, color=MIDGRAY, align=PP_ALIGN.RIGHT)


def orange_callout(sld, text, t=None, size=15):
    if t is None:
        t = SH - Inches(1.22)
    box(sld, 0, t, SW, Inches(1.05), fill=ORANGE)
    txt(sld, text,
        Inches(0.6), t + Inches(0.12), SW - Inches(1.0), Inches(0.82),
        size=size, bold=True, color=WHITE, align=PP_ALIGN.CENTER)


def bullet_tb(sld, l, t, w, h):
    tb = sld.shapes.add_textbox(l, t, w, h)
    tb.word_wrap = True
    tf = tb.text_frame
    tf.word_wrap = True
    tf.paragraphs[0].space_before = Pt(0)
    return tf


def notes(sld, script: str):
    sld.notes_slide.notes_text_frame.text = script


# ── Build ─────────────────────────────────────────────────────────────────────
prs = Presentation()
prs.slide_width  = SW
prs.slide_height = SH


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 1 — Title
# ═══════════════════════════════════════════════════════════════════════════════
sld = blank(prs)
title_slide_bg(sld)
txt(sld, "STABLECOINS AND THE EXORBITANT PRIVILEGE",
    Inches(4.0), Inches(2.65), Inches(9.0), Inches(0.65),
    size=22, color=WHITE, align=PP_ALIGN.LEFT, font="Calibri Light")
txt(sld, "Corrected Event Study  ·  Placebo Test  ·  What the Paper Proves",
    Inches(4.0), Inches(3.3), Inches(9.0), Inches(0.5),
    size=13, italic=True, color=RGBColor(0xAA, 0xC4, 0xE8), align=PP_ALIGN.LEFT)
box(sld, Inches(3.9), Inches(4.45), Inches(7.5), Inches(2.8), fill=RGBColor(0x0E, 0x26, 0x68))
txt(sld,
    "Yonsei GSIS 2026-1  |  Topics in International Finance\n"
    "Mireu Kim · Sara Chekroune · Oybek Ibragimov\n"
    "June 2026",
    Inches(4.1), Inches(4.6), Inches(7.2), Inches(2.5),
    size=16, color=WHITE, align=PP_ALIGN.LEFT)
notes(sld,
    "Good afternoon. Following last week's feedback that our event study CARs were "
    "ridiculously large, we investigated the root cause, corrected the methodology, "
    "ran the placebo test, and want to be clear about what our paper actually proves. "
    "Today's deck covers exactly those four things.")


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 2 — Roadmap
# ═══════════════════════════════════════════════════════════════════════════════
sld = content_slide(prs, "What We Are Covering Today")
slide_number(sld, 2)

items = [
    (RED,     "CAR Correction",
     "Our original event study CARs (+8.9/−18 pp) were inflated by a model specification error. "
     "We show the time series that explains what went wrong, and present the corrected numbers."),
    (MIDGRAY, "Corrected Event Study",
     "With the first-difference model, all three event CARs are near zero and insignificant. "
     "We show the actual CAR paths and explain what this means economically."),
    (HDR_NAVY,"Placebo Test",
     "We ran the same methodology on 3 non-crisis dates. Placebos and actual events are "
     "statistically indistinguishable — confirming the event study finds no quantitative effect."),
    (GREEN,   "What the Paper Proves",
     "The primary evidence is the regression (β₁ = −6.02 bps) and the Hansen threshold (q* = 13%). "
     "We show the threshold graph and explain in plain terms what 'reframing' means."),
]
for i, (col, title, body) in enumerate(items):
    t = Inches(1.15) + i * Inches(1.38)
    box(sld, Inches(0.35), t, Inches(0.65), Inches(1.25), fill=col)
    txt(sld, str(i + 1), Inches(0.35), t + Inches(0.32),
        Inches(0.65), Inches(0.5), size=26, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    box(sld, Inches(1.05), t, Inches(11.9), Inches(1.25), fill=LGRAY if i % 2 == 0 else WHITE)
    txt(sld, title, Inches(1.2), t + Inches(0.1),
        Inches(11.6), Inches(0.35), size=15, bold=True, color=col)
    txt(sld, body,  Inches(1.2), t + Inches(0.48),
        Inches(11.6), Inches(0.65), size=13, color=BODY_DARK)

notes(sld,
    "Today's deck has four parts. "
    "First, the CAR correction — what went wrong with our original numbers, illustrated with the time series. "
    "Second, the corrected event study results and the actual CAR graphs. "
    "Third, the placebo test with the corrected model. "
    "Fourth, what the paper actually proves — we'll use the Hansen threshold graph and explain reframing "
    "in plain terms. Let's begin.")


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 3 — CAR Correction (text + time series graph)
# ═══════════════════════════════════════════════════════════════════════════════
sld = content_slide(prs, "CAR Correction — What Was Wrong and What We Fixed")
slide_number(sld, 3)

# Alert strip
box(sld, Inches(0.35), Inches(1.05), Inches(12.6), Inches(0.38), fill=RED)
txt(sld,
    "Professor's feedback: 'Your percentage points are ridiculously large. Either something wrong, or wrong units.'  — He was right.",
    Inches(0.5), Inches(1.09), Inches(12.1), Inches(0.28),
    size=11, bold=True, italic=True, color=WHITE, align=PP_ALIGN.CENTER)

# Three columns — old | cause | new (compact height)
COL_H = Inches(1.85)
COL_T = Inches(1.52)

# Old numbers
box(sld, Inches(0.35), COL_T, Inches(3.55), Inches(0.33), fill=RED)
txt(sld, "Original  (level model)",
    Inches(0.45), COL_T + Inches(0.04), Inches(3.4), Inches(0.25),
    size=11, bold=True, color=WHITE)
box(sld, Inches(0.35), COL_T + Inches(0.33), Inches(3.55), COL_H - Inches(0.33), fill=LIGHT_RED)
tf = bullet_tb(sld, Inches(0.45), COL_T + Inches(0.38), Inches(3.35), COL_H - Inches(0.45))
for label, val, col in [
    ("LUNA  (May 2022):",  "+8.91 pp  ***", RED),
    ("USDT  (May 2022):",  "+8.85 pp  ***", RED),
    ("SVB   (Mar 2023):", "−18.01 pp  ***", GREEN),
]:
    add_line(tf, label, size=10, color=BODY_DARK, space_before=4)
    add_line(tf, f"        {val}", size=13, bold=True, color=col, space_before=1)

# Root cause
box(sld, Inches(4.05), COL_T, Inches(5.2), Inches(0.33), fill=AMBER)
txt(sld, "Root cause — Fed hiking trend in estimation window",
    Inches(4.15), COL_T + Inches(0.04), Inches(5.05), Inches(0.25),
    size=11, bold=True, color=WHITE)
box(sld, Inches(4.05), COL_T + Inches(0.33), Inches(5.2), COL_H - Inches(0.33),
    fill=RGBColor(0xFF, 0xF5, 0xEA))
tf2 = bullet_tb(sld, Inches(4.15), COL_T + Inches(0.38), Inches(5.0), COL_H - Inches(0.45))
add_line(tf2, "Estimation window for 2022 events: Jan–May 2022", size=11, bold=True, color=BODY_DARK, space_before=2)
add_line(tf2, "Spread in that window: 5 bps → 78 bps (Fed hiking!)", size=11, color=AMBER, bold=True, space_before=4)
add_line(tf2, "Model baseline: 37 bps avg  |  Events happened at: 71 bps", size=11, color=BODY_DARK, space_before=4)
add_line(tf2, "→ 34 bps/day fake 'abnormal' × 26 days = 8.84 pp", size=12, bold=True, color=RED, space_before=5)
add_line(tf2, "Net actual spread change during LUNA event: −0.3 bps", size=10, italic=True, color=MIDGRAY, space_before=4)

# Corrected numbers
box(sld, Inches(9.4), COL_T, Inches(3.6), Inches(0.33), fill=GREEN)
txt(sld, "Corrected  (first-diff model)",
    Inches(9.5), COL_T + Inches(0.04), Inches(3.45), Inches(0.25),
    size=11, bold=True, color=WHITE)
box(sld, Inches(9.4), COL_T + Inches(0.33), Inches(3.6), COL_H - Inches(0.33), fill=LIGHT_GRN)
tf3 = bullet_tb(sld, Inches(9.5), COL_T + Inches(0.38), Inches(3.4), COL_H - Inches(0.45))
for label, val in [
    ("LUNA  (May 2022):",  "−0.15 pp  n.s."),
    ("USDT  (May 2022):",  "−0.04 pp  n.s."),
    ("SVB   (Mar 2023):",  "−0.02 pp  n.s."),
]:
    add_line(tf3, label, size=10, color=BODY_DARK, space_before=4)
    add_line(tf3, f"        {val}", size=13, bold=True, color=MIDGRAY, space_before=1)
add_line(tf3, " ", size=4, space_before=2)
add_line(tf3, "All near zero. All insignificant.", size=11, bold=True, color=BODY_DARK, space_before=2)

# Time series graph — takes up the bottom half of the slide
# Caption strip above the graph
box(sld, Inches(0.35), Inches(3.47), Inches(12.6), Inches(0.3), fill=HDR_NAVY)
txt(sld,
    "Why the model failed: the spread (Panel A) rose from ~0 bps to ~80 bps during our estimation window — "
    "all Fed policy, not stablecoins. The buffer fell below 13% (Panel C shading) right at the 2022 events.",
    Inches(0.5), Inches(3.49), Inches(12.1), Inches(0.25),
    size=10, italic=True, color=WHITE)

img(sld, RESULTS / "fig_timeseries.png",
    Inches(0.35), Inches(3.77), Inches(12.6), Inches(2.6))

notes(sld,
    "This is the most important slide today. The professor told us our percentage points were ridiculously large, "
    "and after investigating, he was correct. Let me explain exactly what happened. "
    "Our original model used the LEVEL of the spread. We estimated a normal baseline using data from "
    "January through May 2022 — which is visible in Panel A of the graph as the steep rising section. "
    "The Fed was raising rates faster than at any point in 40 years. "
    "The spread rose from 5 basis points in January to 78 basis points by May — "
    "entirely because of the Fed, not because of stablecoins. "
    "The model's six-month average baseline was 37 basis points. "
    "But the events happened when the spread was already at 71 basis points. "
    "So every single day, the model computed: actual 71 bps minus expected 37 bps equals 34 bps abnormal. "
    "Over 26 trading days: 34 times 26 equals 884 basis points or 8.84 percentage points. "
    "The spread did not actually move during the event window — the net change was negative 0.3 basis points. "
    "Panel C in the graph shows the liquid buffer falling below the 13 percent threshold — the shaded region — "
    "which is exactly when these events happened. "
    "We fixed this by switching to a first-difference model: we model the day-over-day CHANGE in spread, "
    "not the level. Stock event studies already do this for the same reason. "
    "The Fed hiking trend disappears when you take daily differences, leaving only idiosyncratic movements.")


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 4 — Before vs After CAR Comparison
# ═══════════════════════════════════════════════════════════════════════════════
sld = content_slide(prs, "Before vs After — CAR Paths: Original vs Corrected Model")
slide_number(sld, 4)

# Label strip
box(sld, Inches(0.35), Inches(1.05), Inches(12.6), Inches(0.35), fill=LGRAY)
txt(sld,
    "Top row (red, solid) = ORIGINAL level model   |   "
    "Bottom row (teal, dashed) = CORRECTED first-diff model   |   "
    "Columns: LUNA/UST · USDT Depeg · USDC/SVB",
    Inches(0.5), Inches(1.08), Inches(12.1), Inches(0.28),
    size=11, italic=True, color=HDR_NAVY)

# Comparison graph — nearly full slide
img(sld, RESULTS / "car_comparison.png",
    Inches(0.35), Inches(1.47), Inches(12.6), Inches(4.95))

# Two callout boxes at bottom left and right
box(sld, Inches(0.35), Inches(6.5), Inches(6.1), Inches(0.38), fill=LIGHT_RED)
txt(sld,
    "Original (level model):  LUNA +8.91 pp***  ·  USDT +8.85 pp***  ·  SVB −18.01 pp***",
    Inches(0.5), Inches(6.54), Inches(5.8), Inches(0.28),
    size=11, bold=True, color=RED)
box(sld, Inches(6.6), Inches(6.5), Inches(6.35), Inches(0.38), fill=LIGHT_GRN)
txt(sld,
    "Corrected (first-diff model):  LUNA −0.15 pp n.s.  ·  USDT −0.04 pp n.s.  ·  SVB −0.02 pp n.s.",
    Inches(6.75), Inches(6.54), Inches(6.0), Inches(0.28),
    size=11, bold=True, color=GREEN)

orange_callout(sld,
    "The top row spikes were not stablecoin effects — they were the Fed hiking trend. "
    "The corrected bottom row shows the true market response: near zero.",
    size=13)

notes(sld,
    "This is the direct visual comparison between the original and corrected models. "
    "The top row shows what our original event study produced: "
    "positive 8.9 pp for LUNA, positive 8.85 pp for USDT, and negative 18 pp for SVB. "
    "Every graph shows a clear dramatic trend — either up or down. "
    "The bottom row shows the corrected first-difference model: "
    "all three events produce CARs within a few hundredths of a percentage point from zero. "
    "The contrast is stark. The top row looked like strong evidence. The bottom row is the honest result. "
    "The key insight is that the top row's dramatic trend was the Fed raising rates — "
    "not the stablecoin events themselves. "
    "Once we remove the trend by modelling daily changes instead of levels, "
    "the stablecoin-specific effect on the Treasury spread is indistinguishable from zero.")


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 5 — Corrected Event Study (CAR graph is the main content)
# ═══════════════════════════════════════════════════════════════════════════════
sld = content_slide(prs, "Corrected Event Study — CAR Paths (First-Difference Model)")
slide_number(sld, 5)

# Model spec strip
box(sld, Inches(0.35), Inches(1.05), Inches(12.6), Inches(0.35), fill=LGRAY)
txt(sld,
    "Model:  ΔSpread_t = α + β₁·ΔVIX_t + β₂·Δln(equity)_t     "
    "Estimation window: −120 to −6 trading days     Event window: −5 to +20 trading days",
    Inches(0.5), Inches(1.08), Inches(12.1), Inches(0.28),
    size=11, italic=True, color=HDR_NAVY)

# Graph — left 2/3 of the slide
img(sld, RESULTS / "event_study_cars.png",
    Inches(0.35), Inches(1.48), Inches(8.5), Inches(3.8))

# Annotations — right 1/3
ann_l = Inches(9.0)
ann_w = Inches(4.0)

for i, (name, date, car, sig, hcol, interp) in enumerate([
    ("LUNA/UST Collapse", "May 9, 2022",
     "−0.15 pp  n.s.", "", RED,
     "Spread barely moved (net −0.3 bps). "
     "T-bill selling (Tether) offset by market flight-to-safety buying. "
     "Net effect: indistinguishable from noise."),
    ("USDT Partial Depeg", "May 12, 2022",
     "−0.04 pp  n.s.", "", RED,
     "Same buffer, same period. "
     "$7B in redemptions met via T-bill sales, "
     "but market-wide buying cancelled the effect."),
    ("USDC / SVB Failure", "Mar 11, 2023",
     "−0.02 pp  n.s.", "", GREEN,
     "Govt. guarantee → no T-bill sales. "
     "Sharp transient drop then recovery. "
     "Spread move fully explained by VIX/equity."),
]):
    t = Inches(1.48) + i * Inches(1.28)
    box(sld, ann_l, t, ann_w, Inches(0.28), fill=hcol)
    txt(sld, f"{name}  ({date})",
        ann_l + Inches(0.08), t + Inches(0.03), ann_w - Inches(0.12), Inches(0.22),
        size=10, bold=True, color=WHITE)
    box(sld, ann_l, t + Inches(0.28), ann_w, Inches(0.98), fill=LGRAY if i % 2 == 0 else WHITE)
    txt(sld, f"CAR = {car}", ann_l + Inches(0.1), t + Inches(0.32),
        ann_w - Inches(0.15), Inches(0.3), size=14, bold=True, color=MIDGRAY)
    txt(sld, interp, ann_l + Inches(0.1), t + Inches(0.62),
        ann_w - Inches(0.15), Inches(0.6), size=10, color=BODY_DARK)

# Key reading guide below the graph
box(sld, Inches(0.35), Inches(5.37), Inches(8.5), Inches(0.3), fill=HDR_NAVY)
txt(sld, "How to read these graphs:",
    Inches(0.5), Inches(5.4), Inches(8.2), Inches(0.24),
    size=11, bold=True, color=WHITE)
box(sld, Inches(0.35), Inches(5.67), Inches(8.5), Inches(0.52), fill=LGRAY)
txt(sld,
    "Dashed vertical line = event date (τ = 0).  "
    "Y-axis = cumulative abnormal spread change in pp since 5 days before the event.  "
    "A flat line at zero means the event had no measurable effect on the spread.",
    Inches(0.5), Inches(5.7), Inches(8.2), Inches(0.44),
    size=11, color=BODY_DARK)

# Note about SVB transient
box(sld, Inches(0.35), Inches(6.25), Inches(8.5), Inches(0.52), fill=RGBColor(0xE8, 0xF4, 0xEC))
txt(sld,
    "Note on SVB (right panel): the CAR drops sharply to −0.5 pp around day +5 "
    "(the flight-to-safety spike), then recovers. Final CAR at day +20 is near zero "
    "because the spread normalised as markets calmed. The transient drop is real but "
    "fully explained by the VIX/equity controls.",
    Inches(0.5), Inches(6.28), Inches(8.2), Inches(0.44),
    size=10, italic=True, color=HDR_NAVY)

orange_callout(sld,
    "All three CARs end near zero — not because nothing happened, "
    "but because general market forces (flight to safety, VIX) account for all the spread movement.",
    size=13)

notes(sld,
    "Here are the actual CAR paths from the corrected first-difference model. "
    "All three end near zero at day plus 20. Let me explain what each graph shows. "
    "For LUNA and USDT on the left and centre: the spread was volatile but drifted around zero throughout. "
    "Tether was selling T-bills to meet redemptions, but at the same time the financial panic "
    "caused a general flight to safety — other investors were buying T-bills. "
    "The two forces cancelled. "
    "For SVB on the right: notice the sharp drop to about negative 0.5 pp around day plus 5. "
    "This is the acute flight-to-safety spike — the T-bill spread compressed sharply as "
    "investors rushed out of bank deposits and into T-bills. "
    "But it recovered back to near zero by day plus 20 as markets stabilised. "
    "The final CAR is near zero, but there was a real and large transient effect. "
    "Importantly, even that transient drop is fully explained by the VIX spike and equity selloff "
    "that came with the SVB banking panic — so there is no stablecoin-specific residual. "
    "The key reading: a flat line at zero means no effect. "
    "These graphs show lines that hover near zero, occasionally dipping or rising, "
    "but without the sustained directional trend we would need to call it significant.")


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 6 — Placebo Test: table + summary
# ═══════════════════════════════════════════════════════════════════════════════
sld = content_slide(prs, "Placebo Test — Results Table")
slide_number(sld, 6)

box(sld, Inches(0.35), Inches(1.05), Inches(12.6), Inches(0.38), fill=HDR_NAVY)
txt(sld,
    "Same event study methodology on 3 non-crisis dates with same buffer regimes. "
    "If methodology is sound: placebos near zero, actuals should be larger. "
    "If both are near zero: event study finds no effect.",
    Inches(0.5), Inches(1.09), Inches(12.1), Inches(0.3),
    size=12, italic=True, color=WHITE)

# Table
headers = ["Type", "Date", "Buffer", "CAR (pp)", "t-stat", "Sig.", "Interpretation"]
col_ls  = [Inches(0.35), Inches(1.6),  Inches(4.65), Inches(6.3),
           Inches(7.85), Inches(9.05), Inches(9.98)]
col_ws  = [Inches(1.25), Inches(3.05), Inches(1.65), Inches(1.55),
           Inches(1.2),  Inches(0.93), Inches(3.65)]

for h, l, w in zip(headers, col_ls, col_ws):
    box(sld, l, Inches(1.52), w, Inches(0.34), fill=MED_NAVY)
    txt(sld, h, l + Inches(0.05), Inches(1.55), w - Inches(0.1), Inches(0.26),
        size=11, bold=True, color=WHITE)

rows = [
    ("PLACEBO", "Jun 15, 2021",           "Low",        "+0.01", "0.47",  "n.s.", "Near zero — no event ✓"),
    ("PLACEBO", "Oct 12, 2021",           "Low",        "+0.02", "0.73",  "n.s.", "Near zero — no event ✓"),
    ("PLACEBO", "Jul 15, 2025",           "High",       "−0.11", "−1.80", "*",    "Marginally sig. — likely random"),
    ("ACTUAL",  "May 9, 2022  (LUNA)",    "Low",        "−0.15", "−1.07", "n.s.", "Not different from placebos"),
    ("ACTUAL",  "May 12, 2022  (USDT)",   "Low",        "−0.04", "−0.31", "n.s.", "Not different from placebos"),
    ("ACTUAL",  "Mar 11, 2023  (SVB)",    "High+Gov.",  "−0.02", "−0.04", "n.s.", "Not different from placebos"),
]
for k, (rtype, date, buf, car, tstat, sig, interp) in enumerate(rows):
    bg = LGRAY if k % 2 == 0 else WHITE
    rt = Inches(1.86) + k * Inches(0.63)
    is_act = (rtype == "ACTUAL")
    type_col = RED if is_act else MIDGRAY
    for val, l, w in zip((rtype, date, buf, car, tstat, sig, interp), col_ls, col_ws):
        box(sld, l, rt, w, Inches(0.59), fill=bg)
        vcol = type_col if val == rtype else BODY_DARK
        txt(sld, val, l + Inches(0.05), rt + Inches(0.15),
            w - Inches(0.1), Inches(0.3),
            size=11, bold=(val == rtype), color=vcol)

# Summary comparison boxes
box(sld, Inches(0.35), Inches(5.73), Inches(12.6), Inches(0.32), fill=LGRAY)
txt(sld,
    "Placebo mean |CAR| = 0.05 pp          "
    "Actual mean |CAR| = 0.07 pp          "
    "Ratio = 1.5×          "
    "(original inflated ratio was 21.7×)",
    Inches(0.5), Inches(5.76), Inches(12.1), Inches(0.26),
    size=13, bold=True, color=HDR_NAVY, align=PP_ALIGN.CENTER)

box(sld, Inches(0.35), Inches(6.05), Inches(6.1), Inches(0.5), fill=LIGHT_RED)
txt(sld, "Original (inflated level model):  ratio = 21.7×  — wrong model, inflated CARs",
    Inches(0.5), Inches(6.1), Inches(5.8), Inches(0.38),
    size=11, italic=True, color=RED)
box(sld, Inches(6.6),  Inches(6.05), Inches(6.35), Inches(0.5), fill=LIGHT_GRN)
txt(sld, "Corrected (first-diff model):  ratio = 1.5×  — honest, confirms event study limits",
    Inches(6.75), Inches(6.1), Inches(6.0), Inches(0.38),
    size=11, italic=True, color=GREEN)

orange_callout(sld,
    "Placebos and actuals are statistically indistinguishable → "
    "the event study CANNOT quantitatively identify the buffer channel. "
    "Next slide shows the CAR path comparison.",
    size=13)

notes(sld,
    "This slide shows the placebo test results in table form. "
    "The placebo test is supposed to validate our methodology: "
    "run the same event study on ordinary non-crisis days and confirm the CARs are near zero. "
    "With the original inflated model we got a 21.7 times difference — which looked great but was wrong. "
    "With the corrected first-difference model, the placebo mean absolute CAR is 0.05 pp "
    "and the actual event mean absolute CAR is 0.07 pp — a ratio of only 1.5 times. "
    "They are essentially the same. "
    "This confirms that the event study, with the correct methodology, truly finds no significant effect. "
    "The next slide shows the visual comparison of the CAR paths.")


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 7 — Placebo Test: graph
# ═══════════════════════════════════════════════════════════════════════════════
sld = content_slide(prs, "Placebo Test — CAR Path Comparison")
slide_number(sld, 7)

# Label strips
box(sld, Inches(0.35), Inches(1.05), Inches(12.6), Inches(0.34), fill=LGRAY)
txt(sld,
    "Top row = PLACEBO dates (dashed lines)   |   Bottom row = ACTUAL events (solid lines)   |   "
    "Red = low buffer  ·  Blue = high buffer",
    Inches(0.5), Inches(1.08), Inches(12.1), Inches(0.27),
    size=12, italic=True, color=HDR_NAVY)

# Main graph — full width
img(sld, RESULTS / "placebo_cars.png",
    Inches(0.35), Inches(1.45), Inches(12.6), Inches(4.7))

# Three takeaway labels at the bottom
takeaways = [
    ("Placebos (top row)", MIDGRAY,
     "All near zero — as expected. No event, no effect."),
    ("2022 events (bottom left/centre)", RED,
     "Near zero — same as placebos. Crisis-specific buying offset Tether selling."),
    ("SVB event (bottom right)", GREEN,
     "Sharp transient dip then recovery. Fully explained by banking panic VIX/equity."),
]
for i, (label, col, body) in enumerate(takeaways):
    l = Inches(0.35) + i * Inches(4.3)
    box(sld, l, Inches(6.23), Inches(4.1), Inches(0.26), fill=col)
    txt(sld, label, l + Inches(0.08), Inches(6.25),
        Inches(3.95), Inches(0.2), size=10, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    box(sld, l, Inches(6.49), Inches(4.1), Inches(0.42), fill=LGRAY)
    txt(sld, body, l + Inches(0.08), Inches(6.52),
        Inches(3.95), Inches(0.35), size=10, color=BODY_DARK, align=PP_ALIGN.CENTER)

orange_callout(sld,
    "The placebo PASSES — the corrected methodology finds no effect on either crisis or ordinary days. "
    "The event study is qualitative context only.",
    size=13)

notes(sld,
    "This is the visual comparison. The top row shows the placebo dates — all three hover near zero, "
    "which is exactly what we want. No event happened, no effect is measured. "
    "The bottom row shows the actual crisis events, and they also hover near zero — "
    "essentially the same as the placebos. "
    "The key observation is that you cannot visually distinguish the bottom row from the top row. "
    "For the SVB event in the bottom right, you can see the sharp transient dip to negative 0.5 pp "
    "around day 5, then a recovery. That is the acute flight-to-safety spike during the banking panic. "
    "But because it recovers, the final CAR is near zero. "
    "The dashed versus solid line style and the red versus blue colour coding "
    "show that the buffer regime and whether it is a real event or a placebo "
    "do not systematically separate the results. "
    "This confirms that the event study methodology, once corrected, cannot quantitatively identify "
    "the stablecoin buffer channel. The paper's quantitative evidence lives in the regression.")


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 8 — What the Paper Proves (threshold graph + reframing)
# ═══════════════════════════════════════════════════════════════════════════════
sld = content_slide(prs, "What Our Paper Proves — In Plain Terms")
slide_number(sld, 8)

# Top strip defining "reframing"
box(sld, Inches(0.35), Inches(1.05), Inches(12.6), Inches(0.56), fill=HDR_NAVY)
txt(sld, "What does 'reframing' mean?",
    Inches(0.5), Inches(1.08), Inches(12.1), Inches(0.25),
    size=12, bold=True, color=GOLD)
txt(sld,
    "It means we are NOT changing the paper's conclusion. "
    "We are being honest about WHICH EVIDENCE proves it. "
    "The event study had a flaw. But our other two results are solid, unchanged, and stronger than the event study ever was.",
    Inches(0.5), Inches(1.32), Inches(12.1), Inches(0.25),
    size=11, italic=True, color=WHITE)

# Left side: before/after comparison (text)
# Before
box(sld, Inches(0.35), Inches(1.7), Inches(5.6), Inches(0.3), fill=RED)
txt(sld, "Before — what we were implying",
    Inches(0.45), Inches(1.73), Inches(5.45), Inches(0.24),
    size=12, bold=True, color=WHITE)
box(sld, Inches(0.35), Inches(2.0), Inches(5.6), Inches(2.1), fill=LIGHT_RED)
tf_b = bullet_tb(sld, Inches(0.45), Inches(2.07), Inches(5.4), Inches(1.96))
add_line(tf_b, "\"The event study shows +8.9/−18 pp CARs.\"", size=12, bold=True, color=RED, space_before=2)
add_line(tf_b, "\"A 27 pp swing with Welch t = 15.22.\"", size=12, bold=True, color=RED, space_before=4)
add_line(tf_b, "\"This proves the buffer channel.\"", size=12, bold=True, color=RED, space_before=4)
add_line(tf_b, " ", size=5, space_before=2)
add_line(tf_b, "Problem: CARs were inflated ~12× by the Fed hiking trend.", size=11, color=BODY_DARK, space_before=4)
add_line(tf_b, "Corrected CARs: near zero. The '27 pp swing' disappears.", size=11, bold=True, color=RED, space_before=4)

# After
box(sld, Inches(0.35), Inches(4.2), Inches(5.6), Inches(0.3), fill=GREEN)
txt(sld, "After — what we now say",
    Inches(0.45), Inches(4.23), Inches(5.45), Inches(0.24),
    size=12, bold=True, color=WHITE)
box(sld, Inches(0.35), Inches(4.5), Inches(5.6), Inches(2.2), fill=LIGHT_GRN)
tf_a = bullet_tb(sld, Inches(0.45), Inches(4.57), Inches(5.4), Inches(2.06))
add_line(tf_a, "\"β₁ = −6.02 bps per σ of supply (regression).\"", size=12, bold=True, color=GREEN, space_before=2)
add_line(tf_a, "\"q* = 13% liquid cash threshold (Hansen test).\"", size=12, bold=True, color=GREEN, space_before=4)
add_line(tf_a, "\"Event study is directionally consistent — but illustrative.\"", size=12, color=BODY_DARK, space_before=4)
add_line(tf_a, " ", size=5, space_before=2)
add_line(tf_a, "These two results were never broken. They are the paper.", size=11, bold=True, color=GREEN, space_before=4)
add_line(tf_a, "The conclusion is identical — only the evidence hierarchy changed.", size=11, color=BODY_DARK, space_before=4)

# Right side: threshold graph + label
box(sld, Inches(6.15), Inches(1.7), Inches(6.85), Inches(0.3), fill=ORANGE)
txt(sld, "Finding 2 — Hansen (2000) threshold search: q* = 13%",
    Inches(6.28), Inches(1.73), Inches(6.6), Inches(0.24),
    size=12, bold=True, color=WHITE)
img(sld, RESULTS / "threshold_ssr.png",
    Inches(6.15), Inches(2.0), Inches(6.85), Inches(3.75))
box(sld, Inches(6.15), Inches(5.75), Inches(6.85), Inches(0.52), fill=LGRAY)
tf_ann = bullet_tb(sld, Inches(6.28), Inches(5.78), Inches(6.6), Inches(0.46))
add_line(tf_ann,
    "The SSR (model fit) is minimised at q* = 0.130 (the red dashed line). "
    "Below that threshold, the regime switches — forced T-bill selling reverses the privilege. "
    "This result is independent of the event study and was never affected by the correction.",
    size=10, color=BODY_DARK, space_before=2)

orange_callout(sld,
    "Same conclusion. Same argument. Honest about the evidence. "
    "β₁ = −6.02 bps (regression) + q* = 13% (Hansen) = the paper. The event study illustrates it.",
    size=14)

notes(sld,
    "This slide answers the question: what does it mean to reframe the paper? "
    "In plain terms: we are not changing the conclusion. We are being honest about which evidence proves it. "
    "Before, we were pointing to the event study as the main proof — the 27 pp swing with t = 15. "
    "That was built on inflated numbers. Once corrected, the event study finds nothing significant. "
    "After, we point to two results that were always there and were never affected by the correction. "
    "First: the regression coefficient. Beta one equals negative 6.02 basis points per standard deviation "
    "of stablecoin supply. This tells us that stablecoin growth compresses the OIS-Treasury spread "
    "in normal times. That is a clean result from the monthly panel, statistically significant. "
    "Second: the Hansen threshold. The graph on the right shows what the Hansen threshold regression does. "
    "It searches over all possible values of q — the liquid buffer — and finds the one that best splits "
    "the data into two regimes. The SSR, which is the model's error, is minimised at q* = 0.130, "
    "shown by the red dashed line. That is 13 percent liquid cash. "
    "Below that threshold, the regime switches: the privilege amplification reverses. "
    "Both of these results are completely independent of the event study. "
    "They were not broken. They are the paper. "
    "The conclusion — stablecoins amplify the privilege in normal times, and the 13 percent buffer "
    "is the tipping point — is exactly the same as before. "
    "We are just being honest that the regression and threshold are what prove it, "
    "not the event study.")


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 8 — Thank You
# ═══════════════════════════════════════════════════════════════════════════════
sld = blank(prs)
title_slide_bg(sld)
txt(sld, "THANK YOU",
    Inches(4.0), Inches(2.85), Inches(8.8), Inches(0.6),
    size=28, color=WHITE, align=PP_ALIGN.LEFT, font="Calibri Light")
txt(sld, "CAR corrected  ·  Placebo test complete  ·  Evidence reframed honestly",
    Inches(4.0), Inches(3.5), Inches(9.0), Inches(0.4),
    size=13, italic=True, color=RGBColor(0xAA, 0xC4, 0xE8), align=PP_ALIGN.LEFT)
box(sld, Inches(3.9), Inches(4.45), Inches(7.5), Inches(2.8), fill=RGBColor(0x0E, 0x26, 0x68))
txt(sld,
    "Yonsei GSIS 2026-1  |  Topics in International Finance\n"
    "Mireu Kim · Sara Chekroune · Oybek Ibragimov\n"
    "kimmireu0921@gmail.com",
    Inches(4.1), Inches(4.6), Inches(7.2), Inches(2.5),
    size=16, color=WHITE, align=PP_ALIGN.LEFT)
notes(sld,
    "Thank you. Two sentences to close. "
    "First: stablecoin issuers have become structurally important buyers of U.S. Treasury bills. "
    "Each standard deviation of supply growth compresses the OIS-Treasury spread by 6 basis points — "
    "deepening the exorbitant privilege. "
    "Second: whether this persists or reverses during a shock depends on whether the issuer "
    "holds at least 13 percent of supply in liquid cash. "
    "The regression proves the first. The Hansen threshold proves the second. "
    "The event study is consistent with both — qualitatively. "
    "We are happy to take any questions.")


# ── Save ──────────────────────────────────────────────────────────────────────
out = PRESENTATIONS / "0602_Stablecoin_Exorbitant_Privilege.pptx"
prs.save(str(out))
print(f"Saved: {out}  ({len(prs.slides)} slides)")
