# encoding=utf-8

import sys
import traceback
from Queue import Queue
from threading import Thread


class Handler(object):

    def __init__(self):
        pass

    def init_handler(self):
        pass

    def process_function(self, data_item):
        pass

    def handle_done(self):
        pass


class Worker(Thread):
    """ Thread excuting tasks from a given taks queue"""

    def __init__(self, handler, queue=None):
        Thread.__init__(self)
        self.__queue = queue
        self.__handler = None
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
        """线程即将退出前调用"""
        self.__handler.handle_done()
        pass

    def run(self):
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
        pass


class ThreadPool(object):
    """Pool of threads consuming tasks from a queue"""

    def __init__(self, num_threads):
        self.__workers = []
        self.__num_threads = num_threads
        self.__queue = Queue()
        self.__output = Queue()
        pass

    def add_process_data(self, data):
        """Add a task to the queue"""
        self.__queue.put(data)
        pass

    def wait_completion(self):
        """Wait for completion of all the tasks in the queue"""
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
