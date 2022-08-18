# -*- coding: utf-8 -*-
""" 
@Time    : 2021/7/1 13:50
@Author  : xuhaotian
@FileName: 智能断路器程序（linux）.py
@SoftWare: PyCharm
"""
import pymysql
import datetime


conn = pymysql.connect(
    host='123.60.74.195',
    port=3306,
    user='yiweidatabase',
    password='yiWei2018',
    database='electric_alarm',
    charset='utf8')
cursor = conn.cursor(pymysql.cursors.DictCursor)



def position_alarm(position):
    now = datetime.datetime.now()
    otherStyleTime = now.strftime("%Y-%m-%d %H:%M:%S")
    sql = 'update' + ' ' + 'electric_alarm' + ' ' + 'set' + ' ' + 'create_time' + '=' + "'" + otherStyleTime + "'" + ' ' + 'where' + ' ' + 'position='+ "'"+position+"'"+';'
    cursor.execute(sql)
    conn.commit()
    sql='select'+' ' + 'alarm' + ' '+'FROM' + ' ' + 'electric_alarm'+' '+'where position like' +' '+position
    try:
        cursor.execute(sql)
        result=cursor.fetchone()
        return result
    except:
        print("Error:cannot get data")

while True:

    print(position_alarm('111')['alarm'])
    print(position_alarm('222')['alarm'])
