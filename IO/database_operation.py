# /usr/bin/env python3
# coding: utf-8
# File: database_operation.py
# Author: hchX009
# python 3.5


import pymongo


class MongoOperation():
    def __init__(self):
        self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        dblist = self.myclient.list_database_names()
        if "newsdb" not in dblist:
            self.news_db = self.myclient["newsdb"]
            self.news = self.news_db["news"]
        if "eventdb" not in dblist:
            self.event_db = self.myclient["eventdb"]
            self.events = self.event_db["events"]
        if "abstractdb" not in dblist:
            self.abstract_event_db = self.myclient["abstractdb"]
            self.abstracts = self.abstract_event_db["abstracts"]

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
        self.news.insert_one(data)
