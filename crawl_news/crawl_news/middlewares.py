# -*- coding: utf-8 -*-

import random
import base64
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from settings import USER_AGENTS

class RandomUserAgentMiddleWare(UserAgentMiddleware):
    '''Randomly rotate user agents based on a list of predefined ones'''
  
    def __init__(self, agent=""):
        self.user_agent = agent
  
    def process_request(self, request, spider):
        # print "**************************" + random.choice(USER_AGENTS)
        request.headers.setdefault('User-Agent', random.choice(USER_AGENTS))
        request.headers.setdefault('Accept', r'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
        request.headers.setdefault('Accept-Language', 'zh-CN,zh;q=0.8')
        request.headers.setdefault('Accept-Encoding', 'gzip, deflate, sdch')
        pass


'''        
class ProxyMiddleware(object):
    def process_request(self, request, spider):
        proxy = random.choice(PROXIES)
        if proxy['user_pass'] is not None:
            request.meta['proxy'] = "http://%s" % proxy['ip_port']
            encoded_user_pass = base64.encodestring(proxy['user_pass'])
            request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
            print "**************ProxyMiddleware have pass************" + proxy['ip_port']
        else:
            print "**************ProxyMiddleware no pass************" + proxy['ip_port']
            request.meta['proxy'] = "http://%s" % proxy['ip_port']
        pass
'''