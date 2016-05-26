# -*- coding: utf-8 -*-

from scrapy.http.request import Request
from scrapy.spiders import CrawlSpider
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc

from ..items import GubaListItem

import math
from datetime import datetime, timedelta

from utils import util_func


class EastmoneyGubaListSpider(CrawlSpider):
    ''' 东方财富股吧列表页爬虫 '''
    name = 'EastMoneyGubaListSpider'
    allowed_domains = ['guba.eastmoney.com']
    start_urls = []
    last_date = datetime.now() - timedelta(1)

    def __init__(self, *args, **kwargs):
        super(EastmoneyGubaListSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        base_url = 'http://guba.eastmoney.com/list,%s.html'
        reader = open('ticker_list.txt', 'r')
        for line in reader:
            ticker_id = line.strip()
            url = base_url % ticker_id
            yield Request(url, self.parse_index_page)
        pass

    def get_guba_post_year(self, response):
        '''
        获取帖子的发帖年份
        '''
        # default帖子年份
        post_year = response.xpath(
            '//div[@class="zwfbtime"]/text()').re("[0-9]{4}")
        post_year = "".join(post_year).strip()
        eastmoney_guba_list_item = response.meta['item']
        # 帖子内容
        tiezi_item = eastmoney_guba_list_item['tiezi_item']
        for item in tiezi_item:
            item['a_post_time'] = post_year + '-' + item['a_post_time']
        return eastmoney_guba_list_item

    def parse_index_page(self, response):
        ''' 解析股吧列表第一页的信息 '''
        list_url = response.url
        ticker_id = list_url.split(',')[1][0:6]
        # 获得分页信息
        pager_info = response.xpath(
            '//span[@class="pagernums"]/@data-pager').extract()
        pager_info = "".join(pager_info).split("|")
        total_count = util_func.atoi(pager_info[1])
        num_per_page = util_func.atoi(pager_info[2])
        page_count = int(
            math.ceil(float(total_count) / float(num_per_page)))
        self.parse_list_item(response)
        base_url = 'http://guba.eastmoney.com/list,%s_%d.html'
        for i in range(2, page_count + 1):
            url = base_url % (ticker_id, i)
            yield Request(url, self.parse_list_item)
        pass

    def parse_list_item(self, response):
        ''' 解析股吧的列表 '''
        list_url = response.url
        ticker_name = response.xpath(
            '//span[@id="stockname"]/a/text()').extract()
        ticker_name = ticker_name = ("".join(ticker_name).strip())[0:-1]
        ticker_id = list_url.split(',')[1][0:6]
        tiezi_item = response.xpath('//div[contains(@class,"articleh")]')

        month_items_dict = {}
        month_url_dict = {}
        for item in tiezi_item:
            # 去掉置顶的帖子（陈年老帖）
            top_tiezi = item.xpath('.//em[@class="settop"]').extract()
            if len(top_tiezi) > 0:
                continue
            # 解析标题
            title = item.xpath('./span[@class="l3"]/a/@title').extract()
            title = "".join(title).strip()
            # 解析url
            url = item.xpath('./span[@class="l3"]/a/@href').extract()
            url = "".join(url)
            base_url = get_base_url(response)
            url = urljoin_rfc(base_url, url)
            # 解析发帖人
            poster_name = item.xpath('./span[@class="l4"]//text()').extract()
            poster_name = "".join(poster_name)
            # 解析阅读量
            read_num = item.xpath('./span[@class="l1"]//text()').extract()
            read_num = "".join(read_num)
            read_num = util_func.atoi(read_num)
            # 解析评论量
            comment_num = item.xpath('./span[@class="l2"]//text()').extract()
            comment_num = "".join(comment_num)
            comment_num = util_func.atoi(comment_num)
            # 构造输出字典
            eastmoney_guba_item = dict()
            eastmoney_guba_item['url'] = url
            eastmoney_guba_item['title'] = title
            eastmoney_guba_item['poster_name'] = poster_name
            eastmoney_guba_item['read_num'] = read_num
            eastmoney_guba_item['comment_num'] = comment_num
            # 解析时间
            # 把月份相同的item放在一起
            a_post_time = item.xpath('./span[@class="l6"]/text()').extract()
            a_post_time = "".join(a_post_time)
            eastmoney_guba_item['a_post_time'] = a_post_time
            month = a_post_time.split('-')[0]
            if month not in month_items_dict:
                month_items_dict[month] = []
            month_items_dict[month].append(eastmoney_guba_item)
            if month not in month_url_dict:
                month_url_dict[month] = url
            pass
        # 放入scrapy item中
        for month in month_url_dict:
            eastmoney_guba_list_item = GubaListItem()
            eastmoney_guba_list_item['tiezi_item'] = month_items_dict[month]
            eastmoney_guba_list_item['list_url'] = list_url
            eastmoney_guba_list_item['ticker_id'] = ticker_id
            eastmoney_guba_list_item['ticker_name'] = ticker_name
            yield Request(
                url=month_url_dict[month],
                meta={'item': eastmoney_guba_list_item},
                callback=self.get_guba_post_year)
