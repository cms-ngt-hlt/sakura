# benchmarkingSSD
Scripts for running benchmarks on SSDs

## SSD benchmarking

### FIO
SSD (Micron 9400 PRO) benchmarking with [FIO (Flexible I/O tester)](https://fio.readthedocs.io). Benchmarking with configuration job file `benchmark_micron9400pro.fio` that runs 27 different benchmarks with realistic global I/O settings: read, write, read & write; with single or multiple I/O threads: 
```bash
fio benchmark_micron9400pro.fio --output-format=json --output benchmark_micron9400pro.json
```
which can be ran inside a `fio_logs` directory via `./fio_run.sh`.

Time series performance data in the logs in `fio_logs` can be plotted using [fio-plot](https://github.com/louwrentius/fio-plot):
```bash
fio-plot -i fio_logs -r read  -d 1 32 64 -n 1 5 10 --title "Read Bandwidth (Micron 9400 PRO)" -t bw -g
```
To install `fio-plot` on LXPLUS, it's best to do so in a virtual environment:
```
python3 -m venv fioenv
source fioenv/bin/activate
git clone https://github.com/louwrentius/fio-plot.git
cd fio-plot
pip install -r requirements.txt
```

3D plots of the average bandwidths (extracted from the output JSON files), can be plotted by running either `plot_bandwidth_iodepthJobs.py` or `plot_bandwidth_chunkBlock.py` (modifying the internal hard-coded parameters), to show their dependence on the I/O or queue depth (`iodepth`), parallel I/O jobs (`numjobs`), RAID0 chunk size, or striping granularity, (`cs`) and data block size (`bs`). 

### iostat

`iostat` measures the I/O to a device (e.g. `/dev/md0` which is the RAID0 partition of both SSDs) via:
```
iostat -dxm 5 /dev/md0
```
which can be ran in a standardised way via `./iostat_run.sh`.
