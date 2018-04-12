#!/usr/bin/python
# -*- coding: UTF-8 -*-

import MySQLdb

# 打开数据库连接
db = MySQLdb.connect(host='10.127.2.12', port=8081, user='root',
                     passwd='root', db='test')

# 使用cursor()方法获取操作游标
cursor = db.cursor()

# 使用execute方法执行SQL语句
cursor.execute("select * from user")

# 使用 fetchone() 方法获取一条数据
data = cursor.fetchall()

print data

# 关闭数据库连接
db.close()