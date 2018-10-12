from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from kafka import SimpleProducer, KafkaClient


access_token = "1041437647405817856-DMEnXPH9ONfol0fo2ohxAlLC8lIrYu"
access_token_secret = "WhqIb7px5Gk0F9rh2sULXnCESsRSlKSMUMra6FZ4Et81N"
consumer_key = "Y8ywKhDnHFgBZ1e9anyBz5c3v"
consumer_secret = "xwyUWJvA2i7PcdWM6HFMB7c4tFyprXFuhh5z2S7k5Lzuvr9Urf"

class StdOutListener(StreamListener):
    def on_data(self, data):
        producer.send_messages("taiwan", data.encode('utf-8'))
        print (data)
        return True
    def on_error(self, status):
        print (status)

kafka = KafkaClient("localhost:9092")
producer = SimpleProducer(kafka)
l = StdOutListener()
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
stream = Stream(auth, l)
stream.filter(track=["taiwan"])
