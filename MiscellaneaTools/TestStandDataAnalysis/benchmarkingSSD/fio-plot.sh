# SSD1 XFS
#MAXBW=8000
#TITLE="[SSD1, XFS, 0%]"
#DIRNAME="ssd1_xfs/empty"

#TITLE="[SSD1, XFS, 60%]"
#DIRNAME="ssd1_xfs/60full"

#TITLE="[SSD1, XFS, 90%]"
#DIRNAME="ssd1_xfs/90full"

# SSD1 EXT4
#TITLE="[SSD1, EXT4, 0%]"
#DIRNAME="ssd1_ext4/empty"

#TITLE="[SSD1, EXT4, 60%]"
#DIRNAME="ssd1_ext4/60full"

#TITLE="[SSD1, EXT4, 90%]"
#DIRNAME="ssd1_ext4/90full"

# RAID0 XFS
MAXBW=8
#TITLE="[RAID0 (1M), XFS, 0%]"
#DIRNAME="ssds_raid0_1M_xfs/empty"

#TITLE="[RAID0 (32k), XFS, 0%]"
#DIRNAME="ssds_raid0_32k_xfs/empty"

#TITLE="[RAID0 (64k), XFS, 0%]"
#DIRNAME="ssds_raid0_64k_xfs/empty"

#TITLE="[RAID0 (128k), XFS, 0%]"
#DIRNAME="ssds_raid0_128k_xfs/empty"

#TITLE="[RAID0 (CS256k), XFS, 0%, BS2M]"
#DIRNAME="ssds_raid0_cs256k_xfs/bs2M"

TITLE="[RAID0 (CS256k), XFS, 0%, BS1M]"
DIRNAME="ssds_raid0_cs256k_xfs/bs1M"

#TITLE="[RAID0 (CS256k), XFS, 0%, BS512k]"
#DIRNAME="ssds_raid0_cs256k_xfs/bs512k"

#TITLE="[RAID0 (CS256k), XFS, 0%, BS256k]"
#DIRNAME="ssds_raid0_cs256k_xfs/bs256k"

#TITLE="[RAID0 (CS256k), XFS, 0%, BS128k]"
#DIRNAME="ssds_raid0_cs256k_xfs/bs128k"

#TITLE="[RAID0 (CS256k), XFS, 0%, BS64k]"
#DIRNAME="ssds_raid0_cs256k_xfs/bs64k"

#TITLE="[RAID0 (512k), XFS, 0%]"
#DIRNAME="ssds_raid0_512k_xfs/empty"

#TITLE="[RAID0 (64k), XFS, 0%]"
#DIRNAME="ssds_raid0_64k_xfs/empty"

#TITLE="[RAID0 (2M), XFS, 0%]"
#DIRNAME="ssds_raid0_2M_xfs/empty"

#TITLE="[RAID0 (1M), XFS, 60%]"
#DIRNAME="ssds_raid0_1M_xfs/60full"

#TITLE="[RAID0 (1M), XFS, 90%]"
#DIRNAME="ssds_raid0_1M_xfs/90full"

# RAID0 EXT4
#TITLE="[RAID0 (1M), EXT4, 0%]"
#DIRNAME="ssds_raid0_1M_ext4/empty"

#TITLE="[RAID0 (1M), EXT4, 60%]"
#DIRNAME="ssds_raid0_1M_ext4/60full"

#TITLE="[RAID0 (1M), EXT4, 90%]"
#DIRNAME="ssds_raid0_1M_ext4/90full"

# LVM striping XFS
#TITLE="[LVM Striping, XFS, 0%]"
#DIRNAME="ssds_LVMstriping_xfs/empty"

#TITLE="[LVM Striping, XFS, 60%]"
#DIRNAME="ssds_LVMstriping_xfs/60full"

#TITLE="[LVM Striping, XFS, 90%]"
#DIRNAME="ssds_LVMstriping_xfs/90full"

# Comparisons
#TITLE="[SSD1 Comparisons, XFS, 0%]"
#MAXBW=8000

PLOTDIR=/eos/user/m/mzarucki/www/2025/NGT/SAKURA/SSDbenchmarks/bandwidth/realistic/$DIRNAME
LOGDIRBASE=/eos/user/m/mzarucki/NGT/SAKURA/demonstrator/SSDbenchmarks/fio_logs/realistic
LOGDIR=$LOGDIRBASE/$DIRNAME
mkdir -p $PLOTDIR

# time series
#fio-plot -i $LOGDIR -r read      -d 1 32 64 -n 1 5 10 -t bw -g --max-bw $MAXBW --disable-fio-version -o $PLOTDIR/read_${DIRNAME//\//_}.png            --title "Read Bandwidth (Micron 9400 PRO, $TITLE)"
#fio-plot -i $LOGDIR -r write     -d 1 32 64 -n 1 5 10 -t bw -g --max-bw $MAXBW --disable-fio-version -o $PLOTDIR/write_${DIRNAME//\//_}.png           --title "Write Bandwidth (Micron 9400 PRO, $TITLE)"
#fio-plot -i $LOGDIR -r readwrite -d 1 32 64 -n 1 5 10 -t bw -g --max-bw $MAXBW --disable-fio-version -o $PLOTDIR/readwrite_${DIRNAME//\//_}.png       --title "Read & Write Bandwidth (Micron 9400 PRO, $TITLE)"
#fio-plot -i $LOGDIR -r readwrite -d 1 32    -n 1 5 10 -t bw -g --max-bw $MAXBW --disable-fio-version -o $PLOTDIR/readwrite_${DIRNAME//\//_}.png       --title "Read & Write Bandwidth (Micron 9400 PRO, $TITLE)"
#fio-plot -i $LOGDIR -r readwrite -d 1 32 64 -n 1 5 10 -t bw -g --max-bw $MAXBW --disable-fio-version -o $PLOTDIR/readwrite-total_${DIRNAME//\//_}.png --title "Read & Write Bandwidth (Micron 9400 PRO, $TITLE)" --draw-total -f read write

# Draw total

# 3D
#fio-plot -i $LOGDIR -r read  -d 1 32 64 -n 1 5 10 --title "Read Bandwidth (Micron 9400 PRO, $TITLE)" -t bw -L

# different benchmarks
fio-plot -i $LOGDIRBASE/ssds_raid0_cs256k_xfs/bs1M $LOGDIRBASE/ssds_raid0_cs256k_xfs/bs2M -r readwrite -d 1 -n 10 --title "Read & Write Bandwidth (Micron 9400 PRO, $TITLE)" -o $PLOTDIR/readwrite_comparisons.png -C
#fio-plot -i $LOGDIRBASE/ssd1_xfs/empty $LOGDIRBASE/ssd1_ext4/empty -r read -d 1 -n 10 --title "Read & Write Bandwidth (Micron 9400 PRO, $TITLE)" -o $PLOTDIR/read_comparisons.png -C
#fio-plot -i $LOGDIRBASE/ssd1_xfs/empty $LOGDIRBASE/ssd1_ext4/empty -r readwrite -d 1 -n 10 --title "Read & Write Bandwidth (Micron 9400 PRO, $TITLE)" -o $PLOTDIR/readwrite_comparisons.png --compare-graph
