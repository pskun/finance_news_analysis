# -*- coding: utf-8 -*-

# Define here the models for your scraped items
# 这里定义了爬虫爬下来的数据的实体类
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsItem(scrapy.Item):
    ''' 新闻内容实体 '''
    url = scrapy.Field()                # 新闻内容页url
    title = scrapy.Field()              # 新闻标题
    a_post_time = scrapy.Field()        # 新闻发表时间
    b_section = scrapy.Field()          # 新闻版块
    c_sub_section = scrapy.Field()      # 新闻子版块
    content = scrapy.Field()            # 新闻内容
    mention_tickers_name = scrapy.Field()  # 新闻内容中提及的股票名称
    mention_tickers_id = scrapy.Field()  # 新闻内容中提及的股票代码
    summary = scrapy.Field()            # 新闻摘要
    status = scrapy.Field()             # http返回状态码
    comment_num = scrapy.Field()        # 评论数
    read_num = scrapy.Field()           # 阅读数
    poster_name = scrapy.Field()        # 发布者名称（通常是发布的机构）
    pass


class GubaItem(scrapy.Item):
    ''' 股吧帖子内容实体 '''
    url = scrapy.Field()                # 股吧帖子页url
    title = scrapy.Field()              # 帖子标题
    a_post_time = scrapy.Field()        # 帖子发表时间
    ticker_id = scrapy.Field()          # 股票代码
    ticker_name = scrapy.Field()        # 股票简称
    content = scrapy.Field()            # 发帖内容
    read_num = scrapy.Field()           # 阅读数
    comment_num = scrapy.Field()        # 评论数
    poster_id = scrapy.Field()          # 发帖人ID
    poster_name = scrapy.Field()        # 发帖人名称
    status = scrapy.Field()             # http返回状态码
    tiezi_id = scrapy.Field()           # 帖子在网站中的唯一标识
    pass


class GubaListItem(scrapy.Item):
    ''' 股吧列表实体 '''
    list_url = scrapy.Field()           # 列表页url
    page_id = scrapy.Field()            # 页数
    status = scrapy.Field()             # http返回状态码
    ticker_id = scrapy.Field()          # 股票代码
    ticker_name = scrapy.Field()        # 股票简称
    tiezi_item = scrapy.Field()         # 列表页下的所有帖子内容
    pass


class GubaPageNumItem(scrapy.Item):
    ''' 股吧分页数量实体 '''
    url = scrapy.Field()                # url
    status = scrapy.Field()             # http返回状态
    ticker_id = scrapy.Field()          # 股票代码
    total_count = scrapy.Field()        # 列表页数
    num_per_page = scrapy.Field()       # 一页列表有多少项
    pass


class ResearchPaperItem(scrapy.Item):
    ''' 研报实体 '''
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
