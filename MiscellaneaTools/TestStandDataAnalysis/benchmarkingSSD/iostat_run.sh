timeout 3m iostat -dxm 5 /dev/md0 | awk '// {print strftime("%Y-%m-%d %H:%M:%S"),$0}' > iostat_conversion_single_chunk1M.out
