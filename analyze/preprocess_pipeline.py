# encoding=utf-8

import os
import sys

import time
import datetime
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
        self.__keywordExtrctor = None
        self.__news_website = news_website
        pass

    def before_process(self):
        self.__error_lines = []
        self.__keywordExtrctor = KeywordExtractor()
        for keyword_type in GIVEN_KEYWORD_FILES:
            kfile = os.path.join(
                GIVEN_KEYWORD_DIR, GIVEN_KEYWORD_FILES[keyword_type])
            self.__keywordExtrctor.initGivenKeywords(keyword_type, kfile)
        pass

    def after_process(self):
        pass

    def process_item(self, item):
        post_time = item.get('a_post_time')
        if post_time is None:
            self.handle_error(item, "no post time")
            return None
        # process news post time
        t = time.strptime(post_time, u"%Y年%m月%d日 %H:%M")
        item['a_post_time'] = datetime.datetime(
            *t[:6]).strftime('%Y-%m-%d %H:%M:%S')
        self.count_news_by_date(t)
        # process news url
        url = item.get('url')
        if url is None:
            self.handle_error(item, "no url")
            return None
        # process news content
        content = item.get('content')
        if content is not None:
            all_type_keywords = self.extractKeywords(content)
            item['all_type_keywords'] = all_type_keywords
        try:
            line = json.dumps(
                item, ensure_ascii=False, default=json_util.default)
        except:
            print line
            sys.exit(1)
        return item
        pass

    def count_news_by_date(self, post_time):
        d = datetime.datetime(*post_time[:5])
        date_str = d.strftime('%Y%m%d')
        if date_str in self.__count_news:
            self.__count_news[date_str] += 1
        else:
            self.__count_news[date_str] = 1

    def extractKeywords(self, content):
        all_type_keywords = self.__keywordExtrctor.extractGivenKeywords(
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


class DatabasePipeline(BasicPipeline):
    def __init__(self, news_website):
        self.__db_handler = None
        self.__db_connection = None
        self.__web_id = None
        self.__page_id = None
        self.__news_file_id = None
        self.__keyword_property = None
        self.__keywords = None
        self.__news_website = news_website

    def before_process(self):
        self.__db_handler = mysql_pool.MySQLPool()
        self.__db_connection = self.__db_handler.getConnection()
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
            None,
            "news_file_id")
        self.__news_file_id = result[
            0] if result is not None and len(result) > 0 else None
        # 版面id
        result = self.__db_connection.select(
            mysql_config.DATABASE_TABLES['TABLE_PAGE_LIST'],
            None,
            "page_id",
            "page_name",
            "page_lever")
        self.__page_id = {}
        for item in result:
            if item['page_lever'] == 2:
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
        pass

    def process_item(self, data):
        news_id = self.__db_connection.insertOne(
            mysql_config.DATABASE_TABLES['TABLE_NEWS_LIST'],
            news_title=data['title'],
            publish_time=data['a_post_time'],
            abstract=data['summary'],
            page_id=self.__page_id[data['sub_section']],
            web_id=self.__web_id,
            news_file_id=self.__news_file_id
        )
        news_keywords = data.get('all_type_keywords')
        if news_keywords is not None:
            news_keywords_tuple_list = []
            for kw_type in news_keywords:
                for keyword in news_keywords[kw_type]:
                    news_keywords_tuple_list.append(
                        (news_keywords[kw_type][keyword],
                            self.__keywords[
                                self.__keyword_property[kw_type]][keyword],
                            news_id))
            if len(news_keywords_tuple_list) > 0:
                self.__db_connection.insertMany(
                    mysql_config.DATABASE_TABLES[
                        'TABLE_RELATION_KEYWORDS_NEWS'],
                    news_keywords_tuple_list,
                    "amount_keywords_in_news",
                    "keywords_id",
                    "news_id")
                pass
        pass
