# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import json
import codecs
import traceback

from pybloom import BloomFilter

from scrapy import signals
from scrapy.exceptions import DropItem
from scrapy.exceptions import CloseSpider


class CrawlPipeline(object):

    def __init__(self):
        self.files = {}
        self.bloom_filter = None

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        file = codecs.open('%s.json' % spider.name, 'a+b', 'utf-8', 'ignore')
        self.files[spider.name] = file

    def spider_closed(self, spider):
        file = self.files.pop(spider.name)
        file.close()
        pass

    def init_bloom_filter(self, spider_name):
        self.bloom_file = '%s.bloom' % spider_name
        if os.path.exists(self.bloom_file):
            self.bloom_filter = \
                BloomFilter.fromfile(open(self.bloom_file, 'r'))
        else:
            self.bloom_filter = \
                BloomFilter(capacity=100000000, error_rate=0.001)
        pass

    def dump_bloom_filter(self, spider_name):
        self.bloom_file = '%s.bloom' % spider_name
        self.bloom_filter.tofile(open(self.bloom_file, 'w'))
        pass

    def write_to_file(self, item, spider_name):
        try:
            # dumps 并输出
            line = json.dumps(
                dict(item), ensure_ascii=False, sort_keys=True) + '\n'
            line = line.replace(u'\xa0', u' ')
            self.files[spider_name].write(line)
        except:
            traceback.print_exc()
            pass
        return item

    def process_hexun_yanbao_item(self, item, spider):
        self.write_to_file(item, spider.name)
        pass

    def process_eastmoney_newsguba_item(self, item, spider):
        if 'title' not in item or 'a_post_time' not in item:
            raise DropItem(u'缺失title或者post_time')
        elif item['title'] == "" or item['a_post_time'] == "":
            raise DropItem(u'缺失title或者post_time')
        # self.exporter.export_item(item)
        # 把换行符替换
        if 'content' in item:
            item['content'] = "".join(item['content'].split('\n'))
        self.write_to_file(item, spider.name)
        pass

    def process_eastmoney_gubalist_item(self, item, spider):
        status = item.get('status')
        if status is not None and status != 200:
            self.error_count += 1
            if self.error_count * 5 > self.success_count:
                raise CloseSpider(
                    'too many error occurred, shutdown gracefully.')
            return item

        if 'ticker_id' not in item or item['ticker_id'] == "":
            raise DropItem('缺失ticker_id')
        self.write_to_file(item, spider.name)
        pass

    def process_item(self, item, spider):
        '''
        if item_id in self.bloom_filter:
            return None
        self.bloom_filter.add(item_id)
        '''
        if spider.name == 'HexunResearchPaperSpider':
            return self.process_hexun_yanbao_item(item, spider)
        elif spider.name == 'EastMoneyNewsSpider':
            return self.process_eastmoney_newsguba_item(item, spider)
        elif spider.name == 'EastMoneyGubaSpider':
            return self.process_eastmoney_newsguba_item(item, spider)
        pass
