#!/bin/bash


START=`date +%s`
for i in {1..10};
do 
	./microWrite.py & 
done
wait
END=`date +%s`
DIFF=$((${END}-${START}))
RPS=$(echo "100/${DIFF}" | bc -l)
LATE=$(echo "$(DIFF)/100" | bc -l)
echo "throughput is $RPS requests per second"
echo "latency is $LATE seconds per insert"
