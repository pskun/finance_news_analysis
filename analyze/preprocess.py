# -*- coding: utf-8 -*-

import os
import sys
import codecs
import json
import traceback

from analyze_settings import *
from preprocess_pipeline import NewsPipeline, DatabasePipeline
from utils import threadpool
from database import mysql_pool, mysql_config

try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass


class NewsPreprocessHandler(threadpool.Handler):

    def __init__(self, news_website):
        self.__news_website = news_website
        self.__newsPipe = NewsPipeline(self.__news_website)
        self.__dbPipe = DatabasePipeline(self.__news_website)

    def init_handler(self):
        self.__newsPipe.before_process()
        self.__dbPipe.before_process()
        pass

    def process_function(self, data_item):
        try:
            if data_item is not None:
                data_item = self.__newsPipe.process_item(data_item)
            '''
            if data_item is not None:
                data_item = self.__dbPipe.process_item(data_item)
            '''
        except KeyboardInterrupt:
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)
        pass


class GivenKeywordsHandler():
    def __init__(self):
        pass


# 对新闻数据进行预处理，主要是清洗然后插入数据库
def preprocess_news(news_website):
    pool = threadpool.ThreadPool(PIPELINE_THREAD_SIZE)
    # add customer threadpool worker
    for i in range(PIPELINE_THREAD_SIZE):
        h = NewsPreprocessHandler(news_website)
        h.init_handler()
        pool.add_handler(h)
    pool.startAll()
    # open wrong output log
    wrong_output = codecs.open(
        WRONG_PREPROCESS_OUTPUT, 'w', 'utf-8', errors='ignore')
    # open todo file
    for line in codecs.open(
            CRAWL_FILE_NAMES[news_website], 'r', 'utf-8',
            errors='ignore'):
        try:
            line = line.strip().replace(u'\xa0', u' ')
            data_item = json.loads(line)
            if data_item is not None:
                pool.add_process_data(data_item)
        except:
            # traceback.print_exc()
            wrong_output.write(line + '\n')
            continue
    pool.wait_completion()
    pass


# 对股吧数据进行预处理，主要是清洗和插入数据库
def preprocess_guba(guba_website):
    pool = threadpool.ThreadPool(PIPELINE_THREAD_SIZE)
    '''
    # add customer threadpool worker
    for i in range(PIPELINE_THREAD_SIZE):
        h = NewsPreprocessHandler(guba_website)
        h.init_handler()
        pool.add_handler(h)
    pool.startAll()
    # open wrong output log
    wrong_output = codecs.open(
        WRONG_PREPROCESS_OUTPUT, 'w', 'utf-8', errors='ignore')
    '''
    # open todo file
    for line in codecs.open(
            CRAWL_FILE_NAMES[guba_website], 'r', 'utf-8',
            errors='ignore'):
        try:
            line = line.strip().replace(u'\xa0', u' ')
            print line
            '''
            data_item = json.loads(line)
            if data_item is not None:
                pool.add_process_data(data_item)
            '''
        except:
            # traceback.print_exc()
            wrong_output.write(line)
            continue
    pool.wait_completion()
    pass


def preprocess_given_keywords():
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


def preprocess_primary_info(news_website):
    # get connection
    conn = mysql_pool.MySQLPool.getSingleConnection()
    web_id = conn.insertOne(
        mysql_config.DATABASE_TABLES['TABLE_WEB_LIST'],
        web_name=news_website,
        web_address=CRAWL_WEBSITES[news_website])
    file_id = conn.insertOne(
        mysql_config.DATABASE_TABLES['TABLE_NEWS_FILE_LIST'],
        web_id=web_id,
        file_storage_location=CRAWL_FILE_NAMES[news_website],
        file_name=CRAWL_FILE_NAMES[news_website].split('/')[-1])
    sections = {}
    # open todo file
    for line in codecs.open(
            CRAWL_FILE_NAMES[news_website], 'r', 'utf-8',
            errors='ignore'):
        try:
            line = line.strip().replace(u'\xa0', u' ')
            data_item = json.loads(line)
            if data_item is not None:
                section = data_item.get('section')
                sub_section = data_item.get('sub_section')
                if section is None or sub_section is None:
                    continue
                if section not in sections:
                    sections[section] = set()
                sections[section].add(sub_section)
        except:
            # traceback.print_exc()
            # print line
            continue
    for section in sections:
        section_id = conn.insertOne(
                mysql_config.DATABASE_TABLES['TABLE_PAGE_LIST'],
                web_id=web_id,
                page_name=section,
                page_level="1")
        for sub_section in sections[section]:
            conn.insertOne(mysql_config.DATABASE_TABLES['TABLE_PAGE_LIST'],
                           web_id=web_id,
                           page_name=sub_section,
                           page_level="2",
                           parent_page_id=section_id)
            pass
        pass
    conn.close()
    return web_id, file_id
    pass


if __name__ == '__main__':
    os.chdir(BASE_DIR)
    sys.path.append(os.path.abspath(BASE_DIR))
    '''
    if len(sys.argv) == 1:
        sys.stderr.write(
            "Usage: python %s -t preprocess_type [-w website_name]\n"
            % sys.argv[0])
        sys.stderr.write("type:\n")
        sys.stderr.write(
            "\tnews_type\n\tkeyword_type\n\tbasic_type\n\tguba_type\n")
        sys.exit(1)
    '''
    preprocess_news("eastmoney")
    # preprocess_given_keywords()
    # preprocess_primary_info(u'eastmoney')
    pass
