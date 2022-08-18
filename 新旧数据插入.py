# -*- coding: utf-8 -*-
""" 
@Time    : 2021/11/25 18:48
@Author  : xuhaotian
@FileName: 新旧数据插入.py
@SoftWare: PyCharm
"""
import glob
import shutil
oldpath=glob.glob("F:/image/allimage/*.xml")
#oldxmlname=[i.split('\\')[-1] for i in oldpath]
anotherpath=glob.glob("F:/origin_dataset/*.xml")
anotherxmlname=[i.split('\\')[-1] for i in anotherpath]

newpath='D:/xmldealwith/'
#
for oldxml in oldpath:
    if oldxml.split('\\')[-1] not in anotherxmlname:
        shutil.copyfile(oldxml, newpath+oldxml.split('\\')[-1])
        print(oldxml + 'is successfully moved to ' + newpath)


