# -*- coding: utf-8 -*-
__author__ = "yanhe@chinasofti.com"

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

# 导入MySQL模块
import pymysql

# DoubanmoviePipeline类，继承Object类
# 读取爬虫采集到的MySQL数据库，批量插入到数据库中
class DoubanmoviePipeline(object):
    
	# process_item()函数，将获取到的数据添加到MySQL数据库crawl的数据表movieinfo中
    def process_item(self, item, spider):
        print("--> MySQL: insert to db...")
        # 获取MySQL数据库的链接对象
        db = pymysql.connect(host='localhost',user='root',passwd='1234',db='crawl',port=3306, use_unicode=True, charset="utf8")
        try:           
            # 获取cur操作游标对象
            cur = db.cursor()
            # 设置cur操作游标字符集为utf-8
            cur.execute('SET NAMES utf8;')  
            cur.execute('SET CHARACTER SET utf8;')  
            cur.execute('SET character_set_connection=utf8;') 
                
            # 获取电影排名
            movie_rank = item['rank'][0]
            print("MySQLDB--> %d" % int(movie_rank))

            # 获取电影名称
            movie_title = item['title'][0]
            print("MySQLDB--> %s" % movie_title)
                 
            # 定义sql语句模板
            sql = "insert into movieinfo values(null, %s, %s)" 
            # 发送SQL语句并设置参数 
            cur.execute(sql, (int(movie_rank), (movie_title)))
            
            # 关闭游标
            if cur:
                cur.close()
            # 提交事务
            db.commit()
        except pymysql.Error as err:
            # 异常回滚
            db.rollback()
            # 数据异常处理
            raise ("MySQL Error: " + str(err))
        finally:
            # 关闭数据链接对象
            if db:
                db.close()
        # 返回item
        return item