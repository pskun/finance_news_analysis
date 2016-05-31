# -*- coding: utf-8 -*-

from sqlalchemy import Table
from sqlalchemy import MetaData
from sqlalchemy import Column, Integer, DateTime, Unicode, String, Float
from sqlalchemy.ext.declarative import declarative_base

'''
##############
尚未完成
##############
'''

'''
股吧建表语句
create table eastmoney_guba_list (
    guba_id varchar(255) not null comment'唯一ID,web_name+ID拼接',
    guba_title varchar(255) comment'标题',
    publish_time datetime not null comment'发布时间，用来做分区，要求非空',
    click_amount int comment'点击数量',
    comment_amount int comment'评论数量',
    abstract mediumtext comment'摘要',
    poster varchar(45) comment'作者',
    news_file_id int comment'文件ID',
    web_id int comment'网站ID',
    page_id int comment'页面ID',
    sec_number varchar(8) comment'股票代码'
    primary key(guba_id,publish_time)
) ENGINE=MyISAM default charset=utf8
partition by range (year(publish_time)) (
    partition p2007 values less than (2008),
    partition p2008 values less than (2009),
    partition p2009 values less than (2010),
    partition p2010 values less than (2011),
    partition p2011 values less than (2012),
    partition p2012 values less than (2013),
    partition p2013 values less than (2014),
    partition p2014 values less than (2015),
    partition p2015 values less than (2016),
    partition p2016 values less than (2017)
);
--在时间字段上创建索引
create index i_eastmoney_guba_pubtime on eastmoney_guba_list(publish_time);
create index i_eastmoney_guba_sec on eastmoney_guba_list(sec_number);
create fulltest index i_eastmoney_guba_title on eastmoney_guba_list(guba_title);
create fulltest index i_eastmoney_guba_abstract on eastmoney_guba_list(abstract );
'''

# 创建对象的基类:
Base = declarative_base()
# 跟踪表属性
metadata = MetaData()


class Website(Base):
    ''' 已爬取网站的ORM基类 '''
    __tablename__ = 'web_list'

    web_id = Column(Integer, primary_key=True)
    web_name = Column(String(255))
    web_address = Column(String(255))

    pass


class StorageFile(Base):
    ''' 保存文件ORM的基类 '''
    __tablename__ = 'news_file_list'

    news_file_id = Column(Integer, primary_key=True)
    web_id = Column(Integer)
    page_id = Column(Integer)
    file_storage_location = Column(Unicode(255))
    file_name = Column(Unicode(255))
    pass


class Guba(Base):
    ''' 股吧ORM的基类 '''
    __tablename__ = 'eastmoney_guba_list'

    guba_id = Column(String(255), primary_key=True)
    guba_title = Column(Unicode(256))
    publish_time = Column(DateTime, primary_key=True)
    abstract = Column(Unicode(10240))
    poster = Column(Unicode(30))
    click_amount = Column(Integer)
    comment_amount = Column(Integer)
    news_file_id = Column(Integer)
    web_id = Column(Integer)
    page_id = Column(Integer)
    sec_number = Column(Unicode(8))
    url = Column(Unicode(100))
    pass


class News(Base):
    ''' 新闻ORM的基类 '''
    __tablename__ = 'news_list'

    news_id = Column(Unicode(255), primary_key=True)
    news_title = Column(Unicode(255))
    publish_time = Column(DateTime, primary_key=True)
    click_amount = Column(Integer)
    comment_amount = Column(Integer)
    abstract = Column(Unicode(65535))
    news_file_id = Column(Integer)
    web_id = Column(Integer)
    page_id = Column(Integer)
    poster = Column(Unicode(45))
    pass


class Report(Base):
    ''' 研报ORM基类 '''
    __tablename__ = 'report_list'

    report_id = Column(Integer, primary_key=True)
    report_title = Column(Unicode(255))
    publish_time = Column(DateTime)
    industry = Column(Unicode(45))
    org_name = Column(Unicode(45))
    analyst_name = Column(Unicode(45))
    rating_level = Column(Unicode(45))
    rating_change = Column(Unicode(45))
    upside = Column(Float)
    report_class = Column(Unicode(45))
    abstract = Column(Unicode(65535))
    voting_num = Column(Integer)
    good_ratio = Column(Float)
    general_ratio = Column(Float)
    bad_ratio = Column(Float)
    news_file_id = Column(Integer)
    web_id = Column(Integer)
    page_id = Column(Integer)
    pass


class Page(Base):
    ''' 版面ORM的基类 '''
    __tablename__ = 'page_list'

    page_id = Column(Integer, primary_key=True)
    web_id = Column(Integer)
    page_name = Column(Unicode(255))
    page_level = Column(Integer)
    parent_page_id = Column(Integer)
    pass


class Subject(object):
    ''' 主题ORM映射类 '''
    __tablename__ = 'subject_list'

    subject_id = Column(Integer, primary_key=True)
    subject = Column(Unicode(255))
    subject_type = Column(Integer)
    pass


class KeywordProperty(Base):
    ''' 关键词属性ORM映射 '''
    __tablename__ = 'keywords_property'

    keywords_property_id = Column(Integer, primary_key=True)
    keywords_property_col = Column(Unicode(45))
    pass


class Keyword(object):
    ''' 关键词ORM映射 '''
    __tablename__ = 'keywords_list'

    keywords_id = Column(Integer, primary_key=True)
    keywords = Column(Unicode(255))
    keywords_type = Column(Integer)
    keywords_property_id = Column(Integer)
    pass


class NewsSecRelation(Base):
    ''' 新闻股票代码关系映射类 '''
    __tablename__ = 'cor_sec_of_news'

    news_id = Column(Unicode(255), primary_key=True)
    sec_number = Column(Unicode(8), primary_key=True)
    pass


class KeywordNewsRelation(Base):
    ''' 关键词新闻关联映射类 '''
    __tablename__ = 'rel_keywords_news'
    amount_keywords_in_news = Column(Integer)
    keywords_id = Column(Integer, primary_key=True)
    news_id = Column(Unicode(255), primary_key=True)
    pass


# 版面Mysql表
page_table = Table(
    'page_list', metadata,
    Column('page_id', Integer, primary_key=True),
    Column('web_id', Integer),
    Column('page_name', String(255)),
    Column('page_level', Integer),
    Column('parent_page_id', Integer)
)

# 股吧Mysql表
guba_table = Table(
    'guba_list', metadata,
    Column('tiezi_id', String(255), primary_key=True),
    Column('tiezi_title', Unicode(256)),
    Column('publish_time', DateTime),
    Column('click_amount', Integer),
    Column('comment_amount', Integer),
    Column('content', Unicode(10240)),
    Column('sec_number', Unicode(8)),
    Column('url', Unicode(100)),
    Column('poster', Unicode(30))
)

# 新闻Mysql表
news_table = Table(
    'news_list', metadata,
    Column('news_id', String(255), primary_key=True),
    Column('web_id', Integer),
    Column('page_id', Integer),
    Column('news_file_id', Integer),
    Column('news_title', Unicode(255)),
    Column('publish_time', DateTime),
    Column('click_amount', Integer),
    Column('comment_amount', Integer),
    Column('abstract', String),
    Column('poster', String(45))
)

# 主题Mysql表
subject_table = Table(
    'subject_list', metadata,
    Column('subject_list', Integer, primary_key=True),
    Column('subject', String(255)),
    Column('subject_type', Integer)
)

# 网站Mysql表
web_table = Table(
    'web_list', metadata,
    Column('web_id', Integer, primary_key=True),
    Column('web_name', String(255)),
    Column('web_address', String(255))
)

# 保存文件Mysql表
file_table = Table(
    'news_file_list', metadata,
    Column('news_file_id', Integer, primary_key=True),
    Column('web_id', Integer),
    Column('page_id', Integer),
    Column('file_storage_location', String(255)),
    Column('file_name', String(255))
)

# 关键词Mysql表
keyword_table = Table(
    'key_words_list', metadata,
    Column('keywords_id', Integer, primary_key=True),
    Column('keywords', String(255)),
    Column('keywords_type', Integer),
    Column('keywords_property_id', Integer)
)

# 关键词属性Mysql表
keyword_property_table = Table(
    'keywords_property', metadata,
    Column('keywords_property_id', Integer, primary_key=True),
    Column('keywords_property_col', String(45))
)

# 关键词-股票代码-关联Mysql表
keyword_sec_table = Table(
    'cor_sec_of_keywords', metadata,
    Column('keywords_id', Integer, primary_key=True),
    Column('sec_number', String(8))
)

# 新闻-股票代码-关联Mysql表
news_sec_table = Table(
    'cor_sec_of_news', metadata,
    Column('news_id', Integer, primary_key=True),
    Column('sec_number', String(8), primary_key=True)
)
