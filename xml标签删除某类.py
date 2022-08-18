# -*- coding: utf-8 -*-
""" 
@Time    : 2021/12/8 9:42
@Author  : xuhaotian
@FileName: xml标签删除某类.py
@SoftWare: PyCharm
"""
import os
import glob
input_dir = glob.glob("F:/data/valid/*.xml")  # xml文件所在的目录
#input_dir='allimage_1'  # xml文件所在的目录
shu=0

import xml.etree.ElementTree as ET
for file_path in input_dir:
    #print(file_path)
    dom = ET.parse(file_path)
    root = dom.getroot()
    for obj in root.findall('object'):  # 获取object节点中的name子节点
        name= obj.find('name').text
        if obj.find('name').text == '9':
            print(file_path)
            #root.remove(obj)

            shu+=1
  # 保存到指定文件
    dom.write(file_path, xml_declaration=True)
print("有%d个文件被成功修改。" % shu)
