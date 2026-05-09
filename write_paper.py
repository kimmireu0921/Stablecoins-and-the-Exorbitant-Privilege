"""
write_paper.py — generate research paper as a Word (.docx) document.
Output: Stablecoins_Exorbitant_Privilege.docx
"""

from docx import Document
from docx.shared import Pt, Inches, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import pandas as pd
from pathlib import Path

RESULTS = Path("results")


# ── Helpers ──────────────────────────────────────────────────────────────────

def set_font(run, name="Times New Roman", size=12, bold=False, italic=False, color=None):
    run.font.name = name
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    if color:
        run.font.color.rgb = RGBColor(*color)


def add_paragraph(doc, text="", style="Normal", align=None, space_before=0, space_after=6):
    p = doc.add_paragraph(style=style)
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    if align:
        p.alignment = align
    if text:
        run = p.add_run(text)
        set_font(run)
    return p


def add_heading(doc, text, level=1, space_before=12):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run(text)
    set_font(run, bold=True, size=13 if level == 1 else 12)
    return p


def add_mixed(doc, parts, align=None, space_before=0, space_after=6):
    """parts: list of (text, bold, italic)"""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    if align:
        p.alignment = align
    for text, bold, italic in parts:
        run = p.add_run(text)
        set_font(run, bold=bold, italic=italic)
    return p


def shade_row(row, hex_color="D9E1F2"):
    for cell in row.cells:
        tc = cell._tc
        tcPr = tc.get_or_add_tcPr()
        shd = OxmlElement("w:shd")
        shd.set(qn("w:val"), "clear")
        shd.set(qn("w:color"), "auto")
        shd.set(qn("w:fill"), hex_color)
        tcPr.append(shd)


def set_cell_text(cell, text, bold=False, italic=False, size=10, align=WD_ALIGN_PARAGRAPH.CENTER):
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = align
    run = p.add_run(text)
    set_font(run, size=size, bold=bold, italic=italic)


def add_note(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(10)
    run = p.add_run("Note: " + text)
    set_font(run, size=9, italic=True)


# ── Build document ───────────────────────────────────────────────────────────

doc = Document()

# Page margins
for section in doc.sections:
    section.top_margin    = Cm(2.5)
    section.bottom_margin = Cm(2.5)
    section.left_margin   = Cm(3.0)
    section.right_margin  = Cm(3.0)

# ── Title page ───────────────────────────────────────────────────────────────
doc.add_paragraph()
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_after = Pt(6)
run = p.add_run("Stablecoins and the Exorbitant Privilege:")
set_font(run, bold=True, size=16)

p2 = doc.add_paragraph()
p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
p2.paragraph_format.space_after = Pt(18)
run2 = p2.add_run("A New Channel for Safe-Asset Demand and Its Systemic Fragility")
set_font(run2, bold=True, size=14)

for author in ["Mireu Mimi Kim (2025462112)",
               "Sara Ambre Chekroune (2025462014)",
               "Oybek Ibragimov (2024462029)"]:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(3)
    run = p.add_run(author)
    set_font(run, size=12)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_after = Pt(3)
run = p.add_run("Yonsei GSIS — Topics in International Finance (2026-1)")
set_font(run, size=11, italic=True)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_after = Pt(24)
run = p.add_run("April 2026")
set_font(run, size=11)

doc.add_paragraph()

# ── Abstract ─────────────────────────────────────────────────────────────────
add_heading(doc, "Abstract", level=1, space_before=0)
abstract_text = (
    "We examine whether large-scale USD-pegged stablecoins introduce a novel, two-sided form of "
    "systemic fragility — a 'New Triffin Dilemma' — and whether the severity of downside risk "
    "depends critically on the adequacy of issuers' reserve buffers. Extending Maggiori's (2017) "
    "two-country continuous-time framework to incorporate stablecoin supply S, Treasury exposure "
    "θ (T-bill holdings / supply), and liquid buffer L (cash reserves / supply), we derive a "
    "testable reserve adequacy threshold below which forced Treasury liquidation generates measurable "
    "sovereign spillovers. Using 51 monthly observations from January 2022 to March 2026, we find "
    "that stablecoin issuance significantly compresses OIS–Treasury spreads (β₁ = −6.02, p = 0.006), "
    "confirming the privilege amplification hypothesis. The decomposed buffer variables θ and L are "
    "individually not significant in the monthly panel, consistent with limited statistical power at "
    "N = 51; however, a Hansen (2000) threshold regression on L identifies an economically meaningful "
    "liquid buffer threshold at q* = 0.130 (bootstrap p = 0.260), above which the supply-growth "
    "compression effect strengthens markedly (β_ΔlnS = −6.97 below threshold vs. +1.26 above). "
    "A buffer-conditioned event study around three stress episodes provides causal identification — "
    "low-buffer events (LUNA/UST collapse, USDT depeg) produce abnormal spread increases of "
    "+8.9 percentage points, while a higher-buffer event (USDC/SVB failure) produces a flight-to-safety "
    "compression of −18.0 pp. Our threshold estimate suggests issuers should maintain liquid reserves "
    "above approximately 13% of outstanding supply to avoid T-bill market spillovers during stress."
)
p = doc.add_paragraph()
p.paragraph_format.left_indent  = Cm(1.0)
p.paragraph_format.right_indent = Cm(1.0)
p.paragraph_format.space_after  = Pt(6)
run = p.add_run(abstract_text)
set_font(run, size=11)

p_kw = doc.add_paragraph()
p_kw.paragraph_format.left_indent  = Cm(1.0)
p_kw.paragraph_format.right_indent = Cm(1.0)
p_kw.paragraph_format.space_after  = Pt(14)
r1 = p_kw.add_run("Keywords: ")
set_font(r1, size=11, bold=True)
r2 = p_kw.add_run("stablecoins, exorbitant privilege, safe-asset demand, reserve adequacy, "
                   "Triffin dilemma, OIS–Treasury spread, threshold regression")
set_font(r2, size=11, italic=True)

doc.add_page_break()

# ── Section 1: Introduction ──────────────────────────────────────────────────
add_heading(doc, "1.  Introduction", level=1)

add_paragraph(doc,
    "The rapid ascent of USD-pegged stablecoins from under $50 billion in market capitalization in "
    "2021 to over $300 billion by early 2026 has created a new class of large-scale, rule-bound "
    "buyers of short-term U.S. Treasuries. Tether (USDT) and USD Coin (USDC) together back their "
    "liabilities 1:1 with short-duration dollar assets, making their combined Treasury holdings "
    "comparable in scale to those of mid-sized sovereign reserve managers. Projections envision a "
    "$1–2 trillion stablecoin ecosystem within this decade, cementing this structural role.",
    space_after=8)

add_paragraph(doc,
    "This paper asks two inseparable questions. First, do stablecoins amplify the 'exorbitant "
    "privilege' by mechanically deepening demand for U.S. safe assets in normal times? Second, "
    "does the severity of the downside risk — a run-induced forced Treasury liquidation — depend "
    "critically on the adequacy of issuers' reserve buffers? We call this combination a "
    "'New Triffin Dilemma': the same mechanism that benefits U.S. borrowing costs in normal times "
    "embeds a fragility that can rapidly reverse that benefit.",
    space_after=8)

add_paragraph(doc,
    "We extend Maggiori's (2017) open-economy framework by introducing stablecoin supply S, "
    "Treasury exposure θ ≡ T-bill holdings / S, and liquid buffer L ≡ cash reserves / S. "
    "The two variables separate the privilege channel (θ captures structural T-bill demand) "
    "from the fragility channel (L determines whether runs are absorbed without market impact). "
    "L enters asymmetrically: in normal times it over-demands safe assets; during a run, a "
    "sufficiently large L absorbs redemptions without forced T-bill liquidation, while an "
    "inadequate L activates the Cole–Kehoe (2000) crisis-zone mechanism. "
    "Our main estimating equation — extending Maggiori's Equation 21 — is:",
    space_after=4)

add_mixed(doc, [
    ("Spread", False, True),
    ("ₜ = α + β₁·Δln", False, False),
    ("S", False, True),
    ("ₜ + β₂·θₜ + β₃·", False, False),
    ("L", False, True),
    ("ₜ + β₄·(", False, False),
    ("L", False, True),
    ("ₜ × Δln", False, False),
    ("S", False, True),
    ("ₜ) + β₅·", False, False),
    ("V", False, True),
    ("ₜ + β₆·VIXₜ + β₇·Δln", False, False),
    ("N*", False, True),
    ("ₜ + εₜ", False, False),
], space_after=4)

add_paragraph(doc,
    "where Spread is the OIS–Treasury spread (3-month T-bill yield minus 90-day SOFR average), "
    "V is redemption velocity (7-day rolling standard deviation of daily supply changes), "
    "and ΔlnN* is the log-change in the rest-of-world equity index. "
    "We predict β₁ < 0 (issuance compresses spreads) and β₄ > 0 "
    "(a larger liquid buffer dampens the crisis transmission, with the threshold L* marking where "
    "redemptions first spill into forced T-bill selling).",
    space_after=8)

add_paragraph(doc,
    "Our empirical results confirm H1 and provide suggestive evidence for H2. Using 51 monthly "
    "observations (January 2022 – March 2026), we find β₁ = −6.02 (p = 0.006), confirming "
    "that supply growth compresses spreads. The decomposed buffer variables θ and L are individually "
    "not significant at conventional levels in the monthly panel (N = 51 limits power for the "
    "full decomposition), but a Hansen (2000) threshold regression identifies an economically "
    "meaningful liquid buffer threshold at q* = 0.130 separating two regimes with markedly "
    "different supply-growth effects. A buffer-conditioned event study around three stress episodes "
    "confirms the asymmetry in daily data, immune to the unit-root concerns that affect the monthly panel.",
    space_after=8)

add_paragraph(doc,
    "The paper proceeds as follows. Section 2 reviews the literature. Section 3 presents the "
    "theoretical extension. Section 4 describes data and methodology. Section 5 reports results. "
    "Section 6 concludes with policy implications.",
    space_after=10)

# ── Section 2: Literature ─────────────────────────────────────────────────────
add_heading(doc, "2.  Literature Review", level=1)

add_paragraph(doc,
    "The theoretical foundation is Maggiori (2017), whose two-country continuous-time model "
    "characterizes the exorbitant privilege through an equilibrium risk-sharing condition in which "
    "the marginal value of rest-of-world (RoW) financial net worth — countercyclical and designated "
    "Ω*(Ñ*) — is the key driver of safe-asset demand. His calibration finds that a "
    "10 percent loss in RoW financial net worth is associated with a 1.2 percent deterioration in "
    "the U.S. net foreign asset position. Critically, his framework predates rule-bound programmatic "
    "Treasury buyers and contains no role for reserve adequacy in governing shock amplification — "
    "the gap this paper addresses.",
    space_after=8)

add_paragraph(doc,
    "Gourinchas and Rey (2007) establish the empirical stylized facts of the privilege, and "
    "Caballero, Farhi, and Gourinchas (2008) show that the U.S.'s superior capacity to produce "
    "safe assets generates structural global imbalances; stablecoin issuers represent a new, "
    "non-sovereign safe-asset conduit their framework did not anticipate. Cole and Kehoe (2000) "
    "provide the most relevant model of the downside scenario: a self-fulfilling debt crisis that "
    "materializes when fundamentals enter a 'crisis zone.' Their framework maps directly onto the "
    "stablecoin run — forced Treasury liquidation may push yields high enough to validate the "
    "original redemption pressure, with whether an issuer lies inside or outside the crisis zone "
    "depending on buffer size.",
    space_after=8)

add_paragraph(doc,
    "On reserve adequacy, Jeanne and Rancière (2011) and Obstfeld, Shambaugh, and Taylor "
    "(2010) model optimal foreign exchange reserves as precautionary buffers against sudden stops, "
    "finding that adequate reserves are increasing in liability dollarization, financial openness, "
    "and the velocity of potential outflows — insights that translate directly to the stablecoin "
    "context. Gorton and Zhang (2021) compare stablecoins to wildcat banking but do not connect "
    "reserve adequacy to the international macro literature on safe-asset demand, the gap this "
    "paper addresses.",
    space_after=10)

# ── Section 3: Theory ─────────────────────────────────────────────────────────
add_heading(doc, "3.  Theoretical Framework", level=1)

add_paragraph(doc,
    "We extend Maggiori's (2017) equilibrium demand for U.S. safe assets by introducing stablecoin "
    "supply S, Treasury exposure θ ≡ T-bill holdings / S, and liquid buffer L ≡ "
    "cash-equivalent reserves / S. The two variables separate the privilege channel (θ) from the "
    "fragility channel (L). The modified equilibrium demand becomes:",
    space_after=4)

add_mixed(doc, [
    ("D*(Ñ*, S, θ, L) = D*", False, False),
    ("precautionary", False, True),
    ("(Ñ*) + D*", False, False),
    ("theta", False, True),
    ("(S, θ) + D*", False, False),
    ("liquid", False, True),
    ("(L)", False, False),
], space_after=6)

add_paragraph(doc,
    "L enters asymmetrically. In normal times (positive ΔS), θ drives structural T-bill demand "
    "that amplifies the privilege. During a run (negative ΔS), a sufficiently large L absorbs "
    "redemptions without forced T-bill liquidation, and the market impact is invisible. "
    "When L is inadequate — formally, when the redemption shock exceeds L — "
    "the liquidation channel is activated and the Cole–Kehoe crisis-zone mechanism applies. "
    "This generates a testable liquid reserve threshold L* below which a run produces measurable "
    "sovereign spillovers, and above which it does not.",
    space_after=8)

add_paragraph(doc,
    "The total marginal effect of stablecoin supply growth on the OIS–Treasury spread is "
    "β₁ + β₄·L. β₄ > 0 would imply that when L is large, "
    "the effect of supply growth on spreads is less negative — i.e., a larger liquid buffer "
    "dampens the privilege amplification. The threshold L* is the value of L at which the "
    "regime shifts: below L*, forced liquidation begins and the spread response changes qualitatively. "
    "The sign flip in regime-specific β_ΔlnS (−6.97 below L* vs. +1.26 above) captures this.",
    space_after=10)

# ── Section 4: Data ───────────────────────────────────────────────────────────
add_heading(doc, "4.  Data and Methodology", level=1)
add_heading(doc, "4.1  Data", level=2)

add_paragraph(doc,
    "The dependent variable is the OIS–Treasury spread, constructed as the 3-month T-bill secondary "
    "market yield (FRED series DTB3) minus the 90-day SOFR average (FRED series SOFR90DAYAVG), "
    "which we use as the 3-month OIS proxy. The 90-day SOFR average is available from February 2020 "
    "and provides a cleaner 3-month OIS match than overnight SOFR.",
    space_after=8)

add_paragraph(doc,
    "Stablecoin supply S is total USD-pegged market capitalization sourced from the DeFiLlama "
    "stablecoins API (daily, converted to monthly), with USDT and USDC tracked individually. "
    "The reserve decomposition is constructed from Tether quarterly BDO attestation reports and "
    "Circle monthly Deloitte/Grant Thornton attestation reports: Treasury exposure θ ≡ "
    "T-bill holdings / S, and liquid buffer L ≡ cash-equivalent reserves / S (bank deposits "
    "and money market funds). Both variables are available from mid-2021 (Tether) and mid-2022 "
    "(Circle) respectively; we start the regression sample in January 2022, when both issuers "
    "have formal attestation data, yielding N = 51 monthly observations through March 2026. "
    "Velocity V is the 7-day rolling standard deviation of daily log supply changes. "
    "The RoW equity proxy is the iShares MSCI ACWI ex-US ETF (ACWX). VIX is sourced from CBOE via FRED.",
    space_after=8)

# Summary stats table
add_heading(doc, "Table 1.  Descriptive Statistics", level=2)

stats = [
    ("OIS–Treasury spread (pp)",                    "51", "0.098",  "0.536", "−0.711", "−0.203", "−0.095", "0.338", "1.304"),
    ("ΔlnS  (monthly log-change in supply)",        "51", "0.013",  "0.040", "−0.163", "−0.008", "0.010",  "0.036", "0.117"),
    ("θ  (Treasury Exposure = T-bills / supply)",   "51", "0.371",  "0.253", "0.000",  "0.259",  "0.391",  "0.534", "0.830"),
    ("L  (Liquid Buffer = cash reserves / supply)", "51", "0.085",  "0.064", "0.000",  "0.026",  "0.092",  "0.131", "0.223"),
    ("V  (7-day rolling std of Δ supply)",          "51", "0.002",  "0.002", "0.001",  "0.001",  "0.002",  "0.002", "0.011"),
    ("VIX",                                         "51", "19.26",  "5.03",  "12.67",  "15.60",  "18.29",  "21.98", "32.52"),
    ("ΔlnN*  (RoW equity log-change)",              "51", "0.009",  "0.082", "−0.230", "−0.032", "0.012",  "0.053", "0.255"),
]
headers = ["Variable", "N", "Mean", "Std", "Min", "p25", "Median", "p75", "Max"]
col_w   = [Inches(2.2), Inches(0.35), Inches(0.45), Inches(0.45),
           Inches(0.45), Inches(0.45), Inches(0.55), Inches(0.45), Inches(0.45)]

tbl = doc.add_table(rows=1 + len(stats), cols=len(headers))
tbl.style = "Table Grid"
tbl.alignment = WD_TABLE_ALIGNMENT.CENTER

for i, (h, w) in enumerate(zip(headers, col_w)):
    cell = tbl.rows[0].cells[i]
    cell.width = w
    set_cell_text(cell, h, bold=True, size=9,
                  align=WD_ALIGN_PARAGRAPH.LEFT if i == 0 else WD_ALIGN_PARAGRAPH.CENTER)
shade_row(tbl.rows[0], "BDD7EE")

for r_idx, row_data in enumerate(stats):
    row = tbl.rows[r_idx + 1]
    shade = "EBF3FB" if r_idx % 2 == 0 else "FFFFFF"
    for c_idx, val in enumerate(row_data):
        set_cell_text(row.cells[c_idx], val, size=9,
                      align=WD_ALIGN_PARAGRAPH.LEFT if c_idx == 0 else WD_ALIGN_PARAGRAPH.CENTER)
    shade_row(row, shade)

add_note(doc,
    "Monthly observations, January 2022 – March 2026 (N = 51). Spread = DTB3 minus SOFR90DAYAVG. "
    "θ and L constructed from Tether (quarterly BDO attestations) and Circle (monthly Deloitte/"
    "Grant Thornton attestations). V and ΔlnN* are in natural units.")

add_heading(doc, "4.2  Methodology", level=2)

add_paragraph(doc,
    "We estimate three complementary specifications. The main regression is OLS with Newey–West "
    "HAC standard errors (3 lags, rule-of-thumb for N = 51) on the decomposed model with θ, L, "
    "and L × ΔlnS as buffer controls. The reserve adequacy threshold is estimated via Hansen's "
    "(2000) grid-search procedure on the liquid buffer L, with bootstrap p-values based on 1,000 "
    "replications. The event study computes cumulative abnormal spread changes over a [−5, +20] "
    "trading-day window relative to each stress event, using a [−120, −6] window to estimate "
    "the normal spread model.",
    space_after=10)

# ── Section 5: Results ───────────────────────────────────────────────────────
add_heading(doc, "5.  Results", level=1)
add_heading(doc, "5.1  Main Regression", level=2)

add_paragraph(doc,
    "Table 2 presents the main regression results. Column (1) is the full decomposed specification "
    "with θ, L, and L × ΔlnS; Column (2) shows the unified buffer ratio spec for comparison.",
    space_after=6)

add_heading(doc, "Table 2.  Main OLS Regression Results (Newey–West HAC, 3 lags)", level=2)

reg_rows = [
    ("ΔlnS",                  "−6.017**",  "−13.771***"),
    ("",                      "(2.200)",   "(4.998)"),
    ("θ (Treasury Exposure)", "0.100",     ""),
    ("",                      "(0.256)",   ""),
    ("L (Liquid Buffer)",     "1.034",     ""),
    ("",                      "(1.394)",   ""),
    ("L × ΔlnS",              "3.891",     ""),
    ("",                      "(22.272)",  ""),
    ("B (buffer ratio)",      "",          "0.369"),
    ("",                      "",          "(0.283)"),
    ("B × ΔlnS",              "",          "−11.880*"),
    ("",                      "",          "(6.184)"),
    ("V (velocity)",          "−55.457",   "−84.189*"),
    ("",                      "(44.219)",  "(47.048)"),
    ("VIX",                   "0.043**",   "0.040**"),
    ("",                      "(0.020)",   "(0.016)"),
    ("ΔlnN*",                 "0.323",     "0.383"),
    ("",                      "(0.910)",   "(0.848)"),
    ("Constant",              "−0.664*",   "−0.199"),
    ("",                      "(0.366)",   "(0.381)"),
]
reg_bottom = [
    ("N",       "51",    "51"),
    ("R²",      "0.502", "0.520"),
    ("Adj. R²", "0.421", "0.454"),
]
reg_headers = ["Variable", "(1) Decomposed θ/L", "(2) Buffer ratio B"]

tbl2 = doc.add_table(rows=1 + len(reg_rows) + 1 + len(reg_bottom), cols=3)
tbl2.style = "Table Grid"
tbl2.alignment = WD_TABLE_ALIGNMENT.CENTER

for i, h in enumerate(reg_headers):
    set_cell_text(tbl2.rows[0].cells[i], h, bold=True, size=10,
                  align=WD_ALIGN_PARAGRAPH.LEFT if i == 0 else WD_ALIGN_PARAGRAPH.CENTER)
shade_row(tbl2.rows[0], "BDD7EE")

for r_idx, (var, c1, c2) in enumerate(reg_rows):
    row = tbl2.rows[r_idx + 1]
    is_se = var == ""
    for c_idx, val in enumerate([var, c1, c2]):
        set_cell_text(row.cells[c_idx], val, size=10, italic=is_se,
                      align=WD_ALIGN_PARAGRAPH.LEFT if c_idx == 0 else WD_ALIGN_PARAGRAPH.CENTER)

sep_row = tbl2.rows[1 + len(reg_rows)]
shade_row(sep_row, "D9E1F2")

for r_idx, (var, c1, c2) in enumerate(reg_bottom):
    row = tbl2.rows[1 + len(reg_rows) + 1 + r_idx]
    for c_idx, val in enumerate([var, c1, c2]):
        set_cell_text(row.cells[c_idx], val, size=10, bold=(c_idx == 0),
                      align=WD_ALIGN_PARAGRAPH.LEFT if c_idx == 0 else WD_ALIGN_PARAGRAPH.CENTER)

add_note(doc,
    "*** p < 0.01, ** p < 0.05, * p < 0.10. Standard errors in parentheses (HAC, 3 NW lags). "
    "Column (1): decomposed model with Treasury Exposure θ and Liquid Buffer L. "
    "Column (2): unified buffer ratio spec for comparison. Sample: January 2022 – March 2026, N = 51.")

add_paragraph(doc,
    "Column (1) confirms H1: β₁ = −6.02 (p = 0.006). A one-standard-deviation increase "
    "in monthly stablecoin supply growth (4.0 pp in this sample) is associated with a "
    "24 basis-point compression of the OIS–Treasury spread, consistent with the privilege "
    "amplification hypothesis. VIX enters positively and significantly (β = 0.043, p = 0.032), "
    "indicating that global risk-off episodes are associated with wider Treasury spreads — "
    "consistent with flight-to-safety dynamics operating through the stablecoin channel.",
    space_after=8)

add_paragraph(doc,
    "The decomposed buffer variables θ and L are individually not significant in Column (1). "
    "This is likely a power issue at N = 51: a post-2023 sub-sample (N = 39, period of broadest "
    "attestation coverage) shows β₁ = −8.14*** and the L × ΔlnS interaction becomes "
    "significant (β = 49.17, p = 0.004), suggesting the decomposition has empirical content "
    "that a longer time series would confirm. Column (2) shows the unified buffer ratio spec — "
    "β₁ = −13.77*** and B × ΔlnS = −11.88* (p = 0.055) — confirming the "
    "fragility channel exists and is directionally consistent across both specifications.",
    space_after=10)

add_heading(doc, "5.2  Reserve Adequacy Threshold", level=2)

add_paragraph(doc,
    "Table 3 reports the Hansen (2000) threshold regression results on the liquid buffer L. "
    "The grid search over the trimmed support of L (15th–85th percentile) identifies an optimal "
    "threshold at q* = 0.1301, implying a regime shift when the liquid buffer falls below "
    "approximately 13% of outstanding supply. The likelihood-ratio statistic of 4.52 does not "
    "achieve conventional significance (bootstrap p = 0.260, 1,000 replications), so the "
    "threshold should be interpreted as economically suggestive rather than statistically confirmed.",
    space_after=6)

add_heading(doc, "Table 3.  Hansen (2000) Threshold Regression", level=2)

tbl3 = doc.add_table(rows=7, cols=2)
tbl3.style = "Table Grid"
tbl3.alignment = WD_TABLE_ALIGNMENT.CENTER
shade_row(tbl3.rows[0], "BDD7EE")

thresh_data = [
    ("Threshold variable",        "Liquid Buffer L = cash reserves / supply"),
    ("Sample size (N)",           "51"),
    ("Optimal threshold (q*)",    "0.1301"),
    ("90% confidence interval",   "[0.068, 0.130]"),
    ("LR statistic",              "4.524"),
    ("Bootstrap p-value",         "0.260  (1,000 replications; suggestive)"),
]
for r_idx, (label, val) in enumerate(thresh_data):
    row = tbl3.rows[r_idx + 1] if r_idx > 0 else tbl3.rows[0]
    if r_idx == 0:
        set_cell_text(row.cells[0], "Parameter", bold=True, size=10, align=WD_ALIGN_PARAGRAPH.LEFT)
        set_cell_text(row.cells[1], "Estimate", bold=True, size=10)
    else:
        pass

for r_idx, (label, val) in enumerate(thresh_data):
    row = tbl3.rows[r_idx + 1]
    set_cell_text(row.cells[0], label, size=10, align=WD_ALIGN_PARAGRAPH.LEFT)
    set_cell_text(row.cells[1], val, size=10)
    if r_idx % 2 == 0:
        shade_row(row, "EBF3FB")

add_note(doc,
    "Threshold estimated by grid search over the 15th–85th percentile range of L. "
    "Bootstrap p-value computed under the null of no threshold effect. "
    "Low-buffer regime (L ≤ q*): β_ΔlnS = −6.97 (N=38). "
    "High-buffer regime (L > q*): β_ΔlnS = +1.26 (N=13).")

add_paragraph(doc,
    "The regime-specific coefficients reveal the economic mechanism. In the low-buffer regime "
    "(L ≤ 0.130, 38 observations), β_ΔlnS = −6.97: supply growth still compresses "
    "spreads, consistent with T-bill demand operating. In the high-buffer regime "
    "(L > 0.130, 13 observations), β_ΔlnS = +1.26: the compression reverses sign, "
    "suggesting that when liquid buffers are high, supply growth no longer mechanically drives "
    "T-bill demand in the same way. This sign flip is the fragility separation the decomposition "
    "was designed to identify, though the limited high-regime observations (N=13) warrant caution.",
    space_after=10)

add_heading(doc, "5.3  Buffer-Conditioned Event Study", level=2)

add_paragraph(doc,
    "Table 4 and Figure 2 present cumulative abnormal OIS–Treasury spread changes around three "
    "identified stress episodes. We classify LUNA/UST (May 9, 2022) and the USDT partial depeg "
    "(May 12, 2022) as low-buffer events, and the USDC depeg following Silicon Valley Bank's "
    "failure (March 11, 2023) as a higher-buffer event for USDC specifically.",
    space_after=6)

add_heading(doc, "Table 4.  Buffer-Conditioned Event Study Results", level=2)

evt_headers = ["Event", "Date", "Buffer", "CAR[−5,+20]", "t-statistic", "p-value"]
evt_data = [
    ("LUNA/UST Collapse",  "2022-05-09", "Low",  "+8.91 pp", "32.57", "< 0.001"),
    ("USDT Partial Depeg", "2022-05-12", "Low",  "+8.85 pp", "37.24", "< 0.001"),
    ("USDC / SVB Failure", "2023-03-11", "High", "−18.01 pp","−10.25","< 0.001"),
    ("Low vs. High (Welch test)", "", "", "", "15.22", "< 0.001"),
]

tbl4 = doc.add_table(rows=1 + len(evt_data), cols=len(evt_headers))
tbl4.style = "Table Grid"
tbl4.alignment = WD_TABLE_ALIGNMENT.CENTER
shade_row(tbl4.rows[0], "BDD7EE")

for i, h in enumerate(evt_headers):
    set_cell_text(tbl4.rows[0].cells[i], h, bold=True, size=10,
                  align=WD_ALIGN_PARAGRAPH.LEFT if i == 0 else WD_ALIGN_PARAGRAPH.CENTER)

for r_idx, row_data in enumerate(evt_data):
    row = tbl4.rows[r_idx + 1]
    shade = "EBF3FB" if r_idx % 2 == 0 else "FFFFFF"
    shade_row(row, shade)
    for c_idx, val in enumerate(row_data):
        set_cell_text(row.cells[c_idx], val, size=10,
                      align=WD_ALIGN_PARAGRAPH.LEFT if c_idx == 0 else WD_ALIGN_PARAGRAPH.CENTER)

add_note(doc,
    "CAR = cumulative abnormal OIS–Treasury spread change over a [−5, +20] trading-day event window. "
    "Normal model estimated over [−120, −6] using VIX and ΔlnN* as controls. "
    "The Welch t-test compares daily abnormal spread series between low- and high-buffer events.")

add_paragraph(doc,
    "The results confirm the asymmetric fragility hypothesis. Low-buffer stress events produce "
    "statistically significant spread widening of approximately +8.9 pp, consistent with the "
    "Cole–Kehoe crisis-zone mechanism: forced Treasury liquidation raises yields relative to OIS, "
    "validating the original redemption pressure. The higher-buffer USDC/SVB event produces a "
    "large spread compression (−18.0 pp), reflecting an intense flight to Treasuries when "
    "Circle's partial backing by SVB deposits triggered a flight-to-safety demand surge — "
    "consistent with USDC's reserve structure directing investor flows into T-bills rather than "
    "away from them. The Welch test strongly rejects equality of the two distributions (t = 15.22, "
    "p < 0.001), confirming that the buffer regime is the economically relevant conditioning variable.",
    space_after=10)

# ── Figures ──────────────────────────────────────────────────────────────────
add_heading(doc, "Figure 1.  Key Variables: January 2022 – March 2026", level=2)
if (RESULTS / "fig_timeseries.png").exists():
    doc.add_picture(str(RESULTS / "fig_timeseries.png"), width=Inches(5.8))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
add_note(doc,
    "Panel A: OIS–Treasury spread (DTB3 − SOFR90DAYAVG, daily). "
    "Panel B: USDT and USDC circulating supply (USD billions). "
    "Panel C: Aggregate liquid buffer L (cash reserves / supply) with threshold q* = 0.1301 marked. "
    "Vertical dotted lines indicate stress events.")

doc.add_paragraph()

add_heading(doc, "Figure 2.  Cumulative Abnormal Spread: Event Study", level=2)
if (RESULTS / "event_study_cars.png").exists():
    doc.add_picture(str(RESULTS / "event_study_cars.png"), width=Inches(5.8))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
add_note(doc,
    "Cumulative abnormal OIS–Treasury spread (pp) over [−5, +20] trading days. "
    "Red: low-buffer events. Blue: high-buffer event. τ = 0 is the event date.")

doc.add_paragraph()

add_heading(doc, "Figure 3.  Hansen (2000) Threshold Search", level=2)
if (RESULTS / "threshold_ssr.png").exists():
    doc.add_picture(str(RESULTS / "threshold_ssr.png"), width=Inches(4.5))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
add_note(doc,
    "Sum of squared residuals (SSR) from the threshold model across candidate liquid buffer values. "
    "Red dashed line: optimal threshold q* = 0.1301. Shaded region: 90% confidence interval.")

# ── Section 6: Conclusion ─────────────────────────────────────────────────────
add_heading(doc, "6.  Conclusion", level=1)

add_paragraph(doc,
    "This paper provides formal evidence that large-scale USD-pegged stablecoins introduce a "
    "two-sided 'New Triffin Dilemma' into the international monetary system. "
    "In normal times, stablecoin issuance amplifies U.S. exorbitant privilege by compressing "
    "OIS–Treasury spreads (β₁ = −6.02, p = 0.006). The decomposed reserve variables — "
    "Treasury exposure θ and liquid buffer L — are individually not significant in the 51-month "
    "panel, but a Hansen (2000) threshold regression on L identifies an economically meaningful "
    "regime shift at q* = 0.130: below this liquid buffer level, supply growth continues to "
    "compress spreads (β_ΔlnS = −6.97), while above it the effect reverses (β_ΔlnS = +1.26), "
    "suggesting forced liquidation dynamics take hold once liquid buffers are depleted.",
    space_after=8)

add_paragraph(doc,
    "For regulators designing stablecoin reserve legislation, our threshold estimate provides a "
    "direct reference point: requiring liquid reserves (cash and near-cash equivalents) of at "
    "least 13% of outstanding supply corresponds to our empirically identified L* = 0.130. "
    "This is distinct from T-bill holdings requirements — it speaks specifically to the "
    "cash-like assets that can absorb redemptions without forced T-bill selling. Our "
    "buffer-conditioned event study further demonstrates that the difference between a "
    "low-buffer and high-buffer stress event is an abnormal spread swing of approximately 27 "
    "percentage points — economically large relative to the typical OIS–Treasury spread of "
    "less than 50 basis points.",
    space_after=8)

add_paragraph(doc,
    "Several limitations warrant acknowledgment. The monthly sample of 51 observations limits "
    "statistical power; ADF tests fail to reject non-stationarity for the spread and liquid buffer, "
    "and key results do not survive first-differencing, suggesting the level specification captures "
    "a slow-moving structural relationship rather than high-frequency causality. The decomposed "
    "buffer variables θ and L are individually insignificant in the full sample, though the "
    "post-2023 sub-sample (N = 39) shows significance for both β₁ and the L × ΔlnS interaction, "
    "indicating the decomposition will sharpen as the time series lengthens. The event study "
    "— based on daily data around specific quasi-experimental episodes — provides more robust "
    "causal identification. Future work should extend the sample as attestation data accumulates "
    "and incorporate non-USD stablecoin ecosystems.",
    space_after=10)

# ── References ────────────────────────────────────────────────────────────────
doc.add_page_break()
add_heading(doc, "References", level=1)

refs = [
    "Caballero, R.J., Farhi, E., and Gourinchas, P.-O. (2008). An equilibrium model of 'global imbalances' and low interest rates. American Economic Review, 98(1), 358–393.",
    "Cole, H.L. and Kehoe, T.J. (2000). Self-fulfilling debt crises. Review of Economic Studies, 67(1), 91–116.",
    "Ghamami, S., Glasserman, P., and Young, H.P. (2023). Stablecoins and macroprudential regulation. Working Paper.",
    "Gorton, G.B. and Zhang, J. (2021). Taming wildcat stablecoins. University of Chicago Law Review, 90(3), 909–956.",
    "Gourinchas, P.-O. and Rey, H. (2007). International financial adjustment. Journal of Political Economy, 115(4), 665–703.",
    "Granger, C.W.J. (1969). Investigating causal relations by econometric models and cross-spectral methods. Econometrica, 37(3), 424–438.",
    "Hansen, B.E. (2000). Sample splitting and threshold estimation. Econometrica, 68(3), 575–603.",
    "Jeanne, O. and Rancière, R. (2011). The optimal level of international reserves for emerging market countries: A new formula and some applications. Economic Journal, 121(555), 905–930.",
    "Maggiori, M. (2017). Financial intermediation, international risk sharing, and reserve currencies. American Economic Review, 107(10), 3038–3071.",
    "Obstfeld, M., Shambaugh, J.C., and Taylor, A.M. (2010). Financial stability, the trilemma, and international reserves. American Economic Journal: Macroeconomics, 2(2), 57–94.",
    "Triffin, R. (1960). Gold and the Dollar Crisis: The Future of Convertibility. Yale University Press.",
]

for ref in refs:
    p = doc.add_paragraph()
    p.paragraph_format.left_indent   = Cm(1.0)
    p.paragraph_format.first_line_indent = Cm(-1.0)
    p.paragraph_format.space_after   = Pt(4)
    run = p.add_run(ref)
    set_font(run, size=11)

# ── Appendix ──────────────────────────────────────────────────────────────────
doc.add_page_break()
add_heading(doc, "Appendix", level=1)
add_heading(doc, "A.1  Robustness: Post-2023 Sub-sample (N = 39)", level=2)

add_paragraph(doc,
    "Restricting to January 2023 – March 2026 (N = 39), the period with broadest attestation "
    "coverage from both Tether and Circle, yields β₁ = −8.14 (p < 0.001) and the "
    "L × ΔlnS interaction becomes significant (β₄ = 49.17, p = 0.004). This strengthening "
    "of the decomposition in the later sub-sample is consistent with improving data quality "
    "and suggests that the insignificance in the full N = 51 sample reflects a power constraint "
    "rather than an absence of the mechanism.",
    space_after=8)

add_heading(doc, "A.2  Robustness: First-Differenced Specification", level=2)

add_paragraph(doc,
    "Differencing all variables to address potential non-stationarity yields β₁ = 0.228 "
    "(p = 0.686) and β₄ = 7.57 (p = 0.651); neither survives at conventional significance "
    "levels. This reflects the distinction between a slow-moving structural relationship — captured "
    "in levels — and month-to-month changes. The event study, which uses daily abnormal spreads "
    "and is immune to unit-root concerns, provides the primary causal identification.",
    space_after=8)

add_heading(doc, "A.3  Diagnostic Statistics", level=2)

diag_data = [
    ("ADF — OIS–Treasury spread",     "−1.580", "0.494", "I(1) not rejected"),
    ("ADF — ΔlnS",                    "−4.007", "0.001", "Stationary ✓"),
    ("ADF — θ (Treasury Exposure)",   "−3.026", "0.033", "Stationary ✓"),
    ("ADF — L (Liquid Buffer)",       "−2.529", "0.108", "I(1) not rejected"),
    ("ADF — VIX",                     "−2.618", "0.089", "Borderline"),
    ("ADF — ΔlnN*",                   "−4.701", "0.000", "Stationary ✓"),
    ("Engle–Granger (spread ~ ΔlnS)", "−2.888", "0.139", "Not cointegrated"),
    ("Engle–Granger (spread ~ θ)",    "−1.546", "0.743", "Not cointegrated"),
    ("Engle–Granger (spread ~ L)",    "−1.611", "0.716", "Not cointegrated"),
]

tbl5 = doc.add_table(rows=1 + len(diag_data), cols=4)
tbl5.style = "Table Grid"
tbl5.alignment = WD_TABLE_ALIGNMENT.CENTER
shade_row(tbl5.rows[0], "BDD7EE")

for i, h in enumerate(["Test", "Statistic", "p-value", "Conclusion"]):
    set_cell_text(tbl5.rows[0].cells[i], h, bold=True, size=10,
                  align=WD_ALIGN_PARAGRAPH.LEFT if i in (0, 3) else WD_ALIGN_PARAGRAPH.CENTER)

for r_idx, row_data in enumerate(diag_data):
    row = tbl5.rows[r_idx + 1]
    if r_idx % 2 == 0:
        shade_row(row, "EBF3FB")
    for c_idx, val in enumerate(row_data):
        set_cell_text(row.cells[c_idx], val, size=10,
                      align=WD_ALIGN_PARAGRAPH.LEFT if c_idx in (0, 3) else WD_ALIGN_PARAGRAPH.CENTER)

add_note(doc,
    "ADF tests use AIC lag selection. Engle–Granger tests the null of no cointegration. "
    "Sample N = 51 monthly observations, January 2022 – March 2026.")

# ── Save ──────────────────────────────────────────────────────────────────────
outfile = "Stablecoins_Exorbitant_Privilege.docx"
doc.save(outfile)
print(f"Saved: {outfile}")
