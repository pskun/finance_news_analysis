# -*- coding: utf-8 -*-

from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from mysql_config import DATABASE_TABLES

# 创建对象的基类:
Base = declarative_base()


class News(Base):
    # 表的名字
    __tablename__ = DATABASE_TABLES['TABLE_NEWS_LIST']

    # 表的结构
    id = Column(Integer)
    pass
