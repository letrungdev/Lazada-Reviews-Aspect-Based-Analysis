from dictionary import to_noun, to_adj, degree


def fix_pos_tag(tags):
    for tag in tags:
        if tag[0] in to_noun:
            tag[1] = 'N'
        if tag[0] in to_adj:
            tag[1] = 'A'
    return tags


def fix_degree(tags):
    for index, tag in enumerate(tags[:-1]):
        if tag[0] in degree and tags[index+1][1] == 'A':
            tag[0] = tag[0] + ' ' + tags[index+1][0]
            tag[1] = 'A'
    return tags