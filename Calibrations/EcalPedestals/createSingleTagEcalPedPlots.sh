#!/bin/bash
set -euo pipefail

tags=(
    "EcalPedestals_NGT_2023485_test"
    "EcalPedestals_NGT_1000000_test"
    "EcalPedestals_NGT_500000_test"
    "EcalPedestals_NGT_100000_test"
    "EcalPedestals_NGT_75000_test"
)


for tag in "${tags[@]}"; do
	echo "Processing tag: $tag"

	 getPayloadData.py --plugin pluginEcalPedestals_PayloadInspector --plot plot_EcalPedestalsPlot --tag "$tag" --input_params "{}" --time_type Run --iovs '{"start_iov": "400000", "end_iov": "400000"}' --db Prep --test >& out.json
	 filename=$(tail -n +2 out.json | jq -r '.file')
	mv "$filename" "plot_EcalPedestalsPlot_${tag}.png"
done
