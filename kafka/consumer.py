from kafka import KafkaConsumer
from pymongo import MongoClient


category = 'dien-thoai-di-dong'


def get_messages(category):
    myclient = MongoClient("mongodb://localhost:27017/")
    mydb = myclient["lazada-reviews"]
    mycol = mydb[category]
    consumer = KafkaConsumer(category, auto_offset_reset='earliest',
                             bootstrap_servers=['localhost:9092'], api_version=(0, 10), consumer_timeout_ms=1000)

    aspect_point = {}
    itemid = 0
    mycol.insert_one(aspect_point)
    for msg in consumer:
        key = msg.key.decode('utf-8')
        itemid = key
        text = msg.value.decode('utf-8')
        print(text)

    if consumer is not None:
        consumer.close()