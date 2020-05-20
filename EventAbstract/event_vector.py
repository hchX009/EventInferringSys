# /usr/bin/env python3
# coding: utf-8
# File: event_vector.py
# Author: hchX009
# python 3.5


from gensim.models import Word2Vec
from gensim.models import KeyedVectors
from IO.database_operation import MongoOperation
from NLP.ltp_parser import LtpParser


class EventVector:
    def __init__(self):
        self.mongo_operation = MongoOperation()
        self.ltp_parser = LtpParser()

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

    def get_event_words(self, event_sets):
        for event in event_sets:
            words_list = self.ltp_parser.get_words_by_pyltp(event)
            print(words_list)
        #words_embedding_file = "../Data/Tencent_AILab_ChineseEmbedding/Tencent_AILab_ChineseEmbedding.txt"
        #wv_from_text = KeyedVectors.load_word2vec_format(words_embedding_file, binary=False, limit=100000)
        #wv_from_text.init_sims(replace=True)

        #word = '书记'

        #vector = wv_from_text[word]

        #print(vector)

        # sentences = [[],[]]

        # 使用默认CBOW算法，默认维数100
        # model = Word2Vec(sentences, min_count=1)

        return


if __name__ == "__main__":
    event_vector = EventVector()
    event_sets = event_vector.get_event_from_triple()
    print(event_sets)
    event_vector.get_event_words(event_sets)