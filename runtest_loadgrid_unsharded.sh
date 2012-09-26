#!/bin/bash
db='testdb2'
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
		python ./load_s3.py --node-count $i --node $(($j - 1)) --db $db --user $usr --passwd $passwd --server $server --port $port --collection $collection >> out_load_unsharded_${i}_${j} &
	done
	wait
	echo $(date)
	python emptyGrid.py --db $db --user $usr --passwd $passwd --server $server --port $port --collection $collection
done