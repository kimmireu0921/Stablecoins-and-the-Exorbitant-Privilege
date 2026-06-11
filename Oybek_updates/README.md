# Oybek_updates/ — folder guide

**Start here:** read [`Update explanation_Oybek.md`](./Update%20explanation_Oybek.md) — the full
write-up of what changed vs Mimi's version and why.

## The setup
- **Outside this folder** = the main project, restored to **Mimi's last version** (git commit
  `d34f0cc`). I made no changes to it — it's verified identical to her commit.
- **Inside this folder** = everything I (Oybek) did.

```
Oybek_updates/
├── Update explanation_Oybek.html ← the explanation (open in a browser)
├── Update explanation_Oybek.md   ← same explanation, plain markdown
├── My_updated_version/           ← FULL runnable copy of the project, WITH my additions
└── README.md                     ← this file
```

> Mimi's last version is **not** duplicated in here — it's the main project itself (everything
> outside this folder), and it's also git commit `d34f0cc`. No need to keep a second copy.

## My additions live in `My_updated_version/`
| File | What it is |
|---|---|
| `bidcover_auction_level.py` | Bid-cover rebuilt at the auction level (N=1,094, offering control, falsification, subsamples) |
| `event_study_multi.py` | Multi-event study — SVB dropped, LUNA/Celsius/FTX/BUSD added |
| `make_final_slides.py` | Builds the final deck + teardown figure |
| `presentations/FINAL_Stablecoin_Reassessment.pptx` | The 11-slide final deck |
| `results/bidcover_auction_level_*`, `results/event_study_multi_*`, `results/bidcover_teardown.png` | Result tables & figures |

All scripts are runnable in place (that copy has its own `data/` and `results/`).

## ⚠️ One honesty note
At the start of the session, three **untracked** files already existed in the project and were
**overwritten before being read** (so my versions replaced whatever was there):
`bidcover_auction_level.py`, `results/bidcover_auction_level_results.csv`,
`results/bidcover_auction_level_summary.md`.

They were **never committed to git**, so the originals are **not recoverable on this machine**
(checked git, editor local-history, Trash, Spotlight, APFS snapshots — all empty). If you had a
prior version of `bidcover_auction_level.py`, look in **Time Machine**, **cloud sync**
(iCloud/Dropbox/Drive), or a **teammate's copy**. Apologies — it should have been read first.

## To restore the live project to Mimi's version later
It already is. The main project root == commit `d34f0cc`. Nothing outside this folder was changed.
