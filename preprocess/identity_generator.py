# -*- coding: utf-8 -*-


class IdentityGenerator(object):

    def __init__(self, initial_counter=1, mutex=None):
        self.id_counter = initial_counter
        self.mutex = mutex
        pass

    def set_initial_counter(self, initial_counter):
        self.id_counter = initial_counter
        pass

    def lock(self):
        if self.mutex is not None:
            self.mutex.acquire()
        pass

    def unlock(self):
        if self.mutex is not None:
            self.mutex.release()
        pass

    def generate_news_id(self):
        ''' 生成插入数据库中的新闻id
            当前规则: "news" + counter
        '''
        self.lock()
        news_id = "news" + str(self.id_counter)
        self.id_counter += 1
        self.unlock()
        return news_id

    def generate_guba_id(self, website_name):
        ''' 生成插入数据库中的股吧id
            当前规则: website_name + counter
        '''
        self.lock()
        guba_id = website_name + str(self.id_counter)
        self.id_counter += 1
        self.unlock()
        return guba_id
