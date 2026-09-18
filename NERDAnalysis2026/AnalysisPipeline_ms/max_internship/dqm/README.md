# DQM workflows

Run DQM through [`04_run_dqm.sh`](../04_run_dqm.sh) after checking production
outputs with `03_check.py`. Each recipe is a shell script executed locally in its
own working directory; step 4 does not submit HTCondor jobs.

## Configure and run

Edit [`pipeline.cfg`](../pipeline.cfg) in the pipeline directory. The checked-in
configuration enables both recipes:

```bash
DQM_CONFIGS=("dqm/scouting.sh" "dqm/hlt.sh")
# For scouting only, use instead:
# DQM_CONFIGS=("dqm/scouting.sh")
```

| Setting | Current behavior |
| --- | --- |
| `EOS_BASE` | Required mounted input directory; inputs live under `<EOS_BASE>/<tag>/run_<run>`. No XRootD input URLs are used by these recipes. |
| `DQM_DEST_BASE` | Required destination for published histogram files. |
| `DQM_WORK_BASE` | Attempt storage; defaults to `DQM_work`. Intermediate ROOT files remain here, so allow sufficient disk space. |
| `CMSSW_SRC` | Required for HLT: release `src` directory containing `DQM/Integration/python/clients/hlt_dqm_sourceclient-live_cfg.py`. |
| `DQM_THREADS` | Positive integer, currently 24; controls scouting DQM processing, not harvesting or the HLT client. |
| `ERA` | Currently `Run3_2026`; used for scouting processing and harvesting. |
| `TAGS`, `GTAGS` | Matching arrays; scouting processing uses the global tag at the selected tag's index. |
| `RUNS` | Runs available to the wrapper, including when using `--run`. |

`EOS_BASE`, `DQM_DEST_BASE`, and `CMSSW_SRC` are blank placeholders in the
checked-in config. Both recipes require an active CMSSW environment. Run
`cmsenv` from the release's `src` directory, then return to the pipeline directory:

```bash
# Every enabled recipe for one tag/run:
bash 04_run_dqm.sh --tag NGT --run 403863

# Every enabled recipe for NGT over every configured run:
bash 04_run_dqm.sh --tag NGT

# Every enabled recipe, tag, and run:
bash 04_run_dqm.sh
```

Choose recipes only through `DQM_CONFIGS` in `pipeline.cfg`; every listed recipe
runs. `--tag` and `--run` must match configured entries. Each filter accepts a
single value, and omitted filters select all entries in that loop. Use `--help`
to display usage.

The wrapper runs recipes in `DQM_CONFIGS` order, then tags in `TAGS` order, then
runs in `RUNS` order. It stops at the first failure. All relative paths in its
configuration are resolved from the pipeline directory. A nonblank `CMSSW_SRC`
must point to an existing directory even when selecting scouting only.

## Inputs and conditions

Both recipes discover files directly in `EOS_BASE/<tag>/run_<run>`:

| Recipe | Exact input filename pattern | Processing |
| --- | --- | --- |
| `scouting` | `<tag>_run<run>_job*_DQMTestDataScouting.root` | `DQM:hltDqmOnlyScouting`, then `HARVESTING:@standardDQM`. |
| `hlt` | `<tag>_run<run>_job*_LocalTestDataRaw.root` | Existing HLT source client copied from `CMSSW_SRC`. |

They require at least one matching file and reject zero-byte inputs. They do
not consult `manifest_<tag>.tsv`, verify that every production job is represented,
or validate ROOT contents before execution. Missing jobs or leftover files from
an older production can therefore affect the result; check production completion
and input-directory contents first. The discovered paths are saved in `inputs.txt`.

Scouting processes all events with the selected `GTAGS` entry. The current mapping
is:

| Input tag | Scouting processing conditions |
| --- | --- |
| `HLT` | `160X_dataRun3_HLT_v1` |
| `Prompt` | `160X_dataRun3_Prompt_v1` |
| `NGT` | `160X_dataRun3_NGT_v6` |

Its four customizations are appended to `dqm.py`: use `hltOnlineMetaDataDigis`,
enable `onlyScouting`, and set the collection and track monitors' beam spots to
`hltOnlineBeamSpotFromDB`.

**Scouting harvesting is fixed to `160X_dataRun3_HLT_v1` in `scouting.sh`.**
`DQM_HARVEST_CONDITIONS` is mentioned in the wrapper's exports, but is not defined
in the checked-in config or read by either supplied recipe. Setting it does not
change harvesting conditions. The HLT recipe passes only `inputFiles` to its
source client; conditions and thread settings come from that client, not from
`GTAGS` or `DQM_THREADS`.

## Outputs and reruns

Each invocation creates a fresh directory:

```text
<DQM_WORK_BASE>/<recipe>/<tag>/run_<run>/attempt_XXXXXX/
```

The wrapper prints its location and copies the executed script to `recipe.sh`.
Artifacts depend on the recipe:

| Recipe | Files retained in the attempt directory |
| --- | --- |
| `scouting` | `recipe.sh`, `inputs.txt`, `dqm.py`, `dqm.log`, `step2.root` (DQMIO), `harvesting.py`, `harvesting.log`, the harvested `DQM*.root`, and `result.root`. |
| `hlt` | `recipe.sh`, `inputs.txt`, `client.py`, `dqm.log`, `upload/*.root`, and `result.root`. |

Failed attempts retain whatever was created before the failure. `cmsRun` output
is redirected to the listed logs; `cmsDriver.py` output goes to the terminal.
Scouting requires exactly one harvested `DQM*.root`; HLT requires exactly one
`upload/*.root`. The recipe copies that file to `result.root`.

After checking that `result.root` is nonempty, the wrapper copies it to a temporary
file in the destination directory and renames it to the final path:

```text
<DQM_DEST_BASE>/scouting/NGT/DQM_scouting_R000403863.root
<DQM_DEST_BASE>/hlt/NGT/DQM_hlt_R000403863.root
```

Run numbers are padded to nine digits. A successful rerun replaces the previous
result for that recipe/tag/run; a recipe failure leaves any previous published
result in place. The wrapper neither skips completed results nor cleans attempt
directories. Use filters to rerun the failed selection without reprocessing
all earlier combinations.

## Troubleshooting and plotting

- **Environment or path error:** activate `cmsenv`, fill the required paths, and
  check mounted EOS access. For HLT, verify that the source-client config exists
  under `CMSSW_SRC`.
- **No matching or empty inputs:** check the selected tag/run directory and the
  filename patterns above against production outputs and the step 3 report.
- **Recipe failure:** inspect `dqm.log`; for scouting harvesting failures also
  inspect `harvesting.log`. If config generation failed, inspect the terminal
  output and any generated config in the attempt directory.
- **Missing or multiple final outputs:** inspect the harvested `DQM*.root` or HLT
  `upload/` directory and the corresponding log. `step2.root` is intermediate
  DQMIO, not the final histogram file for plotting.

Point `conditions[].path` in [`plotting/config.yaml`](../plotting/config.yaml) at
`<DQM_DEST_BASE>/scouting/<tag>` for each condition, preferably using absolute
paths, and run plot entry scripts from `plotting/`. Paths are relative to the
plotting process's working directory, and every `*.root` file in each condition
directory is included. Check that compared tags cover the same intended runs.
See the [main README](../readme.md#5-plot-scouting-results) for dependencies and the
legacy event-counter directory requirements.

`summarize_logs.py` still expects the old `dqmclient_<tag>_DQMTestDataScouting_run<run>.log`
naming and source-client log format; it is not adapted to these attempt logs.

## Add a recipe

Create a shell script and add its path to `DQM_CONFIGS`. Use a unique basename:
that name becomes the output-directory component. The wrapper
copies only the script into the attempt directory and invokes it with `bash`, so
resolve any additional dependencies explicitly rather than assuming the original
recipe directory is the working directory.

The wrapper supplies these environment variables:

| Variable | Value |
| --- | --- |
| `LOCALPATH` | Absolute `EOS_BASE/<tag>/run_<run>` input directory. |
| `TAG`, `RUN` | Current tag and run. |
| `GTAG` | Corresponding entry in `GTAGS`. |
| `ERA`, `DQM_THREADS` | Values from `pipeline.cfg`. |
| `CMSSW_SRC` | Absolute source directory when configured. |

A recipe should fail with a nonzero exit code on errors and leave a nonempty
`result.root` in its working directory on success. Save an input list and logs as
the supplied recipes do. The wrapper handles publication; no JSON manifest or
Python runner is required.
