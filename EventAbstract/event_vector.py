# /usr/bin/env python3
# coding: utf-8
# File: event_vector.py
# Author: hchX009
# python 3.5


from gensim.models import KeyedVectors
from IO.database_operation import MongoOperation
from NLP.ltp_parser import LtpParser
import numpy


class EventVector:
    def __init__(self):
        self.mongo_operation = MongoOperation()
        self.ltp_parser = LtpParser()
        self.words_embedding_file = "../Data/Tencent_AILab_ChineseEmbedding/Tencent_AILab_ChineseEmbedding.txt"
        self.wv_from_text = KeyedVectors.load_word2vec_format(self.words_embedding_file, binary=False, limit=100000)
        self.wv_from_text.init_sims(replace=True)

    # 从数据库中得到事件三组元按“,”划分的事件，并不重复
    def get_event_from_triple(self):
        event_triple_sets = self.mongo_operation.event_db_get()
        event_sets = list()
        for event_triple in event_triple_sets:
            event = event_triple.split(',')[0]
            if event not in event_sets:
                event_sets.append(event)
            event = event_triple.split(',')[2]
            if event not in event_sets:
                event_sets.append(event)
        return event_sets

    # 得到事件的向量（词向量平均得到）
    def get_event_vectors(self, event_sets):
        for event in event_sets:
            words_list = self.ltp_parser.get_words_by_pyltp(event)
            # print(words_list)
            # 建立长度向量长度的0向量
            vector_sum = [0 for index in range(self.wv_from_text.wv.syn0[0].shape[0])]
            for word in words_list:
                vector = self.wv_from_text[word]
                # print(vector)
                vector_sum = list(numpy.array(vector_sum) + numpy.array(vector))
            # print(vector_sum)
            event_vector = [i / len(words_list) for i in vector_sum]
            print(event_vector)
        return


if __name__ == "__main__":
    event_vector = EventVector()
    event_sets = event_vector.get_event_from_triple()
    print(event_sets)
    event_vector.get_event_vectors(event_sets)