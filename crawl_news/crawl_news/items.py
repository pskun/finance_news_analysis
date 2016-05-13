# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsItem(scrapy.Item):
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
    comment_num = scrapy.Field()
    read_num = scrapy.Field()
    poster_name = scrapy.Field()
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
    # item_name = scrapy.Field()
    pass


class EastMoneyGubaListItem(scrapy.Item):
    list_url = scrapy.Field()
    page_id = scrapy.Field()
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


class HexunResearchPaperItem(scrapy.Item):
    url = scrapy.Field()                # url
    b_section = scrapy.Field()          # 研报板块名称
    title = scrapy.Field()              # 标题
    ticker_name = scrapy.Field()        # 股票名称
    ticker_id = scrapy.Field()          # 股票代码
    industry = scrapy.Field()           # 所属行业
    poster_name = scrapy.Field()        # 机构名称
    analyst_name = scrapy.Field()       # 分析师
    rating_level = scrapy.Field()       # 评级分类
    rating_change = scrapy.Field()      # 评级变动
    upside = scrapy.Field()             # 上涨空间
    a_post_time = scrapy.Field()        # 发布时间
    yanbao_class = scrapy.Field()       # 研报分类（公司研究、新股、行业研究）
    abstract = scrapy.Field()           # 研报摘要
    status = scrapy.Field()             # http返回码
    pass
