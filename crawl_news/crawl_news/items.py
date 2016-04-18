# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlNewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class EastMoneyNewsItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    a_post_time = scrapy.Field()
    b_section = scrapy.Field()
    c_sub_section = scrapy.Field()
    content = scrapy.Field()
    mention_tickers_name = scrapy.Field()
    mention_tickers_id = scrapy.Field()
    summary = scrapy.Field()
    status = scrapy.Field()
    #item_name = scrapy.Field()
    #comment_nums = scrapy.Field()
    #discuss_nums = scrapy.Field()
    pass
    

class EastMoneyGubaItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    a_post_time = scrapy.Field()
    ticker_id = scrapy.Field()
    ticker_name = scrapy.Field()
    content = scrapy.Field()
    read_num = scrapy.Field()
    comment_num = scrapy.Field()
    poster_id = scrapy.Field()
    poster_name = scrapy.Field()
    status = scrapy.Field()
    #item_name = scrapy.Field()
    