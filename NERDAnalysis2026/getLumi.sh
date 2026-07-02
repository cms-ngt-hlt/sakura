#!/bin/bash -ex


export PATH=$HOME/.local/bin:/cvmfs/cms-bril.cern.ch/brilconda/bin:$PATH
brilcalc lumi --begin 403550 --end 404100 -u /pb --output-style csv > lumi_data.csv

