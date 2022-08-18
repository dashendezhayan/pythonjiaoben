# -*- coding: utf-8 -*-
""" 
@Time    : 2021/6/30 14:43
@Author  : xuhaotian
@FileName: 2e01.py
@SoftWare: PyCharm
"""
import re
f1 = open('/tmp/test.txt')
f2 = open('/tmp/myhello.txt','r+')
for s in f1.readlines():
f2.write(s.replace('hello','hi'))
f1.close()
f2.close()
