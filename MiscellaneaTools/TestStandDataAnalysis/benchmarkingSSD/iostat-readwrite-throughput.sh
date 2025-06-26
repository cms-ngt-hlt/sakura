#!/bin/bash
# Credit: https://github.com/markcurtis1970/graph-iostats

echo "usage: $0 <iostat.log> <disk name> <out.png>"
echo "procesing $1 for device $2, plotting $3"

cat $1 | grep "$2 " > dat.dat

gnuplot <<_EOF_
stats "dat.dat" using 6 name "R" nooutput
stats "dat.dat" using 7 name "W" nooutput

R_mean = R_mean
W_mean = W_mean

set terminal png
set output "$3"
set title "Read/Write Throughput (Micron 9400 PRO, RAID0, CS256k, XFS)"
set xdata time
set timefmt "%Y-%m-%d %H:%M:%S"
set format x "%M:\n%S"
set xlabel "Time"
set xtics nomirror scale 3,2
set ylabel "Throughput [MB/s]"
set yrange [0:7000]

# Add labels with averages - adjust positions (x,y) as needed
set label 1 sprintf("Avg. Read: %.2f MB/s", R_mean) at graph 0.1, 0.9 tc rgb "blue" front
set label 2 sprintf("Avg. Write: %.2f MB/s", W_mean) at graph 0.1, 0.85 tc rgb "red" front

plot "dat.dat" using 1:6 title "Read [MB/s]" with lines lw 2 lt rgb "blue", \
     "dat.dat" using 1:7 title "Write [MB/s]" with lines lw 2 lt rgb "red", \
     #R_mean title "Avg Read" with lines lc rgb "blue" dt 2, \
     #W_mean title "Avg Write" with lines lc rgb "red" dt 2
_EOF_

rm dat.dat
