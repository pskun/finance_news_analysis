# encoding=utf-8
import sys
import MySQLdb
from mysql_config import DATABASE_CONFIG


def init_mysql():
    '''
    初始化mysql的编码设置，设置成utf-8编码
    '''
    db = MySQLdb.connect(
        host=DATABASE_CONFIG['HOST'],
        user=DATABASE_CONFIG['USER'],
        passwd=DATABASE_CONFIG['PASSWORD'],
        db=DATABASE_CONFIG['DATABASE']
    )

    cursor = db.cursor()

    cursor.execute(
        "ALTER DATABASE `%s` CHARACTER SET 'utf8' COLLATE 'utf8_unicode_ci'"
        % DATABASE_CONFIG['DATABASE'])

    sql = """SELECT DISTINCT(table_name) \
            FROM information_schema.columns \
            WHERE table_schema = '%s'
            """ % DATABASE_CONFIG['DATABASE']
    cursor.execute(sql)

    results = cursor.fetchall()
    for row in results:
        sql = "ALTER TABLE `%s` \
            convert to character set DEFAULT COLLATE DEFAULT" % (row[0])
    cursor.execute(sql)
    db.close()
    sys.stderr.write("Init Mysql encoding done.\n")
    pass


if __name__ == '__main__':
    init_mysql()
    pass
