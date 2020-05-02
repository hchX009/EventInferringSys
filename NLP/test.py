# /usr/bin/env python3
# coding: utf-8
# File: test.py
# Author: hchX009
# python 3.5

from event_extractor import EventExtrator
from event_relation_extractor import EventRelationExtractor
from file_operation import FileOperation

if __name__ == '__main__':
    content = ""
    #content = '''
    #部分研究结果显示即使在病毒传播密集地区，已有抗体的人群比例仍很低，意味着绝大多数人易感。
    #如果想回到没有封锁措施的社会，需要等待一个中长期过程。
    #因为我已经成功完成了作业了，因此我可以出去玩。
    #我出去玩，结果摔了一跤。
    #'''
    # print(content)
    file_operation = FileOperation()
    text_list = file_operation.get_file_rows_list("/home/hchx009/Downloads/source_BIO_2014_cropus.txt", 8)
    for index in range(len(text_list)):
        content += text_list[index]
    event_sets_list = list()
    event_extractor = EventExtrator()
    event_relation_extractor = EventRelationExtractor()
    event_relations_list = event_relation_extractor.event_relation_extrator_main(content)
    for event_relation in event_relations_list:
        if event_relation:
            pre_event = event_extractor.event_extrator_main(event_relation[0])
            post_event = event_extractor.event_extrator_main(event_relation[2])
            event_set = [pre_event, event_relation[1], post_event]
            event_sets_list.append(event_set)
            # print(event_set)
    for i in event_relations_list:
        print(i)
    print('\n')
    for j in event_sets_list:
        print(j)