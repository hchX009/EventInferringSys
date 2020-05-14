# /usr/bin/env python3
# coding: utf-8
# File: get_model.py
# Author: hchX009
# python 3.5

from gensim.models import Word2Vec
from gensim.models import KeyedVectors

words_embedding_file = "../Data/Tencent_AILab_ChineseEmbedding/Tencent_AILab_ChineseEmbedding.txt"
wv_from_text = KeyedVectors.load_word2vec_format(words_embedding_file, binary=False)

sentences = [[],[]]

# 使用默认CBOW算法，默认维数100
model = Word2Vec(sentences, min_count=1)

