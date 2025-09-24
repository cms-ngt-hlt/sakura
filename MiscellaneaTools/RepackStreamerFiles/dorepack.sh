#!/bin/bash -ex

for i in $(seq 460 480); do

	file="file:/eos/cms/store/t0streamer/Data/Express/000/397/383/run397383_ls0${i}_streamExpress_StorageManager.dat"
    	cmsRun repack.py inputFiles=$file
    	mv repacked.root repacked_397383_ls0${i}.root
done

