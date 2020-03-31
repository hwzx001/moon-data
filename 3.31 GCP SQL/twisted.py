# 用twisted库将数据进行异步插入到数据库
 
import pymysql
from twisted.enterprise import adbapi
from twisted.internet import reactor
 

settings={
    'MYSQL_HOST':"35.224.151.74",
    'MYSQL_USER':"root",
    'MYSQL_PASSWORD':"******",
    'MYSQL_DBNAME':"ShopList",
}
 
class MysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool
 
    @classmethod
    def from_settings(cls, settings):

        # 需要在setting中设置数据库配置参数
        dbparms = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWORD'],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True,
        )
        # 连接ConnectionPool（使用MySQLdb连接，或者pymysql）
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)  # **让参数变成可变化参数
        return cls(dbpool)   # 返回实例化对象
 
 
    def process_item(self, item, spider):
        # 使用twisted将MySQL插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        # 添加异常处理
        query.addCallback(self.handle_error)
 
 
    def handle_error(self, failure):
        # 处理异步插入时的异常
        print(failure)
 
 
    def do_insert(self, cursor, item):
        # 执行具体的插入
        insert_sql = """
                    insert into jobbole_artitle(name, base_url, date, comment)
                    VALUES (%s, %s, %s, %s)
                """
        cursor.execute(insert_sql, (item['name'], item['base_url'], item['date'], item['coment'],))
