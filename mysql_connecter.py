# -*- coding:utf-8 -*-  
"""
--------------------------------
    @Author: Dyson
    @Contact: Weaver1990@163.com
    @file: mysql_connecter.py
    @time: 2017/3/15 14:23
    @info: 个人常用代码
--------------------------------
"""

import MySQLdb as mysql
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import set_log

import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.orm

log_obj = set_log.Logger('mysql_connecter.log', set_log.logging.WARNING,
                         set_log.logging.DEBUG)
log_obj.cleanup('mysql_connecter.log', if_cleanup=True)  # 是否需要在每次运行程序前清空Log文件


class mysql_connecter(object):

    def __init__(self):
        pass
    
    def connect(self,sql,args=None,ip='192.168.1.124',user='user2',password = '123456', dbname = 'data_statistics', charset='utf8'):
        """
        :return: list
        """
        con = ''
        try:
            con = mysql.connect(ip,user,password,dbname,charset = charset)
            cur = con.cursor()
            
            # 多条SQL语句的话，循环执行
            if isinstance(sql,list):
                for sql0 in sql:
                    cur.execute(sql0)
            else:
                cur.execute(sql,args)
                
            data = cur.fetchall()
            con.commit()
            # data.decode('uft8').encode('gbk')
        finally:
            if con:
                #无论如何，连接记得关闭
                con.close()
                
        return [list(t) for t in data]

    def connect0(self,sql,args=None,ip='192.168.1.124',user='user2',password = '123456', dbname = 'data_statistics', charset='utf8'):
        # 初始化数据库连接:
        # '数据库类型+数据库驱动名称://用户名:口令@机器地址:端口号/数据库名'
        db_connect_str = 'mysql+pymysql://{}:{}@{}/{}?charset={}'.format(user,password,ip,dbname,charset)
        engine = sqlalchemy.create_engine(db_connect_str)
        # 创建DBSession类型:
        DB_session = sqlalchemy.orm.sessionmaker(bind=engine)

        return DB_session()
        
if __name__ == '__main__':
    mysql_connecter = mysql_connecter()
    print mysql_connecter.connect('select * from actor', dbname = 'sakila')
    
"""
mysql -P 3306 -h rm-bp1ks9kestihy4wy1o.mysql.rds.aliyuncs.com -u test1 -p
"""