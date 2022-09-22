from underthesea import sent_tokenize, pos_tag, dependency_parse
from preprocess import text_preprocess
from improve_pos_tag import fix_pos_tag, fix_degree
from dictionary import nonsenses


# extract aspect and value from text review
def get_aspect_value(text):
    aspect_value = {}
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
                                aspect_value[i[0]] = j[0]
                                break

    return aspect_value


# get list aspect of a category from dictionary
def get_list_aspect(dictionary, category):
    category_dict = dictionary[category]
    list_aspect = category_dict['object']['name'].copy()
    for key in category_dict['aspect']:
        for n in category_dict['aspect'][key]['name']:
            list_aspect.append(n)
    return list_aspect


# map to dictionary
def map_to_dictionary(category_dict, list_aspect, aspect_value):
    point_dict = {'điện thoại': []}
    for n in category_dict['aspect']:
        point_dict[n] = []

    for key in list(aspect_value):
        values = aspect_value[key].copy()

        # xoa key neu key khong nam trong tap aspect list_aspect lay tu dictionary
        if key not in list_aspect:
            aspect_value.pop(key)
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


