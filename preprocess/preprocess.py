# -*- coding: utf-8 -*-

import codecs
import json
import traceback
import logging

from preprocess_settings import *
from news_preprocess_handler import NewsPreprocessHandler
from guba_list_preprocess_handler import GubaListPreprocessHandler
from utils.threadpool import ThreadPool
from utils.universe_settings import *
from database import mysql_pool, mysql_config


class Preprocess(object):

    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)
        pass

    def generate_preprocess_handler(self, preprocess_type, website_name):
        ''' 使用反射机制动态生成相应处理类 '''
        cls = globals()[CRAWLER_TYPE_HANDLER_DICT[preprocess_type]]
        return cls(website_name)

    def open_crawler_file(self, preprocess_type, website_name):
        ''' 打开相应的爬虫数据文件 '''
        return codecs.open(CRAWL_FILE_NAMES[preprocess_type][website_name],
                           'r', 'utf-8', errors='ignore')
        pass

    def preprocess_crawler_results(self, preprocess_type, website_name):
        ''' 对新闻数据进行预处理，主要是清洗然后插入数据库 '''
        self.logger.debug("start process crawler results.")
        pool = ThreadPool(PIPELINE_THREAD_SIZE)
        # 使用线程池
        for i in range(PIPELINE_THREAD_SIZE):
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


def preprocess_given_keywords():
    ''' 向数据库表中插入给定的关键字 '''
    kwfiles_id = {}
    conn = mysql_pool.MySQLPool.getSingleConnection()
    # 插入关键字类型
    for kwfiles_key in GIVEN_KEYWORD_FILES:
        key_id = conn.insertOne(
            mysql_config.DATABASE_TABLES['TABLE_KEYWORDS_PROPERTY'],
            keywords_property_col=kwfiles_key)
        kwfiles_id[kwfiles_key] = key_id  # key_id为对应主键的id
    # 插入关键字
    for kwfiles_key in GIVEN_KEYWORD_FILES:
        for line in codecs.open(GIVEN_KEYWORD_FILES[kwfiles_key],
                                'r', 'utf-8', errors='ignore'):
            line = line.strip().replace(u'\xa0', u' ')
            conn.insertOne(
                mysql_config.DATABASE_TABLES['TABLE_KEYWORDS_LIST'],
                keywords=line,
                keywords_type=0,
                keywords_property_id=kwfiles_id[kwfiles_key])
    conn.close()
    pass


if __name__ == '__main__':
    process = Preprocess()
    process.preprocess_crawler_results(TYPE_NEWS, WEBSITE_EASTMONEY)
    pass
