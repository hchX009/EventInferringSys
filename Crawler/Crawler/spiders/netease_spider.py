from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from Crawler.items import NewsSpiderItem
import datetime


# 用输入开始日期和结束日期来制作基础网址，格式：20200504
def get_base_url(start, end):
    bace_url = "https://news.163.com/"
    if start == end:
        return [bace_url + end[2:3] + '/' + end[4:] + '/']
    date_start = datetime.datetime.strptime(start, '%Y%m%d')
    date_end = datetime.datetime.strptime(end, '%Y%m%d')
    bace_urls_list = list()
    while date_start <= date_end:
        bace_urls_list.append(bace_url + date_start.strftime('%Y/%m%d')[2:] + '/')
        date_start += datetime.timedelta(days=1)
    return bace_urls_list


class NetEaseSpider(CrawlSpider):
    # 爬虫名称
    name = 'netease'
    # 定义爬取网址
    start_urls = ['https://news.163.com/domestic/',
                  'https://news.163.com/world/']
    # 允许的爬取域
    allowed_domains = ['news.163.com']

    # 爬取规则
    rules = [
        Rule(LinkExtractor(allow=r'({0})\d+/.*?html'.format(bace_url)
                           ), callback='parse_item', follow=True) for bace_url in get_base_url('20200503', '20200504')
    ]

    def parse_item(self, response):
        item = NewsSpiderItem()
        item['news_thread'] = response.url.strip().split('/')[-1][:-5]
        self.get_source(response, item)
        self.get_source_url(response, item)
        self.get_url(response, item)
        self.get_time(response, item)
        self.get_title(response, item)
        self.get_text(response, item)
        return item

    def get_text(self, response, item):
        text = response.css('.post_text p::text').extract()
        if text:
            print('text:{}'.format(text))
            item['news_text'] = text

    def get_url(self, response, item):
        url = response.url
        print(url)
        if url:
            item['news_url'] = url

    def get_title(self, response, item):
        title = response.css('title::text').extract()
        if title:
            print('title:{}'.format(title[0]))
            item['news_title'] = title[0]

    def get_time(self, response, item):
        time = response.css('div.post_time_source::text').extract()
        if time:
            print('time:{}'.format(time[0].strip().replace('来源', '').replace('\u3000', '')))
            item['news_time'] = time[0].strip().replace('来源', '').replace('\u3000', '')

    def get_source(self, response, item):
        source = response.css('#ne_article_source::text').extract()
        if source:
            print('source:{}'.format(source[0]))
            item['news_source'] = source[0]

    def get_source_url(self, response, item):
        source_url = response.css('#ne_article_source::attr(href)').extract()
        if source_url:
            print('source_url:{}'.format(source_url[0]))
            item['news_source_url'] = source_url[0]