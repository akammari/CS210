# data_storage.py
from pymongo import MongoClient
from kafka import KafkaConsumer
import json
from config import KAFKA_TOPIC_NAME, KAFKA_BOOTSTRAP_SERVERS, MONGO_URI, DB_NAME, COLLECTION_NAME

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

consumer = KafkaConsumer(KAFKA_TOPIC_NAME,
                         bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                         auto_offset_reset='earliest',
                         value_deserializer=lambda x: json.loads(x.decode('utf-8')))

for message in consumer:
    tweet = message.value
    collection.insert_one(tweet)
