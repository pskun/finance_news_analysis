# -*- coding: utf-8 -*-

from scrapy.http.request import Request
from scrapy.spiders import CrawlSpider

from ..items import EastMoneyGubaPageNumItem


class EastmoneyGubaPagerSpider(CrawlSpider):
    name = 'EastMoneyGubaPagerSpider'
    allowed_domains = ['guba.eastmoney.com']
    start_urls = []

    def start_requests(self):
        base_url = 'http://guba.eastmoney.com/list,%s.html'
        for ticker_id in open('ticker_list.txt'):
            url = base_url % ticker_id.strip()
            yield Request(url, self.parse_item)
        pass

    def atoi(self, a):
        try:
            a = int(a)
        except ValueError:
            a = None
        return a

    def parse_item(self, response):
        item = EastMoneyGubaPageNumItem()

        if response.status != 200:
            item['status'] = response.status
            item['url'] = response.url
            return item

        list_url = response.url
        ticker_id = list_url.split(',')[1][0:6]
        pager_info = response.xpath(
            '//span[@class="pagernums"]/@data-pager').extract()
        pager_info = "".join(pager_info).split("|")
        total_count = self.atoi(pager_info[1])
        num_per_page = self.atoi(pager_info[2])

        item['ticker_id'] = ticker_id
        item['total_count'] = total_count
        item['num_per_page'] = num_per_page
        return item
