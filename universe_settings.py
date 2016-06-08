# -*- coding: utf-8 -*-

import os

'''
######################
全局性设置
######################
'''

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
BASE_DIR = os.path.split(os.path.realpath(__file__))[0]
# 输出文件目录
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
# 爬虫文件目录
CRAWL_DIR = os.path.join(BASE_DIR, 'crawler')
# 数据文件目录
DATA_DIR = os.path.join(BASE_DIR, 'data')
# 预处理文件目录
PREPROCESS_DIR = os.path.join(BASE_DIR, 'preprocess')
# 文本分析文件目录
ANALYZE_DIR = os.path.join(BASE_DIR, 'analyze')

'''
######################
数据文件设置
######################
'''

# 数据预处理文件的路径
# 新添加一个爬取文件的时候需要加入
CRAWL_FILE_NAMES = {
    TYPE_NEWS: {
        WEBSITE_EASTMONEY: r'EastMoneyNewsSpider.json',
<<<<<<< HEAD
        WEBSITE_JINRONGJIE: r'JinrongjieNewsSpider.json',
=======
        WEBSITE_HEXUN: r'HexunNewsSpider.json'
>>>>>>> bd5d4ab35d81ac5f3e27ecd1873596b6cbd1a902
    },
    TYPE_GUBA: {
        WEBSITE_EASTMONEY: r'EastMoneyGubaSpider.json',
    },
    TYPE_GUBALIST: {
        WEBSITE_EASTMONEY: r'EastMoneyGubaListSpider.json',
    },
    TYPE_REPORT: {
        WEBSITE_HEXUN: r'HexunResearchPaperSpider.json',
    }
}

# 新加入一个爬取网站时需要加入
CRAWL_WEBSITES = {
    WEBSITE_EASTMONEY: r'http://www.eastmoney.com/',
    WEBSITE_HEXUN: r'http://www.hexun.com/',
    WEBSITE_JINRONGJIE: r'http://www.jrj.com.cn/',
}

for precess_type in CRAWL_FILE_NAMES:
    for website in CRAWL_FILE_NAMES[precess_type]:
        CRAWL_FILE_NAMES[precess_type][website] = os.path.join(
            DATA_DIR, CRAWL_FILE_NAMES[precess_type][website])
