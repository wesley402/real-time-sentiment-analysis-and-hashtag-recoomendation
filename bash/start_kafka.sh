#!/bin/bash

# start zookeeper
cd ../tools/zookeeper-3.4.12
bin/zkServer.sh start

cd ../kafka_2.11-2.0.0
#start kafka service
bin/kafka-server-start.sh config/server.properties

#start another window
#create topic


echo "=================================================="
read -p "PRESS [ENTER] TO TERMINATE PROCESSES." PRESSKEY

kill $(jobs -p)
