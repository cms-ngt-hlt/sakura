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
printf '%s\n' "${FILES[@]}" > inputs.txt

mkdir -p upload
cp "$CMSSW_SRC/DQM/Integration/python/clients/hlt_dqm_sourceclient-live_cfg.py" client.py
cmsRun client.py inputFiles="$ALL_FILES" > dqm.log 2>&1

OUTPUTS=(upload/*.root)
(( ${#OUTPUTS[@]} == 1 )) || { echo "ERROR: expected one final HLT DQM file in upload/" >&2; exit 1; }
cp "${OUTPUTS[0]}" result.root
