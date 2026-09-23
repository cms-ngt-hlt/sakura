# DQM workflows

Run DQM through [`04_run_dqm.sh`](../04_run_dqm.sh) after checking production
outputs with `03_check.py`. Each recipe is a shell script executed in its own
working directory, either on the submit node one recipe/tag/run at a time
(`DQM_BACKEND="local"`) or as one HTCondor job per recipe/tag/run
(`DQM_BACKEND="condor"`, the checked-in default). Both backends give the recipe
the same environment and expect the same `result.root`, so a recipe does not
need to know which one runs it.

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
| `DQM_WORK_BASE` | Attempt storage for the local backend; defaults to `DQM_work`. Intermediate ROOT files remain here, so allow sufficient disk space. |
| `CMSSW_SRC` | Required for HLT: release `src` directory containing `DQM/Integration/python/clients/hlt_dqm_sourceclient-live_cfg.py`. Required by every recipe on the HTCondor backend, which sets up the release itself. |
| `DQM_THREADS` | Positive integer, currently 24; controls scouting DQM processing, not harvesting or the HLT client. |
| `ERA` | Currently `Run3_2026`; used for scouting processing and harvesting. |
| `TAGS`, `GTAGS` | Matching arrays; scouting processing uses the global tag at the selected tag's index. |
| `RUNS` | Runs available to the wrapper, including when using `--run`. |
| `DQM_BACKEND` | `condor` (one job per recipe/tag/run) or `local` (sequential). |
| `DQM_SUBMIT` | `condor`: submit immediately, or only write the submission files. |
| `DQM_JOBS_BASE` | Job scripts, Condor logs, and copied-back artifacts; defaults to `DQM_jobs`. |
| `DQM_JOB_FLAVOUR`, `DQM_REQUEST_CPUS`, `DQM_REQUEST_MEMORY_MB`, `DQM_REQUEST_DISK_KB` | Per-job Condor resources. `DQM_REQUEST_CPUS` defaults to `DQM_THREADS`; a large request queues for longer, so lower it (and `DQM_THREADS` with it) if the jobs wait. |
| `DQM_KEEP_ROOT` | `true` also copies the intermediate ROOT files back into the job directory. |

`EOS_BASE`, `DQM_DEST_BASE`, and `CMSSW_SRC` are blank placeholders in the
checked-in config. The local backend requires an active CMSSW environment: run
`cmsenv` from the release's `src` directory, then return to the pipeline
directory. The HTCondor backend only generates and submits, so it needs
`CMSSW_SRC` instead of `cmsenv`; each worker sets up that release itself.

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
single value, and omitted filters select all entries in that loop. `--local`,
`--condor`, `--submit` and `--no-submit` override `DQM_BACKEND` and `DQM_SUBMIT`
for one invocation; nothing else changes with the backend. Use `--help` to
display usage.

The wrapper selects recipes in `DQM_CONFIGS` order, then tags in `TAGS` order,
then runs in `RUNS` order. The local backend executes them in that order and
stops at the first failure; the HTCondor backend prepares them all and lets them
run concurrently, so one failure does not hold back the others. All relative
paths in its configuration are resolved from the pipeline directory, and every
path handed to a job is absolute. A nonblank `CMSSW_SRC` must point to an
existing directory even when selecting scouting only.

## Batch execution

With `DQM_BACKEND="condor"` the wrapper writes, per selected recipe/tag/run:

```text
<DQM_JOBS_BASE>/<recipe>/<tag>/run_<run>/
    recipe.sh      the frozen recipe, copied by the worker into its scratch area
    job.sh         generated from pipeline.cfg: environment, run, publication
    dqm.stdout, dqm.stderr, dqm.log    written by Condor when the job ends
    artifacts/     the work directory copied back, minus *.root by default
```

It then writes `dqm_jobs_to_run.txt` and `condor_dqm.sub`, and submits them when
`DQM_SUBMIT=true` (`--no-submit` only prepares). The jobs need no input sandbox:
they read the mounted `EOS_BASE` and the release under `CMSSW_SRC` directly, so
submit from a node where both are visible to the workers (`module load
lxbatch/eossubmit`). `X509_USER_PROXY` is set to the `PROXY` file in the pipeline
directory when it is readable. A job publishes its own `result.root` exactly as
the local backend does, through a temporary file in the destination directory.

`job.sh` reports what happened through its exit code and a marker on stdout:
`1`/`RECIPE FAILED`, `2`/`MISSING result.root`, `3`/`PUBLISH FAILED`,
`4`/`SETUP FAILED` (environment or inputs unusable on the worker), and `0` with
`DQM_JOB_DONE_OK` on success.

Once the queue drains, collect the outcome:

```bash
bash 04_run_dqm.sh --status
```

This writes `check_report_dqm.md` with one row per selected recipe/tag/run, plus
`dqm_resubmit.txt` and `condor_dqm_resubmit.sub` for everything that is not
`OK`. Statuses are `OK`, `PENDING` (queued, running, or never submitted),
`SETUP_FAILED`, `RECIPE_FAILED`, `NO_RESULT`, `PUBLISH_FAILED`, `MISSING_OUTPUT`
(job reported success but the published file is gone), `NO_MARKER` (stopped
without reaching any marker, typically an eviction or hold), and
`NOT_GENERATED`. `--tag` and `--run` narrow the report the same way they narrow
a run. Resubmit with:

```bash
condor_submit condor_dqm_resubmit.sub
```

Resubmission reuses each job directory and its frozen recipe, and replaces that
directory's `artifacts/` with the new attempt. Regenerating over job directories
that already hold output requires `--force`, which discards those logs and
artifacts; do not use it while the jobs are still in the queue.

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

The local backend runs each recipe in a fresh directory:

```text
<DQM_WORK_BASE>/<recipe>/<tag>/run_<run>/attempt_XXXXXX/
```

The wrapper prints its location and copies the executed script to `recipe.sh`.
A Condor job runs in the worker's own scratch area instead and copies that
directory back to `<DQM_JOBS_BASE>/<recipe>/<tag>/run_<run>/artifacts/`,
excluding `*.root` unless `DQM_KEEP_ROOT=true`. Artifacts depend on the recipe:

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

Run numbers are padded to nine digits. On the HTCondor backend the job itself
publishes, the same way, from the worker. A successful rerun replaces the
previous result for that recipe/tag/run; a recipe failure leaves any previous
published result in place. The wrapper neither skips completed results nor
cleans attempt directories. Use filters to rerun the failed selection without
reprocessing all earlier combinations, or `condor_dqm_resubmit.sub` to rerun
exactly the jobs the last report flagged.

## Troubleshooting and plotting

- **Environment or path error:** activate `cmsenv` (local backend), fill the
  required paths, and check mounted EOS access. For HLT, verify that the
  source-client config exists under `CMSSW_SRC`.
- **`SETUP_FAILED` jobs:** the worker could not reach `CMSSW_SRC`, set up the
  release, or see the input directory. Check `dqm.stdout` in the job directory,
  then EOS access from the workers and the paths in `pipeline.cfg`.
- **Jobs waiting in the queue:** `DQM_REQUEST_CPUS` (by default `DQM_THREADS`,
  24) asks for a whole-machine slot. Lower both and resubmit.
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

Both backends export exactly these variables, so the same recipe works on a
worker node without changes. On the HTCondor backend the recipe runs inside the
worker's scratch directory with the release from `CMSSW_SRC` already set up, and
only `LOCALPATH` and the destination are read from shared storage: keep every
other path the recipe uses relative to its working directory, and expect the
directory itself to disappear once the job ends.

A recipe should fail with a nonzero exit code on errors and leave a nonempty
`result.root` in its working directory on success. Save an input list and logs as
the supplied recipes do. The wrapper handles publication; no JSON manifest or
Python runner is required.
