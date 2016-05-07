# -*- coding: utf-8 -*-

from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()


class Guba(Base):
    __tablename__ = 'guba_list'
    tiezi_id = Column(Integer)
    tiezi_title = Column(String)
    publish_time = Column(DateTime)
    click_amount = Column(Integer)
    comment_amount = Column(Integer)
    content = Column(String)
    sec_number = Column(String)
    url = Column(String)
    poster = Column(String)
    pass
