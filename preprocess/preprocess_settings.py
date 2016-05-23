# -*- coding: utf-8 -*-

import os

from universe_settings import *

''' 需要修改的部分 '''
# 新增一个预处理Handler的时候需要加入
CRAWLER_TYPE_HANDLER_DICT = {
    TYPE_GUBALIST: 'GubaPreprocessHandler',
    TYPE_GUBA: 'GubaPreprocessHandler',
    TYPE_NEWS: 'NewsPreprocessHandler',
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
