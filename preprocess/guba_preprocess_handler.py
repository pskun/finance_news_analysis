# -*- coding: utf-8 -*-

import os
import sys
from datetime import datetime
import traceback
import logging

from utils.universe_settings import TYPE_GUBALIST, TYPE_GUBA
from utils.threadpool import Handler
from database.mysql_pool import MySQLPool
from database import mysql_config
from database import common_db_func


class GubaPreprocessHandler(Handler):

    def __init__(self, preprocess_type, id_generator=None, website_name=None):
        self.preprocess_type = preprocess_type
        self.website_name = website_name
        self.id_generator = id_generator
        self.db_session = None
        self.tiezi_tuple_list = []
        self.bat_insert_num = 1000
        self.guba_table_name = mysql_config.TABLE_GUBA % website_name
        self.earlist_time = None
        # 日志
        self.wrong_file_name = self.guba_table_name + '.txt'
        logging.basicConfig(level=logging.DEBUG, filename=self.wrong_file_name)
        self.logger = logging.getLogger(__name__)

    def before_thread_start(self):
        ''' 回调函数: 线程启动前调用 '''
        # 初始化数据库连接
        self.db_session = MySQLPool().getConnection()
        # 获取新闻表的行数
        guba_id_counter = common_db_func.query_table_count(
            self.db_session, self.guba_table_name) + 1
        # 设置id的初始值
        self.id_generator.set_initial_counter(guba_id_counter)
        # datetime的strptime函数的线程安全问题
        # http://lixipeng.me/2016-03/strptime-thread-not-safe/
        self.earlist_time = datetime.strptime("1990", "%Y")
        pass

    def init_handler(self):
        ''' 初始化handler '''
        pass

    def process_function(self, data_item):
        try:
            if self.preprocess_type == TYPE_GUBALIST:
                self.process_gubalist(data_item)
            elif self.preprocess_type == TYPE_GUBA:
                self.process_gubaitem(data_item)
        except KeyboardInterrupt:
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)
        except:
            traceback.print_exc()
            pass
        pass

    def clear_handler(self):
        if len(self.tiezi_tuple_list) > 0:
            self.db_session.insertMany(
                self.guba_table_name,
                self.tiezi_tuple_list,
                "guba_id", "guba_title", "publish_time",
                "click_amount", "comment_amount",
                "sec_number", "url", "poster")
        pass

    def parse_post_time(self, post_time):
        # TODO 这里需要检查post time是不是有效的
        # 错误的post time对应的item应该保存下来
        if post_time is None or len(post_time.strip()) == 0:
            return None
        temp = post_time.split(' ')
        if len(temp) == 2:
            post_time = datetime.strptime(
                post_time, "%Y-%m-%d %H:%M:%S")
        else:
            post_time = datetime.strptime(temp[0], "%Y-%m-%d")
        if post_time < self.earlist_time:
            return None
        return post_time.strftime("%Y-%m-%d %H:%M:%S")

    def insert_into_db(self, ticker_id, tiezi_item):
        title = tiezi_item.get('title')
        url = tiezi_item.get('url')
        post_time = tiezi_item.get('a_post_time')
        read_num = tiezi_item.get('read_num')
        comment_num = tiezi_item.get('comment_num')
        poster_name = tiezi_item.get('poster_name')
        if title is None or url is None:
            return
        post_time = self.parse_post_time(post_time)
        if post_time is None:
            print url
            self.logger.debug(url)
            return None
        db_id = self.id_generator.generate_guba_id(self.website_name)
        tiezi_tuple = (
            db_id,
            title,
            post_time,
            read_num,
            comment_num,
            ticker_id,
            url,
            poster_name
        )
        self.tiezi_tuple_list.append(tiezi_tuple)
        if len(self.tiezi_tuple_list) >= self.bat_insert_num:
            self.db_session.insertMany(
                self.guba_table_name,
                self.tiezi_tuple_list,
                "guba_id", "guba_title", "publish_time",
                "click_amount", "comment_amount",
                "sec_number", "url", "poster")
            self.tiezi_tuple_list = []
        pass

    def process_gubalist(self, data_item):
        if data_item is None:
            return
        ticker_id = data_item['ticker_id']
        for item in data_item['tiezi_item']:
            self.insert_into_db(ticker_id, item)
        pass

    def process_gubaitem(self, data_item):
        pass
