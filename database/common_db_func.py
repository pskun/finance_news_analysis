# -*- coding: utf-8 -*-

import mysql_config


def query_table_count(db_session, table):
    ''' 获取某张表的行数 '''
    count = db_session.execute("select count(*) from %s" % table)
    count = count[0]['count(*)']
    return count


def query_web_id(db_session, website_name):
    ''' 通过网站名称查找网站id '''
    web_id = db_session.select(
        mysql_config.TABLE_WEB,
        "web_name=\"%s\"" % website_name,
        False,
        "web_id")
    return web_id


def insert_new_website(db_session, website_name, web_address):
    ''' 插入一个新的网站名称 '''
    web_id = db_session.insertOne(
        mysql_config.TABLE_WEB,
        web_name=website_name,
        web_address=web_address)
    return web_id
    pass


def query_file_id(db_session, filename):
    ''' 通过文件名查找文件id '''
    pass


def insert_new_filename(db_session, web_id, filename):
    ''' 插入一个新的文件名称 '''
    news_file_id = db_session.insertOne(
        mysql_config.TABLE_NEWS_FILE,
        web_id=web_id,
        file_storage_location=filename,
        file_name=filename.split('\\')[-1])
    return news_file_id
