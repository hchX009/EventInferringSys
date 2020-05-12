# /usr/bin/env python3
# coding: utf-8
# File: get_model.py
# Author: hchX009
# python 3.5

from gensim.models import Word2Vec

sentences = [[],[]]

# 使用默认CBOW算法，默认维数100
model = Word2Vec(sentences, min_count=1)

