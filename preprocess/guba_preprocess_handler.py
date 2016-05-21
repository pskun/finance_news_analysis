# -*- coding: utf-8 -*-

import os
import sys
from datetime import datetime
import traceback
import logging

from utils.threadpool import Handler
from database.mysql_pool import MySQLPool
from database import mysql_config


class GubaPreprocessHandler(Handler):

    def __init__(self, id_generator, website_name=None, wrong_file=None):
        self.website_name = website_name
        self.id_generator = id_generator
        self.db_session = None
        self.tiezi_tuple_list = []
        self.bat_insert_num = 1000
        self.guba_table_name = mysql_config.TABLE_GUBA % website_name
        # 日志
        logging.basicConfig(level=logging.DEBUG, filename=wrong_file)
        self.logger = logging.getLogger(__name__)

    def init_handler(self):
        ''' 初始化handler '''
        # 初始化数据库连接
        self.db_session = MySQLPool().getConnection()
        pass

    def process_function(self, data_item):
        try:
            data_item = self.filter_gubalist(data_item)
            if data_item is None:
                return
            ticker_id = data_item['ticker_id']
            for item in data_item['tiezi_item']:
                self.insert_into_db(ticker_id, item)
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
        if len(self.__tiezi_tuple_list) > 0:
            self.db_session.insertMany(
                self.guba_table_name,
                self.tiezi_tuple_list,
                "title", "publish_time",
                "click_amount", "comment_amount",
                "sec_number", "url", 'poster_name')
        pass

    def parse_post_time(self, post_time):
        # TODO 这里需要检查post time是不是有效的
        # 错误的post time对应的item应该保存下来
        if post_time is None or len(post_time.strip()) == 0:
            return None
        post_time = datetime.strptime(post_time, "%Y-%m-%d %H:%M:%S")
        earlist_time = datetime.strptime("1990", "%Y")
        if post_time < earlist_time:
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
            self.logger.debug(url)
            return None
        db_id = self.id_generator.generate_guba_id(self.website_name)
        tiezi_tuple = tuple(
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
            self.__db_connection.insertMany(
                self.guba_table_name,
                self.tiezi_tuple_list,
                "tiezi_id", "tiezi_title", "publish_time",
                "click_amount", "comment_amount",
                "sec_number", "url", "poster")
            self.tiezi_tuple_list = []
        pass

    def filter_gubalist(self, item):
        return item
