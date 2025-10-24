#!/bin/bash

BASE_DIR="/fff/dqmruburamdisk"
WATCH_DIR="${BASE_DIR}/mergeMacro"
STREAM="DQMOnlineScouting"
SLEEP_INTERVAL=2

echo "INFO: Starting monitoring of directory every $SLEEP_INTERVAL seconds: $WATCH_DIR"

# ensure file is stable
file_is_stable() {
  local file="$1"
  local last_size=$(stat --printf="%s" "$file" 2>/dev/null)
  sleep 1
  local new_size=$(stat --printf="%s" "$file" 2>/dev/null)
  [[ "$last_size" -eq "$new_size" ]]
}

# store run numbers
runs=()

while true; do

    # check for new run directories
    for run_path in "${WATCH_DIR}/run"*/; do
        if [ ! -d "$run_path" ]; then
            continue
        fi

        run_dir=$(basename "$run_path")
        run=${run_dir#run}

        if [[ ! " ${runs[*]} " =~ " $run " ]]; then
            echo "INFO: New run $run detected"
            global_file="${BASE_DIR}/.${run_dir}.global"
            echo "run_key = pp_run" > "$global_file" &&
            echo "INFO: Created $(basename ${global_file}) file in ${BASE_DIR}"
            runs+=("$run")
        fi
    done

    # move files
    for run_path in "${WATCH_DIR}/run"*/; do
        if [ ! -d "$run_path" ]; then
            continue
        fi
        
        data_dir="${run_path}stream${STREAM}/data"
        jsns_dir="${run_path}stream${STREAM}/jsns"
        
        run_dir=$(basename "$run_path")
        dest_dir="${BASE_DIR}/${run_dir}"
        mkdir -p "$dest_dir"

        if [[ -d "$data_dir" && -d "$jsns_dir" ]]; then
            for dat_file in "$data_dir"/*.dat; do
                file_base=$(basename "$dat_file" .dat)
                [[ -e "$dat_file" ]] && file_is_stable "$dat_file" || continue
                
                nls=$(echo "$file_base" | sed -E 's/.*_ls0*([0-9]+)_.*$/\1/')
                jsn_file="${jsns_dir}/${file_base}.jsn"

                if [[ -f "$jsn_file" ]]; then
                    echo "INFO: Found matching streamer and JSN pair for LS ${nls}"
                    echo "INFO: Moving streamer file: $(basename "$dat_file") to $dest_dir"
                    mv "$dat_file" "$dest_dir"
                    echo "INFO: Moving JSN file: $(basename "$jsn_file") to $dest_dir"
                    mv "$jsn_file" "$dest_dir"
                fi
            done
        fi
    done
    sleep "$SLEEP_INTERVAL"
done
