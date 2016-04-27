# encoding=utf-8

import os
import sys

import time
from datetime import datetime
import locale
import json
from bson import json_util
from analyze_settings import *
sys.path.append(os.path.abspath(BASE_DIR))

from keyword_extraction import KeywordExtractor
from database import mysql_pool
from database import mysql_config


locale.setlocale(locale.LC_CTYPE, 'chinese')


class BasicPipeline(object):
    def __init__(self):
        pass

    def before_process(self):
        pass

    def after_process(self):
        pass

    def process_item(self, item):
        pass


class NewsPipeline(BasicPipeline):
    def __init__(self, news_website):
        self.__count_news = {}
        self.__error_lines = []
        self.__keywordExtractor = None
        self.__news_website = news_website
        pass

    def before_process(self):
        self.__error_lines = []
        self.__keywordExtractor = KeywordExtractor()
        for keyword_type in GIVEN_KEYWORD_FILES:
            kfile = os.path.join(
                GIVEN_KEYWORD_DIR, GIVEN_KEYWORD_FILES[keyword_type])
            self.__keywordExtractor.initGivenKeywords(keyword_type, kfile)
        self.__keywordExtractor.initTfidfKeywords(IDF_FILE)
        pass

    def after_process(self):
        pass

    def process_item(self, item):
        post_time = item.get('a_post_time')
        if post_time is None:
            self.handle_error(item, "no post time")
            return None
        # process news post time
        t = post_time.replace(u"年","-").replace(u"月", "-").replace(u"日", "") + ":00"
        # print t
        # sys.exit(1)
        # t = datetime.strptime(post_time, u"%Y年%m月%d日 %H:%M")
        # item['a_post_time'] = t.strftime('%Y-%m-%d %H:%M:%S')
        item['a_post_time'] = t
        # process news url
        url = item.get('url')
        if url is None:
            self.handle_error(item, "no url")
            return None
        # process news content
        content = item.get('content')
        if content is not None:
            # 抽取给定关键字
            all_type_keywords = self.extractKeywords(content)
            item['all_type_keywords'] = all_type_keywords
            '''
            # 抽取TFIDF关键字
            keywords = self.__keywordExtractor.extractTfidfKeywords(content)
            for k in keywords:
                sys.stderr.write(k[0] + ',')
            sys.stderr.write("\n")
            '''
        # process stock ticker
        mention_tickers_id = item.get('mention_tickers_id')
        if mention_tickers_id is not None:
            item['mention_tickers_id'] = [t[:6] for t in mention_tickers_id]
        # just for debug
        '''
        try:
            line = json.dumps(
                item, ensure_ascii=False, default=json_util.default)
        except:
            print line
            sys.exit(1)
        '''
        return item
        pass

    def extractKeywords(self, content):
        all_type_keywords = self.__keywordExtractor.extractGivenKeywords(
            content)
        return all_type_keywords
        pass

    def handle_error(self, item, error_str):
        try:
            line = error_str + '\t'
            line += json.dumps(dict(item),
                               ensure_ascii=False, sort_keys=True) + '\n'
            self.__error_lines.append(line)
        except:
            pass
        pass


class NewsDBInsertionPipeline(BasicPipeline):
    def __init__(self, news_website):
        self.__db_handler = None
        self.__db_connection = None
        self.__web_id = None
        self.__page_id = None
        self.__news_file_id = None
        self.__keyword_property = None
        self.__keywords = None
        self.__news_website = news_website
        self.__news_tickers_tuple_list = []
        self.__news_keywords_tuple_list = []
        pass

    def before_process(self):
        # self.__db_handler = mysql_pool.MySQLPool.getSingleConnection()
        self.__db_connection = mysql_pool.MySQLPool.getSingleConnection()
        # self.__db_connection.execute("set autocommit=0;")
        # 网站id
        result = self.__db_connection.select(
            mysql_config.DATABASE_TABLES['TABLE_WEB_LIST'],
            "web_name=\"%s\"" % self.__news_website,
            "web_id")
        self.__web_id = result[0] if result is not None and len(
            result) > 0 else None
        # 新闻文件id
        result = self.__db_connection.select(
            mysql_config.DATABASE_TABLES['TABLE_NEWS_FILE_LIST'],
            "web_id=\"%s\"" % self.__web_id,
            "news_file_id")
        self.__news_file_id = result[
            0] if result is not None and len(result) > 0 else None
        # 版面id
        result = self.__db_connection.select(
            mysql_config.DATABASE_TABLES['TABLE_PAGE_LIST'],
            None,
            "page_id",
            "page_name",
            "page_level")
        self.__page_id = {}
        for item in result:
            if item['page_level'] == 1 and item['page_name'] == u'股吧':
                self.__page_id[item['page_name']] = item['page_id']
            elif item['page_level'] == 2:
                if item['page_name'] not in self.__page_id:
                    self.__page_id[item['page_name']] = item['page_id']
        # 关键字属性id
        result = self.__db_connection.select(
            mysql_config.DATABASE_TABLES['TABLE_KEYWORDS_PROPERTY'],
            None,
            "keywords_property_id",
            "keywords_property_col")
        self.__keyword_property = {}
        for item in result:
            self.__keyword_property[item["keywords_property_col"]] = item[
                'keywords_property_id']
        # 关键字id
        result = self.__db_connection.select(
            mysql_config.DATABASE_TABLES['TABLE_KEYWORDS_LIST'],
            None,
            "keywords_id",
            "keywords",
            "keywords_property_id")
        self.__keywords = {}
        for item in result:
            if item['keywords_property_id'] not in self.__keywords:
                self.__keywords[item['keywords_property_id']] = {}
            self.__keywords[item['keywords_property_id']][
                item['keywords']] = item['keywords_id']
        pass

    def after_process(self):
        if len(self.__news_tickers_tuple_list) > 0:
            self.__db_connection.insertMany(
                    mysql_config.DATABASE_TABLES['TABLE_COR_SEC_OF_NEWS'],
                    news_tickers_tuple_list,
                    "news_id", "sec_number")
        if len(self.__news_keywords_tuple_list) > 0:
            self.__db_connection.insertMany(
                    mysql_config.DATABASE_TABLES[
                        'TABLE_RELATION_KEYWORDS_NEWS'],
                    self.__news_keywords_tuple_list,
                    "amount_keywords_in_news", "keywords_id", "news_id")
        pass

    def process_item(self, data):
        try:
            # 插入新闻
            news_id = self.__db_connection.insertOne(
                mysql_config.DATABASE_TABLES['TABLE_NEWS_LIST'],
                news_title=data['title'],
                publish_time=data['a_post_time'],
                abstract=data['summary'],
                page_id=self.__page_id[data['c_sub_section']],
                web_id=self.__web_id,
                news_file_id=self.__news_file_id,
                poster=data.get('poster'))
            # 插入关键字
            news_keywords = data.get('all_type_keywords')
            if news_keywords is not None:
                for kw_type in news_keywords:
                    for keyword in news_keywords[kw_type]:
                        self.__news_keywords_tuple_list.append(
                            (news_keywords[kw_type][keyword],
                                self.__keywords[self.__keyword_property[kw_type]][keyword],
                            news_id))
                if len(self.__news_keywords_tuple_list) >= 800:
                    self.__db_connection.insertMany(
                        mysql_config.DATABASE_TABLES['TABLE_RELATION_KEYWORDS_NEWS'],
                        self.__news_keywords_tuple_list,
                        "amount_keywords_in_news", "keywords_id", "news_id")
                    self.__news_keywords_tuple_list = []
                pass
            # 插入股票新闻关联表
            mention_tickers_id = data.get('mention_tickers_id')
            if mention_tickers_id is not None:
                for ticker in set(mention_tickers_id):
                    self.__news_tickers_tuple_list.append((news_id, ticker))
            if len(self.__news_tickers_tuple_list) >= 800:
                self.__db_connection.insertMany(
                    mysql_config.DATABASE_TABLES['TABLE_COR_SEC_OF_NEWS'],
                    self.__news_tickers_tuple_list,
                    "news_id", "sec_number")
                del self.__news_tickers_tuple_list[:]
                self.__news_tickers_tuple_list = []
        except:
            pass
        pass


class GubaPipeline(object):
    def __init__(self, guba_website):
        self.__error_lines = []
        self.__keywordExtractor = None
        self.__news_website = guba_website
        pass

    def before_process(self):
        pass

    def after_process(self):
        pass

    def process_item(self, item):
        post_time = item.get('a_post_time')
        if post_time is None:
            self.handle_error(item, "no post time")
            return None
        # process news content
        content = item.get('content')
        if content is not None:
            item['summary'] = content
        # process stock ticker
        ticker_id = item.get('ticker_id')
        if ticker_id is not None:
            item['mention_tickers_id'] = [ticker_id]
        item['c_sub_section'] = u"股吧"
        poster = item.get('poster_name')
        if poster is not None:
            item['poster'] = poster
        # just for debug
        '''
        try:
            line = json.dumps(
                item, ensure_ascii=False, default=json_util.default)
        except:
            print line
            sys.exit(1)
        '''
        return item
        pass
