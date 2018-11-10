from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from kafka import SimpleProducer, KafkaClient

class TwitterStreamListener(StreamListener):
    def __init__(self):
        kafkaClient = KafkaClient("localhost:9092")
        self.producer = SimpleProducer(kafkaClient)
    def on_data(self, data):
        self.producer.send_messages("taiwan", data.encode('utf-8'))
        print (data)
        return True
    def on_error(self, status):
        print (status)

class TwitterStreaming():

    stream = None
    auth = None
    tsl = None
    def __init__(self):
        self.auth = OAuthHandler(self.consumer_key, self.consumer_secret)
        self.auth.set_access_token(self.access_token, self.access_token_secret)
        self.tsl = TwitterStreamListener()

    def start(self, keywords):
        self.stream = Stream(self.auth, self.tsl)
        self.stream.filter(track=keywords, async=True)

    def stop(self):
        self.stream.disconnect()
