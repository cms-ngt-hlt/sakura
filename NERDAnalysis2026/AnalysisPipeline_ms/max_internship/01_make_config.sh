#!/bin/bash
# generate + dump ONE config for all tags.
# Needs: cmsenv already sourced. Run once (re-run only when menu/GT/paths change).
set -euo pipefail
cd "$(dirname "$0")"
source ./pipeline.cfg

[ -n "${CMSSW_BASE:-}" ] || { echo "ERROR: cmsenv not active (CMSSW_BASE unset)"; exit 1; }
mkdir -p configs
# Placeholder global tag and inputs; the shared job config overrides them at runtime.

echo "Generating hlt config file.."

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

# customize the output modules
cat <<'EOF' >> "hltData.py"
process.hltOutputLocalTestDataRaw.outputCommands = [
   'drop *',
   'keep GlobalObjectMapRecord_hltGtStage2ObjectMap_*_HLTX',
   'keep edmTriggerResults_*_*_HLTX',
   'keep triggerTriggerEvent_*_*_HLTX'
]

process.hltOutputDQMTestDataScouting.outputCommands = [
    'drop *',
    'keep *_hltFEDSelectorL1_*_HLTX',
    'keep *_hltOnlineMetaDataDigis_*_HLTX',
    'keep *_hltScoutingEgammaPacker_*_HLTX',
    'keep *_hltScoutingMuonPackerNoVtx_*_HLTX',
    'keep *_hltScoutingMuonPackerVtx_*_HLTX',
    'keep *_hltScoutingPFPacker_*_HLTX',
    'keep *_hltScoutingPrimaryVertexPacker_*_HLTX',
    'keep *_hltScoutingRecHitPacker_*_HLTX',
    'keep *_hltScoutingTrackPacker_*_HLTX',
    'keep CTPPSDiamondDigiedmDetSetVector_hltCTPPSDiamondRawToDigi_*_HLTX',
    'keep CTPPSPixelDigiedmDetSetVector_hltCTPPSPixelDigis_*_HLTX',
    'keep edmTriggerResults_*_*_HLTX',
    'keep triggerTriggerEvent_*_*_HLTX'
]

process.options.wantSummary = True
EOF
edmConfigDump "hltData.py" > "configs/hltDataDump.py" # needed for HTCondor
echo "Done!"
