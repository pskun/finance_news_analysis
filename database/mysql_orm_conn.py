# -*- coding: utf-8 -*-


class MySQLORMConnection(object):

    # 构造函数
    def __init__(self, conn):
        self.__orm_session = conn
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

    def insertOne(self, object):
        self.__orm_session.add(object)
        self.__orm_session.commit()
        pass
    # End def insert

    def insertMany(self, object_list):
        self.__orm_session.bulk_save_objects(object_list)
        self.__orm_session.commit()
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
