from pyspark.streaming.kafka import KafkaUtils
from pyspark import SparkContext, SparkConf
import pyspark
from pyspark.streaming import StreamingContext
import findspark
import json, os
import time, sys
from stanfordNLP import StanfordNLP
import redis

def detectSentiment(text):
    nlp = StanfordNLP('http://localhost:9000')
    output = nlp.annotate(text, properties={
        'annotators': 'sentiment',
        'outputFormat': 'json'
    })
    numOfSentence = len(output['sentences'])
    numOfNegative, numOfNeutral,  numOfPositive= 0, 0, 0
    valueSum = 0
    for sentiment in output['sentences']:
        valueSum += float(sentiment['sentimentValue'])

    sentimentValue = valueSum / float(numOfSentence)
    return {'sentimentValue': sentimentValue}

def store_in_redis(rdd):
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    if r.get('numOfTweets') is not None and r.get('sentimentValue') is not None:
        preSentimentValue = float(r.get('numOfTweets').decode('utf8')) * \
                            float(r.get('sentimentValue').decode('utf8'))
        curSentimentValue = preSentimentValue + rdd['sentimentValue']
        r.set('numOfTweets', float(r.get('numOfTweets').decode('utf8')) + 1)
        r.set('sentimentValue', curSentimentValue / float(r.get('numOfTweets').decode('utf8')))
        r.set('created_at', rdd['created_at'])
    else:
        r.set('company', rdd['company'])
        r.set('numOfTweets', 1)
        r.set('sentimentValue', rdd['sentimentValue'])
        r.set('created_at', rdd['created_at'])

def updateRDD(rdd, dict):
    rdd.update(dict)
    print(rdd['created_at'])
    return rdd


# Add the streaming package and initialize
findspark.add_packages(["org.apache.spark:spark-streaming-kafka-0-8_2.11:2.2.2"])
findspark.init()
TOPICS = ['taiwan']
BROKERS = "localhost:9092"
PERIOD = 10
APP_NAME = 'sentiment'
COMPANY = 'taiwan'

sc = SparkContext(appName="PythonStreamingDirectKafkaWordCount")
sc.addPyFile(os.path.dirname(os.path.join(os.path.realpath(__file__), 'stanfordNLP.py')))

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




parsed = directKafkaStream.map(lambda x: json.loads(x[1])) \
                          .map(lambda x: {'created_at': x['created_at'],
                                          'company': COMPANY, 'text': x['text']}) \
                          .map(lambda x: updateRDD(x, detectSentiment(x['text']))) \
                          .map(lambda x: store_in_redis(x))

parsed.pprint()


ssc.start()
try:
    stream_time = int(sys.argv[1])
except:
    stream_time = 5
time.sleep(stream_time*60)
ssc.awaitTermination()

#ssc.stop(stopSparkContext=False, stopGraceFully=True)
