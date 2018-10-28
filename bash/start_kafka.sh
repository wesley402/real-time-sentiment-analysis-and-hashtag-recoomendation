#!/bin/bash
cd ../tools/zookeeper-3.4.12
bin/zkServer.sh start
cd ../kafka_2.11-2.0.0
bin/kafka-server-start.sh config/server.properties
