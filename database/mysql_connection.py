# -*- coding: utf-8 -*-

import traceback
from collections import OrderedDict


class MySQLConnection(object):

    # 构造函数
    def __init__(self, conn):
        self.__conn = conn
        self.__session = self.__conn.cursor()
        self.__session.execute('SET NAMES utf8;')
        self.__session.execute('SET CHARACTER SET utf8;')
        self.__session.execute('SET character_set_connection = utf8;')
        pass
    # End def __init__

    def close(self):
        try:
            self.__session.close()
            self.__conn.close()
        except:
            traceback.print_exc()
        pass

    def execute(self, sql):
        self.__conn.execute(sql)
        pass

    def beginTransaction(self):
        """
        @summary: 开始事务
        """
        self.__conn.autocommit(0)
        pass

    def endTransaction(self, option='commit'):
        """
        @summary: 结束事务
        """
        if option == 'commit':
            self.__conn.commit()
        else:
            self.__conn.rollback()
        pass

    def insertOne(self, table, *args, **kwargs):
        values = None
        query = "INSERT INTO %s " % table
        if kwargs:
            keys = tuple(kwargs.keys())
            values = tuple(kwargs.values())
            query += "(" + ",".join(["`%s`"] * len(keys)) % keys + \
                ") VALUES (" + ",".join(["%s"] * len(values)) + ")"
        elif args:
            values = args
            query += " VALUES(" + ",".join(["%s"] * len(values)) + ")"
        # print query
        self.__session.execute(query, values)
        return self.__session.lastrowid
    # End def insert

    def insertMany(self, table, values_list=None, *args):
        query = "INSERT INTO %s " % table
        if args:
            keys = args
            query += "(" + ",".join(["`%s`"] * len(keys)) % keys + ")"
            query += " VALUES(" + ",".join(["%s"] * len(keys)) + ")"
        print query
        self.__session.executemany(query, values_list)
        pass

    def select(self, table, where=None, *args, **kwargs):
        result = None
        query = 'SELECT '
        keys = args
        values = tuple(kwargs.values())
        l = len(keys) - 1

        for i, key in enumerate(keys):
            query += "`" + key + "`"
            if i < l:
                query += ","
        # End for keys

        query += ' FROM %s' % table

        if where:
            query += " WHERE %s" % where
        # End if where
        print query
        self.__session.execute(query, values)
        number_rows = self.__session.rowcount
        number_columns = len(self.__session.description)
        if number_rows >= 1 and number_columns > 1:
            result = [item for item in self.__session.fetchall()]
        else:
            result = [item.values()[0] for item in self.__session.fetchall()]
            print result
        return result
    # End def select

    def update(self, table, where=None, *args, **kwargs):
        query = "UPDATE %s SET " % table
        keys = kwargs.keys()
        values = tuple(kwargs.values()) + tuple(args)
        l = len(keys) - 1
        for i, key in enumerate(keys):
            query += "`" + key + "` = %s"
            if i < l:
                query += ","
            # End if i less than 1
        # End for keys
        query += " WHERE %s" % where

        self.__session.execute(query, values)

        # Obtain rows affected
        update_rows = self.__session.rowcount

        return update_rows
    # End function update

    def delete(self, table, where=None, *args):
        query = "DELETE FROM %s" % table
        if where:
            query += ' WHERE %s' % where

        values = tuple(args)

        self.__session.execute(query, values)

        # Obtain rows affected
        delete_rows = self.__session.rowcount

        return delete_rows
    # End def delete

    def select_advanced(self, sql, *args):
        od = OrderedDict(args)
        query = sql
        values = tuple(od.values())
        self.__session.execute(query, values)
        number_rows = self.__session.rowcount
        number_columns = len(self.__session.description)

        if number_rows >= 1 and number_columns > 1:
            result = [item for item in self.__session.fetchall()]
        else:
            result = [item[0] for item in self.__session.fetchall()]
        return result
    # End def select_advanced
