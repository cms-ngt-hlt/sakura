# Condition upload latency — NGT demonstrator vs prompt/PCL tags

How long after (or before) the end of a CMS run a condition is in the database,
measured from the conddb tag dumps in the parent directory. Four tags are filled
by the NGT demonstrator loop, two prompt/PCL tags are included for comparison.

| tag dump | workflow | filled by | since | notes |
|---|---|---|---|---|
| `BeamSpot_NGTDemonstrator.txt` | Beam spot | NGT demonstrator | run : LS | |
| `EcalPedestals_NGTDemonstrator.txt` | ECAL pedestals | NGT demonstrator | run | |
| `SiStripQuality_NGTDemonstrator.txt` | Strip bad components | NGT demonstrator | run | |
| `SiStripDetVOff_NGTDemonstrator.txt` | Strip DetVOff | NGT demonstrator (HV O2O) | run : LS | uploads at :15 / :45 |
| `EcalLaserAPDPNRatios_prompt_v3_inRunLSIoVs.txt` | ECAL laser APD/PN | prompt O2O | run : LS | uploads at :00 / :30 |
| `SiPixelAliHLTHGCombined_PCL_v0_hlt.txt` | Pixel alignment HLT HG combined | PCL (Tier-0) | run | one payload per run |

"NGT combined" in the tables and figures is the union of the first four.

## What is measured

Every dump lists the payloads inserted into a tag with their *since* and their
insertion time. `runs.txt` gives start and end of every CMS run. Both are taken
to be UTC: no upload precedes its run start, and the earliest offset is ≈ 1 h in
February as well as in May, which excludes a CET/CEST mismatch.

Per (workflow, run) two records are formed and each is referenced to both run
boundaries:

    run start ─────────────── run end
        │<─ first_from_start ─┼─>│  first upload  (negative from the end = during the run)
        │<─── last_from_start ┼────────>│  last upload

| quantity | definition |
|---|---|
| **first upload** | earliest insertion of a payload whose since is that run |
| **last upload** | latest insertion of a payload whose since is that run |
| `*_from_start_h` | insertion − run start: how old is the oldest data used |
| `*_from_end_h` | insertion − run end: negative means delivered while the run was still ongoing |

Selection: the run must exist in `runs.txt`, and the insertion must be within
48 h of the run end (same window as the PCL analysis in
`~/NGT/3.4/db/stitch/analysis`). Dropped uploads are in `out/dropped.csv`:

| workflow | in file | used | dropped | why |
|---|---:|---:|---:|---|
| Beam spot | 526 uploads / 10 runs | 526 / 10 | 0 | |
| ECAL pedestals | 508 / 104 | 455 / 53 | 53 | 51 = tag bootstrap of 2025-10-24 08:40:18 (one timestamp for runs 390000–398365, 30 of them not in `runs.txt`) + since=1; 2 = run 398860 re-uploaded on 2026-02-10/11 |
| Strip bad components | 663 / 46 | 660 / 45 | 3 | since=1; run 403392 re-uploaded 52 h late |
| Strip DetVOff | 1474 / 367 | 1118 / 290 | 356 | since=0; 242 = back-fill of January–February runs on 2026-02-22/23; 80 = re-uploads on 2026-03-25 and 03-31; a few more in May/June |
| ECAL laser APD/PN | 6113 / 1992 | 5511 / 1732 | 602 | since=0; 43 = batch of 2025-10-27; 558 = back-fill of 2025 runs on 2026-02-13 |
| Pixel ali. HLT HG comb. | 564 / 523 | 559 / 523 | 5 | five re-uploads 2–3 days late |

Runs used: 391670–404950 (2025-05-05 to 2026-06-16); the demonstrator tags
cover 398647–404927 (2025-10-28 to 2026-06-16).

## Headline numbers

One entry per run. Medians, with the 16–84 % range of runs in brackets.
"≤ x h" is the fraction of runs whose upload is in the database at most x h
after the run end (Tiny 1 h / Small 3 h / Medium 6 h / Large 12 h budgets).

### Analysis 1 — first upload of the run

| workflow | runs | from run start | from run end | before run end | ≤ 1 h | ≤ 3 h | ≤ 6 h | ≤ 12 h |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Beam spot (NGT, by LS) | 10 | 3.8 h [1.4, 7.4] | +2.7 h [−6.7, +6.1] | 30 % | 40 % | 60 % | 80 % | 90 % |
| ECAL pedestals (NGT) | 53 | 1.9 h [1.7, 5.6] | −1.7 h [−7.3, +2.0] | 68 % | 77 % | 91 % | 98 % | 100 % |
| Strip bad components (NGT) | 45 | 2.1 h [1.2, 5.8] | −0.1 h [−8.0, +4.5] | 56 % | 69 % | 78 % | 93 % | 98 % |
| Strip DetVOff (NGT, by LS) | 290 | 2.3 h [1.6, 4.1] | +1.4 h [−1.9, +2.1] | 24 % | 33 % | 96 % | 96 % | 97 % |
| **NGT combined** | 398 | **2.2 h** [1.6, 5.0] | **+1.3 h** [−3.7, +2.2] | **34 %** | 43 % | 92 % | 96 % | 97 % |
| ECAL laser APD/PN (prompt O2O, by LS) | 1732 | 2.1 h [1.4, 3.2] | +1.3 h [+0.5, +2.5] | 13 % | 33 % | 86 % | 90 % | 94 % |
| Pixel ali. HLT HG comb. (PCL) | 523 | 12.1 h [6.7, 19.0] | +8.3 h [+3.4, +12.7] | 0 % | 5 % | 15 % | 30 % | 77 % |

### Analysis 2 — last upload of the run

| workflow | runs | from run start | from run end | before run end | ≤ 1 h | ≤ 3 h | ≤ 6 h | ≤ 12 h |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Beam spot (NGT, by LS) | 10 | 9.5 h [8.1, 21.5] | +6.6 h [+1.2, +19.3] | 20 % | 20 % | 30 % | 50 % | 70 % |
| ECAL pedestals (NGT) | 53 | 8.0 h [3.6, 8.2] | +1.0 h [−1.4, +4.1] | 28 % | 49 % | 77 % | 92 % | 98 % |
| Strip bad components (NGT) | 45 | 8.1 h [3.3, 9.5] | +2.8 h [−1.3, +9.1] | 22 % | 36 % | 51 % | 76 % | 91 % |
| Strip DetVOff (NGT, by LS) | 290 | 2.7 h [1.9, 9.0] | +1.8 h [+0.6, +2.7] | 13 % | 19 % | 84 % | 90 % | 94 % |
| **NGT combined** | 398 | **3.4 h** [2.0, 8.7] | **+1.8 h** [−0.1, +4.4] | **17 %** | 25 % | 78 % | 88 % | 94 % |
| ECAL laser APD/PN (prompt O2O, by LS) | 1732 | 2.5 h [1.5, 8.0] | +1.7 h [+1.2, +3.3] | 0 % | 8 % | 83 % | 88 % | 94 % |
| Pixel ali. HLT HG comb. (PCL) | 523 | 12.1 h [6.7, 19.3] | +8.3 h [+3.4, +13.0] | 0 % | 5 % | 15 % | 30 % | 77 % |

### Median and mean per workflow

Same content as `fig7_decomposition` / `fig7_decomposition_from_start` (the
analogue of the PCL `fig1_decomposition`): the stacked bars are the means, which
are additive (mean last = mean first + mean first→last span); the markers are
the medians with their 16–84 % bands. Also in `out/median_mean_table.csv`.

| workflow | runs | first, from start<br>median / mean | first, from end<br>median / mean | last, from start<br>median / mean | last, from end<br>median / mean |
|---|---:|---:|---:|---:|---:|
| Beam spot (NGT, by LS) | 10 | 3.84 / 5.85 h | +2.65 / +1.41 h | 9.48 / 13.04 h | +6.56 / +8.60 h |
| ECAL pedestals (NGT) | 53 | 1.94 / 3.22 h | −1.67 / −2.57 h | 8.03 / 7.27 h | +1.05 / +1.48 h |
| Strip bad components (NGT) | 45 | 2.11 / 3.98 h | −0.13 / −0.50 h | 8.09 / 9.67 h | +2.82 / +5.20 h |
| Strip DetVOff (NGT, by LS) | 290 | 2.26 / 4.09 h | +1.43 / +1.29 h | 2.66 / 5.65 h | +1.81 / +2.84 h |
| **NGT combined** | 398 | **2.24 / 4.01 h** | **+1.30 / +0.57 h** | **3.40 / 6.50 h** | **+1.80 / +3.07 h** |
| ECAL laser APD/PN (prompt O2O, by LS) | 1732 | 2.08 / 3.90 h | +1.34 / +2.48 h | 2.52 / 5.04 h | +1.75 / +3.62 h |
| Pixel ali. HLT HG comb. (PCL) | 523 | 12.14 / 12.77 h | +8.34 / +8.25 h | 12.14 / 13.15 h | +8.34 / +8.63 h |

Where the mean differs from the median the tail is the cause: for the first
upload a handful of runs whose first payload came 7–20 h late (beam spot
403751, ECAL pedestals 398647, strips 401121–401139 and 403410, and the 5–6 % of
DetVOff and laser runs whose payloads were inserted more than 12 h late); for the
last upload the next-day beam-spot re-uploads and the 2026-05-02 strip batch.
From the run end the *mean* first-upload latency of the pedestals and bad
components is below the median because the long runs, whose first payload
arrives 10–15 h before the end, weigh more in the mean than the 1–2 h late
starts do.

## What the data says

**The calibration loop streams during the run.** For ECAL pedestals and strip
bad components the first payload lands 1–2 h after the run starts (never earlier
than ≈ 1 h) and further payloads follow every ≈ 12 min. 74 % of the pedestal
uploads and 52 % of the bad-component uploads are inserted before the run has
ended, and for 68 % / 56 % of the runs the first condition exists before the run
is over. Referenced to the run end the first-upload latency of these two is
*negative* on average. The PCL pixel alignment in the same period needs
+8.3 h after the run end (median; the 2025 bookkeeping analysis gave 9.2 h for
this workflow), never delivers during the run, and 70 % of its payloads miss the
Medium budget.

**Uploads of the calibration loop stop 8.1 h after the start of the run.** For
every pedestal or bad-component run longer than 9 h (11 + 9 runs) the last upload
is at 8.08–8.20 h after run start, whatever the run duration (up to 16.4 h). The
"last upload" statistics of these two workflows for long runs therefore measure
this cut-off, not the loop's latency, and the last part of long fills is not
covered. For runs shorter than 7 h the last upload comes 1.9 h (pedestals) /
4.2 h (bad components) after the run end; that is the real processing tail.
Whether the 8 h is a job wall-time, an input-stream limit or a configuration is
not derivable from these files. The O2O-type tags (DetVOff, laser) do not show
the cut-off: their last upload tracks the run end (fig 6).

**The two O2Os are clock-driven.** Strip DetVOff inserts at :15 and :45, the ECAL
laser at :00 and :30 (every 30 min; a laser run with ≥ 2 uploads has a median gap
of exactly 30 min). Their first-upload latency from the run end is +1.4 h and
+1.3 h, remarkably alike, and 96 % / 86 % of the runs are covered within 3 h of
the end. Because their runs are short (median 1.0 h and 0.45 h) only 24 % / 13 %
of the first uploads land before the run ends. Both have a 5–6 % tail of runs
whose payloads were inserted more than 12 h late (back-fills).

**The beam spot sample is small and contaminated.** 10 runs only, all in
2026-05-11 to 05-17. Runs 403747/403748/403751 (the first day) got 12 further
payloads on the morning of 2026-05-12, 16–24 h after their end, and run 403895
(44 min long) received 340 per-LS payloads over 5 h. The beam-spot "last upload"
medians are dominated by these; the first-upload numbers, and better the per-LS
numbers below, are the reliable ones for this workflow.

**Other late batches** (within the 48 h window, so kept): on 2026-05-02 19:00–20:30
eight bad-component payloads for runs 403410–403421 and two pedestal payloads for
403421 were re-inserted 30–40 h after the runs. Removing everything later than
24 h after the run end moves the bad-component last-upload median from +2.8 h to
+1.9 h after run end and leaves the others unchanged.

**Uploads per run** scale with run length for the loop workflows: median 8
(pedestals), 15 (bad components), 13 (beam spot) per run, up to ≈ 20 for an 8 h
run; the first → last upload span is ≈ 6 h for any run longer than 6 h, again the
8 h cut-off minus the ≈ 2 h warm-up. DetVOff has 3 uploads per run (median), the
laser 2, the PCL alignment exactly 1.

## Margin to the demonstrator timeout (8 h after run start)

The demonstrator has an 8 h timeout. `fig10_margin_to_timeout` recasts the
run-level latencies as the margin to that deadline, 8 h − (upload − reference),
with the **first** upload measured against 8 h after the run **start** and the
**last** upload against 8 h after the run **end**. The curves show the fraction
of runs with at least x hours of margin; the value at x = 0 is the fraction of
runs whose payload arrived in time. Beam spot excluded; "NGT combined" here is
pedestals + bad components + DetVOff. Table in `out/margin_to_timeout.csv`.

| workflow | runs | first upload vs start + 8 h: median margin | in time | ≥ 3 h margin | last upload vs end + 8 h: median margin | in time | ≥ 3 h margin |
|---|---:|---:|---:|---:|---:|---:|---:|
| ECAL pedestals (NGT) | 53 | +6.1 h | 96 % | 81 % | +7.0 h | 98 % | 89 % |
| Strip bad components (NGT) | 45 | +5.9 h | 93 % | 80 % | +5.2 h | 82 % | 64 % |
| Strip DetVOff (NGT, by LS) | 290 | +5.7 h | 91 % | 86 % | +6.2 h | 92 % | 89 % |
| **NGT combined (no beam spot)** | 388 | **+5.8 h** | **92 %** | 85 % | **+6.2 h** | **92 %** | 86 % |
| ECAL laser APD/PN (prompt O2O, by LS) | 1732 | +5.9 h | 90 % | 87 % | +6.3 h | 90 % | 87 % |
| Pixel ali. HLT HG comb. (PCL) | 523 | −4.1 h | 22 % | 9 % | −0.3 h | 47 % | 23 % |

The first upload of the calibration loop makes its deadline for 93–96 % of the
runs with ≈ 6 h to spare; the PCL alignment makes it for 22 %. Against run end
+ 8 h the last upload of the demonstrator tags is in time for 92 % of the runs
with ≈ 6 h of margin. The pedestals are in time for 98 %; the bad components
for 82 %, the misses being the 2026-05-02 re-upload batch (runs 403410–403421,
30–40 h late) and a few February runs. The two O2Os are in time for 90–92 %,
the misses being back-filled runs. The PCL alignment straddles this deadline:
47 % in time, median margin −0.3 h.

The 8.08–8.20 h stop of the loop (fig 6) does not enter here: it is 8 h after
the run *start*, and only matters for the first-upload panel of runs longer
than 8 h, where 2 pedestal and 3 bad-component runs miss the deadline.

## Latency per lumisection (by-LS tags)

The beam spot, DetVOff and laser payloads carry a (run, LS) since, so for these
the latency can be measured against the data actually used rather than against
the run boundaries. The lumisection is taken to be acquired at

    LS time = run start + LS × 23.31 s        (2^18 orbits × 88.924 µs)

and the latency is *first upload for that (run, LS)* − LS time.

| workflow | LS / runs / uploads | median / mean | 16–84 % | min | max | LS < 12 h: n, median / mean |
|---|---:|---:|---:|---:|---:|---:|
| Beam spot (NGT) | 50 / 10 / 526 | 4.8 / 6.0 h | 2.7–7.5 h | 0.76 h | 24.4 h | 46, 3.9 / 4.6 h |
| Strip DetVOff (NGT) | 1103 / 290 / 1118 | 2.0 / 4.7 h | 1.5–4.7 h | 1.26 h | 46.9 h | 1000, 2.0 / 2.4 h |
| ECAL laser APD/PN (prompt O2O) | 4234 / 1732 / 5511 | 2.3 / 4.7 h | 1.7–4.0 h | 0.60 h | 50.7 h | 3867, 2.2 / 2.6 h |

Beam spot: the 526 uploads collapse to 50 distinct (run, LS) pairs: the same
since is re-uploaded many times (up to 340 uploads for the 18 LS of run 403895),
and the sinces only cover the first ≈ 2 h of the long runs (403775: LS 2–313 of
1850, 403818: LS 35–66 of 1992) although uploads continue for hours afterwards.
Per run the medians range from 0.9 h (403774) and 2.5–2.9 h (403775, 403818,
403937) to 5.4–7.4 h (403811, 403894, 403895) and 18–22 h for the first-day runs
403747/403748/403751 whose payloads were re-inserted on 2026-05-12. Within a run
the latency is not ordered by LS: in 403895 the LS 50–63 arrived after 2.8 h
while LS 34–48 and 55–56 took 5–8 h. The shortest latency for any lumisection is
46 min.

DetVOff and laser: one upload per LS as expected for an O2O (1118 uploads for
1103 LS; 5511 for 4234). The bulk sits at 1.3–4 h with the 30-min cron visible
as the width of the core; the mean is pulled to 4.7 h by the back-filled runs.
100 of the 1103 DetVOff sinces and 15 of the 4234 laser sinces point to a LS
beyond the run end as computed from `runs.txt`: the O2O assigns LS numbers from
HV / laser timestamps, so transitions after the last LS are booked under the
same run with extrapolated LS numbers. Those entries are kept.

### ECAL laser: every upload against the lumisection it covers

`fig11_ecallaser_upload_delay` shows, for every laser upload, its delay to the
lumisection at which its IOV starts. Of the 5511 uploads, 1275 re-insert a
payload hash that was already in the tag for the same since, one cron tick
(30 min) after the first insertion: repeats of the O2O, not new conditions, and
removed from the figure. The 4236 remaining uploads cover 4234 (run, LS) pairs;
only two sinces ever received a second, different payload (402240:3 after 41 h,
403634:1318 after 2.4 h).

| | uploads | median | mean | 16–84 % |
|---|---:|---:|---:|---:|
| uploads, repeated hashes removed | 4236 | 2.25 h | 4.67 h | 1.68–3.97 h |
| of which below 12 h (91 %) | 3868 | 2.19 h | 2.58 h | |
| (repeated-hash uploads, for reference) | 1275 | 2.72 h | | 2.16–3.47 h |

The delay does not depend on where in the run the lumisection sits: the median
is 2.1 h for LS in the first 30 min of a run and 2.4 h for LS 4–24 h into the
run. The core of the distribution is 1.7–3.0 h wide, the 30-min cron period
plus the laser sequence and processing; the shortest delay is 36 min. The 9 %
above 12 h are the back-filled runs.

Figures: `fig8_perls_latency_<wf>` for the three tags; `fig9_perls_timeline_BeamSpot`
(per run, each LS drawn from its acquisition to its first upload; not drawn for
the two tags with hundreds of runs). Tables: `out/perls_<wf>.csv`.

## Files

| | |
|---|---|
| `analyze_uploads.py` | parses the dumps, writes `out/uploads_<wf>.csv`, `out/perrun_<wf>.csv`, `out/perrun_all.csv`, `out/summary.csv`, `out/summary.json`, `out/dropped.csv`, `out/median_mean_table.csv`, `out/perls_<wf>.csv` |
| `make_figures.py` | figures below (PNG 300 dpi + PDF in `figs/`); also writes `out/margin_to_timeout.csv` |

| figure | content |
|---|---|
| `fig1_timeline_<wf>` | every run as a row: run duration, all uploads, first (●) and last (■) upload, time since run start (only for the three tags with ≤ 150 runs) |
| `fig2_cdf_first`, `fig2_cdf_last` | cumulative fraction of runs with the first / last upload vs time, from run start and from run end, with the Tiny/Small/Medium/Large budgets |
| `fig3_summary_first_vs_last` | median, 16–84 % band and mean per workflow for first and last upload, both references |
| `fig4_histograms` | 2×2 normalised histograms: first/last × from start/from end |
| `fig5_cadence` | uploads per run vs run duration, gap between consecutive uploads, first→last span vs run duration |
| `fig6_latency_vs_duration` | first and last upload vs run duration: shows the in-run delivery and the 8.1 h stop |
| `fig7_decomposition`, `fig7_decomposition_from_start` | PCL-style decomposition: stacked means (reference → first upload, first → last upload) with the medians and 16–84 % bands overlaid; from run end and from run start |
| `fig8_perls_latency_<wf>` | by-LS tags: latency of each lumisection (LS acquired → first upload of that LS) vs acquisition time, and its distribution |
| `fig9_perls_timeline_BeamSpot` | beam spot: per run, every LS from its acquisition to its first upload |
| `fig11_ecallaser_upload_delay` | ECAL laser: delay of every upload to the lumisection its IOV starts at, vs time, as a fine histogram, and vs the position of the LS in the run |
| `fig10_margin_to_timeout` | all tags but the beam spot: fraction of runs with at least x h of margin to the 8 h timeout; first upload vs run start + 8 h, last upload vs run end + 8 h |

Regenerate:

    python3 analyze_uploads.py && python3 make_figures.py
