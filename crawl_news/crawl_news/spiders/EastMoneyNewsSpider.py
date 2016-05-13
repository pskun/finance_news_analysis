# -*- coding: utf-8 -*-

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..items import NewsItem


class EastmoneyNewsSpider(CrawlSpider):
    name = 'EastMoneyNewsSpider'
    allowed_domains = ['eastmoney.com']

    start_urls = [
        'http://finance.eastmoney.com/news/1345,20160315604108128.html',
        'http://finance.eastmoney.com/news/1345,20160317604922713.html',
        'http://stock.eastmoney.com/news/1422,20160317604974655.html',
        'http://stock.eastmoney.com/news/1415,20160317604926179.html',
        'http://finance.eastmoney.com/news/1354,20160225597709653.html',
        'http://finance.eastmoney.com/news/1349,20160227598594533.html',
        'http://finance.eastmoney.com/news/1354,20160126589523116.html',
        'http://stock.eastmoney.com/news/1406,20151021557734237.html',
        'http://finance.eastmoney.com/news/1353,20151018556838721.html',
        'http://stock.eastmoney.com/news/1417,20150918549066939.html',
        'http://finance.eastmoney.com/news/1350,20150105464058146.html',
        'http://finance.eastmoney.com/news/1350,20141226461672322.html',
        'http://finance.eastmoney.com/news/1586,20151218577280426.html',
        'http://finance.eastmoney.com/news/1350,20140116354291437.html',
        'http://stock.eastmoney.com/news/1406,20131226348792329.html',
        'http://finance.eastmoney.com/news/1354,20130516292167087.html',
        'http://finance.eastmoney.com/news/1354,20130904320189293.html',
        'http://finance.eastmoney.com/news/1354,20131226348947522.html',
        'http://finance.eastmoney.com/news/1354,20140325371131983.html',
        'http://stock.eastmoney.com/news/1697,20150630521857938.html',
    ]

    rules = (
        Rule(
            LinkExtractor(
                allow=r'http:\/\/\b(finance|stock)\b.*/news/[0-9]+,[0-9]+\.html'),
            callback='parse_news_item',
            follow=True),
        Rule(
            LinkExtractor(
                allow=r'http:\/\/\b(finance|stock|roll|guba|data|bank)\b.*',
                deny=r'.*iguba.*'),
            follow=True),
    )

    # def parse(self, response):
    def parse_news_item(self, response):
        item = NewsItem()

        if response.status != 200:
            item['status'] = response.status
            item['url'] = response.url
            return item

        # parse
        url = response.url
        title = response.xpath(
            '//div[@class="newText new"]/h1/text()').extract()
        post_time = response.xpath(
            '//div[@class="Info"]/span[1]/text()').extract()
        content_data = response.xpath('//div[@id="ContentBody"]//p')
        content = content_data.xpath('string(.)').extract()
        section = response.xpath(
            '//div[@id="Column_Navigation"]/a[2]/text()').extract()
        sub_section = response.xpath(
            '//div[@id="Column_Navigation"]/a[3]/text()').extract()
        mention_tickers_name = response.xpath(
            '//a[@class="keytip"]/text()').extract()
        mention_tickers_id = response.xpath(
            '//div[@id="ContentBody"]//span[contains(@id, "stock")]/@id').re('([0-9]+)')
        summary = response.xpath('//div[@class="c_review"]/text()').extract()
        # 这俩是动态加载的
        # comment_nums = response.xpath('//div[@class="AboutCtrlBox"]').extract()
        # discuss_nums = response.xpath('//div[@class="AboutCtrlBox"]').extract()

        # preprocess
        title = "".join(title).strip()
        section = "".join(section).strip()
        sub_section = "".join(sub_section).strip()
        post_time = "".join(post_time).strip()
        content = "".join(content).strip()
        summary = "".join(summary).strip()

        item['url'] = url
        item['title'] = title
        item['b_section'] = section
        item['c_sub_section'] = sub_section
        item['a_post_time'] = post_time
        item['content'] = content
        item['mention_tickers_name'] = mention_tickers_name
        item['mention_tickers_id'] = mention_tickers_id
        item['summary'] = summary

        return item
