#!/bin/bash

SOURCE_DIR="input"
DEST_DIR="/data/ssds"
TIMESTAMP="awk '{print strftime(\"%Y-%m-%d %H:%M:%S\"), \$0}'"

while true; do
  echo "Clearing cache..."
  sync
  echo 3 | sudo tee /proc/sys/vm/drop_caches > /dev/null 

  for file in "$SOURCE_DIR"/*; do
    [ -f "$file" ] || continue
    echo "Copying: $(basename "$file")" | eval $TIMESTAMP
    cp "$file" "$DEST_DIR"
    sleep 23
  done
  #rm -r output/run*/*.raw # FIXME: this is too aggressive in freeing up the ramdisk (400 GB) as it also deletes files that are being written by the conversion
done
