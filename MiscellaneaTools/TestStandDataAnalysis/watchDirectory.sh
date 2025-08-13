#!/bin/bash
WATCH_DIR="/fff/ssdcache/sm-c2b13-21-01_ssdcache/mergeMacro"
SCRIPT_DIR="/opt/hltteststand"
OUTPUT_DIR="/fff/ramdisk"
LOG_DIR="/tmp/conversion"
STREAM="LocalTestDataRaw"

mkdir -p "$LOG_DIR"

CMD="cmsRun $SCRIPT_DIR/convertStreamerToFRD.py filePrepend=file: outputPath=$OUTPUT_DIR"
TIMESTAMP="awk '{print strftime(\"%Y-%m-%d %H:%M:%S\"), \$0}'"

echo "Monitoring directory: $WATCH_DIR" | eval $TIMESTAMP
echo "Script directory: $SCRIPT_DIR" | eval $TIMESTAMP

is_file_stable() {
  local file="$1"
  local last_size=$(stat --printf="%s" "$file" 2>/dev/null)
  sleep 1
  local new_size=$(stat --printf="%s" "$file" 2>/dev/null)
  [[ "$last_size" -eq "$new_size" ]]
}

NEWEST_DIR=""
FILES=""
seenfiles=()
seenruns=()

while true; do
  NEW_DIR=$(ls -td "$WATCH_DIR"/run*/stream"$STREAM"/data 2>/dev/null | head -n1)

  if [[ -n "$NEW_DIR" && ! " ${seenruns[*]} " =~ " $NEW_DIR " && -d "$NEW_DIR" ]]; then
    echo "New run directory detected: $NEW_DIR" | eval $TIMESTAMP
    NEWEST_DIR="$NEW_DIR"
    seenruns+=("$NEWEST_DIR")
    seenfiles=()
    FILES=""
  fi

  if [[ -n "$NEWEST_DIR" ]]; then
    NEWFILES=$(ls -t "$NEWEST_DIR"/*.dat 2>/dev/null)

    if [ "$NEWFILES" != "$FILES" ]; then
      for f in $NEWFILES; do
        fname=$(basename "$f")
        if [[ ! " ${seenfiles[*]} " =~ " $fname " && "$fname" == *.dat ]]; then

          until is_file_stable "$f"; do
            sleep 1
          done

          echo "New streamer file detected: $fname" | eval $TIMESTAMP
          seenfiles+=("$fname")

	  RUN_NUMBER_DIR=$(basename "$(dirname "$(dirname "$NEWEST_DIR")")")
          RUN_NUMBER=${RUN_NUMBER_DIR#run}

          LOGFILE="$LOG_DIR/convertStreamerToFRD_${fname%.dat}.log"
          CMD_FULL="$CMD inputFiles=$f runNumber=$RUN_NUMBER"

          (
            echo "Running command: $CMD_FULL" | eval $TIMESTAMP >> "$LOGFILE" &&
            $CMD_FULL >& "$LOGFILE" && 
            echo "Conversion completed. Deleting input streamer file $fname." | eval "$TIMESTAMP" >> "$LOGFILE" &&
            ./addMissingEoLS.sh $RUN_NUMBER &&
            # addMissingEoLS.sh only required for test runs not starting from LS = 1
            sleep 5 &&
            rm "$f"
          ) &
        fi
      done
      FILES="$NEWFILES"
    fi
  fi
  sleep 2
done
