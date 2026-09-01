#!/bin/bash
# generate + dump ONE config for all tags.
# Needs: cmsenv already sourced. Run once (re-run only when menu/GT/paths change).
set -euo pipefail
cd "$(dirname "$0")"
source ./pipeline.cfg

[ -n "${CMSSW_BASE:-}" ] || { echo "ERROR: cmsenv not active (CMSSW_BASE unset)"; exit 1; }
mkdir -p configs
# empty input, just like here https://github.com/jprendi/sakura/blob/main/ApprovedPlots/CMS-DP-2026/028/EGamma/HLTJobSubmissions/EGammaFullHLT.sh
# GT is also left empty - gets later overwriten by 02_submit.py!!!
hltGetConfiguration "${HLT_MENU}" \
  --globaltag " " \
  --data \
  --unprescale \
  --output none \
  --max-events -1 \
  --eras "${ERA}" \
  --l1-emulator uGT --l1 "${L1_MENU}" \
  --paths "${HLT_PATHS}" \
  --input " " \
  > "hltData.py"

cat <<'EOF' >> "hltData.py"
# customize the output modules
process.hltOutputLocalTestDataRaw.outputCommands = [
   'drop *',
   'keep GlobalObjectMapRecord_hltGtStage2ObjectMap_*_HLTX',
   'keep edmTriggerResults_*_*_HLTX',
   'keep triggerTriggerEvent_*_*_HLTX'
]
# make summary available (needed by 03_check.py's HLT-Report parsing)
process.options.wantSummary = True
EOF
module load lxbatch/eossubmit
edmConfigDump "hltData.py" > "configs/hltDataDump.py" # needed for HTCondor
echo "Done"
