#!/bin/bash

SOURCE_DIR="/fff/output/input"
DEST_DIR="/data/ssds"
TIMESTAMP="awk '{print strftime(\"%Y-%m-%d %H:%M:%S\"), \$0}'"

#while true; do
  echo "Clearing cache... " | eval $TIMESTAMP
  sync
  echo 3 | sudo tee /proc/sys/vm/drop_caches > /dev/null 

  for file in "$SOURCE_DIR"/*; do
    [ -f "$file" ] || continue
    echo "Copying: $(basename "$file")" | eval $TIMESTAMP
    cp "$file" "$DEST_DIR"
    sleep 23
  done
#done
