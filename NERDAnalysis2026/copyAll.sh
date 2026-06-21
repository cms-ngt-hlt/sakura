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
