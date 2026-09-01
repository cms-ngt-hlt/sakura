for ds in $(dasgoclient -query="dataset dataset=/Muon*/Run2025G-ZMu-PromptReco-v1/RAW-RECO"); do
    echo "Querying files for: $ds"
    dasgoclient -query="file dataset=$ds run=398858"
done
