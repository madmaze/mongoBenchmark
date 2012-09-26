#!/bin/bash
db='testdb'
usr='testusr'
passwd='testpw'
server='mongoServ1'
port='27017'
collection='brains'
proccnt="1 2 4 8"

for i in $proccnt; do
	echo "${i} threads:"
	echo $(date)
	for j in `seq 1 $i`; do
		python ./dump_s3.py --node-count $i --node $(($j - 1)) --db $db --user $usr --passwd $passwd --server $server --port $port --collection $collection >> out_dump_${i}_${j} &
	done
	wait
	echo $(date)
	rm -f /home/ubuntu/s3_a/*
	sync
done