# -*- coding: utf-8 -*-


class MySQLORMConnection(object):

    # 构造函数
    def __init__(self, conn):
        pass
    # End def __init__

    def close(self):
        pass

    def execute(self, sql):
        pass

    def beginTransaction(self):
        pass

    def endTransaction(self, option='commit'):
        pass

    def insertOne(self, table, *args, **kwargs):
        pass
    # End def insert

    def insertMany(self, table, values_list=None, *args):
        pass

    def select(self, table, where=None, *args, **kwargs):
        pass
    # End def select

    def update(self, table, where=None, *args, **kwargs):
        pass
    # End function update

    def delete(self, table, where=None, *args):
        pass
    # End def delete

    def select_advanced(self, sql, *args):
        pass
    # End def select_advanced
