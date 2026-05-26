"""
add_notes.py — adds speaker notes to the existing pptx pulled from GitHub.
Run once: python add_notes.py
"""

from pptx import Presentation
from pathlib import Path

PATH = Path("presentations/0526_Stablecoin_Exorbitant_Privilege.pptx")

SCRIPTS = {
    1: (
        "Good afternoon everyone. Our paper is called Stablecoins and the Exorbitant Privilege. "
        "The central argument is that large USD-pegged stablecoin issuers — mainly Tether and Circle — "
        "have become significant buyers of U.S. Treasury bills. "
        "In normal times, that deepens demand for safe assets and amplifies America's borrowing advantage. "
        "But when a run hits and their cash reserves are too thin, they are forced to liquidate T-bills, "
        "which rapidly reverses that benefit. "
        "Today we want to address some methodological questions from last session "
        "and walk clearly through our three stress events."
    ),
    2: (
        "Let me quickly orient everyone. On the left is everything we have completed. "
        "We extended Maggiori's 2017 model to incorporate stablecoin supply, treasury exposure, and the liquid buffer. "
        "Our main regression finds that a one standard deviation increase in stablecoin supply "
        "compresses the OIS-Treasury spread by roughly 6 basis points — that is the privilege amplification result. "
        "We also estimated a safety threshold using Hansen's 2000 threshold regression: "
        "issuers need to hold at least 13 percent of supply in liquid cash to stay outside the fragility zone. "
        "And we ran a buffer-conditioned event study across three stress episodes, "
        "which produced a 27 percentage point swing between the low and high buffer regimes. "
        "This deck specifically addresses the clarification questions from last time — "
        "why we use the OIS spread, what the buffer condition actually means, and how to read the CAR graphs. "
        "Baptiste will walk us through this slide, then hand over to Sara."
    ),
    3: (
        "A question came up about why we use the OIS-Treasury spread instead of just Treasury yields. "
        "Here is the intuition. A raw T-bill yield moves for two completely different reasons at the same time — "
        "the Fed raising or cutting rates, and investors specifically wanting to hold safe Treasuries. "
        "We only care about the second one. "
        "The OIS rate tracks market expectations of the Fed Funds path — it is pure monetary policy. "
        "So when we subtract it from the T-bill yield, we cancel out the monetary policy component "
        "and are left with just the premium investors pay to hold Treasuries specifically. "
        "That premium is exactly what stablecoin issuers affect when they buy T-bills. "
        "This approach is well established in the literature. "
        "Krishnamurthy and Vissing-Jorgensen in 2012 use this same spread to measure safe-asset demand. "
        "Nagel in 2016 calls it the convenience yield of near-money assets. "
        "Greenwood, Hanson and Stein in 2015 show it captures demand that is insensitive to monetary policy. "
        "The practical point is this: if we had used raw yields, "
        "a Fed rate cut and a Tether buying surge would look identical in our data. "
        "The spread cleanly separates them."
    ),
    4: (
        "Now let me explain precisely what the buffer condition is, because it is the central variable in our paper. "
        "L is the liquid buffer — the share of an issuer's reserves held in cash or cash equivalents, "
        "divided by total stablecoin supply. "
        "Our Hansen threshold regression estimates a critical cutoff at 13 percent. "
        "Here is why it matters. When investors redeem stablecoins for dollars, the issuer has to pay them back. "
        "If they hold enough cash — above 13 percent — they pay from cash and T-bill holdings are untouched. "
        "The Treasury market feels nothing. "
        "But if the cash buffer is below 13 percent, the issuer cannot cover redemptions from cash alone. "
        "They have to sell Treasury bills quickly to raise the dollars. "
        "That sudden selling pushes T-bill yields up relative to OIS — the spread spikes. "
        "In May 2022, Tether had only around 5 to 8 percent in liquid cash — below the threshold. "
        "That is why both the LUNA contagion and the direct Tether depeg produced large positive CARs. "
        "The buffer condition is what separates an issuer that stabilises Treasury markets from one that disrupts them."
    ),
    5: (
        "CAR stands for Cumulative Abnormal Return — but in our context it measures the cumulative abnormal spread, "
        "not a stock return. Let me explain what the y-axis actually means. "
        "Before each crisis, we estimate how the OIS-Treasury spread normally behaves "
        "using data from around six months prior. We build a model that says: "
        "given today's VIX level and global equity returns, what would we expect the spread to be? "
        "The abnormal spread on any given day is the actual spread minus that prediction. "
        "CAR is the running total of those daily abnormal spreads from five days before the event onward. "
        "A positive CAR means the spread has been persistently higher than expected — T-bill selling pressure. "
        "A negative CAR means it has been persistently lower than expected — flight-to-safety buying. "
        "A flat line at zero would mean the event had no effect on Treasury markets at all. "
        "Now, the second event shown here is the USDT partial depeg on May 12th, 2022 — "
        "three days after the LUNA collapse. "
        "This was a direct bank-run on Tether itself. USDT briefly fell to 95 cents. "
        "Unlike UST, which was algorithmic with no real reserves, Tether holds actual assets. "
        "The problem was that Tether's cash was only 5 to 8 percent of its reserves — the rest was T-bills. "
        "When over 7 billion dollars of USDT was redeemed in a single day, "
        "Tether had to sell T-bills to pay out, and the spread spiked. "
        "The CAR came in at plus 8.85 percentage points — essentially identical to the LUNA event. "
        "Same buffer, same constraint, same outcome — regardless of what triggered the run."
    ),
    6: (
        "Our third event is the SVB failure in March 2023, and the graph needs careful explanation "
        "because the CAR goes deeply negative instead of spiking upward like 2022. "
        "SVB collapsed on March 10th — the second largest U.S. bank failure in history. "
        "Circle disclosed that 3.3 billion dollars of USDC reserves were held at SVB and temporarily inaccessible. "
        "USDC depegged to around 87 cents — a larger nominal depeg than Tether in 2022. "
        "So why does the CAR go to minus 18 instead of spiking? Two forces explain it, and both are on this slide. "
        "Force A is about government intervention. "
        "U.S. regulators guaranteed all SVB deposits within 72 hours of the collapse. "
        "Because of that guarantee, Circle never needed to sell a single Treasury bill "
        "to cover the 3.3 billion that was temporarily frozen. "
        "The crisis was resolved before any forced liquidation became necessary. "
        "So unlike 2022, there was no issuer-side selling pressure on the T-bill market. "
        "If that were the whole story, the CAR would be flat — near zero. "
        "But Force B is what actually drives the CAR negative. "
        "SVB's collapse triggered a massive market-wide flight to safety. "
        "Investors across the entire financial system rushed to buy U.S. Treasury bills — "
        "the safest short-term asset available. "
        "That buying pressure pushed T-bill yields sharply below OIS, "
        "compressing the spread far below what our normal model predicted. "
        "The net effect of Force A — no selling — plus Force B — active buying — "
        "is a CAR of minus 18 percentage points. "
        "The graph is negative, not flat, because the crisis still moved Treasury markets, "
        "just in the opposite direction from 2022. "
        "And the 27 percentage point swing between regimes, with a Welch t of 15.22, "
        "is the core empirical finding of our paper."
    ),
    7: (
        "So where does that leave us? Everything on the left is completed and presented today. "
        "For next week, we are running a placebo test to validate our event study results. "
        "The idea is simple: if our methodology is sound, then running the same event study "
        "on three ordinary, uneventful days with the same buffer conditions should produce CARs near zero. "
        "We picked June 15th 2021 and October 12th 2021 as low-buffer placebos — "
        "quiet periods before LUNA with no stablecoin stress. "
        "And July 15th 2025 as a high-buffer placebo — a stable period well after the SVB recovery. "
        "Our preliminary result already shows the placebo mean absolute CAR is just 0.55 percentage points, "
        "compared to 11.92 for the actual events. "
        "That is a 21.7 times difference. "
        "This directly answers the question of whether our large CARs could just be random market noise — "
        "they cannot. They only appear on real crisis days."
    ),
    8: (
        "Thank you for your time. "
        "To summarize in two sentences: stablecoin issuers have become structurally important buyers "
        "of U.S. Treasury bills, which deepens America's safe-asset privilege in normal times. "
        "But when their liquid cash buffers fall below roughly 13 percent of supply, "
        "a run forces them to liquidate T-bills — turning a privilege amplifier into a systemic disruptor. "
        "We are happy to take any questions."
    ),
}


def set_notes(slide, text: str):
    notes_slide = slide.notes_slide
    notes_slide.notes_text_frame.text = text


prs = Presentation(str(PATH))

if len(prs.slides) != len(SCRIPTS):
    print(f"WARNING: {len(prs.slides)} slides in file but {len(SCRIPTS)} scripts written. Check counts.")

for i, slide in enumerate(prs.slides, 1):
    if i in SCRIPTS:
        set_notes(slide, SCRIPTS[i])
        print(f"  Slide {i}: notes added ({len(SCRIPTS[i])} chars)")
    else:
        print(f"  Slide {i}: no script defined — skipped")

prs.save(str(PATH))
print(f"\nSaved: {PATH}")
