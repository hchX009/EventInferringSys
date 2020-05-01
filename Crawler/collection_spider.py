# /usr/bin/env python3
# coding: utf-8
# File: collection_spider.py
# Author: hchX009
# python 3.5

import scrapy

class CollectionSpider(scrapy.Spider):

    def start_request(self):
        cnbeta_urls = ['https://www.cnbeta.com/category/tech.htm',
                       # 'https://www.cnbeta.com/category/movie.htm',
                       # 'https://www.cnbeta.com/category/music.htm',
                       # 'https://www.cnbeta.com/category/game.htm',
                       # 'https://www.cnbeta.com/category/comic.htm',
                       # 'https://www.cnbeta.com/category/funny.htm',
                       # 'https://www.cnbeta.com/category/science.htm',
                       # 'https://www.cnbeta.com/category/soft.htm',
                       ]
        for url in cnbeta_urls:
            yield scrapy.Request(url=url, callback=self.parse)
