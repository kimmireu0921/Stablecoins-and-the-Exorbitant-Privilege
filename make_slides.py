"""
make_slides.py — presentation matching the Yonsei GSIS template from Digital Currency slides.

Template:
  - Title/end slides: dark navy bg + lighter navy band + white circle + white chevron
  - Content slides:   white bg + dark navy top header bar + slide number bottom right
  - Orange arrow callout for key takeaways
  - Diamond (❖) bullet points, clean Calibri font
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn
from pathlib import Path

RESULTS = Path("results")

# ── Colour palette (matched to original slides) ───────────────────────────────
DARK_NAVY  = RGBColor(0x0A, 0x1E, 0x5C)   # title slide main bg
MED_NAVY   = RGBColor(0x14, 0x30, 0x70)   # title slide lighter band
HDR_NAVY   = RGBColor(0x1B, 0x3A, 0x72)   # content slide header bar
WHITE      = RGBColor(0xFF, 0xFF, 0xFF)
ORANGE     = RGBColor(0xD4, 0x63, 0x2A)   # callout arrow
BODY_DARK  = RGBColor(0x1A, 0x1A, 0x2E)   # body text on white slides
LGRAY      = RGBColor(0xF0, 0xF4, 0xF8)   # subtle bg for boxes
MIDGRAY    = RGBColor(0x55, 0x55, 0x66)   # secondary text

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
    if Path(path).exists():
        if h:
            sld.shapes.add_picture(str(path), l, t, w, h)
        else:
            sld.shapes.add_picture(str(path), l, t, w)


# ── Yonsei template shapes ────────────────────────────────────────────────────

def title_slide_bg(sld):
    """Dark navy bg + lighter navy horizontal band (like original template)."""
    box(sld, 0, 0, SW, SH, fill=DARK_NAVY)
    box(sld, 0, Inches(2.85), SW, Inches(1.15), fill=MED_NAVY)

    # White large circle (top-left, like Yonsei logo area)
    circle = sld.shapes.add_shape(9, Inches(0.1), Inches(0.0), Inches(3.8), Inches(3.8))
    circle.fill.solid()
    circle.fill.fore_color.rgb = WHITE
    circle.line.fill.background()

    # Inner dark circle (the ring effect)
    inner = sld.shapes.add_shape(9, Inches(0.55), Inches(0.45), Inches(2.9), Inches(2.9))
    inner.fill.solid()
    inner.fill.fore_color.rgb = DARK_NAVY
    inner.line.fill.background()

    # White chevron/arrow at bottom-left
    chev = sld.shapes.add_shape(9, Inches(0.1), Inches(4.4), Inches(3.6), Inches(3.6))
    chev.fill.solid()
    chev.fill.fore_color.rgb = WHITE
    chev.line.fill.background()

    # Dark cover to make it look like open chevron
    inner_chev = sld.shapes.add_shape(9, Inches(0.65), Inches(4.85), Inches(2.5), Inches(2.5))
    inner_chev.fill.solid()
    inner_chev.fill.fore_color.rgb = DARK_NAVY
    inner_chev.line.fill.background()

    # Gray section (like original gray band at middle of circle/chevron)
    box(sld, 0, Inches(2.55), Inches(3.8), Inches(0.6), fill=RGBColor(0x55, 0x55, 0x66))


def content_slide(prs, title_text):
    """White bg + dark navy header bar + slide title."""
    sld = blank(prs)
    # White background
    box(sld, 0, 0, SW, SH, fill=WHITE)
    # Dark navy top bar
    box(sld, 0, 0, SW, Inches(0.95), fill=HDR_NAVY)
    # Title text in header
    txt(sld, title_text,
        Inches(0.3), Inches(0.1), Inches(11.5), Inches(0.78),
        size=26, bold=False, color=WHITE, align=PP_ALIGN.LEFT, font="Calibri")
    return sld


def slide_number(sld, num):
    txt(sld, str(num),
        SW - Inches(0.55), SH - Inches(0.42), Inches(0.45), Inches(0.35),
        size=13, color=MIDGRAY, align=PP_ALIGN.RIGHT)


def orange_callout(sld, text, t=None, size=18):
    """Orange arrow/chevron callout box at bottom (like original)."""
    if t is None:
        t = SH - Inches(1.38)
    box(sld, 0, t, SW, Inches(1.2), fill=ORANGE)
    txt(sld, text,
        Inches(0.6), t + Inches(0.18), SW - Inches(1.0), Inches(0.88),
        size=size, bold=True, color=WHITE, align=PP_ALIGN.CENTER)


def bullet_tb(sld, l, t, w, h):
    """Return an empty textbox ready for bullet lines."""
    tb = sld.shapes.add_textbox(l, t, w, h)
    tb.word_wrap = True
    tf = tb.text_frame
    tf.word_wrap = True
    tf.paragraphs[0].space_before = Pt(0)
    return tf


# ── Build presentation ────────────────────────────────────────────────────────

prs = Presentation()
prs.slide_width  = SW
prs.slide_height = SH


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 1 — Title
# ═══════════════════════════════════════════════════════════════════════════════
sld = blank(prs)
title_slide_bg(sld)

# Main title (in the lighter band)
txt(sld,
    "STABLECOINS AND THE EXORBITANT PRIVILEGE",
    Inches(4.0), Inches(2.78), Inches(9.0), Inches(0.65),
    size=22, bold=False, color=WHITE, align=PP_ALIGN.LEFT, font="Calibri Light")

# Subtitle
txt(sld,
    "A New Channel for Safe-Asset Demand and Its Systemic Fragility",
    Inches(4.0), Inches(3.42), Inches(9.0), Inches(0.5),
    size=14, italic=True, color=RGBColor(0xAA, 0xC4, 0xE8),
    align=PP_ALIGN.LEFT)

# Bottom info box
box(sld, Inches(3.9), Inches(4.45), Inches(7.5), Inches(2.8),
    fill=RGBColor(0x0E, 0x26, 0x68))

txt(sld,
    "Yonsei GSIS 2026-1\nTopics in International Finance\n"
    "Mireu Kim · Sara Chekroune · Oybek Ibragimov\n"
    "April 2026",
    Inches(4.1), Inches(4.6), Inches(7.2), Inches(2.5),
    size=16, bold=False, color=WHITE, align=PP_ALIGN.LEFT)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 2 — Roadmap
# ═══════════════════════════════════════════════════════════════════════════════
sld = content_slide(prs, "Roadmap")
slide_number(sld, 2)

items = [
    "Motivation — why stablecoins matter for sovereign debt",
    "The New Triffin Dilemma — our core argument",
    "Theoretical extension of Maggiori (2017)",
    "Data & Methodology",
    "Result 1 — Privilege amplification regression",
    "Result 2 — Reserve adequacy threshold (Hansen 2000)",
    "Result 3 — Buffer-conditioned event study",
    "Conclusion & Policy implications",
]

tf = bullet_tb(sld, Inches(0.7), Inches(1.1), Inches(12.2), Inches(6.0))
for i, item in enumerate(items):
    add_line(tf, f"{'❖' if i > 0 else '❖'}  {item}",
             size=20, color=BODY_DARK, space_before=8 if i > 0 else 2)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 3 — Motivation
# ═══════════════════════════════════════════════════════════════════════════════
sld = content_slide(prs, "Motivation: Stablecoins as Treasury Buyers")
slide_number(sld, 3)

# Left column — text
tf = bullet_tb(sld, Inches(0.5), Inches(1.1), Inches(6.2), Inches(4.8))
add_line(tf, "Key Market Trends", size=18, bold=True, color=HDR_NAVY, space_before=2)
bullets = [
    "Growth: Combined market cap surged from under $50bn (2021) to over $300bn (2026)",
    "Usage: 30%+ of on-chain crypto transactions involve stablecoins",
    "Regulation: US, EU, Japan, and Hong Kong each finalising reserve legislation",
    "Scale: Tether alone holds $127bn in US Treasuries (Q2 2025) — comparable to mid-sized sovereigns",
    "Projection: $1–2 trillion ecosystem within this decade",
]
for b in bullets:
    add_line(tf, f"❖  {b}", size=17, color=BODY_DARK, space_before=10)

# Right column — stat boxes
for i, (stat, label) in enumerate([
    ("$300bn+", "Total USD-pegged supply (2026)"),
    ("$127bn",  "Tether T-bill holdings (Q2 2025)"),
    ("$1–2 tn", "Projected ecosystem size"),
    ("4",       "Jurisdictions finalising legislation"),
]):
    t = Inches(1.05) + i * Inches(1.38)
    box(sld, Inches(7.1), t, Inches(5.8), Inches(1.2), fill=HDR_NAVY)
    txt(sld, stat, Inches(7.2), t + Inches(0.08),
        Inches(5.6), Inches(0.62), size=28, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    txt(sld, label, Inches(7.2), t + Inches(0.72),
        Inches(5.6), Inches(0.4), size=12, italic=True, color=RGBColor(0xAA, 0xC4, 0xE8),
        align=PP_ALIGN.CENTER)

orange_callout(sld,
    "The same structural role that deepens US safe-asset demand "
    "also embeds a fragility that can rapidly reverse it.")


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 4 — The New Triffin Dilemma
# ═══════════════════════════════════════════════════════════════════════════════
sld = content_slide(prs, "The New Triffin Dilemma")
slide_number(sld, 4)

box(sld, Inches(0.4), Inches(1.05), Inches(12.5), Inches(0.85), fill=LGRAY)
tf = bullet_tb(sld, Inches(0.55), Inches(1.1), Inches(12.2), Inches(0.75))
add_line(tf,
    "Triffin (1960): the reserve currency country must supply safe assets to the world — "
    "but that very supply undermines confidence in the currency.",
    size=14, italic=True, color=BODY_DARK)

txt(sld, "Our analogue for stablecoin issuers:",
    Inches(0.5), Inches(2.05), Inches(12.5), Inches(0.38),
    size=17, bold=True, color=HDR_NAVY)

# Three column comparison
cols = [
    ("Normal times ✅",
     ["Stablecoin growth → more T-bill buying",
      "Deepens US safe-asset demand",
      "Compresses OIS–Treasury spreads",
      "Amplifies exorbitant privilege"],
     RGBColor(0xE6, 0xF4, 0xEA), RGBColor(0x1A, 0x7A, 0x4A)),
    ("Run scenario ❌",
     ["Run on issuer → forced T-bill liquidation",
      "Yields spike above OIS",
      "Sovereign-linked liquidity shock",
      "Cole–Kehoe crisis zone activated"],
     RGBColor(0xFC, 0xEB, 0xE8), RGBColor(0xC0, 0x39, 0x2B)),
    ("What determines outcome",
     ["Reserve buffer B = T-bill holdings − supply",
      "B adequate: absorbs run without selling",
      "B inadequate (|ΔS| > B): liquidation forced",
      "→ We estimate the threshold B*"],
     RGBColor(0xEB, 0xF3, 0xFB), HDR_NAVY),
]
for i, (title, points, bg, col) in enumerate(cols):
    l = Inches(0.4) + i * Inches(4.3)
    box(sld, l, Inches(2.5), Inches(4.1), Inches(0.42), fill=col)
    txt(sld, title, l + Inches(0.1), Inches(2.53),
        Inches(3.9), Inches(0.36), size=14, bold=True, color=WHITE)
    box(sld, l, Inches(2.92), Inches(4.1), Inches(2.55), fill=bg)
    tf = bullet_tb(sld, l + Inches(0.12), Inches(2.98), Inches(3.88), Inches(2.4))
    for pt in points:
        add_line(tf, f"•  {pt}", size=13, color=BODY_DARK, space_before=6)

orange_callout(sld,
    "Our paper: formally quantify the reserve buffer threshold that separates the two regimes.")


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 5 — Theoretical Framework
# ═══════════════════════════════════════════════════════════════════════════════
sld = content_slide(prs, "Theoretical Extension: Maggiori (2017)")
slide_number(sld, 5)

# Left: Maggiori original + extension
box(sld, Inches(0.4), Inches(1.05), Inches(6.2), Inches(5.2), fill=LGRAY)
tf = bullet_tb(sld, Inches(0.55), Inches(1.12), Inches(5.9), Inches(5.0))
add_line(tf, "Maggiori (2017) original:", size=14, bold=True, color=HDR_NAVY)
add_line(tf, "Safe-asset demand driven by Ω* (marginal value of RoW net worth).",
         size=13, color=BODY_DARK, space_before=4)
add_line(tf, " ", size=8)
add_line(tf, "Our extension — add stablecoin supply S and buffer B:", size=14,
         bold=True, color=HDR_NAVY, space_before=6)
add_line(tf, "B*(Ñ*, S, B)  =  B*precautionary(Ñ*)  +  B*stablecoin(S)  +  B*buffer(B)",
         size=13, italic=True, color=BODY_DARK, space_before=4)
add_line(tf, " ", size=8)
add_line(tf, "Buffer B enters asymmetrically:", size=14, bold=True, color=HDR_NAVY)
add_line(tf, "❖  |ΔS| < B  →  run absorbed, no liquidation", size=13,
         color=RGBColor(0x1A, 0x7A, 0x4A), space_before=4)
add_line(tf, "❖  |ΔS| > B  →  liquidation channel activated", size=13,
         color=RGBColor(0xC0, 0x39, 0x2B), space_before=4)

# Right: Estimating equation
box(sld, Inches(6.8), Inches(1.05), Inches(6.1), Inches(5.2), fill=HDR_NAVY)
txt(sld, "Main Estimating Equation",
    Inches(6.95), Inches(1.12), Inches(5.8), Inches(0.5),
    size=15, bold=True, color=WHITE)
txt(sld,
    "Spreadₜ = α + β₁·ΔlnSₜ + β₂·Bₜ\n"
    "           + β₃·(Bₜ × ΔlnSₜ)\n"
    "           + β₄·Vₜ + β₅·VIXₜ\n"
    "           + β₆·ΔlnN*ₜ + εₜ",
    Inches(6.95), Inches(1.68), Inches(5.8), Inches(1.85),
    size=14, color=WHITE, font="Courier New")

tf2 = bullet_tb(sld, Inches(6.95), Inches(3.65), Inches(5.8), Inches(2.5))
add_line(tf2, "Predicted signs:", size=13, bold=True,
         color=RGBColor(0xAA, 0xC4, 0xE8))
for var, interp in [
    ("β₁ < 0", "ΔlnS compresses spreads (privilege amplification)"),
    ("β₂ < 0", "Higher buffer → more T-bill demand → lower spreads"),
    ("β₃ < 0", "Lower buffer reverses the compression effect"),
]:
    add_line(tf2, f"❖  {var}: {interp}", size=12,
             color=WHITE, space_before=6)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 6 — Data
# ═══════════════════════════════════════════════════════════════════════════════
sld = content_slide(prs, "Data & Sample")
slide_number(sld, 6)

rows = [
    ("OIS–Treasury Spread",  "DTB3 − SOFR90DAYAVG",        "FRED (direct CSV, no API key)",           "Daily → Monthly"),
    ("Stablecoin Supply S",  "USDT + USDC market cap",      "DeFiLlama stablecoins API (free)",        "Daily → Monthly"),
    ("Reserve Buffer B",     "T-bill holdings − supply",    "Tether/BDO + Circle/Deloitte attestations","Quarterly/Monthly"),
    ("Velocity V",           "7-day rolling SD of ΔlnS",   "Computed from DeFiLlama",                 "Daily → Monthly"),
    ("VIX",                  "CBOE VIX index",              "FRED",                                    "Daily → Monthly"),
    ("ΔlnN* (RoW equity)",   "ACWX ETF log-return",         "Yahoo Finance",                           "Daily → Monthly"),
]
hdrs = ["Variable", "Definition", "Source", "Frequency"]
col_ls = [Inches(0.35), Inches(2.75), Inches(5.55), Inches(10.55)]
col_ws = [Inches(2.35), Inches(2.75), Inches(4.95), Inches(2.35)]

# Header row
box(sld, Inches(0.35), Inches(1.05), Inches(12.6), Inches(0.42), fill=HDR_NAVY)
for h, l, w in zip(hdrs, col_ls, col_ws):
    txt(sld, h, l + Inches(0.05), Inches(1.08),
        w - Inches(0.08), Inches(0.36), size=13, bold=True, color=WHITE)

# Data rows
for r_i, row in enumerate(rows):
    t = Inches(1.47) + r_i * Inches(0.73)
    bg = LGRAY if r_i % 2 == 0 else WHITE
    box(sld, Inches(0.35), t, Inches(12.6), Inches(0.73), fill=bg)
    for val, l, w in zip(row, col_ls, col_ws):
        txt(sld, val, l + Inches(0.06), t + Inches(0.1),
            w - Inches(0.1), Inches(0.55), size=12, color=BODY_DARK)

txt(sld,
    "Sample: January 2020 – March 2026  |  N = 75 monthly observations  "
    "|  Pre-2021 buffer estimated at 2% of supply (first attestation: 2.94%, Moore Cayman Q1 2021)",
    Inches(0.35), SH - Inches(0.55), Inches(12.6), Inches(0.42),
    size=11, italic=True, color=MIDGRAY, align=PP_ALIGN.CENTER)
slide_number(sld, 6)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 7 — Time Series Figure
# ═══════════════════════════════════════════════════════════════════════════════
sld = content_slide(prs, "Key Variables: January 2020 – March 2026")
slide_number(sld, 7)

img(sld, RESULTS / "fig_timeseries.png",
    Inches(0.3), Inches(1.0), Inches(8.5))

tf = bullet_tb(sld, Inches(9.0), Inches(1.1), Inches(3.9), Inches(5.8))
add_line(tf, "Key observations", size=15, bold=True, color=HDR_NAVY)
obs = [
    "Spread compresses as stablecoin supply grows (2021–22)",
    "Spread spikes during LUNA/USDT run (May 2022)",
    "Buffer improves 2023–25 as Tether shifts to T-bills",
    "Crisis zone (B < −0.524) covers 2020–2022",
    "Vertical lines: 3 stress events studied",
]
for o in obs:
    add_line(tf, f"❖  {o}", size=13, color=BODY_DARK, space_before=10)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 8 — Result 1: Regression
# ═══════════════════════════════════════════════════════════════════════════════
sld = content_slide(prs, "Result 1: Privilege Amplification Regression")
slide_number(sld, 8)

txt(sld, "OLS with Newey–West HAC (3 lags, N = 75)  |  Variables mean-centered before interaction",
    Inches(0.4), Inches(1.05), Inches(12.5), Inches(0.32),
    size=12, italic=True, color=MIDGRAY)

# Regression table
reg_rows = [
    ("ΔlnS (centered)",      "−5.947", "***", "(1.436)"),
    ("B — buffer (centered)","−0.555", "***", "(0.139)"),
    ("B × ΔlnS (centered)",  "−11.296","***", "(3.873)"),
    ("V — velocity",         "−16.027","*",   "(9.125)"),
    ("VIX",                  "−0.003", "",    "(0.016)"),
    ("ΔlnN*",                "−0.211", "",    "(0.603)"),
    ("N",                    "75",     "",    ""),
    ("R²",                   "0.324",  "",    ""),
    ("Adj. R²",              "0.264",  "",    ""),
]
col_ls_r = [Inches(0.4), Inches(4.5), Inches(5.6), Inches(6.3)]
col_ws_r = [Inches(4.05), Inches(1.05), Inches(0.65), Inches(1.2)]

box(sld, Inches(0.4), Inches(1.44), sum(col_ws_r), Inches(0.38), fill=HDR_NAVY)
for h, l, w in zip(["Variable", "Coef.", "Sig.", "HAC SE"],
                    col_ls_r, col_ws_r):
    txt(sld, h, l + Inches(0.04), Inches(1.47), w, Inches(0.3),
        size=12, bold=True, color=WHITE, align=PP_ALIGN.CENTER if h != "Variable" else PP_ALIGN.LEFT)

for r_i, (var, coef, sig, se) in enumerate(reg_rows):
    t  = Inches(1.82) + r_i * Inches(0.46)
    bg = LGRAY if r_i % 2 == 0 else WHITE
    key = var in ("ΔlnS (centered)", "B × ΔlnS (centered)")
    if key:
        bg = RGBColor(0xFF, 0xF5, 0xDC)
    box(sld, Inches(0.4), t, sum(col_ws_r), Inches(0.46), fill=bg)
    for val, l, w, al in zip([var, coef, sig, se],
                               col_ls_r, col_ws_r,
                               [PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.CENTER]):
        txt(sld, val, l + Inches(0.04), t + Inches(0.07),
            w - Inches(0.06), Inches(0.34), size=12, bold=key, color=BODY_DARK, align=al)

txt(sld, "*** p<0.01  * p<0.10",
    Inches(0.4), Inches(6.12), Inches(7.5), Inches(0.28),
    size=10, italic=True, color=MIDGRAY)

# Interpretation (right side)
box(sld, Inches(7.9), Inches(1.44), Inches(5.0), Inches(2.25), fill=HDR_NAVY)
txt(sld, "β₁ = −5.95***", Inches(8.0), Inches(1.52),
    Inches(4.8), Inches(0.6), size=24, bold=True, color=WHITE)
txt(sld, "1 SD supply growth (9.9 pp) → −59 bp spread compression\n→ Privilege amplification confirmed ✅",
    Inches(8.0), Inches(2.1), Inches(4.8), Inches(0.88),
    size=13, color=RGBColor(0xAA, 0xC4, 0xE8))

box(sld, Inches(7.9), Inches(3.82), Inches(5.0), Inches(2.25), fill=RGBColor(0x14, 0x30, 0x70))
txt(sld, "β₃ = −11.30***", Inches(8.0), Inches(3.9),
    Inches(4.8), Inches(0.6), size=24, bold=True, color=WHITE)
txt(sld,
    "Total effect of ΔlnS = β₁ + β₃·B\n"
    "At mean B (−0.48): effect = −0.52 pp\n"
    "At threshold B = −0.524: effect ≈ 0 ✅",
    Inches(8.0), Inches(4.48), Inches(4.8), Inches(0.88),
    size=13, color=RGBColor(0xAA, 0xC4, 0xE8))


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 9 — Result 2: Threshold
# ═══════════════════════════════════════════════════════════════════════════════
sld = content_slide(prs, "Result 2: Reserve Adequacy Threshold (Hansen 2000)")
slide_number(sld, 9)

img(sld, RESULTS / "threshold_ssr.png",
    Inches(0.3), Inches(1.0), Inches(6.5))

tf = bullet_tb(sld, Inches(7.0), Inches(1.05), Inches(5.9), Inches(4.2))
add_line(tf, "Threshold estimate", size=16, bold=True, color=HDR_NAVY)
stats = [
    ("Optimal q*",         "−0.524"),
    ("LR statistic",       "25.28"),
    ("Bootstrap p-value",  "< 0.001  (1,000 replications)"),
    ("90% CI",             "[−0.524, −0.344]"),
]
for label, val in stats:
    add_line(tf, f"❖  {label}:  {val}", size=15, color=BODY_DARK, space_before=8)

add_line(tf, " ", size=6)
add_line(tf, "What q* = −0.524 means:", size=15, bold=True, color=HDR_NAVY, space_before=6)
add_line(tf,
    "Treasury holdings must exceed 47.6% of outstanding supply\n"
    "to stay outside the crisis zone.",
    size=14, color=BODY_DARK, space_before=4)

# Regime boxes
box(sld, Inches(0.3), Inches(5.75), Inches(6.2), Inches(0.85), fill=RGBColor(0xFC, 0xEB, 0xE8))
txt(sld, "Low buffer  (B ≤ −0.524, N=31):  β_ΔlnS = −1.03  →  No privilege amplification",
    Inches(0.45), Inches(5.82), Inches(5.9), Inches(0.7),
    size=13, color=RGBColor(0xC0, 0x39, 0x2B))

box(sld, Inches(6.75), Inches(5.75), Inches(6.2), Inches(0.85), fill=RGBColor(0xE6, 0xF4, 0xEA))
txt(sld, "High buffer  (B > −0.524, N=44):  β_ΔlnS = −8.68  →  Strong privilege compression",
    Inches(6.9), Inches(5.82), Inches(5.9), Inches(0.7),
    size=13, color=RGBColor(0x1A, 0x7A, 0x4A))


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 10 — Result 3: Event Study
# ═══════════════════════════════════════════════════════════════════════════════
sld = content_slide(prs, "Result 3: Buffer-Conditioned Event Study")
slide_number(sld, 10)

# Three events
events = [
    ("LUNA / UST Collapse", "May 9, 2022",  "Low buffer",  "CAR = +8.91 pp***",  RGBColor(0xC0, 0x39, 0x2B)),
    ("USDT Partial Depeg",  "May 12, 2022", "Low buffer",  "CAR = +8.85 pp***",  RGBColor(0xC0, 0x39, 0x2B)),
    ("USDC / SVB Failure",  "Mar 11, 2023", "High buffer", "CAR = −18.01 pp***", RGBColor(0x1A, 0x7A, 0x4A)),
]
for i, (name, date, regime, car, col) in enumerate(events):
    l = Inches(0.35) + i * Inches(4.35)
    box(sld, l, Inches(1.05), Inches(4.1), Inches(0.38), fill=HDR_NAVY)
    txt(sld, name, l + Inches(0.08), Inches(1.08),
        Inches(3.95), Inches(0.3), size=13, bold=True, color=WHITE)
    box(sld, l, Inches(1.43), Inches(4.1), Inches(0.32), fill=col)
    txt(sld, regime, l + Inches(0.08), Inches(1.46),
        Inches(3.95), Inches(0.26), size=12, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    box(sld, l, Inches(1.75), Inches(4.1), Inches(1.1), fill=LGRAY)
    txt(sld, f"{date}\n{car}", l + Inches(0.1), Inches(1.8),
        Inches(3.9), Inches(0.95), size=14, bold=True, color=col, align=PP_ALIGN.CENTER)

img(sld, RESULTS / "event_study_cars.png",
    Inches(0.35), Inches(3.0), Inches(7.5))

tf = bullet_tb(sld, Inches(8.0), Inches(3.05), Inches(4.9), Inches(3.4))
add_line(tf, "Interpretation", size=15, bold=True, color=HDR_NAVY)
add_line(tf,
    "❖  Low-buffer runs → T-bill yields spike (+8.9 pp)\n"
    "    Cole–Kehoe crisis zone activated",
    size=13, color=BODY_DARK, space_before=8)
add_line(tf,
    "❖  High-buffer stress → flight to Treasuries\n"
    "    compresses spread (−18.0 pp)",
    size=13, color=BODY_DARK, space_before=8)
add_line(tf,
    "❖  Welch test: t = 15.22, p < 0.001\n"
    "    Buffer regime is the key conditioning variable ✅",
    size=13, color=BODY_DARK, space_before=8)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 11 — Robustness
# ═══════════════════════════════════════════════════════════════════════════════
sld = content_slide(prs, "Robustness Checks")
slide_number(sld, 11)

checks = [
    ("NW lag sensitivity\n(1, 2, or 3 lags)",
     "β₁ and β₃ stable across all lag choices\n(−5.95 and −11.30, p < 0.01 throughout)",
     "✅  PASS", RGBColor(0x1A, 0x7A, 0x4A)),
    ("Drop pre-attestation period\n(Jan 2020 – Feb 2021)",
     "N = 61  →  β₁ = −8.04*** (p < 0.001)\nβ₃ = −7.97** (p = 0.008)  |  Threshold unchanged",
     "✅  PASS", RGBColor(0x1A, 0x7A, 0x4A)),
    ("Mean-centering\n(VIF reduction)",
     "VIF reduced from 24/32 to 5.7/7.2\nCoefficients and significance unchanged",
     "✅  PASS", RGBColor(0x1A, 0x7A, 0x4A)),
    ("First-differenced\nspecification",
     "β₁ and β₃ not significant in differences\nLevel spec captures slow structural relationship;\nevent study provides causal identification",
     "⚠️  PARTIAL", RGBColor(0xD4, 0x63, 0x2A)),
]

for i, (label, desc, verdict, col) in enumerate(checks):
    l = Inches(0.35) + (i % 2) * Inches(6.35)
    t = Inches(1.12) + (i // 2) * Inches(2.65)
    box(sld, l, t, Inches(6.05), Inches(2.5), fill=LGRAY)
    box(sld, l, t, Inches(6.05), Inches(0.42), fill=HDR_NAVY)
    txt(sld, label.split("\n")[0], l + Inches(0.1), t + Inches(0.07),
        Inches(4.0), Inches(0.3), size=13, bold=True, color=WHITE)
    txt(sld, verdict, l + Inches(4.1), t + Inches(0.07),
        Inches(1.85), Inches(0.3), size=12, bold=True, color=col, align=PP_ALIGN.RIGHT)
    txt(sld, desc, l + Inches(0.12), t + Inches(0.55),
        Inches(5.82), Inches(1.75), size=13, color=BODY_DARK)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 12 — Summary of Results
# ═══════════════════════════════════════════════════════════════════════════════
sld = content_slide(prs, "Summary of Results")
slide_number(sld, 12)

findings = [
    ("✅", HDR_NAVY,
     "Privilege amplification confirmed",
     "β₁ = −5.95***  |  1 SD supply growth → −59 bp spread compression"),
    ("✅", HDR_NAVY,
     "Buffer interaction significant",
     "β₃ = −11.30***  |  Lower buffer reverses the privilege amplification"),
    ("✅", HDR_NAVY,
     "Reserve adequacy threshold identified",
     "q* = −0.524, Bootstrap p < 0.001  |  Treasury holdings must exceed 47.6% of supply"),
    ("✅", HDR_NAVY,
     "Event study confirms asymmetry",
     "Low-buffer runs: CAR +8.9 pp  vs.  High-buffer stress: CAR −18.0 pp  (Welch t = 15.2***)"),
    ("⚠️", ORANGE,
     "Stationarity caveat",
     "Level results don't survive first-differencing; event study provides causal identification"),
]

for i, (icon, col, title, detail) in enumerate(findings):
    t = Inches(1.1) + i * Inches(1.08)
    box(sld, Inches(0.35), t, Inches(0.55), Inches(0.93), fill=col)
    txt(sld, icon, Inches(0.35), t + Inches(0.2),
        Inches(0.55), Inches(0.55), size=18, color=WHITE, align=PP_ALIGN.CENTER)
    box(sld, Inches(0.95), t, Inches(12.0), Inches(0.93),
        fill=LGRAY if i % 2 == 0 else WHITE)
    txt(sld, title, Inches(1.1), t + Inches(0.06),
        Inches(11.7), Inches(0.36), size=15, bold=True, color=HDR_NAVY)
    txt(sld, detail, Inches(1.1), t + Inches(0.46),
        Inches(11.7), Inches(0.4), size=13, color=BODY_DARK)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 13 — Policy Implications
# ═══════════════════════════════════════════════════════════════════════════════
sld = content_slide(prs, "Policy Implications")
slide_number(sld, 13)

txt(sld,
    "Our threshold estimate provides a direct reference point at a moment when the US, EU, "
    "Japan, and Hong Kong are each finalising stablecoin reserve legislation.",
    Inches(0.4), Inches(1.05), Inches(12.5), Inches(0.5),
    size=14, italic=True, color=MIDGRAY)

policies = [
    ("Minimum reserve ratio",
     "Require T-bill holdings ≥ 50% of outstanding supply — "
     "this places issuers outside the empirically identified crisis zone (q* = −0.524 → 47.6%)."),
    ("Liquidity-weighted requirements",
     "Not all T-bill holdings are equal. Short-duration bills can be sold faster. "
     "Weight reserves by remaining maturity, not just dollar amount."),
    ("Velocity-contingent buffers",
     "Our velocity variable V (7-day rolling SD of supply changes) predicts stress. "
     "Higher recent redemption velocity → higher required buffer. Dynamic rules."),
    ("Systemic size threshold",
     "Fragility is proportional to scale. A $100bn issuer's forced liquidation is 10× "
     "more disruptive than a $10bn issuer. Tiered requirements by AUM."),
]

for i, (title, desc) in enumerate(policies):
    l = Inches(0.35) + (i % 2) * Inches(6.45)
    t = Inches(1.72) + (i // 2) * Inches(2.35)
    box(sld, l, t, Inches(6.1), Inches(2.2), fill=LGRAY)
    box(sld, l, t, Inches(0.18), Inches(2.2), fill=HDR_NAVY)
    txt(sld, title, l + Inches(0.28), t + Inches(0.12),
        Inches(5.7), Inches(0.38), size=14, bold=True, color=HDR_NAVY)
    txt(sld, desc, l + Inches(0.28), t + Inches(0.55),
        Inches(5.7), Inches(1.5), size=13, color=BODY_DARK)

orange_callout(sld,
    "Policy bottom line: T-bill reserves ≥ 50% of supply keeps issuers outside the crisis zone.",
    size=17)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 14 — Conclusion
# ═══════════════════════════════════════════════════════════════════════════════
sld = content_slide(prs, "Conclusion")
slide_number(sld, 14)

box(sld, Inches(0.35), Inches(1.05), Inches(12.6), Inches(1.15), fill=LGRAY)
txt(sld,
    "Large-scale USD-pegged stablecoins introduce a two-sided 'New Triffin Dilemma': "
    "amplifying U.S. exorbitant privilege in normal times, while embedding a fragility that "
    "can rapidly reverse that benefit when reserve buffers fall below a critical threshold.",
    Inches(0.5), Inches(1.1), Inches(12.3), Inches(1.05), size=15, color=HDR_NAVY)

contribs = [
    ("Theory",     "Extended Maggiori (2017) with stablecoin supply S\nand reserve buffer B — asymmetric mechanism"),
    ("Empirics 1", "β₁ = −5.95*** (privilege amplification)\nβ₃ = −11.30*** (buffer-conditioned fragility)"),
    ("Empirics 2", "First data-driven threshold: q* = −0.524\nBootstrap p < 0.001 — applicable to regulation"),
    ("Empirics 3", "27 pp CAR swing between low- and\nhigh-buffer stress episodes"),
]
for i, (label, text) in enumerate(contribs):
    l = Inches(0.35) + (i % 2) * Inches(6.35)
    t = Inches(2.35) + (i // 2) * Inches(1.7)
    box(sld, l, t, Inches(6.1), Inches(1.55), fill=LGRAY)
    box(sld, l, t, Inches(1.3), Inches(1.55), fill=HDR_NAVY)
    txt(sld, label, l + Inches(0.05), t + Inches(0.5),
        Inches(1.2), Inches(0.55), size=13, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    txt(sld, text, l + Inches(1.38), t + Inches(0.15),
        Inches(4.6), Inches(1.25), size=13, color=BODY_DARK)

tf = bullet_tb(sld, Inches(0.5), Inches(5.85), Inches(12.4), Inches(0.55))
add_line(tf,
    "Limitation: Level results don't survive first-differencing. "
    "Event study (daily data, quasi-experimental) provides the primary causal identification.",
    size=12, italic=True, color=MIDGRAY)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 15 — Thank You (matches original template style)
# ═══════════════════════════════════════════════════════════════════════════════
sld = blank(prs)
title_slide_bg(sld)

txt(sld, "THANK YOU",
    Inches(4.0), Inches(2.85), Inches(8.8), Inches(0.6),
    size=28, bold=False, color=WHITE, align=PP_ALIGN.LEFT, font="Calibri Light")

box(sld, Inches(3.9), Inches(4.45), Inches(7.5), Inches(2.8),
    fill=RGBColor(0x0E, 0x26, 0x68))

txt(sld,
    "Yonsei GSIS 2026-1\nTopics in International Finance\n"
    "Mireu Kim · Sara Chekroune · Oybek Ibragimov\n"
    "kimmireu0921@gmail.com",
    Inches(4.1), Inches(4.6), Inches(7.2), Inches(2.5),
    size=16, color=WHITE, align=PP_ALIGN.LEFT)


# ── Save ──────────────────────────────────────────────────────────────────────
out = "Stablecoins_Presentation.pptx"
prs.save(out)
print(f"Saved: {out}  ({len(prs.slides)} slides)")
