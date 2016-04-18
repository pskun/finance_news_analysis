# encoding=utf-8

import sys
import traceback
from Queue import Queue
from threading import Thread


class Worker(Thread):
    """ Thread excuting tasks from a given taks queue"""

    def __init__(self, handler):
        Thread.__init__(self)
        self.__queue = None
        self.__handler = None
        self.__daemon = True
        self.__handler = handler

    def setTaskQueue(self, queue):
        self.__queue = queue

    def startWorker(self):
        self.start()

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


class ThreadPool(object):
    """Pool of threads consuming tasks from a queue"""

    def __init__(self, num_threads):
        self.__workers = []
        self.__num_threads = num_threads
        self.__queue = Queue()
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

    def startAll(self):
        for t in self.__workers:
            t.startWorker()
        pass

    def shutdown(self):
        # TODO
        for t in self.__workers:
            pass
        pass
