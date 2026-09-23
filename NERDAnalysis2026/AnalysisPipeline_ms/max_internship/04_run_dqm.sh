#!/bin/bash
# Run each script in DQM_CONFIGS for the selected tags and runs, either locally
# (one after the other) or as one HTCondor job per recipe/tag/run.
# Backend, resources and paths all come from pipeline.cfg.
set -euo pipefail
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
cd "$HERE"
source ./pipeline.cfg

usage() {
    cat <<'EOF'
Usage: bash 04_run_dqm.sh [--tag NGT] [--run 403863] [--local|--condor]
                          [--submit|--no-submit] [--force] [--status]

  --tag, --run           Restrict to one configured tag/run (default: all).
  --local, --condor      Override DQM_BACKEND for this invocation.
  --submit, --no-submit  Override DQM_SUBMIT (HTCondor backend only).
  --force                Regenerate job directories that already hold output.
  --status               Report the state of the generated HTCondor jobs and
                         write dqm_resubmit.txt / condor_dqm_resubmit.sub.
EOF
}

SELECT_TAG=""
SELECT_RUN=""
SELECT_BACKEND=""
SELECT_SUBMIT=""
FORCE=false
MODE="run"
while (( $# )); do
    case "$1" in
        --tag|--run)
            [[ $# -ge 2 ]] || { echo "ERROR: $1 needs a value" >&2; exit 1; }
            case "$1" in
                --tag) SELECT_TAG="$2" ;;
                --run) SELECT_RUN="$2" ;;
            esac
            shift 2 ;;
        --local)     SELECT_BACKEND="local";  shift ;;
        --condor)    SELECT_BACKEND="condor"; shift ;;
        --submit)    SELECT_SUBMIT=true;      shift ;;
        --no-submit) SELECT_SUBMIT=false;     shift ;;
        --force)     FORCE=true;              shift ;;
        --status)    MODE="status";           shift ;;
        -h|--help)
            usage
            exit 0 ;;
        *) echo "ERROR: unknown argument '$1'" >&2; usage >&2; exit 1 ;;
    esac
done

# --- configuration, all of it from pipeline.cfg -----------------------------
BACKEND=${SELECT_BACKEND:-${DQM_BACKEND:-}}
[[ "$BACKEND" == "local" || "$BACKEND" == "condor" ]] || {
    echo "ERROR: set DQM_BACKEND to 'local' or 'condor' in pipeline.cfg" >&2; exit 1;
}
SUBMIT=${SELECT_SUBMIT:-${DQM_SUBMIT:-}}
[[ "$SUBMIT" == true || "$SUBMIT" == false ]] || {
    echo "ERROR: set DQM_SUBMIT to true or false in pipeline.cfg" >&2; exit 1;
}
[[ "$MODE" != "status" || "$BACKEND" == "condor" ]] || {
    echo "ERROR: --status applies to the HTCondor backend only" >&2; exit 1;
}

[[ -n "${EOS_BASE//[[:space:]]/}" && -n "${DQM_DEST_BASE//[[:space:]]/}" ]] || {
    echo "ERROR: set EOS_BASE and DQM_DEST_BASE in pipeline.cfg" >&2; exit 1;
}
[[ ${#TAGS[@]} -eq ${#GTAGS[@]} ]] || { echo "ERROR: TAGS and GTAGS must match" >&2; exit 1; }
[[ "$DQM_THREADS" =~ ^[1-9][0-9]*$ ]] || { echo "ERROR: DQM_THREADS must be positive" >&2; exit 1; }
if [[ -n "$SELECT_TAG" ]]; then
    found=false
    for TAG in "${TAGS[@]}"; do [[ "$TAG" != "$SELECT_TAG" ]] || found=true; done
    $found || { echo "ERROR: unknown tag '$SELECT_TAG'" >&2; exit 1; }
fi
if [[ -n "$SELECT_RUN" ]]; then
    found=false
    for RUN in "${RUNS[@]}"; do [[ "$RUN" != "$SELECT_RUN" ]] || found=true; done
    $found || { echo "ERROR: unknown run '$SELECT_RUN'" >&2; exit 1; }
fi
if [[ "$BACKEND" == "local" ]]; then
    [[ -n "${CMSSW_BASE:-}" ]] || { echo "ERROR: run cmsenv first" >&2; exit 1; }
else
    for name in DQM_JOBS_BASE DQM_JOB_FLAVOUR DQM_REQUEST_CPUS DQM_REQUEST_MEMORY_MB \
                DQM_REQUEST_DISK_KB DQM_KEEP_ROOT; do
        [[ -n "${!name:-}" ]] || { echo "ERROR: set $name in pipeline.cfg" >&2; exit 1; }
    done
    for name in DQM_REQUEST_CPUS DQM_REQUEST_MEMORY_MB DQM_REQUEST_DISK_KB; do
        [[ "${!name}" =~ ^[1-9][0-9]*$ ]] || {
            echo "ERROR: $name must be a positive integer" >&2; exit 1; }
    done
    [[ "$DQM_KEEP_ROOT" == true || "$DQM_KEEP_ROOT" == false ]] || {
        echo "ERROR: DQM_KEEP_ROOT must be true or false" >&2; exit 1; }
    # Workers set up CMSSW themselves, so the release is not optional there.
    [[ -n "${CMSSW_SRC//[[:space:]]/}" ]] || {
        echo "ERROR: the HTCondor backend needs CMSSW_SRC in pipeline.cfg" >&2; exit 1; }
fi

# Resolve paths before moving into each job's working directory: a job runs
# somewhere else entirely, so everything handed to it has to be absolute.
mkdir -p "$DQM_DEST_BASE"
DEST_BASE=$(cd "$DQM_DEST_BASE" && pwd)
EOS_BASE=$(cd "$EOS_BASE" && pwd)
if [[ -n "${CMSSW_SRC//[[:space:]]/}" ]]; then
    CMSSW_SRC=$(cd "$CMSSW_SRC" && pwd)
fi
WORK_BASE=""
JOBS_BASE=""
if [[ "$BACKEND" == "local" ]]; then
    mkdir -p "$DQM_WORK_BASE"
    WORK_BASE=$(cd "$DQM_WORK_BASE" && pwd)
else
    mkdir -p "$DQM_JOBS_BASE"
    JOBS_BASE=$(cd "$DQM_JOBS_BASE" && pwd)
fi
export ERA DQM_THREADS DQM_HARVEST_CONDITIONS CMSSW_SRC

JOB_LIST="$HERE/dqm_jobs_to_run.txt"
RESUBMIT_LIST="$HERE/dqm_resubmit.txt"
SUB_FILE="$HERE/condor_dqm.sub"
RESUBMIT_SUB="$HERE/condor_dqm_resubmit.sub"
REPORT="$HERE/check_report_dqm.md"

# --- the (recipe, tag, run) combinations this invocation selects ------------
COMBOS=()
build_combinations() {
    local script name i tag gtag run
    for script in "${DQM_CONFIGS[@]}"; do
        name=$(basename "$script" .sh)
        [[ "$script" = /* ]] || script="$HERE/$script"
        [[ -f "$script" ]] || { echo "ERROR: missing script $script" >&2; exit 1; }
        for i in "${!TAGS[@]}"; do
            tag=${TAGS[$i]}
            gtag=${GTAGS[$i]}
            [[ -z "$SELECT_TAG" || "$tag" == "$SELECT_TAG" ]] || continue
            for run in "${RUNS[@]}"; do
                [[ -z "$SELECT_RUN" || "$run" == "$SELECT_RUN" ]] || continue
                COMBOS+=("$name"$'\t'"$script"$'\t'"$tag"$'\t'"$gtag"$'\t'"$run")
            done
        done
    done
}
build_combinations
(( ${#COMBOS[@]} )) || { echo "ERROR: no recipe/tag/run combination selected" >&2; exit 1; }

output_path() {  # recipe name, tag, run
    printf '%s/%s/%s/DQM_%s_R%09d.root' "$DEST_BASE" "$1" "$2" "$1" "$3"
}

# --- local backend: unchanged sequential behaviour --------------------------
run_local() {
    local NAME SCRIPT TAG GTAG RUN combo LOCALPATH WORK OUTPUT TEMP_OUTPUT
    for combo in "${COMBOS[@]}"; do
        IFS=$'\t' read -r NAME SCRIPT TAG GTAG RUN <<< "$combo"
        LOCALPATH="$EOS_BASE/$TAG/run_$RUN"
        export TAG GTAG RUN LOCALPATH
        mkdir -p "$WORK_BASE/$NAME/$TAG/run_$RUN" "$DEST_BASE/$NAME/$TAG"
        WORK=$(mktemp -d "$WORK_BASE/$NAME/$TAG/run_$RUN/attempt_XXXXXX")
        echo "Running $NAME / $TAG / $RUN in $WORK"
        # Keep the exact recipe alongside the generated configs and logs.
        cp "$SCRIPT" "$WORK/recipe.sh"
        (cd "$WORK" && bash recipe.sh) || {
            echo "ERROR: $NAME failed; see $WORK" >&2; exit 1;
        }
        [[ -s "$WORK/result.root" ]] || { echo "ERROR: no result.root in $WORK" >&2; exit 1; }
        OUTPUT=$(output_path "$NAME" "$TAG" "$RUN")
        TEMP_OUTPUT=$(mktemp "$DEST_BASE/$NAME/$TAG/.publishing_XXXXXX")
        cp "$WORK/result.root" "$TEMP_OUTPUT"
        mv -f "$TEMP_OUTPUT" "$OUTPUT"
        echo "Saved $OUTPUT"
    done
}

# --- HTCondor backend ------------------------------------------------------
# The worker runs the very same recipe, with the same environment contract as
# the local backend, then publishes result.root itself.
write_job_sh() {  # job.sh path, job dir, recipe name, tag, gtag, run, input dir, output
    local job_sh=$1
    {
        echo '#!/bin/bash'
        echo '# Generated by 04_run_dqm.sh from pipeline.cfg: do not edit by hand.'
        echo '# Exit codes: 1 = recipe failed, 2 = no result.root, 3 = publication'
        echo '# failed, 4 = the worker could not be set up (environment or inputs).'
        echo 'set -uo pipefail'
        printf 'JOBDIR=%q\n' "$2"
        printf 'NAME=%q\n' "$3"
        printf 'export TAG=%q\n' "$4"
        printf 'export GTAG=%q\n' "$5"
        printf 'export RUN=%q\n' "$6"
        printf 'export LOCALPATH=%q\n' "$7"
        printf 'OUTPUT=%q\n' "$8"
        printf 'export ERA=%q\n' "$ERA"
        printf 'export DQM_THREADS=%q\n' "$DQM_THREADS"
        printf 'export CMSSW_SRC=%q\n' "$CMSSW_SRC"
        printf 'export DQM_HARVEST_CONDITIONS=%q\n' "${DQM_HARVEST_CONDITIONS:-}"
        printf 'KEEP_ROOT=%q\n' "$DQM_KEEP_ROOT"
        printf 'PROXY_PATH=%q\n' "$HERE/$PROXY"
        cat <<'WORKER'

WORK=$(mktemp -d "${TMPDIR:-/tmp}/dqm_XXXXXX") ||
    { echo "SETUP FAILED: no scratch directory on $(hostname)"; exit 4; }
cd "$WORK" || { echo "SETUP FAILED: cannot enter $WORK"; exit 4; }
echo "Running $NAME / $TAG / $RUN in $WORK on $(hostname)"

cp "$JOBDIR/recipe.sh" recipe.sh ||
    { echo "SETUP FAILED: cannot read $JOBDIR/recipe.sh"; exit 4; }

if [ -r "$PROXY_PATH" ]; then
    export X509_USER_PROXY="$PROXY_PATH"
    export X509_CERT_DIR=/cvmfs/grid.cern.ch/etc/grid-security/certificates
else
    echo "WARNING: no readable proxy at $PROXY_PATH"
fi

cd "$CMSSW_SRC" || { echo "SETUP FAILED: CMSSW_SRC unreachable: $CMSSW_SRC"; exit 4; }
eval "$(scramv1 runtime -sh)" || { echo "SETUP FAILED: scramv1 runtime"; exit 4; }
cd "$WORK" || { echo "SETUP FAILED: cannot return to $WORK"; exit 4; }

[ -d "$LOCALPATH" ] ||
    { echo "SETUP FAILED: input directory not visible here: $LOCALPATH"; exit 4; }

bash recipe.sh
rc=$?
echo "--- recipe exit $rc; files in $WORK ---"
ls -la

# Keep logs and generated configs next to the job whatever the outcome; the
# worker's scratch directory is gone by the time anyone reads the report. A
# resubmitted job replaces them, so the directory always holds one attempt.
rm -rf "$JOBDIR/artifacts"
mkdir -p "$JOBDIR/artifacts"
if [ "$KEEP_ROOT" = true ]; then
    tar cf - . | (cd "$JOBDIR/artifacts" && tar xf -) ||
        echo "WARNING: could not copy the work directory back"
else
    tar cf - --exclude='*.root' . | (cd "$JOBDIR/artifacts" && tar xf -) ||
        echo "WARNING: could not copy the work directory back"
fi

[ "$rc" -eq 0 ] || { echo "RECIPE FAILED (exit $rc)"; exit 1; }
[ -s result.root ] || { echo "MISSING result.root"; exit 2; }

DEST_DIR=$(dirname "$OUTPUT")
mkdir -p "$DEST_DIR" || { echo "PUBLISH FAILED: cannot create $DEST_DIR"; exit 3; }
TEMP_OUTPUT=$(mktemp "$DEST_DIR/.publishing_XXXXXX") ||
    { echo "PUBLISH FAILED: no temporary file in $DEST_DIR"; exit 3; }
if ! cp result.root "$TEMP_OUTPUT" || ! mv -f "$TEMP_OUTPUT" "$OUTPUT"; then
    rm -f "$TEMP_OUTPUT"
    echo "PUBLISH FAILED: $OUTPUT"
    exit 3
fi
echo "Saved $OUTPUT"

cd / && rm -rf "$WORK"
echo "DQM_JOB_DONE_OK"
exit 0
WORKER
    } > "$job_sh"
    chmod 755 "$job_sh"
}

write_sub() {  # .sub path, job list path
    cat > "$1" <<EOF
executable = \$(jobscript)
output = \$Fp(jobscript)dqm.stdout
error  = \$Fp(jobscript)dqm.stderr
log    = \$Fp(jobscript)dqm.log
request_cpus   = $DQM_REQUEST_CPUS
request_memory = $DQM_REQUEST_MEMORY_MB
request_disk   = $DQM_REQUEST_DISK_KB
+JobFlavour = "$DQM_JOB_FLAVOUR"
queue jobscript from $2
EOF
}

job_dir() {  # recipe name, tag, run
    printf '%s/%s/%s/run_%s' "$JOBS_BASE" "$1" "$2" "$3"
}

run_condor() {
    local NAME SCRIPT TAG GTAG RUN combo LOCALPATH OUTPUT JOBDIR
    local -a scripts=() conflicts=()

    # Nothing is touched before every selected job directory is known to be
    # free: a refused invocation must leave earlier jobs and lists intact.
    for combo in "${COMBOS[@]}"; do
        IFS=$'\t' read -r NAME SCRIPT TAG GTAG RUN <<< "$combo"
        JOBDIR=$(job_dir "$NAME" "$TAG" "$RUN")
        if [[ -e "$JOBDIR/dqm.stdout" || -e "$JOBDIR/artifacts" ]]; then
            conflicts+=("$JOBDIR")
        fi
    done
    if (( ${#conflicts[@]} )) && [[ "$FORCE" != true ]]; then
        echo "ERROR: ${#conflicts[@]} job directory(ies) already hold output" \
             "from an earlier job:" >&2
        printf '  %s\n' "${conflicts[@]}" >&2
        echo "Use --force to discard those logs and artifacts, but not while" \
             "the jobs are still in the queue." >&2
        exit 1
    fi

    for combo in "${COMBOS[@]}"; do
        IFS=$'\t' read -r NAME SCRIPT TAG GTAG RUN <<< "$combo"
        LOCALPATH="$EOS_BASE/$TAG/run_$RUN"
        OUTPUT=$(output_path "$NAME" "$TAG" "$RUN")
        JOBDIR=$(job_dir "$NAME" "$TAG" "$RUN")
        rm -rf "$JOBDIR"
        mkdir -p "$JOBDIR" "$DEST_BASE/$NAME/$TAG"
        # Freeze the recipe next to the job, as the local backend does.
        cp "$SCRIPT" "$JOBDIR/recipe.sh"
        write_job_sh "$JOBDIR/job.sh" "$JOBDIR" "$NAME" "$TAG" "$GTAG" "$RUN" \
                     "$LOCALPATH" "$OUTPUT"
        scripts+=("$JOBDIR/job.sh")
        echo "Prepared $NAME / $TAG / $RUN in $JOBDIR"
    done
    printf '%s\n' "${scripts[@]}" > "$JOB_LIST"
    write_sub "$SUB_FILE" "$JOB_LIST"

    echo "${#COMBOS[@]} DQM job(s) -> $JOB_LIST"
    printf 'Per job: %s cpu(s), %s MB memory, %s KB disk, flavour %s.\n' \
           "$DQM_REQUEST_CPUS" "$DQM_REQUEST_MEMORY_MB" "$DQM_REQUEST_DISK_KB" \
           "$DQM_JOB_FLAVOUR"
    if [[ "$SUBMIT" == true ]]; then
        command -v condor_submit >/dev/null || {
            echo "ERROR: condor_submit is not available; nothing was submitted." >&2; exit 1; }
        condor_submit "$SUB_FILE"
        echo "Follow with: condor_q   then   bash 04_run_dqm.sh --status"
    else
        echo "Submit with: condor_submit $SUB_FILE"
    fi
}

# --- HTCondor backend: report and resubmission -----------------------------
job_status() {  # stdout path -> status on stdout
    local stdout=$1
    if grep -qF "DQM_JOB_DONE_OK" "$stdout"; then
        echo "OK"
    elif grep -qF "MISSING result.root" "$stdout"; then
        echo "NO_RESULT"
    elif grep -qF "RECIPE FAILED" "$stdout"; then
        echo "RECIPE_FAILED"
    elif grep -qF "PUBLISH FAILED" "$stdout"; then
        echo "PUBLISH_FAILED"
    elif grep -qF "SETUP FAILED" "$stdout"; then
        echo "SETUP_FAILED"
    else
        # No end marker at all: evicted, killed, or still writing its log.
        echo "NO_MARKER"
    fi
}

status_condor() {
    local NAME SCRIPT TAG GTAG RUN combo OUTPUT JOBDIR STATUS queued
    local -a rows=() resubmit=()
    local -A counts=()
    for combo in "${COMBOS[@]}"; do
        IFS=$'\t' read -r NAME SCRIPT TAG GTAG RUN <<< "$combo"
        OUTPUT=$(output_path "$NAME" "$TAG" "$RUN")
        JOBDIR=$(job_dir "$NAME" "$TAG" "$RUN")
        if [[ ! -f "$JOBDIR/job.sh" ]]; then
            STATUS="NOT_GENERATED"
        elif [[ ! -f "$JOBDIR/dqm.stdout" ]]; then
            STATUS="PENDING"
        else
            STATUS=$(job_status "$JOBDIR/dqm.stdout")
            if [[ "$STATUS" == "OK" && ! -s "$OUTPUT" ]]; then
                STATUS="MISSING_OUTPUT"
            fi
        fi
        counts[$STATUS]=$(( ${counts[$STATUS]:-0} + 1 ))
        case "$STATUS" in
            SETUP_FAILED|RECIPE_FAILED|NO_RESULT|PUBLISH_FAILED|NO_MARKER|MISSING_OUTPUT)
                resubmit+=("$JOBDIR/job.sh") ;;
        esac
        rows+=("| $NAME | $TAG | $RUN | $STATUS | $JOBDIR |")
    done

    if command -v condor_q >/dev/null; then
        queued=$(condor_q -totals -af ClusterId 2>/dev/null | grep -c . || true)
    else
        queued=0
    fi

    local summary=""
    for STATUS in $(printf '%s\n' "${!counts[@]}" | sort); do
        summary+="${counts[$STATUS]} $STATUS · "
    done
    summary=${summary% · }

    {
        echo "# DQM check report"
        echo
        if (( queued )); then
            echo "> **WARNING:** ~$queued job(s) still in condor_q: provisional report."
            echo
        fi
        echo "| Recipe | Tag | Run | Status | Job directory |"
        echo "|:--|:--|---:|:--|:--|"
        printf '%s\n' "${rows[@]}"
        echo
        echo "**Totals:** $summary"
        echo
        echo "**To resubmit:** ${#resubmit[@]} job(s) -> $(basename "$RESUBMIT_LIST")"
        echo
        echo "NOTE: PENDING means the job is queued, running, or was never submitted;"
        echo "NO_MARKER means it stopped without reaching any of its own markers,"
        echo "typically an eviction or a hold. Each job's logs are in artifacts/."
    } > "$REPORT"

    if (( ${#resubmit[@]} )); then
        printf '%s\n' "${resubmit[@]}" > "$RESUBMIT_LIST"
        write_sub "$RESUBMIT_SUB" "$RESUBMIT_LIST"
    else
        : > "$RESUBMIT_LIST"
    fi

    echo "[DQM] $summary"
    echo "Report: $REPORT"
    if (( ${#resubmit[@]} )); then
        echo "${#resubmit[@]} job(s) to redo ->  condor_submit $RESUBMIT_SUB"
        echo "Resubmission reuses the frozen recipe in each job directory;" \
             "the artifacts of the failed attempt stay there until it reruns."
    else
        echo "No failed DQM jobs to resubmit."
    fi
}

if [[ "$MODE" == "status" ]]; then
    status_condor
elif [[ "$BACKEND" == "local" ]]; then
    run_local
else
    run_condor
fi
