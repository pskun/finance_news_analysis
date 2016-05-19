# -*- coding: utf-8 -*-

import traceback
import logging

from preprocess_settings import *
from utils.threadpool import Handler
from analyze.keyword_extraction import KeywordExtractor
from database.mysql_pool import MySQLPool
from database import mysql_config


class NewsPreprocessHandler(Handler):

    def __init__(self, website_name):
        self.website_name = website_name
        self.keyword_extractor = KeywordExtractor()
        self.db_session = None
        # 数据库批量插入的列表缓存
        self.bat_insert_num = 1
        self.news_tuple_list = []
        self.news_tickers_tuple_list = []
        self.news_keywords_tuple_list = []
        # 新闻基本信息
        self.web_id = None
        self.news_file_id = None
        self.section_ids = {}
        self.sub_section_ids = {}
        self.keyword_property = {}
        self.keywords = {}
        self.news_id_counter = 1
        # 日志
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)

    def init_handler(self):
        ''' 初始化handler '''
        # 初始化数据库连接
        self.db_session = MySQLPool().getConnection()
        # 载入关键词
        for keyword_type in GIVEN_KEYWORD_FILES:
            kfile = os.path.join(
                GIVEN_KEYWORD_DIR, GIVEN_KEYWORD_FILES[keyword_type])
            self.keyword_extractor.initGivenKeywords(keyword_type, kfile)
        # 从数据库中查询基本的新闻信息
        self.query_basic_info()
        pass

    def process_function(self, data_item):
        try:
            if data_item is not None:
                data_item = self.filter_news(data_item)
            if data_item is not None:
                data_item = self.insert_into_db(data_item)
        except KeyboardInterrupt:
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)
        pass

    def clear_handler(self):
        if len(self.news_tuple) > 0:
            self.db_session.insertMany(
                mysql_config.TABLE_NEWS,
                self.news_tuple_list,
                "news_id", "news_title", "publish_time", "abstract",
                "page_id", "web_id", "news_file_id", "poster")
        if len(self.news_tickers_tuple_list) > 0:
            self.__db_connection.insertMany(
                mysql_config.TABLE_NEWS_SEC,
                self.__news_tickers_tuple_list,
                "news_id", "sec_number")
        if len(self.news_keywords_tuple_list) > 0:
            self.db_session.insertMany(
                mysql_config.TABLE_KEYWORDS_NEWS,
                self.news_keywords_tuple_list,
                "amount_keywords_in_news", "keywords_id", "news_id")
        pass

    def query_basic_info(self):
        # 网站id
        self.web_id = self.db_session.select(
            mysql_config.TABLE_WEB,
            "web_name=\"%s\"" % self.website_name,
            False, "web_id")
        # 新闻文件id
        self.news_file_id = self.db_session.select(
            mysql_config.TABLE_NEWS_FILE,
            "web_id=\"%s\"" % self.web_id,
            False, "news_file_id")
        # 板块id
        result = self.db_session.select(
            mysql_config.TABLE_PAGE, None, True,
            "page_id",
            "page_name",
            "page_level")
        for item in result:
            page_name = item['page_name']
            page_level = item['page_level']
            page_id = item['page_id']
            if page_level == 1:
                self.section_ids[page_name] = page_id
            if page_level == 2:
                self.sub_section_ids[page_name] = page_id
        # 关键字属性id
        result = self.db_session.select(
            mysql_config.TABLE_KEYWORDS_PROPERTY, None, True,
            "keywords_property_id",
            "keywords_property_col")
        # 对所有返回的关键字属性结果
        for item in result:
            self.keyword_property[item["keywords_property_col"]] = item[
                'keywords_property_id']
        # 关键字id
        result = self.db_session.select(
            mysql_config.TABLE_KEYWORDS, None, True,
            "keywords_id", "keywords",
            "keywords_property_id")
        for item in result:
            kp_id = item['keywords_property_id']
            if kp_id not in self.keywords:
                self.keywords[kp_id] = {}
            self.keywords[kp_id][item['keywords']] = item['keywords_id']
        pass

    def extractKeywords(self, content, kw_type='given'):
        if kw_type == 'given':
            # 抽取给定关键词
            all_type_keywords = self.keyword_extractor.extractGivenKeywords(
                content)
            return all_type_keywords
        if kw_type == 'tfidf':
            # 抽取TFIDF关键字
            keywords = self.__keywordExtractor.extractTfidfKeywords(content)
            for k in keywords:
                sys.stderr.write(k[0] + ',')
            sys.stderr.write("\n")
        pass

    def filter_news(self, item):
        # 对新闻的json数据进行预处理
        post_time = item.get('a_post_time')
        if post_time is None:
            self.handle_error(item, "no post time.")
            return None
        url = item.get('url')
        if url is None:
            self.handle_error(item, "no url")
            return None
        # 对新闻正文抽取关键字
        content = item.get('content')
        if content is not None:
            # 抽取给定的关键字
            all_type_keywords = self.extractKeywords(content)
            item['all_type_keywords'] = all_type_keywords
        # 处理股票代码
        mention_tickers_id = item.get('mention_tickers_id')
        if mention_tickers_id is not None:
            item['mention_tickers_id'] = [t[:6] for t in mention_tickers_id]
        return item
        pass

    def generate_news_db_id(self):
        ''' 生成插入数据库中的新闻id
            当前规则: "news" + counter
        '''
        return "news" + str(self.news_id_counter)

    def insert_section_info(self, section_name, level, parent_section=None):
        page_id = self.db_session.insertOne(
            mysql_config.TABLE_PAGE,
            page_name=section_name, page_level=level)
        return page_id

    def insert_news_info(self, news_id, data):
        # 判断板块信息是否已经存在
        page_id = None
        self.logger.debug(data)
        sub_section = data['c_sub_section']
        if sub_section not in self.sub_section_ids:
            parent_page_id = None
            # 父版面是否在数据库中
            section = data['b_section']
            if section not in self.section_ids:
                # 没有则需要先插入数据库
                parent_page_id = self.insert_section_info(section, 1)
            else:
                parent_page_id = self.section_ids[section]
            # 需要把子版面信息先插入数据库
            page_id = self.insert_section_info(
                sub_section, 2, parent_page_id)
        else:
            page_id = self.sub_section_ids[sub_section]

        # 新闻插入缓存元组
        news_tuple = tuple(
            news_id,
            data['title'],
            data['a_post_time'],
            data['summary'],
            page_id,
            self.web_id,
            self.news_file_id,
            poster=data.get('poster')
        )
        self.news_tuple_list.append(news_tuple)
        if len(self.news_tuple_list) >= self.bat_insert_num:
            self.db_session.insertMany(
                mysql_config.TABLE_NEWS,
                self.news_tuple_list,
                "news_id", "news_title", "publish_time", "abstract",
                "page_id", "web_id", "news_file_id", "poster")
            self.news_tuple_list = []
        pass

    def insert_keyword_info(self, news_id, data):
        news_keywords = data.get('all_type_keywords')
        if news_keywords is not None:
            # 如果提取出了关键字
            for kw_type in news_keywords:
                # 对每种关键字类型
                for keyword in news_keywords[kw_type]:
                    # 对每种关键字类型中的关键字
                    keyword_tuple = tuple(
                        # 关键字在新闻中出现的数量
                        news_keywords[kw_type][keyword],
                        self.keywords[
                            self.keyword_property[kw_type]][keyword],
                        news_id
                    )
                    self.news_keywords_tuple_list.append(keyword_tuple)
        if len(self.__news_keywords_tuple_list) >= 800:
            self.db_session.insertMany(
                mysql_config.TABLE_KEYWORDS_NEWS,
                self.news_keywords_tuple_list,
                "amount_keywords_in_news", "keywords_id", "news_id")
            self.news_keywords_tuple_list = []
        pass

    def insert_ticker_info(self, news_id, data):
        mention_tickers_id = data.get('mention_tickers_id')
        if mention_tickers_id is not None:
            for ticker in set(mention_tickers_id):
                self.__news_tickers_tuple_list.append((news_id, ticker))
        if len(self.__news_tickers_tuple_list) >= 800:
            self.__db_connection.insertMany(
                mysql_config.TABLE_NEWS_SEC,
                self.__news_tickers_tuple_list,
                "news_id", "sec_number")
            self.__news_tickers_tuple_list = []
        pass

    def insert_into_db(self, data):
        try:
            news_id = self.generate_news_db_id()
            # 插入新闻至news_list中
            self.insert_news_info(news_id, data)
            # 新闻提取的关键字插入至rel_news_keywords中
            self.insert_keyword_info(news_id, data)
            # 插入股票新闻关联表
            self.insert_ticker_info(news_id, data)
            self.news_id_counter += 1
        except:
            traceback.print_exc()
            pass
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
