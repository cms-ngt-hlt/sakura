#!/bin/bash
# Parameters are supplied by 04_run_nano.sh from pipeline.cfg.
set -euo pipefail
shopt -s nullglob

FILES=("${LOCALPATH}/${TAG}_run${RUN}_job"*_DQMTestDataScouting.root)
(( ${#FILES[@]} )) || { echo "ERROR: no scouting files in $LOCALPATH" >&2; exit 1; }
for f in "${FILES[@]}"; do
    [[ -s "$f" ]] || { echo "ERROR: empty input $f" >&2; exit 1; }
done
echo "Input source: $LOCALPATH (${#FILES[@]} files, listed in inputs.txt)"
# cmsDriver reads the list from the file: a comma-joined --filein exceeds the
# kernel's 128 kB limit on a single argument for runs with many input files.
printf 'file:%s\n' "${FILES[@]}" > inputs.txt

cmsDriver.py step2 -s NANO:@Scout \
    --process NANO \
    --conditions "$GTAG" \
    --datatier NANOAOD \
    -n -1 \
    --eventcontent NANOAOD \
    --geometry DB:Extended \
    --era "$ERA" \
    --filein filelist:inputs.txt \
    --fileout file:result.root \
    --nThreads "$NANO_THREADS" \
    --python_filename scoutingnano_data_standalone.py \
    --no_exec

cmsRun scoutingnano_data_standalone.py > scoutingnano_data_standalone.log 2>&1
