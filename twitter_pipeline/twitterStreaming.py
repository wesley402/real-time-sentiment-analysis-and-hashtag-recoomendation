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
        #print (data)
        return True
    def on_error(self, status):
        print (status)

class TwitterStreaming():
    def __init__(self):
        with open('../keys/twitter_key.txt','r') as key:
            lines = key.readlines()
            self.access_token = lines[1].rstrip('\n')
            self.access_token_secret = lines[3].rstrip('\n')
            self.consumer_key = lines[5].rstrip('\n')
            self.consumer_secret = lines[7].rstrip('\n')
        self.auth = OAuthHandler(self.consumer_key, self.consumer_secret)
        self.auth.set_access_token(self.access_token, self.access_token_secret)
        self.tsl = TwitterStreamListener()

    def start(self, keywords):
        self.stream = Stream(self.auth, self.tsl)
        self.stream.filter(track=keywords, async=True)

    def stop(self):
        self.stream.disconnect()
