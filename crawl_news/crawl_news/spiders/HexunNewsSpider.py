# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider
from scrapy.http.request import Request

from ..items import NewsItem


class HexunNewsSpider(CrawlSpider):
    name = 'HexunNewsSpider'
    allowed_domains = ['stock.hexun.com']
    start_urls = []
    incremental = False

    def start_requests(self):
        section_index_num_dict = {
            # 公司新闻的列表页数
            'gsxw': 4944,
            # 证券要闻的列表页数
            'news': 2024,
        }
        for section_name in section_index_num_dict:
            index_url = 'http://stock.hexun.com/%s/index.html' % section_name
            base_url = 'http://stock.hexun.com/%s/index-%d.html'
            for i in range(1, section_index_num_dict[section_name] + 1):
                url = base_url % (section_name, i)
                yield Request(url, callback=self.parse_list_page)
            yield Request(index_url, callback=self.parse_list_page)

    def parse_list_page(self, response):
        list_urls = response.xpath(
            '//div/div[@class="temp01"]/ul/li/a/@href').extract()
        for url in list_urls:
            yield Request(url, callback=self.parse_news_item)
        pass

    def parse_news_item(self, response):
        item = NewsItem()
        # 抽取xpath
        url = response.url
        title = response.xpath(
            '//div[@id="artibodyTitle"]/h1/text()').extract()
        if len(title) == 0:
            # 旧版网页代码，如 http://stock.hexun.com/2007-09-13/100730003.html
            # 使用其他规则解析
            return self.parse_old_version_news_item(response)
        post_time = response.xpath(
            '//span[@id="pubtime_baidu"]/text()').extract()
        content = response.xpath('//div[@id="artibody"]/p/text()').extract()
        section = response.xpath(
            '//div[@id="page_navigation"]/a[2]/text()').extract()
        sub_section = response.xpath(
            '//div[@id="page_navigation"]/a[3]/text()').extract()
        mention_tickers_name = response.xpath(
            '//div[@id="artibody"]/p//a[@onmouseover]/text()').extract()
        mention_tickers_id = response.xpath(
            '//div[@id="artibody"]/p//a[@onmouseover]/@href').re('([0-9]+)')
        poster_name = response.xpath(
            '//span[@id="source_baidu"]/a/text()').extract()

        # preprocess
        title = "".join(title).strip()
        section = "".join(section).strip()
        sub_section = "".join(sub_section).strip()
        post_time = "".join(post_time).strip()
        content = "".join(content).strip()
        poster_name = "".join(poster_name).strip()
        temp = [i for i in mention_tickers_id if len(i) == 6]
        mention_tickers_id = list(set(temp))
        mention_tickers_name = list(set(mention_tickers_name))

        item['url'] = url
        item['title'] = title
        item['b_section'] = section
        item['c_sub_section'] = sub_section
        item['a_post_time'] = post_time
        item['content'] = content
        item['mention_tickers_name'] = mention_tickers_name
        item['mention_tickers_id'] = mention_tickers_id
        return item

    def parse_old_version_news_item(self, response):
        item = NewsItem()
        url = response.url
        title = response.xpath(
            '//div[@class="mainboxcontent"]/p/text()').extract()
        a_post_time = response.xpath(
            '//div[@class="de_blue"][1]/font/text()').extract()
        section = response.xpath(
            '//div[@class="breadcrumbs"]/div/a[1]/text()').extract()
        sub_section = response.xpath(
            '//div[@class="breadcrumbs"]/div/a[2]/text()').extract()
        content = response.xpath(
            '//div[@class="detail_cnt"]//text()').extract()
        mention_tickers = response.xpath(
            '//div[@class="detail_cnt"]//a[contains(@href, "stockdata")]')
        mention_tickers_name = mention_tickers.xpath('.//text()').extract()
        mention_tickers_id = mention_tickers.xpath('./@href').re('([0-9]+)')

        title = "".join(title).strip()
        section = "".join(section).strip()
        sub_section = "".join(sub_section).strip()
        content = "".join(content).strip()
        a_post_time = "".join(a_post_time).strip()
        a_post_time = a_post_time.replace(
            u"年", "-").replace(u"月", "-").replace(u"日", " ") + ":00"
        temp = [i for i in mention_tickers_name if u"行情" not in i]
        mention_tickers_name = list(set(temp))
        mention_tickers_id = list(set(mention_tickers_id))
        # self.logger.debug("name: " + " ".join(mention_tickers_name))
        # self.logger.debug("id: " + " ".join(mention_tickers_id))

        item['url'] = url
        item['title'] = title
        item['b_section'] = section
        item['c_sub_section'] = sub_section
        item['a_post_time'] = a_post_time
        item['content'] = content
        item['mention_tickers_name'] = mention_tickers_name
        item['mention_tickers_id'] = mention_tickers_id
        return item
