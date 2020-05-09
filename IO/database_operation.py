# /usr/bin/env python3
# coding: utf-8
# File: database_operation.py
# Author: hchX009
# python 3.5


import pymongo


class MongoOperation():
    def __init__(self):
        self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        # 新闻数据库
        self.news_db = self.myclient["newsdb"]
        self.news = self.news_db["news"]
        # 事件数据库
        self.event_db = self.myclient["eventdb"]
        self.events = self.event_db["events"]
        # 抽象事件数据库
        self.abstract_event_db = self.myclient["abstractdb"]
        self.abstracts = self.abstract_event_db["abstracts"]

    # 将爬到的新闻放入数据库中
    def news_db_add(self, dataline):
        data = {
            "news_thread": dataline['news_thread'],
            "news_title": dataline['news_title'],
            "news_time": dataline['news_time'],
            "news_text": dataline['news_text'],
            "news_url": dataline['news_url'],
            "news_source": dataline['news_source'],
            "news_source_url": dataline['news_source_url']
        }
        res = self.news.insert_one(data)
        return res

    # 将获得的事件三组元放入数据库中
    def event_db_add(self, datalines):
        datas = list()
        for event_set in datalines:
            events_list_pre = event_set[0]
            events_list_post = event_set[2]
            for event_pre in events_list_pre:
                for event_post in events_list_post:
                    if event_pre and event_post:
                        data = {
                            "pre_event": ''.join(event_pre),
                            "relation": event_set[1],
                            "post_event": ''.join(event_post)
                        }
                        datas.append(data)
        res = self.events.insert_many(datas)
        return res
