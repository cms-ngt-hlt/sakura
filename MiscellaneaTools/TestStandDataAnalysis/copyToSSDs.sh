#!/bin/bash

RUN_NUMBER=396309
MAX_LS=${1:-10}
SLEEP_TIME=23
SOURCE_DIR="/fff/ssdcache/sm-c2b13-21-01_ssdcache/run${RUN_NUMBER}"
SOURCE_FILE="run${RUN_NUMBER}_ls0205_streamLocalTestDataRaw_StorageManager.dat"
DEST_BASE="/fff/ssdcache/sm-c2b13-21-01_ssdcache/mergeMacro"

DEST_RUN=$((1000 + RUN_NUMBER))
DEST_DIR="${DEST_BASE}/run${DEST_RUN}/streamLocalTestDataRaw/data"

TIMESTAMP="awk '{print strftime(\"%Y-%m-%d %H:%M:%S\"), \$0}'"

sudo mkdir -p "$DEST_DIR"

for ((LS=1; LS<=MAX_LS; LS++)); do
  OUTFILE=$(printf "run%d_ls%04d_streamLocalTestDataRaw_StorageManager.dat" "$DEST_RUN" "$LS")
  DEST_PATH="$DEST_DIR/$OUTFILE"
  
  echo "Copying to: $DEST_PATH" | eval $TIMESTAMP
  
  sudo cp "$SOURCE_DIR/$SOURCE_FILE" "$DEST_PATH"
  
  if [ "$LS" -lt "$MAX_LS" ]; then
      sleep $SLEEP_TIME
  fi
done
