# -*- coding: utf-8 -*-

from scrapy.http.request import Request
from scrapy.spiders import CrawlSpider

from ..items import GubaPageNumItem
from utils import util_func


class EastmoneyGubaPagerSpider(CrawlSpider):
    ''' 东方财富股吧列表的页数爬虫
        注意: 目前已经弃用，功能已经整合到股票列表页爬虫中
    '''
    name = 'EastMoneyGubaPagerSpider'
    allowed_domains = ['guba.eastmoney.com']
    start_urls = []

    def start_requests(self):
        base_url = 'http://guba.eastmoney.com/list,%s.html'
        for ticker_id in open('ticker_list.txt'):
            url = base_url % ticker_id.strip()
            yield Request(url, self.parse_item)
        pass

    def parse_item(self, response):
        item = GubaPageNumItem()

        if response.status != 200:
            item['status'] = response.status
            item['url'] = response.url
            return item

        list_url = response.url
        ticker_id = list_url.split(',')[1][0:6]
        pager_info = response.xpath(
            '//span[@class="pagernums"]/@data-pager').extract()
        pager_info = "".join(pager_info).split("|")
        total_count = util_func.atoi(pager_info[1])
        num_per_page = util_func.atoi(pager_info[2])

        item['ticker_id'] = ticker_id
        item['total_count'] = total_count
        item['num_per_page'] = num_per_page
        return item
