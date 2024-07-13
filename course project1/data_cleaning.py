# data_cleaning.py
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from textblob import TextBlob
import nltk
from pymongo import MongoClient
from config import MONGO_URI, DB_NAME, COLLECTION_NAME

nltk.download('stopwords')
nltk.download('punkt')

stop_words = set(stopwords.words('english'))

def clean_tweet(tweet):
    tweet = re.sub(r'http\S+', '', tweet)
    tweet = re.sub(r'@\w+', '', tweet)
    tweet = re.sub(r'#', '', tweet)
    tweet = re.sub(r'RT[\s]+', '', tweet)
    tweet = re.sub(r'\W', ' ', tweet)
    tweet = tweet.lower()
    tweet = word_tokenize(tweet)
    tweet = [word for word in tweet if word not in stop_words]
    return ' '.join(tweet)

def get_sentiment(tweet):
    analysis = TextBlob(tweet)
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

for tweet in collection.find():
    cleaned_text = clean_tweet(tweet['text'])
    sentiment = get_sentiment(cleaned_text)
    collection.update_one({'_id': tweet['_id']}, {'$set': {'cleaned_text': cleaned_text, 'sentiment': sentiment}})
