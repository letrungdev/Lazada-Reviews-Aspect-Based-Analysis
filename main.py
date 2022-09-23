from kafka import KafkaConsumer
from pymongo import MongoClient
from map_to_dictionary import get_list_aspect, map_to_dictionary, aspect_average_point, get_aspect_value
from dictionary import dictionary


def get_messages(category):
    consumer = KafkaConsumer(category, auto_offset_reset='earliest',
                             bootstrap_servers=['localhost:9092'], api_version=(0, 10), consumer_timeout_ms=1000)
    items = {}
    for msg in consumer:
        key = msg.key.decode('utf-8')
        if items.get(key) is None:
            items[key] = {}
        text = msg.value.decode('utf-8')
        opinion = get_aspect_value(text)
        for aspect in opinion:
            if items[key].get(aspect) is None:
                items[key][aspect] = [opinion[aspect]]
            else:
                items[key][aspect].append(opinion[aspect])

    if consumer is not None:
        consumer.close()

    return items


if __name__ == "__main__":
    category = 'dien-thoai-di-dong'
    category_dict = dictionary[category]
    list_aspect = get_list_aspect(dictionary, category)
    myclient = MongoClient("mongodb://localhost:27017/")
    mydb = myclient["lazada-reviews"]
    mycol = mydb[category]
    items = get_messages(category)
    for item in items:
        aspects = map_to_dictionary(category_dict, list_aspect, items[item])
        aspects = aspect_average_point(aspects)
        aspects['_id'] = item
        print(aspects)
        mycol.insert_one(aspects)







