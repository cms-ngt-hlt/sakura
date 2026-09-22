#!/bin/bash
# Optional existing HLT source client, until its cmsDriver recipe is ready.
set -euo pipefail
shopt -s nullglob

FILES=("${LOCALPATH}/${TAG}_run${RUN}_job"*_LocalTestDataRaw.root)
(( ${#FILES[@]} )) || { echo "ERROR: no HLT files in $LOCALPATH" >&2; exit 1; }
ALL_FILES=""
for f in "${FILES[@]}"; do
    [[ -s "$f" ]] || { echo "ERROR: empty input $f" >&2; exit 1; }
    ALL_FILES+="file:${f},"
done
ALL_FILES="${ALL_FILES%,}"
echo "Input source: $LOCALPATH"
echo "Discovered files: $ALL_FILES"
printf '%s\n' "${FILES[@]}" > inputs.txt

cmsDriver.py step2 -s DQM:onlinehlt4vector \
    --conditions "$GTAG" \
    --datatier DQMIO \
    -n -1 \
    --eventcontent DQMIO \
    --geometry DB:Extended \
    --era "$ERA" \
    --filein "$ALL_FILES" \
    --fileout file:step2.root \
    --nThreads "$DQM_THREADS" \
    --customise_commands 'process.hltObjectMonitor.processName = cms.string("HLTX")' \
    --python_filename dqm.py \
    --no_exec

cmsRun dqm.py > dqm.log 2>&1

cmsDriver.py step3 -s HARVESTING:@standardDQM \
    --conditions 160X_dataRun3_HLT_v1 \
    --data \
    --geometry DB:Extended \
    --scenario pp \
    --filetype DQM \
    --era "$ERA" \
    -n -1 \
    --filein file:step2.root \
    --fileout file:step3.root \
    --python_filename harvesting.py \
    --no_exec

cmsRun harvesting.py > harvesting.log 2>&1

rm -f step2.root

# The harvester writes the histogram file separately from step2's DQMIO.
OUTPUTS=(DQM*.root)
(( ${#OUTPUTS[@]} == 1 )) || { echo "ERROR: expected one harvested DQM file" >&2; exit 1; }
cp "${OUTPUTS[0]}" result.root
