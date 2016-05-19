# -*- coding: utf-8 -*-

import os

from utils.universe_settings import *

CRAWLER_TYPE_HANDLER_DICT = {
    TYPE_GUBALIST: 'GubaListPreprocessHandler',
    TYPE_NEWS: 'NewsPreprocessHandler',
}

# 预处理数据文件目录
PRE_DATA_DIR = os.path.join(PREPROCESS_DIR, 'pre_data')
# 给定关键词文件目录
GIVEN_KEYWORD_DIR = os.path.join(PRE_DATA_DIR, 'given_keywords')

# 数据预处理文件的路径
CRAWL_FILE_NAMES = {
    TYPE_NEWS: {
        WEBSITE_EASTMONEY: r'EastMoneyNewsSpider-bak.json',
    },
    TYPE_GUBA: {
        WEBSITE_EASTMONEY: r'EastMoneyGubaSpider.json',
    },
    TYPE_GUBALIST: {
        WEBSITE_EASTMONEY: r'EastMoneyGubaListSpider-bak.json',
    },
}
for precess_type in CRAWL_FILE_NAMES:
    for website in CRAWL_FILE_NAMES[precess_type]:
        CRAWL_FILE_NAMES[precess_type][website] = os.path.join(DATA_DIR, CRAWL_FILE_NAMES[precess_type][website])

CRAWL_WEBSITES = {
    WEBSITE_EASTMONEY: r'http://www.eastmoney.com/',
}

# 预处理错误输出文件
WRONG_PREPROCESS_OUTPUT = os.path.join(OUTPUT_DIR, 'wrong_preprocess_output')

GIVEN_KEYWORD_FILES = {
    'wind_concept': r'concept_keywords.txt',
    'shenwan_1st_industry': r'shenwan_1st_industry.txt',
    'shenwan_2nd_industry': r'shenwan_2nd_industry.txt',
    'shenwan_3rd_industry': r'shenwan_3rd_industry.txt',
}

for key in GIVEN_KEYWORD_FILES:
    GIVEN_KEYWORD_FILES[key] = os.path.join(
        GIVEN_KEYWORD_DIR, GIVEN_KEYWORD_FILES[key])

MAX_INSERT_NUM = 500

PIPELINE_THREAD_SIZE = 1
