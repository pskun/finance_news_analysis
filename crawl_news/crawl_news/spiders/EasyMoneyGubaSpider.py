# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from crawl_news.items import EastMoneyGubaItem


class EasymoneygubaSpider(CrawlSpider):
    name = 'EastMoneyGubaSpider'
    allowed_domains = ['guba.eastmoney.com']
    start_urls = ['http://guba.eastmoney.com/news,601989,246372924.html',
                  'http://guba.eastmoney.com/news,600234,275614627.html',
                  'http://guba.eastmoney.com/news,600234,275621218.html',
                  ]

    rules = (
        Rule(LinkExtractor(allow=r'.*guba.*/news,[0-9]+,[0-9]+\.html'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'.*guba.*'), follow=True),
    )
    
    def parse(self, response):
    #def parse_item(self, response):
        item = EastMoneyGubaItem()
        '''
        url = response.url
        title = response.xpath('//div[@id="zwconttbt"]/text()').extract()
        content = response.xpath('//div[@class="stockcodec"]/text()').extract()
        a_post_time = response.xpath('//div[@class="zwfbtime"]/text()').extract()
        
        #title = "".join(title).strip()
        #content = "".join(content).strip()
        #a_post_time = "".join(a_post_time).strip()
        #a_post_time = a_post_time.encode('gbk')
        
        #print a_post_time
        '''
        item['title'] = u""
        item['a_post_time'] = u""
        return item
