# -*- coding: utf-8 -*-

import os

from utils.universe_settings import *

''' 需要修改的部分 '''
# 新增一个预处理Handler的时候需要加入
CRAWLER_TYPE_HANDLER_DICT = {
    TYPE_GUBALIST: 'GubaPreprocessHandler',
    TYPE_GUBA: 'GubaPreprocessHandler',
    TYPE_NEWS: 'NewsPreprocessHandler',
}

# 数据预处理文件的路径
# 新添加一个爬取文件的时候需要加入
CRAWL_FILE_NAMES = {
    TYPE_NEWS: {
        WEBSITE_EASTMONEY: r'EastMoneyNewsSpider.json',
    },
    TYPE_GUBA: {
        WEBSITE_EASTMONEY: r'EastMoneyGubaSpider.json',
    },
    TYPE_GUBALIST: {
        WEBSITE_EASTMONEY: r'EastMoneyGubaListSpider.json',
    },
}

# 新加入一个爬取网站时需要加入
CRAWL_WEBSITES = {
    WEBSITE_EASTMONEY: r'http://www.eastmoney.com/',
}

''' 基本不需要修改的部分 '''
# 预处理数据文件目录
PRE_DATA_DIR = os.path.join(PREPROCESS_DIR, 'pre_data')
# 给定关键词文件目录
GIVEN_KEYWORD_DIR = os.path.join(PRE_DATA_DIR, 'given_keywords')

GIVEN_KEYWORD_FILES = {
    'wind_concept': r'concept_keywords.txt',
    'shenwan_1st_industry': r'shenwan_1st_industry.txt',
    'shenwan_2nd_industry': r'shenwan_2nd_industry.txt',
    'shenwan_3rd_industry': r'shenwan_3rd_industry.txt',
}

for key in GIVEN_KEYWORD_FILES:
    GIVEN_KEYWORD_FILES[key] = os.path.join(
        GIVEN_KEYWORD_DIR, GIVEN_KEYWORD_FILES[key])

for precess_type in CRAWL_FILE_NAMES:
    for website in CRAWL_FILE_NAMES[precess_type]:
        CRAWL_FILE_NAMES[precess_type][website] = os.path.join(
            DATA_DIR, CRAWL_FILE_NAMES[precess_type][website])
