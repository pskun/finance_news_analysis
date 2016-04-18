# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
import time, datetime
import traceback

from scrapy import signals
from scrapy.exporters import JsonLinesItemExporter
from crawl_news.items import EastMoneyNewsItem
from crawl_news.items import EastMoneyGubaItem
from scrapy.exceptions import DropItem
from scrapy.exceptions import CloseSpider

class CrawlNewsPipeline(object):

    def __init__(self):
        self.files = {}
        self.error_count = 0
        self.success_count = 0
        
    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline    
    
    def spider_opened(self, spider):
        
        news_file = codecs.open('%s.json' % "EastMoneyNewsSpider", 'a+b', 'utf-8', 'ignore')
        guba_file = codecs.open('%s.json' % "EastMoneyGubaSpider", 'a+b', 'utf-8', 'ignore')
        error_url_file = codecs.open('%s_error_url.txt' % spider.name, 'wb', 'utf-8', 'ignore')
        '''
        news_file = open('%s.json' % "EastMoneyNewsSpider", 'a+b')
        guba_file = open('%s.json' % "EastMoneyGubaSpider", 'a+b')
        '''
        self.files["EastMoneyNewsSpider"] = news_file
        self.files["EastMoneyGubaSpider"] = guba_file
        self.files["EastMoneyErrorUrls"] = error_url_file
        '''
        self.exporter = JsonLinesItemExporter(file)
        self.exporter.start_exporting()
        '''

    def spider_closed(self, spider):
        # self.exporter.finish_exporting()
        #file = self.files.pop(spider)
        news_file = self.files.pop("EastMoneyNewsSpider")
        news_file.close()
        guba_file = self.files.pop("EastMoneyGubaSpider")
        guba_file.close()
        error_url_file = self.files.pop("EastMoneyErrorUrls")
        error_url_file.close()
        
    def process_item(self, item, spider):
        status = item.get('status')
        if status is not None and status != 200:
            line = item['url'] + '\t' + str(status) + '\n'
            self.files["EastMoneyErrorUrls"].write(line)
            self.error_count += 1
            if self.error_count * 5 > self.success_count:
                raise CloseSpider('too many error occurred, shutdown gracefully.')
            return item
        
        if 'title' not in item or 'a_post_time' not in item:
            raise DropItem('缺失title或者post_time')
        elif item['title'] == "" or item['a_post_time'] == "":
            raise DropItem('缺失title或者post_time')
        # self.exporter.export_item(item)
        # 把换行符替换
        if 'content' in item:
            item['content'] = "".join(item['content'].split('\n'))
        try:
            # dumps 并输出
            line = json.dumps(dict(item), ensure_ascii=False, sort_keys=True) + '\n'
            #line = line.encode('utf-8')
            #print line
            if isinstance(item, EastMoneyNewsItem):
                #self.files["EastMoneyNewsSpider"].write(line.decode('unicode_escape'))
                self.files["EastMoneyNewsSpider"].write(line)
            elif isinstance(item, EastMoneyGubaItem):
                #self.files["EastMoneyGubaSpider"].write(line.decode('unicode_escape'))
                self.files["EastMoneyGubaSpider"].write(line)
        except:
            traceback.print_exc()
            pass
        self.success_count += 1
        return item
