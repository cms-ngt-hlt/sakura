#!/bin/bash
WATCH_DIR=$PWD
SCRIPT_DIR=$PWD
CMD="cmsRun $SCRIPT_DIR/convertStreamerToFRD.py filePrepend=file: outputPath=/fff/output/output"
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

FILES=`ls -t "$WATCH_DIR"`
seenfiles=($FILES)

while true; do
  NEWFILES=`ls -t "$WATCH_DIR"`
  if [ "$NEWFILES" != "$FILES" ]; then
    for f in $NEWFILES; do
      if [[ ! " ${seenfiles[*]} " =~ " $f " && "$f" == *.dat ]]; then
	FULL_PATH="$WATCH_DIR/$f"

        echo "New streamer file detected: $f" | eval $TIMESTAMP
        until is_file_stable "$FULL_PATH"; do
          sleep 1
        done

        echo "New stable streamer file detected: $f" | eval $TIMESTAMP
        seenfiles+=("$f")

        RUN_NUMBER=${f#run} # FIXME: runNumber to be retrieved from DAQ instead of file name
        RUN_NUMBER=${RUN_NUMBER%%_*}

        LOGFILE="$SCRIPT_DIR/logs/convertStreamerToFRD_${f%.dat}.log"
        CMD_FULL="$CMD inputFiles=$FULL_PATH runNumber=$RUN_NUMBER"

	echo "Clearing cache..." | eval "$TIMESTAMP"
	sync
	echo 3 | sudo tee /proc/sys/vm/drop_caches > /dev/null

	(
          echo "Running command: $CMD_FULL" | eval $TIMESTAMP
          $CMD_FULL >& "$LOGFILE" && \
          echo "Conversion completed. Deleting file $f and output FRD files." | eval "$TIMESTAMP" && \
	  sleep 5 && \
          rm "$WATCH_DIR/$f" && \
          rm /fff/output/output/run*/${f%%_stream*}_index*.raw
        ) &
      fi
    done
    FILES="$NEWFILES"
  fi
  sleep 3
done
