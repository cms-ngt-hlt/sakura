#iostat -dxm 5 /dev/md0
#iostat -dxm 5 /dev/md0 | awk '// {print strftime("%Y-%m-%d %H:%M:%S"),$0}'
timeout 15m iostat -dxm 5 /dev/md0 | awk '// {print strftime("%Y-%m-%d %H:%M:%S"),$0}' > iostat_copy-sleep23-loop_conversion-6files_chunk256k_samplingWindow5_noCache.out
