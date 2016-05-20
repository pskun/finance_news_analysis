# encoding=utf-8

import psutil
import sys
import time
import traceback
from Queue import Queue
from threading import Thread


class Handler(object):
    ''' 每一个线程将调用一个Handler类 '''
    def __init__(self):
        pass

    def init_handler(self):
        ''' 回调函数: 线程启动后立马调用该方法 '''
        pass

    def process_function(self, data_item):
        ''' 回调函数: 从任务队列中取出一个数据进行处理 '''
        pass

    def clear_handler(self):
        ''' 回调函数: 线程结束前调用 '''
        pass


class Worker(Thread):
    """ Thread excuting tasks from a given taks queue"""

    def __init__(self, handler, queue=None):
        Thread.__init__(self)
        self.__queue = queue
        self.__daemon = True
        self.__handler = handler

    def setTaskQueue(self, queue):
        self.__queue = queue
        pass

    def startWorker(self):
        self.setDaemon(self.__daemon)
        self.start()
        pass

    def worker_done(self):
        """ 线程即将退出前调用 """
        self.__handler.clear_handler()
        pass

    def run(self):
        self.__handler.init_handler()
        while True:
            try:
                data = self.__queue.get()
                self.__handler.process_function(data)
            except:
                traceback.print_exc()
                sys.exit()
            self.__queue.task_done()
            pass
        self.worker_done()
        self.__handler.clear_handler()
        pass


class ThreadPool(object):
    """Pool of threads consuming tasks from a queue"""

    def __init__(self, num_threads):
        self.__workers = []
        self.__num_threads = num_threads
        self.__queue = Queue()
        self.__output = Queue()
        self.__push_count = 0
        pass

    def add_process_data(self, data):
        ''' 向队列中添加任务数据 '''
        self.__queue.put(data)
        # 如果生产者一直向队列中push数据，内存可能对撑爆
        # 所以需要wait，等待消费者把数据处理一部分再push
        self.__push_count += 1
        if self.__push_count >= 15000:
            mem = psutil.virtual_memory()
            if float(mem.used) / float(mem.total) > 0.80:
                time.sleep(8)
            self.__push_count = 0
        pass

    def wait_completion(self):
        """ 等待数据处理完成 """
        self.__queue.join()
        pass

    def add_handler(self, handler):
        if len(self.__workers) >= self.__num_threads:
            return False
        w = Worker(handler)
        w.setTaskQueue(self.__queue)
        # w.setDaemon(True)
        self.__workers.append(w)
        return True

    def produce_completed(self):
        """ 生成者消费者模式中，生产者把数据全局put进队列后调用"""
        # TODO
        pass

    def startAll(self):
        for t in self.__workers:
            t.startWorker()
        pass

    def shutdown(self):
        # TODO
        for t in self.__workers:
            pass
        pass
