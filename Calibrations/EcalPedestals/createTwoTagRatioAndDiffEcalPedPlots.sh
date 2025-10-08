#!/bin/bash
set -euo pipefail

# reference (highest-statistics) tag
ref_tag="EcalPedestals_NGT_2023485_test"

# other tags to compare against the reference
tags=(
    "EcalPedestals_NGT_1000000_test"
    "EcalPedestals_NGT_500000_test"
    "EcalPedestals_NGT_100000_test"
    "EcalPedestals_NGT_75000_test"
)

for tag in "${tags[@]}"; do
    echo "Processing comparison: ${ref_tag} vs ${tag}"

    for plot in plot_EcalPedestalsDiffTwoTags plot_EcalPedestalsRatioTwoTags; do
        echo "  → Generating $plot"

        getPayloadData.py \
            --plugin pluginEcalPedestals_PayloadInspector \
            --plot "$plot" \
            --tag "$ref_tag" \
            --tagtwo "$tag" \
            --input_params "{}" \
            --time_type Run \
            --iovs '{"start_iov": "400000", "end_iov": "400000"}' \
            --iovstwo '{"start_iov": "400000", "end_iov": "400000"}' \
            --db Prep --test >& out.json

        filename=$(tail -n +2 out.json | jq -r '.file')

        mv "$filename" "${plot}_${ref_tag}_vs_${tag}.png"
    done
done

