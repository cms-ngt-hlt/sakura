#!/bin/bash
# generate + dump the HLT config for every tag.
# NGT needs a per-run GlobalTag snapshotTime -> one config per run in RUNS.
# The other tags are run-independent -> a single config each.
# Needs: cmsenv already sourced. Run once (re-run only when menu/GT/paths/runs change).
set -euo pipefail
cd "$(dirname "$0")"
source ./pipeline.cfg

[ -n "${CMSSW_BASE:-}" ] || { echo "ERROR: cmsenv not active (CMSSW_BASE unset)"; exit 1; }
mkdir -p configs

OMS_CSV="oms_runs.csv"

snapshot_time_for_run() {
    awk -F, -v run="$1" '$1 == run { gsub(/\r$/, "", $6); print $6; found=1; exit } END { if (!found) exit 1 }' "$OMS_CSV"
}

# $1=globaltag  $2=config file  $3=dump file  $4=snapshot time (empty -> no snapshotTime line)
make_config() {
    local gt="$1" cfg="$2" dump="$3" snapshot="$4"
    # empty input, just like here https://github.com/jprendi/sakura/blob/main/ApprovedPlots/CMS-DP-2026/028/EGamma/HLTJobSubmissions/EGammaFullHLT.sh
    hltGetConfiguration "${HLT_MENU}" \
        --globaltag "${gt}" \
        --data \
        --unprescale \
        --output none \
        --max-events -1 \
        --eras "${ERA}" \
        --l1-emulator uGT --l1 "${L1_MENU}" \
        --paths "${HLT_PATHS}" \
        --input " " \
        > "${cfg}"

    cat <<'EOF' >> "${cfg}"
# customize the output modules
process.hltOutputLocalTestDataRaw.outputCommands = [
   'drop *',
   'keep GlobalObjectMapRecord_hltGtStage2ObjectMap_*_HLTX',
   'keep edmTriggerResults_*_*_HLTX',
   'keep triggerTriggerEvent_*_*_HLTX'
]
EOF
    if [ -n "${snapshot}" ]; then
        echo "process.GlobalTag.snapshotTime = cms.string(\"${snapshot}\")" >> "${cfg}"
    fi
    cat <<'EOF' >> "${cfg}"
# make summary available (needed by 03_check.py's HLT-Report parsing)
process.options.wantSummary = True
EOF
    module load lxbatch/eossubmit
    edmConfigDump "${cfg}" > "${dump}" # needed for HTCondor
}

for i in "${!TAGS[@]}"; do
    tag="${TAGS[$i]}"; gt="${GTAGS[$i]}"

    if [ "${tag}" = "NGT" ]; then
        [ -f "$OMS_CSV" ] || { echo "ERROR: $OMS_CSV not found"; exit 1; }
        mkdir -p "configs/${tag}_configs"
        for run in "${RUNS[@]}"; do
            snapshot=$(snapshot_time_for_run "$run") || { echo "ERROR: no snapshot_time found for run ${run} in ${OMS_CSV}"; exit 1; }
            echo "=== ${tag} (${gt}), run ${run}, snapshot ${snapshot} ==="
            make_config "${gt}" "hltData_${tag}_${run}.py" "configs/${tag}_configs/hltDataDump_${tag}_${run}.py" "${snapshot}"
        done
    else
        echo "=== ${tag} (${gt}) ==="
        make_config "${gt}" "hltData_${tag}.py" "configs/hltDataDump_${tag}.py" ""
    fi
done
echo "Done"
