import tweepy
import json
from pymongo import MongoClient
from config import API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, MONGO_URI, DB_NAME, COLLECTION_NAME

# Setup Tweepy API
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Setup MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

class TwitterStreamListener(tweepy.Stream):
    def on_data(self, data):
        tweet = json.loads(data)
        collection.insert_one(tweet)
        return True

    def on_error(self, status):
        print(status)
        return True

if __name__ == "__main__":
    stream_listener = TwitterStreamListener()
    stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
    stream.filter(track=['keyword1', 'keyword2'], languages=['en'])
