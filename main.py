from underthesea import sent_tokenize, pos_tag, dependency_parse
from preprocess import text_preprocess
import pandas as pd
from dictionary import dictionary, nonsenses
import os
from pymongo import MongoClient


def aspect_value(text):
    opinion = {}
    sentences = sent_tokenize(text)
    for sentence in sentences:
        sentence = text_preprocess(sentence)
        splits = sentence.split(',')
        for split in splits:
            has_nonsense = False
            for nonsense in nonsenses:
                if nonsense in split:
                    has_nonsense = True
                    break

            if not has_nonsense:
                word_tags = [list(n) for n in pos_tag(split)]
                word_tags = fix_pos_tag(word_tags)
                word_tags = fix_degree(word_tags)

                for index, i in enumerate(word_tags[:-1]):
                    if i[1] == 'N':
                        for j in word_tags[(index+1):]:
                            if j[1] == 'A':
                                opinion[i[0]] = j[0]
                                break

    return opinion


degree = ["rất", "quá", "khá", "hơi", "cũng"]
verb_to_noun = ["thiết kế", "cấu hình"]
feature_word = ["chụp", "sạc"]
adj_word = ["ok", "trâu"]
n_word = ["pin"]
v_word = ["sạc"]


def fix_pos_tag(tags):
    for tag in tags:
        if tag[0] in verb_to_noun and tag[1] == 'V':
            tag[1] = 'N'
        if tag[0] in adj_word:
            tag[1] = 'A'
        if tag[0] in n_word:
            tag[1] = 'N'
    return tags


def fix_degree(tags):
    for index, tag in enumerate(tags[:-1]):
        if tag[0] in degree and tags[index+1][1] == 'A':
            tag[0] = tag[0] + ' ' + tags[index+1][0]
            tag[1] = 'A'

    return tags


def standardized_result(list_aspect, aspects):
    # initialize point
    point_dict = {'điện thoại': []}
    for n in category_dict['aspect']:
        point_dict[n] = []

    for key in list(aspects):
        values = aspects[key].copy()

        # xoa key neu key khong nam trong tap aspect list_aspect lay tu dictionary
        if key not in list_aspect:
            aspects.pop(key)
            continue

        # gop key trong tap aspect chi san pham va map value voi diem tu dictionary
        elif key in category_dict['object'].get('name'):
            for value in values:
                for value_point in category_dict['object']['value']:
                    if value in category_dict['object']['value'].get(value_point):
                        point_dict['điện thoại'].append(int(value_point))

        else:
            for aspect in category_dict['aspect']:
                if key in category_dict['aspect'][aspect].get('name'):
                    for value in values:
                        for value_point in category_dict['aspect'][aspect]['value']:
                            if value in category_dict['aspect'][aspect]['value'].get(value_point):
                                point_dict[aspect].append(int(value_point))

    return point_dict


def aspect_average_point(point_dict):
    none_aspects = []
    for aspect in point_dict:
        if not point_dict[aspect]:
            none_aspects.append(aspect)
        else:
            point_dict[aspect] = round((sum(point_dict[aspect]) / len(point_dict[aspect])), 2)
    for n in none_aspects:
        point_dict.pop(n)
    return point_dict


def get_list_aspect(dictionary, category):
    list_aspect = dictionary[category]['object']['name'].copy()
    for key in category_dict['aspect']:
        for n in category_dict['aspect'][key]['name']:
            list_aspect.append(n)
    return list_aspect


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






