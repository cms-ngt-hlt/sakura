#!/bin/bash

SOURCE_DIR="input"
DEST_DIR="/data/ssds"
TIMESTAMP="awk '{print strftime(\"%Y-%m-%d %H:%M:%S\"), \$0}'"

while true; do
  for file in "$SOURCE_DIR"/*; do
    [ -f "$file" ] || continue
    echo "Copying: $(basename "$file")" | eval $TIMESTAMP
    cp "$file" "$DEST_DIR"
    sleep 23
  done

  echo "Clearing page caches."
  sync
  echo 3 | sudo tee /proc/sys/vm/drop_caches > /dev/null 
done
