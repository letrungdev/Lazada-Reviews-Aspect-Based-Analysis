from kafka import KafkaConsumer
from pymongo import MongoClient
from map_to_dictionary import get_list_aspect, map_to_dictionary, aspect_average_point, get_aspect_value

category = 'dien-thoai-di-dong'


def get_messages(category):
    consumer = KafkaConsumer(category, auto_offset_reset='earliest',
                             bootstrap_servers=['localhost:9092'], api_version=(0, 10), consumer_timeout_ms=1000)
    myclient = MongoClient("mongodb://localhost:27017/")
    mydb = myclient["lazada-reviews"]
    mycol = mydb[category]

    aspect_value = {}
    itemid = 0
    for msg in consumer:
        key = msg.key.decode('utf-8')
        text = msg.value.decode('utf-8')
        opinion = get_aspect_value(text)

        if key != itemid and itemid == 0:
            aspect_value['_id'] = itemid
            mycol.insert_one(aspect_value)

            # assign new itemid and aspect_value
            itemid = key


        for key in opinion:
            if aspect_value.get(key) is None:
                aspect_value[key] = [opinion[key]]
            else:
                if opinion[key] not in aspect_value[key]:
                    aspect_value[key].append(opinion[key])






    if consumer is not None:
        consumer.close()








