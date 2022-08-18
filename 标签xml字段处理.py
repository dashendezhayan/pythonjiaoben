# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 08:24:33 2019

@author: Administrator
"""


import os
import os.path
from xml.etree.ElementTree import parse, Element
#批量修改xml中内容
def test():
    #changedict()
    path = "D:/xmldealwith"  #xml文件所在的目录
    files = os.listdir(path)  # 得到文件夹下所有文件名称
    s = []
    for xmlFile in files:  # 遍历文件夹
        filetype = os.path.splitext(xmlFile)[1]
        if filetype == '.xml':
            if not os.path.isdir(xmlFile):  # 判断是否是文件夹,不是文件夹才打开
                #print
                xmlFile
                pass
            path = "D:/xmldealwith/"
            #print(xmlFile)
            path1 = path+xmlFile#定位当前处理的文件的路径
            newStr = os.path.join(path, xmlFile)
            # name1 = "4"
            # name2 = "5"
            dom = parse(newStr)  ###最核心的部分,路径拼接,输入的是具体路径
            root = dom.getroot()
            #print(root)
            for obj in root.iter('object'):#获取object节点中的name子节点
                #print(type(obj.find('name').text))
                obj.find('name').text=str(int(obj.find('name').text)+1)


                print(obj.find('name').text)


            #         obj.find('name').text = name2
            #     elif obj.find('name').text=="5":
            #         obj.find('name').text=name1
            #     name_new = obj.find('name').text#修改
            #     print(name_new)
            dom.write(path1, xml_declaration=True)#保存到指定文件
            # pass
if __name__ == '__main__':
    test()
