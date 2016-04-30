# -*- coding: utf-8 -*-

import os
import sys
import csv
import traceback
from string import Template

from tonglian_data_api import Client

TOKEN = '0750879ead818fbb5f3bce241340e5b82c0d64c5b613b1b3f83a3e3bfa6977a5'

WORK_DIR = r'C:\Users\s_pankh\news_data'
os.chdir(WORK_DIR)

client = Client()
client.init(TOKEN)

def getData(url, file_name=None):
    code, result = client.getData(url)
    if code == 200:
        if file_name is not None:
            file_object = open(file_name, 'w')
            file_object.write(result)
            file_object.close()
            return code
        else:
            return result
    else:
        sys.stderr.write("return code: %d\n" % (code))
    pass

def dealCsvData(data):
    if data is None:
        return None, None
    pos = data.index('\n')
    header = data[:pos]
    body = data[pos+1:]
    if header is None or body is None:
        sys.stderr.write('deal csv data failed.\n')
        sys.stderr.write(data + '\n')
        return None, None
    return header, body
    
def getEquBasic():
    url = '/api/equity/getEqu.csv?field=&ticker=&secID=&equTypeCD=A&listStatusCD='
    file_name = "stock_basic.csv"
    getData(url, file_name)

# 获取指数基本情况   
def getIndexBasic():
    url = '/api/idx/getIdx.csv?field=&ticker=&secID='
    file_name = 'index_basic.csv'
    getData(url, file_name)

# 获取某个股票的所有交易日数据    
def getIndexTradeDay(ticker):
    t = Template('/api/market/getMktIdxd.csv?field=&beginDate=&endDate=&indexID=&ticker=$tick&tradeDate=')
    url = t.substitute({"tick": ticker})
    file_name = 'index_daily.csv'
    getData(url, file_name)
    
def getSocialDataXQ(tickerList = None):
    if tickerList is None:
        #url = '/api/subject/getSocialDataXQ.csv?field=&ticker=&beginDate=20140101&endDate='
        url = '/api/subject/getSocialDataXQByTicker.csv?field=&ticker=000001'
        file_name = 'social_xq_000001.csv'
        getData(url, file_name)
    else:
        hasHeader = False
        t = Template('/api/subject/getSocialDataXQ.csv?field=&ticker=$tick&beginDate=20140101&endDate=')
        for ticker in tickerList:
            url = t.substitute({"tick": ticker})
            res = getData(url)
            header, body = dealCsvData(res)
            if hasHeader is False:
                print header
                hasHeader = True
            sys.stdout.write(body)
    pass

def getSocialDataGuba(tickerList = None):
    if tickerList is None:
        url = '/api/subject/getSocialDataGuba.csv?field=&ticker=&beginDate=&endDate='
        file_name = 'social_guba.csv'
        getData(url, file_name)
    else:
        hasHeader = False
        t = Template('/api/subject/getSocialDataGuba.csv?field=&ticker=$tick&beginDate=&endDate=')
        for ticker in tickerList:
            url = t.substitute({"tick": ticker})
            res = getData(url)
            header, body = dealCsvData(res)
            if hasHeader is False:
                print header
                hasHeader = True
            sys.stdout.write(body)
    pass

# 按天获取证券相关的新闻正文  
def getNewsContentByTime(dateList):
    NEWS_CONTENT_DIR = 'news_content_by_date'
    if not os.path.exists(NEWS_CONTENT_DIR):
        os.makedirs(NEWS_CONTENT_DIR)
    t = Template('/api/subject/getNewsContentByTime.csv?field=&beginTime=&endTime=&newsPublishDate=$date')
    for d in dateList:
        url = t.substitute({"date": d})
        # print url
        file_name = os.path.join(NEWS_CONTENT_DIR, d+'.csv')
        res = getData(url, file_name)
        if res != 200:
            sys.stderr.write("date %s is None.\n" % d)
            continue
        sys.stderr.write("get news data of %s done.\n" % d)

def getNewsInfoByTimeAndSite(dateList):
    NEWS_CONTENT_DIR = 'news_content_by_site'
    if not os.path.exists(NEWS_CONTENT_DIR):
        os.makedirs(NEWS_CONTENT_DIR)
    t = Template('/api/subject/getNewsInfoByTimeAndSite.csv?field=&beginTime=&endTime=&newsPublishDate=$date&newsPublishSite=和讯网')
    for d in dateList:
        url = t.substitute({"date": d})
        # print url
        file_name = os.path.join(NEWS_CONTENT_DIR, d+'.csv')
        res = getData(url, file_name)
        if res != 200:
            sys.stderr.write("date %s is None.\n" % d)
            continue
        sys.stderr.write("get news data of %s done.\n" % d)
        
# 获取证券关联的新闻
def getNewsByTickers(tickerList):
    hasHeader = False
    t = Template('/api/subject/getNewsByTickers.csv?field=&secID=&exchangeCD=&ticker=$tick&secShortName=&beginDate=20140101&endDate=')
    for ticker in tickerList:
        url = t.substitute({"tick": ticker})
        res = getData(url)
        header, body = dealCsvData(res)
        if header is None or body is None:
            sys.stderr.write('get news by ticker %s failed.\n' % ticker)
            continue
        if hasHeader is False:
            print header
            hasHeader = True
        sys.stdout.write(body)
    pass

# 获取证券关联的新闻热度指数
def getNewsHeatIndex():
    hasHeader = False
    t = Template('/api/subject/getNewsHeatIndex.csv?field=&exchangeCD=&ticker=$tick&secShortName=&beginDate=20140101&endDate=')
    for ticker in tickerList:
        url = t.substitute({"tick": ticker})
        res = getData(url)
        header, body = dealCsvData(res)
        if hasHeader is False:
            print header
            hasHeader = True
        sys.stdout.write(body)
    pass

# 获取新闻来源
def getNewsPublishSite():
    url = '/api/subject/getNewsPublishSite.csv?field='
    file_name = 'news_pub_site.csv'
    getData(url, file_name)
    
def getTickerList():
    tickerList = []
    stock_basic_file = "stock_basic.csv"
    f = file(stock_basic_file, 'r')
    next(f)
    reader = csv.reader(f)
    for row in reader:
        tickerList.append(row[1])
    return tickerList
    
def getSecIdList():
    secIdList = []
    stock_basic_file = "stock_basic.csv"
    f = file(stock_basic_file, 'r')
    next(f)
    reader = csv.reader(f)
    for row in reader:
        secIdList.append(row[0])
    return secIdList

#生成20140101之后的天数    
def generateDate():
    xq_000001 = "social_xq_000001.csv"
    f = file(xq_000001, 'r')
    next(f)
    reader = csv.reader(f)
    for row in reader:
        date = (row[1].split(" "))[0]
        year, month, day = date.split('-')
        print "%s%s%s" % (year, month, day)
    pass
        
# 获取20140101之后的日期        
def getDate():
    dateList = []
    date_from_20140101 = "date_from_20140101.csv"
    f = open(date_from_20140101, 'r')
    for line in f:
        dateList.append(line.strip())
    return dateList

    
if __name__ == "__main__":
    try:
        secIdList = getSecIdList()
        tickerList = getTickerList()
        #generateDate()
        dateList = getDate()
        #getSocialDataGuba(tickerList)
        getNewsContentByTime(dateList)
        #getNewsInfoByTimeAndSite(dateList)
        #getNewsByTickers(tickerList)
        #getNewsPublishSite()
    except Exception, e:
        traceback.print_exc()
        raise e
