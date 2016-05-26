# -*- coding: utf-8 -*-

'''
增量爬取日志文件格式
2016-05-12 00:00:00\tstart crawl
2016-05-12 01:00:00\tend crawl
crawl count: 10000
update to: 20160512

注意: 增量爬虫部分尚未完成
'''

import os
from datetime import datetime


def parse_incremental_logging(filename=None):
    pass


def get_last_crawl_date(filename=None):
    if not os.path.exists(filename):
        return None
    f = open(filename, 'r')
    last_line = f.readlines()[-1]
    update_time = last_line.strip().split(' ')[1]
    last_date = datetime.strptime(update_time, "%Y%m%d")
    return last_date


def log_spider(filename=None, start_time, end_time, crawl_count):
    if not os.path.exists(filename):
        return None
    f = open(filename, 'a+')
    f.write(str(start_time) + " start crawl\n")
    f.write(str(end_time) + " end crawl\n")
    f.write("crawl_count: " + str(crawl_count))
    f.write("update to: " + start_time.strftime("%Y%m%d"))
    f.close()
