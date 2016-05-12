# -*- coding: utf-8 -*-

from scrapy.http.request import Request
from scrapy.spiders import CrawlSpider
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc

from ..items import EastMoneyGubaListItem

import random
from ..settings import USER_AGENTS

import math
import urllib2
from lxml import etree


class EastmoneyGubaListSpider(CrawlSpider):
    name = 'EastMoneyGubaListSpider'
    allowed_domains = ['guba.eastmoney.com']
    start_urls = []
    headers = {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': r'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
    }
    incremental_logging_file = r'%s_incre.log' % name

    def __init__(self, incremental=False, *args, **kwargs):
        '''
        Args:
            incremental: 是否增量爬取
        '''
        super(EastmoneyGubaListSpider, self).__init__(*args, **kwargs)
        self.incremental = incremental
        if self.incremental:
            
        pass

    def start_requests(self):
        base_url = 'http://guba.eastmoney.com/list,%s_1.html'
        reader = open('ticker_list.txt', 'r')
        for line in reader:
            ticker_id = line.strip()
            url = base_url % ticker_id
            if self.incremental:
                yield Request(url, self.parse_incremental)
            else:
                yield Request(url, self.parse_index_page)
        pass

    def atoi(self, a):
        try:
            a = int(a)
        except ValueError:
            a = None
        return a

    def get_guba_post_year(self, url):
        retry_times = 10
        req = urllib2.Request(url=url, headers=EastmoneyGubaListSpider.headers)
        for i in range(retry_times):
            try:
                response = urllib2.urlopen(req, timeout=10)
                html = response.read()
                html = etree.HTML(html.lower().decode('utf-8'))
                post_time = html.xpath('//div[@class="zwfbtime"]/text()')
                post_time = "".join(post_time).strip()
                if post_time is None:
                    return None
                post_time = post_time.split(" ")[1]
                year = post_time.split('-')[0]
                return year
            except urllib2.URLError:
                continue
            except urllib2.HTTPError:
                continue
            except:
                continue
        return None
        pass

    def parse_index_page(self, response):
        ''' 解析股吧列表第一页的信息 '''
        list_url = response.url
        ticker_id = list_url.split(',')[1][0:6]
        # 获得分页信息
        pager_info = response.xpath(
            '//span[@class="pagernums"]/@data-pager').extract()
        pager_info = "".join(pager_info).split("|")
        total_count = self.atoi(pager_info[1])
        num_per_page = self.atoi(pager_info[2])
        page_count = int(
            math.ceil(float(total_count) / float(num_per_page)))
        self.parse_list_item(response)
        base_url = 'http://guba.eastmoney.com/list,%s_%d.html'
        for i in range(2, page_count + 1):
            url = base_url % (ticker_id, i)
            yield Request(url, self.parse_list_item)
        pass

    def parse_incremental(self, response):
        ''' 增量式爬取：根据上次爬取的日期，爬取上次日期之后至今日的所有股吧列表 '''
        pass

    def parse_list_item(self, response):
        ''' 解析股吧的列表 '''
        eastmoney_guba_list_item = EastMoneyGubaListItem()

        if response.status != 200:
            eastmoney_guba_list_item['status'] = response.status
            eastmoney_guba_list_item['list_url'] = response.url
            return eastmoney_guba_list_item

        list_url = response.url
        ticker_name = response.xpath(
            '//span[@id="stockname"]/a/text()').extract()
        ticker_name = ticker_name = ("".join(ticker_name).strip())[0:-1]
        ticker_id = list_url.split(',')[1][0:6]
        tiezi_item = response.xpath('//div[contains(@class,"articleh")]')

        month_dict = {}
        output_list = []
        for item in tiezi_item:
            # 去掉置顶的帖子（陈年老帖）
            top_tiezi = item.xpath('.//em[@class="settop"]').extract()
            if len(top_tiezi) > 0:
                continue
            # 解析标题
            title = item.xpath('./span[@class="l3"]/a/@title').extract()
            title = "".join(title)
            # 解析url
            url = item.xpath('./span[@class="l3"]/a/@href').extract()
            url = "".join(url)
            base_url = get_base_url(response)
            url = urljoin_rfc(base_url, url)
            # 解析时间
            a_post_time = item.xpath('./span[@class="l6"]/text()').extract()
            a_post_time = "".join(a_post_time)
            month = a_post_time.split('-')[0]
            if month not in month_dict:
                year = self.get_guba_post_year(url)
                if year is None:
                    # 默认年份
                    year = '2016'
                month_dict[month] = year
            a_post_time = month_dict[month] + '-' + a_post_time
            # 解析发帖人
            poster_name = item.xpath('./span[@class="l4"]//text()').extract()
            poster_name = "".join(poster_name)
            # 解析阅读量
            read_num = item.xpath('./span[@class="l1"]//text()').extract()
            read_num = "".join(read_num)
            read_num = self.atoi(read_num)
            # 解析评论量
            comment_num = item.xpath('./span[@class="l2"]//text()').extract()
            comment_num = "".join(comment_num)
            comment_num = self.atoi(comment_num)
            # 构造输出字典
            eastmoney_guba_item = dict()
            eastmoney_guba_item['url'] = url
            eastmoney_guba_item['title'] = title
            eastmoney_guba_item['a_post_time'] = a_post_time
            eastmoney_guba_item['poster_name'] = poster_name
            eastmoney_guba_item['read_num'] = read_num
            eastmoney_guba_item['comment_num'] = comment_num
            output_list.append(eastmoney_guba_item)
            pass
        # 放入scrapy item中
        eastmoney_guba_list_item['tiezi_item'] = output_list
        eastmoney_guba_list_item['list_url'] = list_url
        eastmoney_guba_list_item['ticker_id'] = ticker_id
        eastmoney_guba_list_item['ticker_name'] = ticker_name
        return eastmoney_guba_list_item
