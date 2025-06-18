fio --name=fill60 --directory=/data/ssd1 --rw=write --bs=1M --size=2095G --numjobs=8 --iodepth=16  --ioengine=libaio --direct=1
#fio --name=fill60 --directory=/data/ssds --rw=write --bs=1M --size=2095G --numjobs=16 --iodepth=16 --ioengine=libaio --direct=1
#fio --name=fill30 --directory=/data/ssd1 --rw=write --bs=1M --size=864G  --numjobs=10 --iodepth=16 --ioengine=libaio --direct=1
#fio --name=fill30 --directory=/data/ssds --rw=write --bs=1M --size=864G  --numjobs=18 --iodepth=16 --ioengine=libaio --direct=1

#nohup fio --name=fill60 --directory=/data/ssd1 --rw=write --bs=1M --size=2095G --numjobs=8  --iodepth=16 --ioengine=libaio --direct=1 > fill60.log 2>&1 &
#nohup fio --name=fill60 --directory=/data/ssds --rw=write --bs=1M --size=2095G --numjobs=16 --iodepth=16 --ioengine=libaio --direct=1 > fill60.log 2>&1 &
#nohup fio --name=fill30 --directory=/data/ssd1 --rw=write --bs=1M --size=864G  --numjobs=10 --iodepth=16 --ioengine=libaio --direct=1 > fill30.log 2>&1 &
#nohup fio --name=fill30 --directory=/data/ssds --rw=write --bs=1M --size=864G  --numjobs=18 --iodepth=16 --ioengine=libaio --direct=1 > fill30.log 2>&1 &
