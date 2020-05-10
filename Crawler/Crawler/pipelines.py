# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sys
sys.path.append("../..")
from IO.file_operation import FileOperation
from IO.database_operation import MongoOperation


class NewsSpiderPipeline(object):
    def __init__(self):
        self.file = FileOperation()
        self.db = MongoOperation()

    def process_item(self, item, spider):
        self.file.get_news_list_file(item)
        self.db.news_db_add(item)
        return item

    def spider_closed(self, spider):
        pass
