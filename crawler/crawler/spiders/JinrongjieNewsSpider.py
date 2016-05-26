# -*- coding: utf-8 -*-

import re

from scrapy.spiders import CrawlSpider
from scrapy.http.request import Request
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc

from ..items import NewsItem
from utils import util_func


class JinrongjieNewsSpider(CrawlSpider):
    ''' 金融界新闻爬虫 '''
    name = 'JinrongjieNewsSpider'
    allowed_domains = ['jrj.com.cn']
    start_urls = []
    incremental = False

    def start_requests(self):
        crawl_years = range(2007, 2017)
        sections = ['stock', 'finance']
        base_url = "http://%s.jrj.com.cn/xwk/%d.shtml"
        for section in sections:
            for year in crawl_years:
                url = base_url % (section, year)
                yield Request(url, callback=self.parse_year_list)

    '''
    def start_requests(self):
        item = NewsItem()
        url = 'http://stock.jrj.com.cn/invest/2013/12/31141316423152.shtml'
        yield Request(url,
                      meta={'item': item, 'is_page': False},
                      callback=self.parse_news_item)
    '''

    def parse_year_list(self, response):
        ''' 解析新闻的总列表 '''
        daily_news_urls = response.xpath(
            '//div[@class="cont"]/ul/li/table//tr/td/a/@href').extract()
        for url in daily_news_urls:
            yield Request(url, callback=self.parse_index_list)
        pass

    def parse_index_list(self, response):
        ''' 获取每日新闻的首页信息 '''
        pager = response.xpath('//p[@class="page_newslib"]/a/@href').extract()
        self.parse_list_page(response)
        for url in list(set(pager)):
            base_url = get_base_url(response)
            url = urljoin_rfc(base_url, url)
            yield Request(url, callback=self.parse_list_page)
        pass

    def parse_list_page(self, response):
        ''' 解析每日新闻的列表信息 '''
        list_url_items = response.xpath('//ul[@class="list"]/li')
        for item in list_url_items:
            url = "".join(item.xpath('./a/@href').extract())
            if len(url) == 0:
                continue
            a_post_time = "".join(item.xpath('./span/text()').extract())
            item = NewsItem()
            item['a_post_time'] = a_post_time
            yield Request(url,
                          meta={'item': item, 'is_page': False},
                          callback=self.parse_news_item)
        pass

    def parse_news_item(self, response):
        ''' 解析新闻内容 '''
        item = response.meta['item']
        is_page = response.meta['is_page']
        # 抽取xpath
        url = response.url
        title = response.xpath('//div[@class="titmain"]/h1/text()').extract()
        if len(title) == 0:
            # 旧版网页代码，如 http://stock.hexun.com/2007-09-13/100730003.html
            # 使用旧版规则解析
            item = self.parse_old_version_news_item(response)
            # 返回的可能是request对象
            if not isinstance(item, Request):
                # 不是旧版网页代码，是新版网页代码的另外一个版本
                # http://stock.jrj.com.cn/ipo/2013/12/31024216419537.shtml
                if 'title' not in item or len(item['title']) == 0:
                    item = self.parse_another_version_news_item(response)
            return item
        content = response.xpath(
            '//div[@class="texttit_m1"]//p')
        content = content.xpath('string(.)').extract()
        section = response.xpath(
            '//div[@class="cbox"]/p/a[2]/text()').extract()
        sub_section = response.xpath(
            '//div[@class="cbox"]/p/a[3]/text()').extract()
        mention_tickers_name = response.xpath(
            '//div[@class="texttit_m1"]//a[@class="stbu"]//text()').extract()
        mention_tickers_id = response.xpath(
            '//div[@class="texttit_m1"]//p/span/@kwid').re('([0-9]+)')
        poster_name = response.xpath(
            '//p[@class="inftop"]/span[2]//text()').extract()

        # preprocess
        title = "".join(title).strip()
        section = "".join(section).strip()
        sub_section = "".join(sub_section).strip()
        content = "".join(content).strip()
        poster_name = "".join(poster_name).strip()
        poster_split = poster_name.split(u"：")
        if len(poster_split) > 1:
            poster_name = poster_split[1]
        # self.logger.debug("poster: " + poster_name)
        temp = [i for i in mention_tickers_id if len(i) == 6]
        mention_tickers_id = list(set(temp))
        mention_tickers_name = list(set(mention_tickers_name))

        # 一个新闻有多页的情况
        # http://stock.jrj.com.cn/hotstock/2016/05/12143820948669.shtml
        # WARNING: 这里的分页信息是动态加载的
        item = self.constructItem(
            item, url, title, section, sub_section,
            content, mention_tickers_id, mention_tickers_name, poster_name,
            is_page)
        return item

    def parse_old_version_news_item(self, response):
        '''
            解析旧版本的新闻内容，多见于2010年前
            样例: http://news1.jrj.com.cn/2007-12-04/000003009042.html
            样例: http://stock.jrj.com.cn/2008/07/3023071478728.shtml
        '''
        item = response.meta['item']
        is_page = response.meta['is_page']
        url = response.url
        title = response.xpath(
            '//div[@class="newsConTit"]/h1/text()').extract()
        if len(title) == 0:
            return item
        section = response.xpath(
            '//div[@class="newsGuide"]/a[2]/text()').extract()
        sub_section = response.xpath(
            '//div[@class="newsGuide"]/a[3]/text()').extract()
        content = response.xpath(
            '//div[@id="IDNewsDtail"]//p')
        content = content.xpath('string(.)').extract()
        mention_tickers_name = response.xpath(
            '//div[@id="IDNewsDtail"]//p//a[@class="stbu"]//text()').extract()
        mention_tickers_id = response.xpath(
            '//div[@id="IDNewsDtail"]//p//span/@kwid').re('([0-9]+)')
        poster_name = response.xpath(
            '//p[@class="newsource"]/span[2]//text()').extract()

        title = "".join(title).strip()
        section = "".join(section).strip()
        sub_section = "".join(sub_section).strip()
        content = "".join(content).strip()
        poster_name = "".join(poster_name).strip()
        poster_split = poster_name.split(u"：")
        if len(poster_split) > 1:
            poster_name = poster_split[1]
        # 一个新闻有多页的情况
        # http://stock.jrj.com.cn/hotstock/2012/12/31114114890232.shtml
        item = self.constructItem(
            item, url, title, section, sub_section,
            content, mention_tickers_id, mention_tickers_name, poster_name,
            is_page)
        pager = response.xpath(
            '//p[@id="divpage"]/a[last()-1]/text()').extract()
        pager = util_func.atoi("".join(pager))
        cur_pager = response.xpath(
            '//p[@id="divpage"]/a[contains(@class,"cur")]/text()').extract()
        cur_pager = util_func.atoi("".join(cur_pager))
        return self.deal_with_pager(item, pager, cur_pager, url)

    def parse_another_version_news_item(self, response):
        '''
            解析另一种版本的新闻内容
            样例: http://stock.jrj.com.cn/ipo/2013/12/31024216419537.shtml
        '''
        item = response.meta['item']
        is_page = response.meta['is_page']
        # 判断是否有分页信息
        # 有【全文阅读】字样
        # 样例: http://stock.jrj.com.cn/invest/2013/12/31141316423152.shtml
        all_content_read_url = response.xpath(
            '//div[@class="pnf"]/a[@class="all"]/@href').extract()
        all_content_read_url = "".join(all_content_read_url)
        if all_content_read_url != "":
            base_url = get_base_url(response)
            url = urljoin_rfc(base_url, all_content_read_url)
            return Request(url,
                           meta={'item': item, 'is_page': False},
                           callback=self.parse_news_item)
        url = response.url
        title = response.xpath(
            '//div[contains(@class,"text-col")]//h1[@class="newsLeft"]/text()').extract()
        section = response.xpath(
            '//div[@class="newsGuide"]/a[2]/text()').extract()
        sub_section = response.xpath(
            '//div[@class="newsGuide"]/a[3]/text()').extract()
        content = response.xpath(
            '//div[contains(@class,"textmain")]//p')
        content = content.xpath('string(.)').extract()
        mention_tickers_name = response.xpath(
            '//div[contains(@class,"textmain")]//p//a[@class="stbu"]//text()'
        ).extract()
        mention_tickers_id = response.xpath(
            '//div[contains(@class,"textmain")]//p//span/@kwid').re('([0-9]+)')
        poster_name = response.xpath(
            '//div[@class="newsource"]/span[3]//text()').extract()

        title = "".join(title).strip()
        section = "".join(section).strip()
        sub_section = "".join(sub_section).strip()
        content = "".join(content).strip()
        poster_name = "".join(poster_name).strip()
        poster_split = poster_name.split(u"：")
        if len(poster_split) > 1:
            poster_name = poster_split[1]
        return self.constructItem(
            item, url, title, section, sub_section,
            content, mention_tickers_id, mention_tickers_name, poster_name,
            is_page)
        pass

    def constructItem(self, item,
                      url, title, section, sub_section, content,
                      mention_tickers_id, mention_tickers_name, poster_name,
                      is_page):
        if is_page is False:
            item['url'] = url
            item['title'] = title
            item['b_section'] = section
            item['c_sub_section'] = sub_section
            item['content'] = content
            item['mention_tickers_name'] = mention_tickers_name
            item['mention_tickers_id'] = mention_tickers_id
            item['poster_name'] = poster_name
        else:
            item['content'] += content
            item['mention_tickers_name'] += mention_tickers_name
            item['mention_tickers_id'] += mention_tickers_id
        return item
        pass

    def parse_posttime_from_url(self, url):
        a_post_time = None
        # url pattern 1: http://news1.jrj.com.cn/2007-12-04/000003009042.html
        url_pattern_1 = r'.*([\d]{4}-[\d]{2}-[\d]{2}).*'
        # url pattern 2:
        # http://stock.jrj.com.cn/invest/2015/01/02133118638111.shtml
        url_pattern_2 = r'.*([\d]{4})/([\d]{2})/([\d]{2})([\d]{2})([\d]{2}).*'
        m = re.match(url_pattern_1, url)
        if m is not None and len(m.groups()) > 0:
            # 是pattern 1的格式
            a_post_time = m.group(1)
            a_post_time += ' 00:00'
        else:
            m = re.match(url_pattern_2, url)
            post_time_tuple = m.groups()
            if len(post_time_tuple) == 5:
                a_post_time = '-'.join(post_time_tuple[:3]) + ' '
                a_post_time += ':'.join(post_time_tuple[3:])
        return a_post_time
        pass

    def deal_with_pager(self, item, pager, cur_pager, url):
        if pager is None or pager == cur_pager:
            return item
        else:
            url_pattern = None
            if cur_pager == 1:
                url_pattern = r'(.*)\.shtml'
            else:
                url_pattern = r'(.*)-[\d]+\.shtml'
            m = re.match(url_pattern, url)
            url = m.group(1) + '-%d.shtml' % cur_pager
            return Request(url,
                           meta={'item': item, 'is_page': True},
                           callback=self.parse_news_item)
        pass
