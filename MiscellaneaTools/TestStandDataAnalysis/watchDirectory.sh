#!/bin/bash
WATCH_DIR=$PWD
SCRIPT_DIR=$PWD
CMD="cmsRun $SCRIPT_DIR/convertStreamerToFRD.py filePrepend=file: runNumber=390811 inputFiles=" # FIXME: runNumber to be retrieved from DAQ

echo "Monitoring directory:" $WATCH_DIR
echo "Script directory:" $SCRIPT_DIR

FILES=`ls -t "$WATCH_DIR"`
seenfiles=($FILES)
while true; do
  NEWFILES=`ls -t "$WATCH_DIR"`
  if [ "$NEWFILES" != "$FILES" ]; then
    echo "Changes in directory detected."
    for f in $NEWFILES; do
      if [[ ! " ${seenfiles[*]} " =~ " $f " && "$f" == *.dat ]]; then
        echo "New streamer file detected: $f"
        seenfiles+=("$f")
        LOGFILE="$SCRIPT_DIR/convertStreamerToFRD_${f%.dat}.log"
        CMD_FULL="$CMD$WATCH_DIR/$f"
        echo "Running command: $CMD_FULL" 
        $CMD_FULL >& $LOGFILE &
      fi
    done
    FILES="$NEWFILES"
  fi
  sleep 24
done
