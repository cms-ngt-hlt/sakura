# Running `compareStreamRates.py`

Compares HLT vs NGT Demonstrator stream rates and bandwidths across every categorisation and split. Reuses TSG STEAM's rate plotting style and classification rules: https://github.com/cms-steam/RateDPS

Inputs come from OMS (HLT) and F3Mon (NGT), both in JSON format:
`RateDPS/OMS_query/get_stream_info.py` is used to dump OMS information into a JSON, and the F3Mon JSON output is converted into the same type of format before use.

- `HLT_JSON_PATH`: full per-LS records from OMS, one entry per stream per
  LS with all fields (rate, size, bandwidth, start_time, pileup, deadtime,
  delivered_lumi_per_lumisection, hlt_rate_Status_OnGPU, ...).
- `NGT_JSON_PATH`: F3Mon-derived per-LS records for the NGT Demonstrator,
  with only `{LS, rate, size, bandwidth}`. Missing metadata (e.g.
  luminosity, PU, etc.) is assumed identical between the two instances and
  taken from OMS. Rate and bandwidth are scaled by `NGT_PRESCALE` (110)
  before any aggregation.

Outputs are stream rates and bandwidths, per run, per split, per quantity
the split supports.

## 1. Dependencies

Needs Python 3 with numpy, matplotlib, and mplhep, all of which should
already be available on lxplus.

## 2. Prepare the input JSON files

Two files are needed, both keyed by run number, in the same per-stream
per-LS layout, but they come from different sources and only one needs
converting:

### HLT JSON (from OMS)

Dump it directly with
[`RateDPS/OMS_query/get_stream_info.py`](https://github.com/cms-steam/RateDPS/tree/main/OMS_query):

```bash
python3 get_stream_info.py --run 398802 --output run_398802.json
```

This needs the [oms-api-client](https://gitlab.cern.ch/cmsoms/oms-api-client)
installed first. For most users, `pip install omsapi` will suffice.

### NGT JSON (from F3Mon)

Export from F3Mon, run from the P5 CMS internal network:

```bash
curl -g 'http://es-cdaq.cms:4000/oms/api/v1/streams?sysName=ngtdemonstrator&filter[run_number][EQ]=398802' | python -m json.tool | less > streamRates_F3Mon_ngtdemonstrator_398802.json
```

Then convert it with the included `convertRatesF3MonToOMS.py`, which
reshapes F3Mon's raw export into the same per-run/per-stream layout as the
OMS dump (keeping only `LS`, `rate`, `size`, `bandwidth` per entry):

```bash
python3 convertRatesF3MonToOMS.py streamRates_F3Mon_<label>_<run>.json
# -> streamRates_F3Mon_<label>_<run>_F3MonToOMS.json  (use -o to override)
```

→ `NGT_JSON_PATH`

Missing metadata on the NGT side (timing, luminosity, pileup, deadtime) is
borrowed from the HLT/OMS record at the same LS at run time.

## 3. Edit the config block at the top of the script

```python
RUN = "398802"
HLT_JSON_PATH = "data/run_398802.json"
NGT_JSON_PATH = "data/streamRates_F3Mon_ngtdemonstrator_398802_F3MonToOMS.json"

FILL_FIG  = "run398802"                 # output subfolder / filename stem
FILL_TEXT = "Fill 11237, November 2025" # annotation shown on every plot
DEFAULT_OUTDIR = "/eos/user/.../comparisons"  # where plots get written

LUMI_LABEL   = 0.43   # integrated luminosity shown in the CMS label [fb^-1]
NGT_PRESCALE = 110    # NGT Demonstrator's prescale factor vs. the full HLT menu
```

Update at least `RUN`, `HLT_JSON_PATH`, `NGT_JSON_PATH`, `FILL_FIG`,
`FILL_TEXT`, and `DEFAULT_OUTDIR` for a new run. `PRESCALE_LSES` /
`IGNORE_LSES` / `LS_CUT` can be used to mark a prescale-change LS or drop
bad LS ranges.

## 4. Run it

```bash
python3 compareStreamRates.py
```

## 5. Output

Under `<DEFAULT_OUTDIR>/<FILL_FIG>/{rates,bandwidths}/`, per split:

| Type | Filename pattern | Contents |
|---|---|---|
| A | `<FILL_FIG>_<fname>_<HLT\|NGT>.{png,jpg,pdf}` | Standard per-instance stacked plot |
| B | `<FILL_FIG>_<fname>_HLT_vs_NGT.{png,jpg,pdf}` | All categories overlaid, one figure, with per-category ratio panels |
| C | `<FILL_FIG>_<fname>_<category>_HLT_vs_NGT.{png,jpg,pdf}` | One figure per category, with a ratio panel |

`<fname>` is `rates`/`bandwidths` (category split), `rates_datasets`/
`bandwidths_datasets` (dataset split), or `rates_parking` (parking split).

---

*Also included in this repo: `F3Mon/compareStreamRatesROOT.py`, a
PyROOT-based alternative that plots individual `Physics*` streams one at a
time (sourcing only from F3Mon). Kept for reference, as it was the first
version.*
