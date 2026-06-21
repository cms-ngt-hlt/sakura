BASE="https://cmsweb.cern.ch"
INDEX_URL="$BASE/dqm/online/data/browse/Offline/Run2026/Online/0004035xx/"
CERT="/tmp/x509up_u$(id -u)"
CAPATH="/etc/grid-security/certificates"

mkdir -p dqm_files
cd dqm_files

curl -s --capath "$CAPATH" --cert "$CERT" --key "$CERT" "$INDEX_URL" \
  | grep -oP "href='\K[^']+\.root" \
  | while read -r path; do
      fname=$(basename "$path")
      if [[ -f "$fname" ]]; then
          echo "Skipping $fname (already exists)"
          continue
      fi
      echo "Downloading $fname"
      curl -s --capath "$CAPATH" --cert "$CERT" --key "$CERT" \
           -o "$fname" "$BASE$path"
    done
