# -*- coding: utf-8 -*-
""" 
@Time    : 2022/1/4 17:01
@Author  : xuhaotian
@FileName: 镜像路由数据筛选.py
@SoftWare: PyCharm
"""
choose_content='192.168.124.3'
file_name='20220104.log'
file = open(file_name,mode='r',encoding='utf-8')
new_file = open('new_'+file_name,mode='a',encoding='utf-8')
content = file.readlines()   #读出的为列表
for i in content:
    if choose_content in i and 'HEX' in i:
        i=i.replace("[main] INFO  com.zmn.iot.pcap.PcapService","")
        new_file.write(i)
        print(i)
file.close()
new_file.close()
