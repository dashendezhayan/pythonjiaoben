# -*- coding: utf-8 -*-
""" 
@Time    : 2021/8/27 15:32
@Author  : xuhaotian
@FileName: 车辆数据汇总.py
@SoftWare: PyCharm
"""
import pandas as pd
import os
import copy
import numpy as np
path=input('请输入要清洗的BMS文件（加后缀）：')
outpath=input('请输入清洗后的文件名（不加后缀）：')
data=pd.read_csv(path,low_memory=False)
car_vin_unique=data['vin_code'].unique()
print(len(car_vin_unique))
row_list=[]

#数据清洗，将不符合vin码标准的清理，并将正确的放入列表里，用于取值
for i in car_vin_unique:
    if type(i)==str and len(i)==17  and i.isalnum and 'Ÿ' not in i and (i.isdigit() is False):  #字符串判断去除float的none，isalnum是字母或数字，没有非法字符，不是纯数字
        row_list.append(i)
print(len(row_list))
with open(outpath+'.csv', 'ab') as f:
    for i in row_list:
        newdata = (data[data['vin_code'] == i])
        if i[0].isdigit():
            newdata['vin_code']=i[::-1]      #数据存在取反，实际是对的，需要将他逆序打印并将数据存储
            i=i[::-1]
        if os.path.getsize(outpath+'.csv'):
            newdata.to_csv(f,header=False)
            print(i)
        else:
            newdata.to_csv(f)
            print(i)


