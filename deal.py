# -*- coding: utf-8 -*-
""" 
@Time    : 2022/7/14 9:00
@Author  : xuhaotian
@FileName: deal.py
@SoftWare: PyCharm
"""
with open('2022_07_13.txt', 'r') as file:
    contents = file.readlines()

new=[]
for i in contents:
    if "e461970301" in i:
        new.append(i)
with open('2022_07_13new.txt','w') as f:
    for i in new:
        f.write(i)

