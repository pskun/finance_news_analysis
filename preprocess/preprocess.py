# -*- coding: utf-8 -*-

import codecs
import json
import threading
import traceback
import logging

from universe_settings import *
from preprocess_settings import *
from identity_generator import IdentityGenerator
from news_preprocess_handler import NewsPreprocessHandler
from guba_preprocess_handler import GubaPreprocessHandler
from utils.threadpool import ThreadPool
from database.mysql_pool import MySQLPool
from database import mysql_config


class Preprocess(object):

    def __init__(self, thread_size=1):
        self.thread_size = thread_size
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)
        self.mutex = threading.Lock()
        self.id_generator = IdentityGenerator(mutex=self.mutex)
        pass

    def generate_preprocess_handler(self, preprocess_type, website_name):
        ''' 使用反射机制动态生成相应处理类 '''
        cls = globals()[CRAWLER_TYPE_HANDLER_DICT[preprocess_type]]
        return cls(preprocess_type, self.id_generator, website_name)

    def open_crawler_file(self, preprocess_type, website_name):
        ''' 打开相应的爬虫数据文件 '''
        return codecs.open(CRAWL_FILE_NAMES[preprocess_type][website_name],
                           'r', 'utf-8', errors='ignore')
        pass

    def preprocess_crawler_results(self, preprocess_type, website_name):
        ''' 对新闻数据进行预处理，主要是清洗然后插入数据库 '''
        self.logger.debug("start process crawler results.")
        pool = ThreadPool(self.thread_size)
        # 使用线程池
        for i in range(self.thread_size):
            h = self.generate_preprocess_handler(preprocess_type, website_name)
            pool.add_handler(h)
        pool.startAll()
        # 打开新闻爬虫文件
        f = self.open_crawler_file(preprocess_type, website_name)
        if f is None:
            return
        self.logger.debug("start read data from file.")
        for line in f:
            try:
                line = line.strip().replace(u'\xa0', u' ')
                data_item = json.loads(line)
                if data_item is not None:
                    pool.add_process_data(data_item)
            except:
                traceback.print_exc()
                continue
        self.logger.debug("read data completed.")
        pool.wait_completion()
        pass

    def preprocess_given_keywords(self):
        ''' 向数据库表中插入给定的关键字 '''
        kwfiles_id = {}
        conn = MySQLPool().getSingleConnection()
        # 插入关键字类型
        for kwfiles_key in GIVEN_KEYWORD_FILES:
            key_id = conn.insertOne(
                mysql_config.TABLE_KEYWORDS_PROPERTY,
                keywords_property_col=kwfiles_key)
            kwfiles_id[kwfiles_key] = key_id  # key_id为对应主键的id
        # 插入关键字
        for kwfiles_key in GIVEN_KEYWORD_FILES:
            f = codecs.open(GIVEN_KEYWORD_FILES[kwfiles_key], 'r', 'utf-8')
            for line in f:
                line = line.strip().replace(u'\xa0', u' ')
                conn.insertOne(
                    mysql_config.TABLE_KEYWORDS,
                    keywords=line,
                    keywords_type=0,
                    keywords_property_id=kwfiles_id[kwfiles_key])
        conn.close()
    pass


if __name__ == '__main__':
    process = Preprocess(thread_size=2)
    process.preprocess_crawler_results(TYPE_NEWS, WEBSITE_EASTMONEY)
    pass
