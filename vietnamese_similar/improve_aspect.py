import json
from gensim.models import KeyedVectors


def semi():
	f = open("Viet74K.txt", encoding='utf-8')
	list_word = [x.replace('\n', '') for x in f]
	list_word = list(set(list_word))
	list_word = {x: 1 for x in list_word}

	dir = 'wiki.vi.model.bin'
	model = KeyedVectors.load_word2vec_format(dir, binary=True)
	out = {}
	print(len(model.index_to_key))

	for x in model.index_to_key:
		if list_word.get(x) is not None:
			try:
				out[x] = [[y[0].replace('_', ' ').strip(), y[1]] for y in model.most_similar(x, topn=50) if y[1] >= 0.5]
				print(x + '\n')
				print(out[x])
			except:
				continue
	with open('similar_vietnamese.json', 'w', encoding='utf8') as f:
		json.dump(out, f, ensure_ascii=False, indent=4)


semi()
