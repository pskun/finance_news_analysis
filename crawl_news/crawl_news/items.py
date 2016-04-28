# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

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
    tiezi_id = scrapy.Field()
    #item_name = scrapy.Field()


class EastMoneyGubaListItem(scrapy.Item):
    list_url = scrapy.Field()
    status = scrapy.Field()
    ticker_id = scrapy.Field()
    ticker_name = scrapy.Field()
    tiezi_item = scrapy.Field()
    pass

class EastMoneyGubaPageNumItem(scrapy.Item):
    url = scrapy.Field()
    status = scrapy.Field()
    ticker_id = scrapy.Field()
    total_count = scrapy.Field()
    num_per_page = scrapy.Field()
    pass