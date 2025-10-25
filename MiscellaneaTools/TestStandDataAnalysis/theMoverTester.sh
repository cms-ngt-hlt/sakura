#!/bin/bash

# --- Configuration ---
# This should match the WATCH_DIR in your other script.
TARGET_DIR="mergeMacro"

# How many seconds to wait before creating a NEW 'run' directory.
NEW_RUN_INTERVAL=15

# How many seconds to wait between creating each new file within a run.
NEW_FILE_INTERVAL=3

# How many files (.dat and .jsn) to create for each run.
FILES_PER_RUN=5

# --- Script Logic ---

# To be safe, create the main directory if it doesn't already exist.
mkdir -p "$TARGET_DIR"

echo "Starting test data generator..."
echo "It will create a new 'run' directory every $NEW_RUN_INTERVAL seconds."
echo "Each run will have $FILES_PER_RUN pairs of .dat and .jsn files created."
echo "Press [CTRL+C] to stop the script."

# Initialize the run counter.
run_counter=23153

# This is the main loop that runs forever, generating data.
while true; do
    # Define the path for the current run.
    run_path="${TARGET_DIR}/run${run_counter}"
    echo "---"
    echo "Creating new run directory: $(basename "$run_path")"

    # Define the specific subdirectories for data and json files.
    data_dir="${run_path}/streamLocalTestDataScouting/data"
    jsns_dir="${run_path}/streamLocalTestDataScouting/jsns"

    # Create the full directory structure needed for this run.
    mkdir -p "$data_dir"
    mkdir -p "$jsns_dir"

    # Create a batch of files for the current run.
    for i in $(seq 1 $FILES_PER_RUN); do
        # Use nanoseconds for a more unique filename.
        timestamp=$(date +%s%N)
        
        # Create a dummy .dat file.
        dat_file="${data_dir}/event_${timestamp}.dat"
        echo "This is a dummy dat file." > "$dat_file"
        echo "  -> Created $(basename "$dat_file")"

        # Create a dummy .jsn file.
        jsn_file="${jsns_dir}/event_${timestamp}.jsn"
        echo '{ "status": "dummy_json" }' > "$jsn_file"
        echo "  -> Created $(basename "$jsn_file")"

        # Wait a moment before creating the next file.
        sleep "$NEW_FILE_INTERVAL"
    done

    # Increment the counter for the next run.
    run_counter=$((run_counter + 1))

    # Wait for a longer period before starting the next run.
    echo "Waiting $NEW_RUN_INTERVAL seconds until next run..."
    sleep "$NEW_RUN_INTERVAL"
done

