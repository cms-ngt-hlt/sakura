#!/bin/bash

SOURCE_DIR="/fff/ssdcache/sm-c2b13-21-01_ssdcache/run392642"
DEST_DIR="/fff/ssdcache/sm-c2b13-21-01_ssdcache/mergeMacro/run392642/streamLocalTestDataRaw/data"
TIMESTAMP="awk '{print strftime(\"%Y-%m-%d %H:%M:%S\"), \$0}'"

sudo mkdir -p "$DEST_DIR"

#while true; do
  #echo "Clearing cache... " | eval $TIMESTAMP
  #sync
  #echo 3 | sudo tee /proc/sys/vm/drop_caches > /dev/null 

  for file in "$SOURCE_DIR"/*; do
    [ -f "$file" ] || continue
    echo "Copying: $(basename "$file")" | eval $TIMESTAMP
    sudo cp "$file" "$DEST_DIR"
    sleep 23
  done
#done
