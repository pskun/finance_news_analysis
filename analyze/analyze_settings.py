# -*- coding: utf-8 -*-

import os

# 处理类型
TYPE_NEWS = 0x01
PROCESS_TYPE = TYPE_NEWS

# 项目默认编码字符集
DEFAULT_CAHRSET = 'utf-8'

# 程序运行的绝对路径
BASE_DIR = r'C:\Users\s_pankh\finance_news_analysis'
OUTPUT_DIR = os.path.join(BASE_DIR, r'output')
CRAWL_DIR = os.path.join(BASE_DIR, r'crawl_news')
ANALYZE_DIR = os.path.join(BASE_DIR, r'analyze')
ANALYZE_DATA_DIR = os.path.join(ANALYZE_DIR, 'pre_data')
GIVEN_KEYWORD_DIR = os.path.join(ANALYZE_DATA_DIR, 'given_keywords')

# 数据预处理文件的路径
CRAWL_FILE_NAMES = {
    u"eastmoney": r'EastMoneyNewsSpider-bak.json',
    u"guba": r'EastMoneyGubaSpider.json',
}
for key in CRAWL_FILE_NAMES:
    CRAWL_FILE_NAMES[key] = os.path.join(CRAWL_DIR, CRAWL_FILE_NAMES[key])

CRAWL_WEBSITES = {
    u"eastmoney": r'http://www.eastmoney.com/',
}

# 预处理错误输出文件
WRONG_PREPROCESS_OUTPUT = os.path.join(OUTPUT_DIR, 'wrong_preprocess_output')

# 文本分析相关路径
STOPWORDS_FILE = os.path.join(ANALYZE_DATA_DIR, r'stopwords.txt')
IDF_FILE = os.path.join(ANALYZE_DATA_DIR, "idf.txt")

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
