# -*- coding: utf-8 -*-

import traceback
import logging

from preprocess_settings import *
from utils.threadpool import Handler
from universe_settings import *
from analyze.keyword_extraction import KeywordExtractor
from database.mysql_pool import SqlAlchemyPool
from database import mysql_config
from database import common_db_func


class ReportPreprocessHandler(Handler):
    ''' 研报数据预处理Handler '''
    def __init__(self, preprocess_type, id_generator=None, website_name=None):
        self.preprocess_type = preprocess_type
        self.website_name = website_name
        self.id_generator = id_generator
        self.keyword_extractor = KeywordExtractor()
        self.db_session = None
        # 数据库批量插入的列表缓存
        self.bat_insert_num = 800
        self.report_tuple_list = []
        self.report_tickers_tuple_list = []
        self.report_keywords_tuple_list = []
        # 研报基本信息
        self.report_id = None
        self.news_file_id = None
        self.top_section_id = None
        self.section_ids = {}
        self.keyword_property = {}
        self.keywords = {}
        # 日志
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)

    def before_thread_start(self):
        ''' 回调函数: 线程启动前调用 '''
        # 初始化数据库连接
        self.db_session = SqlAlchemyPool().getConnection()
        # 获取新闻表的行数
        report_id_counter = common_db_func.query_table_count(
            self.db_session, mysql_config.TABLE_REPORT) + 1
        # 设置id的初始值
        self.id_generator.set_initial_counter(report_id_counter)
        pass

    def init_handler(self):
        ''' 初始化handler的回调函数 '''
        # 载入关键词
        for keyword_type in GIVEN_KEYWORD_FILES:
            kfile = os.path.join(
                GIVEN_KEYWORD_DIR, GIVEN_KEYWORD_FILES[keyword_type])
            self.keyword_extractor.initGivenKeywords(keyword_type, kfile)
        # 从数据库中查询基本的新闻信息
        self.process_basic_info()
        pass

    def process_function(self, data_item):
        try:
            if data_item is not None:
                data_item = self.filter_report(data_item)
            if data_item is not None:
                data_item = self.insert_into_db(data_item)
        except KeyboardInterrupt:
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)
        pass

    def clear_handler(self):
        if len(self.report_tuple_list) > 0:
            self.db_session.insertMany(
                mysql_config.TABLE_REPORT,
                self.report_tuple_list,
                "news_id", "news_title", "publish_time", "abstract",
                "page_id", "web_id", "news_file_id", "poster")
        if len(self.report_tickers_tuple_list) > 0:
            self.__db_connection.insertMany(
                mysql_config.TABLE_NEWS_SEC,
                self.report_tickers_tuple_list,
                "news_id", "sec_number")
        if len(self.news_keywords_tuple_list) > 0:
            self.db_session.insertMany(
                mysql_config.TABLE_KEYWORDS_NEWS,
                self.report_keywords_tuple_list,
                "amount_keywords_in_news", "keywords_id", "news_id")
        pass

    def process_basic_info(self):
        # 网站id
        # 插入新网站名称
        self.web_id = common_db_func.insert_new_website(
            self.db_session, self.website_name,
            CRAWL_WEBSITES[self.website_name])
        if self.web_id == 0:
            self.web_id = common_db_func.query_web_id(
                self.db_session, self.website_name)
        # 新闻文件id
        # 插入新文件的文件名
        file = CRAWL_FILE_NAMES[TYPE_NEWS][self.website_name]
        self.news_file_id = common_db_func.insert_new_filename(
            self.db_session, self.web_id, file)
        if self.news_file_id == 0:
            self.news_file_id = common_db_func.query_file_id(
                self.db_session, file)
        # 板块id
        top_page_name = u"研报"
        self.top_section_id = common_db_func.insert_page(top_page_name, 1)
        # 关键字属性id
        result = self.db_session.select(
            mysql_config.TABLE_KEYWORDS_PROPERTY, None, True,
            "keywords_property_id",
            "keywords_property_col")
        # 对所有返回的关键字属性结果
        if result is not None:
            for item in result:
                self.keyword_property[item["keywords_property_col"]] = item[
                    'keywords_property_id']
        # 关键字id
        result = self.db_session.select(
            mysql_config.TABLE_KEYWORDS, None, True,
            "keywords_id", "keywords",
            "keywords_property_id")
        if result is not None:
            for item in result:
                kp_id = item['keywords_property_id']
                if kp_id not in self.keywords:
                    self.keywords[kp_id] = {}
                self.keywords[kp_id][item['keywords']] = item['keywords_id']
        pass

    def extractKeywords(self, content, kw_type='given'):
        ''' 抽取关键词 '''
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

    def filter_report(self, item):
        ''' 对研报的json数据进行预处理 '''
        post_time = item.get('a_post_time')
        if post_time is None:
            self.handle_error(item, "no post time.")
            return None
        url = item.get('url')
        if url is None:
            self.handle_error(item, "no url")
            return None
        # 对研报摘要抽取关键字
        abstract = item.get('abstract')
        if abstract is not None:
            # 抽取给定的关键字
            all_type_keywords = self.extractKeywords(abstract)
            item['all_type_keywords'] = all_type_keywords
        return item

    def insert_report_info(self, report_id, data):
        ''' 插入研报数据 '''
        # 判断板块信息是否已经存在
        page_id = None
        section = data['b_section']
        # 版面是否存在数据库中
        if section is not None:
            section = sub_section.strip()
            if len(section) == 0:
                section = u"空版面"
        if section not in self.section_ids:
            # 需要把版面信息插入数据库
            page_id = common_db_func.insert_page(
                db_session, section, 2, self.top_page_name)
            self.section_ids[section] = page_id
        else:
            page_id = self.section_ids[section]
        # 分析师名称
        analyst_name = data.get('analyst_name')
        if analyst_name is not None:
            analyst_name = ";".join(analyst_name)
        # 新闻插入缓存元组
        report_tuple = (
            report_id,
            data['title'],              # 研报标题
            data['a_post_time'],        # 发表时间
            data['industry'],           # 所属行业
            data['poster_name'],        # 发布机构名称
            analyst_name,               # 分析师名称
            data['abstract'],           # 摘要
            data.get('rating_level'),   # 评级分类
            data.get('rating_change'),  # 评级变动
            data.get('upside'),         # 上涨空间
            data.get('yanbao_class'),   # 研报分类
            self.news_file_id,
            self.web_id,
            page_id,
        )
        self.report_tuple_list.append(report_tuple)
        if len(self.report_tuple_list) >= self.bat_insert_num:
            self.db_session.insertMany(
                mysql_config.TABLE_REPORT,
                self.report_tuple_list,
                "report_id", "report_title", "publish_time", "industry",
                "org_name", "analyst_name", "rating_level", "rating_change",
                "upside", "report_class", "abstract",
                "news_file_id", "web_id", "page_id")
            self.report_tuple_list = []
        pass

    def insert_keyword_info(self, report_id, data):
        ''' 插入研报摘要的关键词数据 '''
        report_keywords = data.get('all_type_keywords')
        if report_keywords is not None:
            # 如果提取出了关键字
            for kw_type in report_keywords:
                # 对每种关键字类型
                for keyword in report_keywords[kw_type]:
                    # 对每种关键字类型中的关键字
                    keyword_tuple = (
                        # 关键字在新闻中出现的数量
                        report_keywords[kw_type][keyword],
                        self.keywords[
                            self.keyword_property[kw_type]][keyword],
                        report_id
                    )
                    self.report_keywords_tuple_list.append(keyword_tuple)
        if len(self.report_keywords_tuple_list) >= self.bat_insert_num:
            self.db_session.insertMany(
                mysql_config.TABLE_KEYWORDS_NEWS,
                self.report_keywords_tuple_list,
                "amount_keywords_in_news", "keywords_id", "news_id")
            self.report_keywords_tuple_list = []
        pass

    def insert_ticker_info(self, report_id, data):
        ''' 向数据库中插入新闻股票关联数据 '''
        ticker_id = data.get('ticker_id')
        if ticker_id is not None:
            self.report_tickers_tuple_list.append((report_id, ticker_id))
        if len(self.report_tickers_tuple_list) >= self.bat_insert_num:
            self.db_session.insertMany(
                mysql_config.TABLE_NEWS_SEC,
                self.report_tickers_tuple_list,
                "news_id", "sec_number")
            self.report_tickers_tuple_list = []
        pass

    def insert_into_db(self, data):
        try:
            report_id = self.id_generator.generate_news_id()
            # 插入新闻至news_list中
            self.insert_report_info(report_id, data)
            # 新闻提取的关键字插入至rel_news_keywords中
            self.insert_keyword_info(report_id, data)
            # 插入股票新闻关联表
            self.insert_ticker_info(report_id, data)
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
