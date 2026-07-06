#!/bin/bash

if ! voms-proxy-info -exists -valid 0:5 >  /dev/null 2>&1; then
	echo "Error no valid GRID proxy found, or it will be expiring in 5 minutes"
	echo "Please run 'voms-proxy-init --voms cms' and try again."
fi

BASE="https://cmsweb.cern.ch"
PREFIX="$BASE/dqm/online/data/browse/Offline/Run2026/Online"
CERT="/tmp/x509up_u$(id -u)"
CAPATH="/etc/grid-security/certificates"

START=4035
END=4040

mkdir -p dqm_files
cd dqm_files

for n in $(seq $START $END); do
    folder=$(printf "%07dxx" "$n")     # 4035 -> 0004035xx
    index_url="$PREFIX/$folder/"

    echo "=== Folder: $folder ==="

    file_list=$(curl -s --capath "$CAPATH" --cert "$CERT" --key "$CERT" "$index_url" \
                | grep -oP "href='\K[^']+\.root")

    if [[ -z "$file_list" ]]; then
        echo "  (no .root files found, or folder doesn't exist yet — skipping)"
        continue
    fi

    while read -r path; do
        fname=$(basename "$path")
        if [[ -f "$fname" ]]; then
            echo "  skip $fname (already exists)"
            continue
        fi
        echo "  downloading $fname"
        curl -s --capath "$CAPATH" --cert "$CERT" --key "$CERT" \
             -o "$fname" "$BASE$path"
    done <<< "$file_list"
done



cd ../
DIR="dqm_files"
MISMATCH_DIR="dqm_files_mismatched"

mkdir -p "$MISMATCH_DIR"

echo "Scanning $DIR for mismatched run files..."

ngt_runs=$(ls "$DIR"/*NGT*.root 2>/dev/null | grep -o 'R000[0-9]\{6\}' | sort)
hts_runs=$(ls "$DIR"/*Test*.root 2>/dev/null | grep -o 'R000[0-9]\{6\}' | sort)

ngt_only=$(comm -23 <(echo "$ngt_runs") <(echo "$hts_runs"))
hts_only=$(comm -13 <(echo "$ngt_runs") <(echo "$hts_runs"))

mismatched_runs=$(echo -e "${ngt_only}\n${hts_only}" | grep -v '^$')

if [[ -z "$mismatched_runs" ]]; then
    echo "All files have perfect twins! Nothing to move."
    exit 0
fi

echo "Found orphaned files. Moving them to $MISMATCH_DIR:"
for run in $mismatched_runs; do
    echo "  -> Quarantining files for run: $run"
    mv "$DIR"/*"${run}"*.root "$MISMATCH_DIR"/ 2>/dev/null
done

echo "Cleanup complete! Your dqm_files folder is now perfectly symmetric."
