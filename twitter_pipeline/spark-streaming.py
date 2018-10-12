from pyspark.streaming.kafka import KafkaUtils
from pyspark import SparkContext, SparkConf
import pyspark
from pyspark.streaming import StreamingContext
import findspark
import json, os
import time, sys
import pymongo_spark
pymongo_spark.activate()

# Add the streaming package and initialize
findspark.add_packages(["org.apache.spark:spark-streaming-kafka-0-8_2.11:2.2.2"])
findspark.init()
# Create a local StreamingContext with two working thread and batch interval of 1 second
#sc = SparkContext("local[2]", "NetworkWordCount")
#ssc = StreamingContext(sc, 1)
TOPICS = ['taiwan']
BROKERS = "localhost:9092"
PERIOD = 10
APP_NAME = 'sentiment'
COMPANY = 'taiwan'

sc = SparkContext(appName="PythonStreamingDirectKafkaWordCount")
# except:
#     conf = SparkConf().set("spark.default.paralleism", 1)
#     spark = pyspark.sql.SparkSession.builder \
#                                     .master("local[4]") \
#                                     .appName(APP_NAME) \
#                                     .config(conf=conf)  \
#                                     .getOrCreate()
    # sc = spark.sparkContext
#create a streaming context with batch interval 10 sec
ssc = StreamingContext(sc, PERIOD)
directKafkaStream = KafkaUtils.createDirectStream(
                        ssc,
                        TOPICS,
                        {"metadata.broker.list": BROKERS})

def detectSentiment(text):
    nlp = StanfordNLP('http://localhost:9000')
    output = nlp.annotate(, properties={
        'annotators': 'sentiment',
        'outputFormat': 'json'
    })
    numOfSentence = len(output['sentences'])
    for sentiment in output['sentences']:
        if sentiment['value'] == 1:
            numOfNegative = numOfNegative + 1
        else if sentiment['value'] == 2:
            numOfNeutral = numOfNeutral + 1
        else:
            numOfPositive = numOfPositive + 1
    return {'numOfSentence': numOfSentence, 'numOfNegative': numOfNegative,
            'numOfNeutral': numOfNeutral, 'numOfPositive': numOfPositive}

def updateRDD(rdd, dict):
    rdd.update(dict)
    return rdd


parsed = directKafkaStream.map(lambda x: json.loads(x[1])) \
                          .map(lambda x: {'created_at': x['created_at'].encode('ascii', 'ignore'),
                                          'company': COMPANY, 'text': x['text'].encode('ascii', 'ignore')}) \
                          .map(lambda x: updateRDD(x, detectSentiment(x, detectSentiment(x, detectSentiment( x['text']))))


ssc.start()
try:
    stream_time = int(sys.argv[1])
except:

    stream_time = 5
time.sleep(stream_time*60)
ssc.awaitTermination()

#ssc.stop(stopSparkContext=False, stopGraceFully=True)
