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
    path = "D:/TRAIN/old_2021_4_14/Oufeng1"  #xml文件所在的目录
    files = os.listdir(path)  # 得到文件夹下所有文件名称
    s = []
    for xmlFile in files:  # 遍历文件夹
        filetype = os.path.splitext(xmlFile)[1]
        if filetype=='.xml':
            if not os.path.isdir(xmlFile):  # 判断是否是文件夹,不是文件夹才打开
                print
                xmlFile
                pass
            print(xmlFile)
            path1 = path+'/'+xmlFile#定位当前处理的文件的路径
            newStr = os.path.join(path, xmlFile)
            width= "2560"
            height = "1440"
            dom = parse(newStr)  ###最核心的部分,路径拼接,输入的是具体路径
            root = dom.getroot()
            print(root)
            for obj in root.iter('size'):#获取object节点中的name子节点

                if obj.find('width').text<obj.find('width').text:
                    obj.find('width').text,obj.find('height').text=obj.find('height').text,obj.find('width').text


            dom.write(path1, xml_declaration=True)#保存到指定文件
            pass
if __name__ == '__main__':
    test()
