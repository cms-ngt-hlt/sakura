#!/bin/bash
# Run each script in DQM_CONFIGS for the selected tags and runs.
set -euo pipefail
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
cd "$HERE"
source ./pipeline.cfg

SELECT_TAG=""
SELECT_RUN=""
SELECT_WORKFLOW=""
MODE=local
while (( $# )); do
    case "$1" in
        --tag|--run|--workflow)
            [[ $# -ge 2 ]] || { echo "ERROR: $1 needs a value" >&2; exit 1; }
            case "$1" in
                --tag) SELECT_TAG="$2" ;;
                --run) SELECT_RUN="$2" ;;
                --workflow) SELECT_WORKFLOW="$2" ;;
            esac
            shift 2 ;;
        --prepare|--submit)
            [[ "$MODE" == local ]] || { echo "ERROR: choose only one batch mode" >&2; exit 1; }
            MODE=${1#--}
            shift ;;
        -h|--help)
            echo "Usage: bash 04_run_dqm.sh [--prepare|--submit] [--tag NGT] [--run 403863] [--workflow scouting]"
            echo "Default: run locally. --prepare: generate HTCondor files. --submit: generate and submit."
            exit 0 ;;
        *) echo "ERROR: unknown argument '$1'" >&2; exit 1 ;;
    esac
done

if [[ "$MODE" == local ]]; then
    [[ -n "${CMSSW_BASE:-}" ]] || { echo "ERROR: run cmsenv first" >&2; exit 1; }
fi
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

# Validate all recipes before executing or preparing any jobs.
NAMES=()
for SCRIPT in "${DQM_CONFIGS[@]}"; do
    [[ -f "$SCRIPT" ]] || { echo "ERROR: missing script $SCRIPT" >&2; exit 1; }
    NAME=$(basename "$SCRIPT" .sh)
    [[ "$NAME" =~ ^[a-zA-Z0-9_-]+$ ]] || { echo "ERROR: invalid workflow name $NAME" >&2; exit 1; }
    for SEEN in ${NAMES[@]+"${NAMES[@]}"}; do
        [[ "$NAME" != "$SEEN" ]] || { echo "ERROR: duplicate workflow name $NAME" >&2; exit 1; }
    done
    NAMES+=("$NAME")
done
if [[ -n "$SELECT_WORKFLOW" ]]; then
    found=false
    for NAME in ${NAMES[@]+"${NAMES[@]}"}; do [[ "$NAME" != "$SELECT_WORKFLOW" ]] || found=true; done
    $found || { echo "ERROR: unknown workflow '$SELECT_WORKFLOW'" >&2; exit 1; }
fi
(( ${#NAMES[@]} && ${#TAGS[@]} && ${#RUNS[@]} )) || { echo "ERROR: empty DQM selection" >&2; exit 1; }

if [[ "$MODE" != local ]]; then
    CMSSW_SRC=${CMSSW_SRC:-}
    if [[ -z "${CMSSW_SRC//[[:space:]]/}" ]]; then
        [[ -n "${CMSSW_BASE:-}" ]] || { echo "ERROR: set CMSSW_SRC or run cmsenv" >&2; exit 1; }
        CMSSW_SRC="$CMSSW_BASE/src"
    fi
    DQM_JOB_FLAVOUR=${DQM_JOB_FLAVOUR:-${JOB_FLAVOUR:-workday}}
    DQM_REQUEST_MEMORY_MB=${DQM_REQUEST_MEMORY_MB:-${REQUEST_MEMORY_MB:-5000}}
    [[ "$DQM_REQUEST_MEMORY_MB" =~ ^[1-9][0-9]*$ ]] || { echo "ERROR: DQM_REQUEST_MEMORY_MB must be positive" >&2; exit 1; }
    [[ "$DQM_JOB_FLAVOUR" =~ ^[a-zA-Z0-9_]+$ ]] || { echo "ERROR: invalid DQM_JOB_FLAVOUR" >&2; exit 1; }
    PROXY=${PROXY:?Set PROXY in pipeline.cfg}
    [[ "$PROXY" = /* ]] || PROXY="$HERE/$PROXY"
    [[ -r "$PROXY" ]] || { echo "ERROR: unreadable proxy $PROXY" >&2; exit 1; }
    if [[ "$MODE" == submit ]]; then
        command -v condor_submit >/dev/null || { echo "ERROR: condor_submit is not available" >&2; exit 1; }
    fi
fi

# Resolve paths before moving into each job's working directory.
mkdir -p "$DQM_WORK_BASE" "$DQM_DEST_BASE"
WORK_BASE=$(cd "$DQM_WORK_BASE" && pwd)
DEST_BASE=$(cd "$DQM_DEST_BASE" && pwd)
EOS_BASE=$(cd "$EOS_BASE" && pwd)
if [[ -n "${CMSSW_SRC//[[:space:]]/}" ]]; then
    CMSSW_SRC=$(cd "$CMSSW_SRC" && pwd)
fi
export ERA DQM_THREADS DQM_HARVEST_CONDITIONS CMSSW_SRC
if [[ "$MODE" != local ]]; then
    BATCH=$(mktemp -d "$WORK_BASE/batch_XXXXXX")
    # HTCondor quoted paths cannot contain quotes or newlines.
    [[ "$BATCH" != *\"* && "$BATCH" != *$'\n'* && "$BATCH" != *\\* ]] || { echo "ERROR: unsupported batch path $BATCH" >&2; exit 1; }
    printf 'job\tworkflow\ttag\trun\toutput\n' > "$BATCH/manifest.tsv"
fi
run_recipe() {
    # A scheduler retry must not publish a result left by an earlier execution.
    rm -f result.root
    bash recipe.sh || { echo "ERROR: recipe failed; see $PWD" >&2; exit 1; }
    [[ -s result.root ]] || { echo "ERROR: no result.root in $PWD" >&2; exit 1; }
    TEMP_OUTPUT=$(mktemp "$(dirname "$OUTPUT")/.publishing_XXXXXX")
    trap 'rm -f "$TEMP_OUTPUT"' EXIT
    cp result.root "$TEMP_OUTPUT"
    mv -f "$TEMP_OUTPUT" "$OUTPUT"
    echo "Saved $OUTPUT"
    echo DQM_JOB_DONE_OK
}

COUNT=0

for SCRIPT in "${DQM_CONFIGS[@]}"; do
    NAME=$(basename "$SCRIPT" .sh)
    [[ -z "$SELECT_WORKFLOW" || "$NAME" == "$SELECT_WORKFLOW" ]] || continue
    [[ "$SCRIPT" = /* ]] || SCRIPT="$HERE/$SCRIPT"
    [[ -f "$SCRIPT" ]] || { echo "ERROR: missing script $SCRIPT" >&2; exit 1; }
    for i in "${!TAGS[@]}"; do
        TAG=${TAGS[$i]}
        GTAG=${GTAGS[$i]}
        [[ -z "$SELECT_TAG" || "$TAG" == "$SELECT_TAG" ]] || continue
        for RUN in "${RUNS[@]}"; do
            [[ -z "$SELECT_RUN" || "$RUN" == "$SELECT_RUN" ]] || continue
            LOCALPATH="$EOS_BASE/$TAG/run_$RUN"
            export TAG GTAG RUN LOCALPATH
            mkdir -p "$WORK_BASE/$NAME/$TAG/run_$RUN" "$DEST_BASE/$NAME/$TAG"
            if [[ "$MODE" == local ]]; then
                WORK=$(mktemp -d "$WORK_BASE/$NAME/$TAG/run_$RUN/attempt_XXXXXX")
            else
                WORK="$BATCH/job_$COUNT"
                mkdir "$WORK"
            fi
            OUTPUT="$DEST_BASE/$NAME/$TAG/DQM_${NAME}_R$(printf '%09d' "$RUN").root"
            export OUTPUT
            cp "$SCRIPT" "$WORK/recipe.sh"
            if [[ "$MODE" == local ]]; then
                echo "Running $NAME / $TAG / $RUN in $WORK"
                (cd "$WORK" && run_recipe)
            else
                # Freeze settings; workers never reread a mutable pipeline.cfg.
                {
                    printf '#!/bin/bash\nset -euo pipefail\n'
                    printf 'cd %q\n' "$WORK"
                    for VAR in TAG GTAG RUN LOCALPATH ERA DQM_THREADS DQM_HARVEST_CONDITIONS CMSSW_SRC OUTPUT; do
                        printf 'export %s=%q\n' "$VAR" "${!VAR-}"
                    done
                    printf 'export X509_USER_PROXY=%q\n' "$PROXY"
                    printf 'export X509_CERT_DIR=/cvmfs/grid.cern.ch/etc/grid-security/certificates\n'
                    printf 'if ! command -v scramv1 >/dev/null; then source /cvmfs/cms.cern.ch/cmsset_default.sh; fi\n'
                    printf 'cd "$CMSSW_SRC"\nCMS_RUNTIME=$(scramv1 runtime -sh)\neval "$CMS_RUNTIME"\n'
                    declare -f run_recipe
                    printf 'cd %q\nrun_recipe\n' "$WORK"
                } > "$WORK/job.sh"
                chmod +x "$WORK/job.sh"
                printf '%s\t%s\t%s\t%s\t%s\n' "$COUNT" "$NAME" "$TAG" "$RUN" "$OUTPUT" >> "$BATCH/manifest.tsv"
            fi
            COUNT=$((COUNT + 1))
        done
    done
done

if [[ "$MODE" != local ]]; then
    cat > "$BATCH/condor_dqm.sub" <<EOF
universe = vanilla
executable = "$BATCH/job_\$(Process)/job.sh"
output = "$BATCH/job_\$(Process)/dqm.stdout"
error = "$BATCH/job_\$(Process)/dqm.stderr"
log = "$BATCH/job_\$(Process)/dqm.condor.log"
should_transfer_files = NO
request_cpus = $DQM_THREADS
request_memory = $DQM_REQUEST_MEMORY_MB
+JobFlavour = "$DQM_JOB_FLAVOUR"
queue $COUNT
EOF
    echo "Prepared $COUNT DQM jobs in $BATCH"
    echo "Manifest: $BATCH/manifest.tsv"
    printf 'Submit with: condor_submit %q\n' "$BATCH/condor_dqm.sub"
    if [[ "$MODE" == submit ]]; then
        condor_submit "$BATCH/condor_dqm.sub"
    fi
fi
