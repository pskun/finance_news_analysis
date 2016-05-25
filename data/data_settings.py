# -*- coding: utf-8 -*-

import os

from universe_settings import *

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

for precess_type in CRAWL_FILE_NAMES:
    for website in CRAWL_FILE_NAMES[precess_type]:
        CRAWL_FILE_NAMES[precess_type][website] = os.path.join(
            DATA_DIR, CRAWL_FILE_NAMES[precess_type][website])
