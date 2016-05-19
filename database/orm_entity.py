# -*- coding: utf-8 -*-

from sqlalchemy import Table
from sqlalchemy import MetaData
from sqlalchemy import Column, Integer, DateTime, Unicode, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapper

from mysql_pool import SqlAlchemyPool

# 创建对象的基类:
Base = declarative_base()
# 跟踪表属性
metadata = MetaData()


class Website(Base):
    ''' 网站ORM的基类 '''
    __tablename__ = 'web_list'

    web_id = Column(Integer, primary_key=True)
    web_name = Column(String(255))
    web_address = Column(String(255))
    pass


class StorageFile(object):
    ''' 保存文件ORM的基类 '''
    pass


class Guba(object):
    ''' 股吧ORM的基类 '''
    pass


class News(object):
    ''' 新闻ORM的基类 '''
    pass


class Page(object):
    ''' 版面ORM的基类 '''
    pass


class Subject(object):
    ''' 主题ORM映射类 '''
    pass


class KeywordProperty(object):
    ''' 关键词属性ORM映射 '''
    pass


class Keyword(object):
    ''' 关键词ORM映射 '''
    pass


class KeywordSecRelation(object):
    ''' 关键词股票代码关系映射类 '''
    pass


class NewsSecRelation(object):
    ''' 新闻股票代码关系映射类 '''
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
    Column('tiezi_id', Integer, primary_key=True),
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

# 把表映射到类
mapper(Guba, guba_table)
mapper(News, news_table)
mapper(Page, page_table)
mapper(Subject, subject_table)


def main():
    mysql = SqlAlchemyPool()
    conn = mysql.getConnection()
    web = Website()
    result = conn.query(web)
    print result
    pass

if __name__ == '__main__':
    main()
