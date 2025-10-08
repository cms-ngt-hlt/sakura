#!/bin/bash
set -euo pipefail

tags=(
    "EcalPedestals_NGT_2023485_test"
    "EcalPedestals_NGT_1000000_test"
    "EcalPedestals_NGT_500000_test"
    "EcalPedestals_NGT_100000_test"
    "EcalPedestals_NGT_75000_test"
)

for ((i=0; i<${#tags[@]}; i++)); do
    for ((j=i+1; j<${#tags[@]}; j++)); do
        tag1="${tags[i]}"
        tag2="${tags[j]}"

        echo "Processing pair: $tag1 vs $tag2"

        for plot in plot_EcalPedestalsDiffTwoTags plot_EcalPedestalsRatioTwoTags; do
            getPayloadData.py \
                --plugin pluginEcalPedestals_PayloadInspector \
                --plot "$plot" \
                --tag "$tag1" \
                --tagtwo "$tag2" \
                --input_params "{}" \
                --time_type Run \
                --iovs '{"start_iov": "400000", "end_iov": "400000"}' \
                --iovstwo '{"start_iov": "400000", "end_iov": "400000"}' \
                --db Prep --test >& out.json

            filename=$(tail -n +2 out.json | jq -r '.file')
            filename=$(head -n 1 out.json | awk '{print $6}')
            mv "$filename" "${plot}_${tag1}_vs_${tag2}.png"
        done
    done
done

