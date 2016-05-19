# -*- coding: utf-8 -*-

import os

# 处理类型
TYPE_NEWS = 'news'
TYPE_GUBA = 'guba'
TYPE_GUBALIST = 'guba_list'
TYPE_REPORT = 'report'
TYPE_KEYWORD = 'keyword'

# 爬取网站
WEBSITE_EASTMONEY = 'eastmoney'
WEBSITE_HEXUN = 'hexun'
WEBSITE_JINRONGJIE = 'jinrongjie'

# 程序运行的绝对路径
BASE_DIR = r'C:\Users\s_pankh\finance_news_analysis'
# 输出文件目录
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
# 爬虫文件目录
CRAWL_DIR = os.path.join(BASE_DIR, 'crawl_news')
# 数据文件目录
DATA_DIR = os.path.join(BASE_DIR, 'data')
# 预处理文件目录
PREPROCESS_DIR = os.path.join(BASE_DIR, 'preprocess')
# 文本分析文件目录
ANALYZE_DIR = os.path.join(BASE_DIR, 'analyze')
