# encoding=utf-8

import sys
import traceback
import multiprocessing

class ProcessHandler(object):
    ''' 每一个线程将调用一个Handler类 '''
    def __init__(self):
        pass

    def before_thread_start(self):
        ''' 回调函数: 线程启动前调用 '''
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


def process_worker(handler, handle_queue, output_queue):
    handler.init_handler()
    while True:
        try:
            data = queue.get()
            process_data = handler.process_function(data)
            if process_data is not None and output_queue is not None:
                output_queue.put(process_data)
        except:
            traceback.print_exc()
        queue.task_done()
    handler.clear_handler()
    pass


def process_output(handler, output_queue):
    handler.init_handler()
    while True:
        try:
            data = queue.get()
            handler.process_function(data)
        except:
            traceback.print_exc()
        queue.task_done()
    handler.clear_handler()
    pass


class ProcessPool(object):
    """Pool of threads consuming tasks from a queue"""
    def __init__(self, num_processes, handle_queue_size, output_queue_size=0):
        self.__workers = []
        self.__num_processes = num_processes
        self.__queue = multiprocessing.Queue(handle_queue_size)
        if output_queue_size != 0:
            self.__output = multiprocessing.Queue(output_queue_size)
        else:
            self.__output = None
        pass

    def add_process_data(self, data):
        ''' 向队列中添加任务数据 '''
        self.__queue.put(data)
        pass

    def wait_completion(self):
        """ 等待数据处理完成 """
        self.__queue.join()
        pass

    def add_handler(self, process_handler, output_handler):
        for i in range(len(self.__num_processes)):
            process = multiprocessing.Process(
                target=process_worker,
                args=(process_handler, self.__queue, self.__output))
            self.__workers.append(process)
        output_process = multiprocessing.Process(
            target=process_output,
            args=(output_handler, self.__output))
        self.__workers.append(output_process)
        pass

    def startAll(self):
        for process in self.__workers:
            process.start()
            process.join()
        pass

    def shutdown(self):
        # TODO
        for t in self.__workers:
            pass
        pass
