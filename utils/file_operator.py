# -*- coding: utf-8 -*-

'''
模式      描述
r       以读方式打开文件，可读取文件信息.文件必须已存在
w       以写方式打开文件，可向文件写入信息。存在则清空，不存在创建
a       以追加方式打开文件，文件指针自动移到文件尾。追加
r+      以读写方式打开文件，可对文件进行读和写操作。
w+      消除文件内容，然后以读写方式打开文件。
a+      以读写方式打开文件，并把文件指针移到文件尾。
b       以二进制模式打开文件，而不是以文本模式。该模式只对Windows或Dos有效，类Unix的文件是用二进制模式进行操作的

U      通用换行符支持，任何系统下的文件, 不管换行符是什么, 使用U模式打开时, 换行符都会被替换为NEWLINE(\n)
'''

import codecs
import threading


class FileMultiReadWrite(object):
    ''' 多线程读写文件 '''

    def __init__(self, filename, rb_mode):
        self.filename = filename
        self.file = codecs.open(self.filename, rb_mode,
                                'utf-8', errors='ignore')
        self.mutex = threading.Lock()
        pass

    def lock(self):
        if self.mutex is not None:
            self.mutex.acquire()
        pass

    def unlock(self):
        if self.mutex is not None:
            self.mutex.release()
        pass

    def write(self, line):
        ''' 向文件中写 '''
        self.lock()
        self.file.write(line)
        self.unlock()

    def read(self):
        ''' 从文件中读 '''
        self.lock()
        line = self.file.readline()
        if line == "":
            line = None
        self.unlock()
        return line

    def close(self):
        self.file.close()
        pass
