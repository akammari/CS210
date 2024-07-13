import tweepy
import config

consumer_key = config.API_KEY
consumer_secret = config.API_SECRET_KEY

access_token = config.ACCESS_TOKEN
access_token_secret = config.ACCESS_TOKEN_SECRET

auth = tweepy.OAuth1UserHandler(
    consumer_key, consumer_secret, access_token, access_token_secret
)

api = tweepy.API(auth)

print(api.verify_credentials().screen_name)

public_tweets = api.home_timeline()
for tweet in public_tweets:
    print(tweet.text)