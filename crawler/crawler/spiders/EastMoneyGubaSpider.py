# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider

from ..items import GubaItem


class EastmoneyGubaSpider(CrawlSpider):
    ''' 东方财富股吧内容页爬虫 '''
    name = 'EastMoneyGubaSpider'
    allowed_domains = ['guba.eastmoney.com']

    def start_requests(self):
        # 从文件中读取url
        pass

    # def parse(self, response):
    def parse_item(self, response):
        item = GubaItem()

        url = response.url
        title = response.xpath('//div[@id="zwconttbt"]/text()').extract()
        content_data = response.xpath('//div[@id="zwconbody"]')
        content = content_data.xpath('string(.)').extract()
        a_post_time = response.xpath(
            '//div[@class="zwfbtime"]/text()').extract()
        ticker_name = response.xpath(
            '//span[@id="stockname"]/a/text()').extract()
        ticker_id = response.xpath(
            '//span[@id="stockname"]/@data-popstock').extract()
        poster_name = response.xpath(
            '//div[@id="zwconttbn"]//strong//text()').extract()
        poster_id = response.xpath(
            '//div[@id="zwconttbn"]//a/@data-popper').extract()
        comment_num = response.xpath(
            '//div[@id="zwcontab"]/ul/li[@class="on"]/a/text()').re('([0-9]+)')
        # 这是动态加载的
        # read_num = response.xpath('//div[@id="mainbody"]').extract()

        title = "".join(title).strip()
        content = "".join(content).strip()
        a_post_time = "".join(a_post_time).strip()
        a_post_time = a_post_time.split(" ")
        a_post_time = " ".join(a_post_time[1:3])
        ticker_name = ("".join(ticker_name).strip())[0:-1]
        ticker_id = "".join(ticker_id).strip()
        poster_name = "".join(poster_name).strip()
        poster_id = "".join(poster_id).strip()
        try:
            if comment_num is not None:
                comment_num = int("".join(comment_num).strip())
        except:
            comment_num = None
        tiezi_id = None
        url_split = url.split(",")
        if len(url_split) >= 3:
            tiezi_id = url_split[2].split(".")[0]

        item['url'] = url
        item['title'] = title
        item['a_post_time'] = a_post_time
        item['content'] = content
        item['ticker_id'] = ticker_id
        item['ticker_name'] = ticker_name
        item['poster_name'] = poster_name
        item['poster_id'] = poster_id
        if comment_num is not None:
            item['comment_num'] = comment_num
        if tiezi_id is not None:
            item['tiezi_id'] = tiezi_id

        return item
