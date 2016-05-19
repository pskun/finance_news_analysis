# encoding=utf-8

import sys
import MySQLdb
from MySQLdb.cursors import DictCursor
from DBUtils.PooledDB import PooledDB

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from mysql_config import DATABASE_CONFIG
from mysql_connection import MySQLConnection
from orm_conn import ORMConnection


def singleton(cls, *args, **kw):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton


@singleton
class SqlAlchemyPool(object):

    def __init__(self, min_conn=2):
        self.__host = DATABASE_CONFIG['HOST']
        self.__user = DATABASE_CONFIG['USER']
        self.__password = DATABASE_CONFIG['PASSWORD']
        self.__database = DATABASE_CONFIG['DATABASE']
        conn_info = "mysql://" + self.__user + ":" + \
            self.__password + "@" + self.__host + "/" + self.__database
        self.__engine = create_engine(
            conn_info, encoding='utf-8',
            pool_size=20, max_overflow=0, convert_unicode=True)
        pass

    def getConnection(self):
        # 创建一个自定义了的 Session类
        Session = sessionmaker()
        # 将创建的数据库连接关联到这个session
        Session.configure(bind=self.__engine)
        session = Session()
        wraped_conn = ORMConnection(session)
        return wraped_conn
        pass


@singleton
class MySQLPool(object):
    ''' Python Class for connecting with MySQL server \
    and accelerate development project using SqlAlchemy'''

    __instance = None

    @staticmethod
    def getSingleConnection():
        conn = MySQLdb.connect(
            DATABASE_CONFIG['HOST'],
            DATABASE_CONFIG['USER'],
            DATABASE_CONFIG['PASSWORD'],
            DATABASE_CONFIG['DATABASE'],
            charset='utf8',
            use_unicode=True,
            cursorclass=DictCursor
        )
        wraped_conn = MySQLConnection(conn)
        return wraped_conn

    def __init__(self, min_conn=2):
        self.__host = DATABASE_CONFIG['HOST']
        self.__user = DATABASE_CONFIG['USER']
        self.__password = DATABASE_CONFIG['PASSWORD']
        self.__database = DATABASE_CONFIG['DATABASE']
        self.__min_conn = min_conn
        self.__pool = PooledDB(
            MySQLdb,
            self.__min_conn,
            host=self.__host,
            user=self.__user,
            passwd=self.__password,
            db=self.__database,
            charset='utf8',
            use_unicode=True,
            cursorclass=DictCursor)
    # End def __init__

    def getConnection(self):
        try:
            conn = self.__pool.connection()
            wraped_conn = MySQLConnection(conn)
            return wraped_conn
        except MySQLdb.Error as e:
            sys.stderr.write("Error %d: %s\n" % (e.args[0], e.args[1]))
            return None
    # End def __open
# End class
