# -*- coding: utf-8 -*-

from sqlalchemy import Table
from sqlalchemy import MetaData
from sqlalchemy import Column, Integer, DateTime, Unicode
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapper

# 创建对象的基类:
Base = declarative_base()
# 跟踪表属性
metadata = MetaData()


class Guba(object):
    pass

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

mapper(Guba, guba_table)  # 把表映射到类
