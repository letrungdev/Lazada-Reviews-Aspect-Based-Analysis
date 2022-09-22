import pandas as pd
import os
from pymongo import MongoClient


if __name__ == '__main__':
    category = 'dien-thoai-di-dong'
    category_dict = dictionary[category]
    list_aspect = get_list_aspect(dictionary, category)
    category_folder = 'lazada_reviews/dien-thoai-di-dong'

    myclient = MongoClient("mongodb://localhost:27017/")
    mydb = myclient["lazada-reviews"]
    mycol = mydb[category]
    # list reviews by product
    products = os.listdir(category_folder)
    for product in products:
        aspects = {}
        path = category_folder + '/' + product
        try:
            data = pd.read_csv(path).values.tolist()
            for record in data:
                try:
                    opinion = aspect_value(record[1])
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

        aspect_point = standardized_result(list_aspect, aspects)
        aspect_point = aspect_average_point(aspect_point)
        print(aspect_point)
        aspect_point['_id'] = product.replace('.csv', '')
        mycol.insert_one(aspect_point)






