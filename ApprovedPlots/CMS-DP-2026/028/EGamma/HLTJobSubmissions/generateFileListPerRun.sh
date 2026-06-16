#!/bin/bash

# list of run numbers, compiled "by hand"
runs=(
"398675"
"398680"
"398681"
"398682"
"398683"
"398787"
"398797"
"398801"
"398802"
"398803"
"398827"
"398828"
"398858"
)

for run in "${runs[@]}"; do
    output_file="run_${run}.txt"
    
    dasgoclient --query="file dataset=/EGamma1/Run2025G-ZElectron-PromptReco-v1/RAW-RECO run=${run}" > "$output_file"
    
    # Check if the file is empty (optional check to see if files were found)
    if [ ! -s "$output_file" ]; then
        echo "  Warning: No files found for run ${run} (output is empty)."
    else
        echo "  Saved output to $output_file"
    fi
done

echo "---"
echo "Done! All queries executed."
