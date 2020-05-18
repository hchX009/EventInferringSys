# /usr/bin/env python3
# coding: utf-8
# File: event_vector.py
# Author: hchX009
# python 3.5


from gensim.models import Word2Vec
from gensim.models import KeyedVectors

class EventVector:
    def __init__(self):
        pass

    def get_event_from_triple(self):

        return

    def get_event_words(self, event):

        return


words_embedding_file = "../Data/Tencent_AILab_ChineseEmbedding/Tencent_AILab_ChineseEmbedding.txt"
wv_from_text = KeyedVectors.load_word2vec_format(words_embedding_file, binary=False, limit=100000)
wv_from_text.init_sims(replace=True)

word = '书记'

vector = wv_from_text[word]

print(vector)

#sentences = [[],[]]

# 使用默认CBOW算法，默认维数100
#model = Word2Vec(sentences, min_count=1)


