#!/bin/bash

RUN_NUMBER=396309
MAX_LS=${1:-10}
SLEEP_TIME=23
SOURCE_DIR="/fff/ssdcache/run${RUN_NUMBER}"
SOURCE_FILE="run${RUN_NUMBER}_ls0205_streamLocalTestDataRaw_StorageManager.dat"
SOURCE_PATH="$SOURCE_DIR/$SOURCE_FILE"
DEST_BASE="/fff/ssdcache/mergeMacro"

LS_START=$(echo "$SOURCE_FILE" | grep -oP 'ls\K\d+')
LS_START=$((10#$LS_START))

DEST_RUN=$(((1 * 10**9) + RUN_NUMBER))
DEST_DIR="${DEST_BASE}/run${DEST_RUN}/streamLocalTestDataRaw/data"

TIMESTAMP="awk '{print strftime(\"%Y-%m-%d %H:%M:%S\"), \$0}'"

sudo mkdir -p "$DEST_DIR"

for ((LS=LS_START; LS<LS_START + MAX_LS; LS++)); do
  OUTFILE=$(printf "run%d_ls%04d_streamLocalTestDataRaw_StorageManager.dat" "$DEST_RUN" "$LS")
  DEST_PATH="$DEST_DIR/$OUTFILE"

  echo "Copying $SOURCE_PATH to $DEST_PATH" | eval $TIMESTAMP
  sudo cp "$SOURCE_PATH" "$DEST_PATH" &
  
  sleep $SLEEP_TIME
done
