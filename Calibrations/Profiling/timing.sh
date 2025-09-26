#!/bin/bash

#Add configurations to test. These correspond to python config files named NAME_config.py
hlt_config_names=("expressStep2_RAW2DIGI_RECO_ALCAPRODUCER" "expressStep2_RAW2DIGI_RECO_ALCAPRODUCER_trimmed")

# Add presets here as needed following the "jobs,threads,streams" format
jobs_threads_streams_presets=(
    #"64,4,4"
    "32,8,8"
    #"8,32,32"
    #"8,32,24"
)

# GPU Monitoring Configuration
ENABLE_GPU_MONITORING=false  # Set to 'false' to disable GPU memory checks
MONITOR_INTERVAL=1           # Check GPU memory every X seconds
USE_FLOATING_POINT_MEAN=true # Use 'bc' for a more precise mean; falls back to integer if 'bc' not found

# Check prerequisites for GPU Monitoring
if [[ "$ENABLE_GPU_MONITORING" = true ]]; then
    # Check for nvidia-smi
    if ! command -v nvidia-smi &>/dev/null; then
        echo "Error: GPU Monitoring is enabled, but 'nvidia-smi' command not found. Aborting."
        exit 1
    fi

    # Check for bc if floating point mean is requested
    if [[ "$USE_FLOATING_POINT_MEAN" = true ]] && ! command -v bc &>/dev/null; then
        echo "Warning: 'bc' command not found, will fall back to integer division for mean calculation."
        USE_FLOATING_POINT_MEAN=false
    fi

    # Function to get current total GPU memory usage
    get_current_total_gpu_mem() {
        nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits | awk '{ total += $1 } END { print total }' || echo "error"
    }
fi

# Benchmark execution
echo "Starting HLT benchmark for configurations: ${hlt_config_names[@]}"
echo "With jobs,threads,streams presets: ${jobs_threads_streams_presets[@]}"
echo "GPU Memory Monitoring is: ${ENABLE_GPU_MONITORING}"
echo "----------------------------------------------------"

for config_name in "${hlt_config_names[@]}"; do
    echo "Configuration: $config_name"
    cfg="${config_name}_config.py"

    for preset in "${jobs_threads_streams_presets[@]}"; do
        IFS=',' read -r jobs threads streams <<<"$preset"
        echo "  Running with Preset: jobs=$jobs, threads=$threads, streams=$streams"

        events=1000
        logdir="logs.$config_name.${jobs}j.${threads}t.${streams}s"
        output_filename="${config_name}_${jobs}j_${threads}t_${streams}s.json"

        # Setup patatrack-scripts and log directory
        if [ ! -d 'patatrack-scripts' ]; then
            echo "Cloning patatrack-scripts repository"
            git clone git@github.com:cms-patatrack/patatrack-scripts.git --depth 1
        fi
        if [ ! -d "${logdir}" ]; then
            echo "Creating directory for the logs at ${logdir}"
            mkdir -p "${logdir}"
        fi

        # Run the benchmark
        if [[ "$ENABLE_GPU_MONITORING" = true ]]; then
            # With GPU monitoring
            CSV_FILE="${logdir}/gpu_memory_${config_name}_${jobs}j_${threads}t_${streams}s.csv"
            TMP_LOG_FILE="${logdir}/benchmark.tmp.log"
            echo "elapsed_seconds,memory_mib" >"$CSV_FILE"

            # Initialize monitoring variables
            max_total_memory_mib=0
            sum_total_memory_mib=0
            measurement_count=0
            START_TIME=$(date +%s)

            echo "    Starting benchmark with GPU memory monitoring..."

            # Start the benchmark, redirecting output to a temporary log file
            patatrack-scripts/benchmark -j ${jobs} -t ${threads} -s ${streams} -e ${events} --run-io-benchmark \
                -k timing_tracking_upperbound_s2.json --event-skip 100 --event-resolution 25 --wait 30 \
                --logdir ${logdir} -- ${cfg} >"$TMP_LOG_FILE" 2>&1 &
            PROGRAM_PID=$!

            # Display the benchmark's output live using tail -f
            tail -f "$TMP_LOG_FILE" &
            TAIL_PID=$!

            # Set up a trap to kill background jobs if the script is interrupted (e.g., with Ctrl+C)
            trap "kill $TAIL_PID &>/dev/null; kill $PROGRAM_PID &>/dev/null; echo -e '\nScript interrupted, processes cleaned up.'" EXIT SIGINT SIGTERM

            # The monitoring loop checks on the benchmark program
            while ps -p $PROGRAM_PID >/dev/null; do
                current_total_mem=$(get_current_total_gpu_mem)
                if [[ "$current_total_mem" =~ ^[0-9]+$ ]]; then
                    current_time=$(date +%s)
                    elapsed_seconds=$((current_time - START_TIME))
                    echo "$elapsed_seconds,$current_total_mem" >>"$CSV_FILE"
                    if ((current_total_mem > max_total_memory_mib)); then max_total_memory_mib=$current_total_mem; fi
                    sum_total_memory_mib=$((sum_total_memory_mib + current_total_mem))
                    measurement_count=$((measurement_count + 1))
                fi
                sleep $MONITOR_INTERVAL
            done

            # The benchmark has finished, so we can stop the 'tail' process
            kill $TAIL_PID &>/dev/null

            # Disable the trap now that this section is complete
            trap - EXIT SIGINT SIGTERM

            # Rename the temporary log to the final log file
            mv "$TMP_LOG_FILE" "${logdir}/output.log"

            mean_total_memory_mib="N/A"
            if ((measurement_count > 0)); then
                if [[ "$USE_FLOATING_POINT_MEAN" = true ]]; then
                    mean_total_memory_mib=$(echo "scale=2; $sum_total_memory_mib / $measurement_count" | bc)
                    mean_calculation_note="(float using bc)"
                else
                    mean_total_memory_mib=$((sum_total_memory_mib / measurement_count))
                    mean_calculation_note="(integer)"
                fi
            fi

            # Append GPU monitoring results to the log file and print to console
            tee -a "${logdir}/output.log" <<EOF

-------------------------------------
           GPU MEMORY USAGE
-------------------------------------
Monitoring Interval: $MONITOR_INTERVAL second(s)
Number of Measurements: $measurement_count
Data points saved to: '$CSV_FILE'

Peak Total GPU Memory Usage: $max_total_memory_mib MiB
Mean Total GPU Memory Usage: $mean_total_memory_mib MiB $mean_calculation_note
-------------------------------------
EOF
        else
            # Without GPU Monitoring
            echo "    Starting benchmark without GPU memory monitoring..."
            patatrack-scripts/benchmark -j ${jobs} -t ${threads} -s ${streams} -e ${events} --run-io-benchmark \
                -k timing_tracking_upperbound_s2.json --event-skip 100 --event-resolution 25 --wait 30 \
                --logdir ${logdir} -- ${cfg} | tee ${logdir}/output.log
        fi

        # Post-processing
        mergeResourcesJson.py ${logdir}/step*/pid*/timing_tracking_upperbound_s2.json >${output_filename}

        script_dir=$(dirname -- "$0")
        if [ -f "$script_dir/augmentResources.py" ]; then
            echo "Running augmentResources.py"
            python3 "$script_dir/augmentResources.py"
        fi

        cp -p ${output_filename} ${logdir}
        cp -p ${cfg} ${logdir}
        echo "  Finished processing preset with jobs=$jobs, threads=$threads, streams=$streams"
        echo ""
    done # End of inner loop (presets)
    echo "Finished processing configuration: $config_name"
done # End of outer loop (configurations)

echo "All HLT configurations have been processed successfully."
