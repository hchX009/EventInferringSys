# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    news_thread = scrapy.Field()
    news_title = scrapy.Field()
    news_time = scrapy.Field()
    news_text = scrapy.Field()
    news_source = scrapy.Field()
    news_url = scrapy.Field()
    news_source_url = scrapy.Field()
