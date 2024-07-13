# data_collection.py
import tweepy
import json
from kafka import KafkaProducer
from config import API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, KAFKA_TOPIC_NAME, KAFKA_BOOTSTRAP_SERVERS

# Setup Tweepy API
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

class TwitterStreamListener(tweepy.StreamListener):
    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                                      value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    def on_data(self, data):
        tweet = json.loads(data)
        self.producer.send(KAFKA_TOPIC_NAME, tweet)
        return True

    def on_error(self, status):
        print(status)
        return True

if __name__ == "__main__":
    stream_listener = TwitterStreamListener()
    stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
    stream.filter(track=['keyword1', 'keyword2'], languages=['en'])
