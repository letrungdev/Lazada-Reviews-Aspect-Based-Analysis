import pandas as pd
import os
from map_to_dictionary import get_list_aspect, map_to_dictionary, aspect_average_point, get_aspect_value
from pymongo import MongoClient
from dictionary import dictionary


if __name__ == '__main__':
    category = 'dien-thoai-di-dong'
    myclient = MongoClient("mongodb://localhost:27017/")
    mydb = myclient["lazada-reviews"]
    mycol = mydb[category]

    category_dict = dictionary[category]
    list_aspect = get_list_aspect(dictionary, category)
    category_folder = 'lazada_reviews/dien-thoai-di-dong'

    # list reviews by product
    products = os.listdir(category_folder)
    for product in products:
        aspects = {}
        path = category_folder + '/' + product
        try:
            data = pd.read_csv(path).values.tolist()
            for record in data:
                try:
                    opinion = get_aspect_value(record[1])
                    for key in opinion:
                        if aspects.get(key) is None:
                            aspects[key] = [opinion[key]]
                        else:
                            if opinion[key] not in aspects[key]:
                                aspects[key].append(opinion[key])
                except:
                    continue
        except:
            continue

        aspects = map_to_dictionary(category_dict, list_aspect, aspects)
        aspects = aspect_average_point(aspects)
        print(aspects)
        aspects['_id'] = product.replace('.csv', '')
        mycol.insert_one(aspects)






