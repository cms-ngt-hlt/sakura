iostat -dxm 1 600 /dev/md0 | awk '// {print strftime("%Y-%m-%d %H:%M:%S"),$0}' > iostat_copy-sleep23-loop_conversion-14files_chunk256k_samplingWindow1_noCache.out &
iostat -dxm /dev/md0 1 600
