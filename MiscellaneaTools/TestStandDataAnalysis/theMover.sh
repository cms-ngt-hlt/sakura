#!/bin/bash

WATCH_DIR="mergeMacro"

# how many seconds to wait between each check.
TIMING_INTERVAL=5

# store run numbers for which .global file has already been created 
declare -A processed_runs

echo "Starting monitoring of directory: '$WATCH_DIR'"
echo "The script will check for new files and folders every $TIMING_INTERVAL seconds."
echo "Press [CTRL+C] to stop the script."

while true; do

    # check for new 'run' directories
    for run_path in "${WATCH_DIR}/run"*/; do
        if [ ! -d "$run_path" ]; then
            continue
        fi

        run_basename=$(basename "$run_path")
        run_num_only=${run_basename#run}

        if [[ -z "${processed_runs[$run_num_only]}" ]]; then
            echo "New run detected: '$run_basename'. Creating global file."
            global_file="${WATCH_DIR}/${run_num_only}.global"
            echo "run_key = pp_run" > "$global_file"
            echo "  -> Created '$global_file'"
            processed_runs[$run_num_only]=1
        fi
    done

    # moves files
    for run_path in "${WATCH_DIR}/run"*/; do
        if [ ! -d "$run_path" ]; then
            continue
        fi

        data_dir="${run_path}streamLocalTestDataScouting/data"
        jsns_dir="${run_path}streamLocalTestDataScouting/jsns"
        
        destination_dir="$run_path"

        if [ -d "$data_dir" ]; then
            find "$data_dir" -maxdepth 1 -type f -name "*.dat" -print0 | while IFS= read -r -d '' file_to_move; do
                if [ -f "$file_to_move" ]; then
                    echo "  -> Moving file: '$(basename "$file_to_move")' to '$(basename "$destination_dir")/'"
                    mv "$file_to_move" "$destination_dir"
                fi
            done
        fi

        if [ -d "$jsns_dir" ]; then
            find "$jsns_dir" -maxdepth 1 -type f -name "*.jsn" -print0 | while IFS= read -r -d '' file_to_move; do
                if [ -f "$file_to_move" ]; then
                     echo "  -> Moving file: '$(basename "$file_to_move")' to '$(basename "$destination_dir")/'"
                    mv "$file_to_move" "$destination_dir"
                fi
            done
        fi
    done

    sleep "$TIMING_INTERVAL"
done


