# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import CsvItemExporter


class NewsSpiderPipeline(object):
    def __init__(self):
        self.file = open('/home/hchx009/Downloads/temp_data.csv', 'wb')
        self.exporter = CsvItemExporter(self.file, encoding='UTF-8')
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        self.file.close()
