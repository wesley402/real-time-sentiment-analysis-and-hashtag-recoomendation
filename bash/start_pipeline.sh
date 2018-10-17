#!/bin/bash

# setup virtualenv
cd ..
source env/bin/activate

# start streaming
cd /twitter_pipeline
python3 producer.py & spark-streaming.py

echo "=================================================="
read -p "PRESS [ENTER] TO TERMINATE PROCESSES." PRESSKEY
kill $(jobs -p)
