# -*- coding: utf-8 -*-
""" 
@Time    : 2022/7/26 13:19
@Author  : xuhaotian
@FileName: daiwenjie.py
@SoftWare: PyCharm
"""
import pandas as pd
from tqdm import tqdm
from copy import deepcopy

import os
import copy
import numpy as np
import copy
import array as arr
path1="D:/python脚本/戴文婕/新加表-吴中文化.xlsx"
path2="D:/python脚本/戴文婕/主表-吴中文化.xlsx"
outpath1="D:/python脚本/戴文婕/终表符合-吴中文化.xlsx"
outpath2="D:/python脚本/戴文婕/终表不符合-吴中文化.xlsx"
data1=pd.read_excel(path2).values
#data2=pd.read_excel(path2).values
data3=pd.read_excel(outpath2).values

data3=data3.tolist()



for i in tqdm(range(len(data3))):
    for j in tqdm(range(len(data1))):
        if data3[i][-1]==data1[j][5]:
            if data3[j][2]
                print(data1[j])
                data4.remove(data1[j])

print(len(data4))
data4=pd.DataFrame(data4)
data4.to_excel(excel_writer=outpath2)
# for i in data2:
#     i[1]=pd.to_datetime(i[1],format='%Y-%m-%d %H:%M:%S')
#     i[2]=pd.to_datetime(i[2], format='%Y-%m-%d %H:%M:%S')
#
# data1=data1.tolist()
# data3=deepcopy(data1)
#
# for i in tqdm(range(len(data1))):
#     for j in tqdm(range(len(data2))):
#         if data1[i][-1]==data2[j][5]:
#             if data1[i][2]<data2[j][1] or data1[i][1]>data2[j][2]:
#                 continue
#             else:
#                 if data1[i] in data3:
#                     data4.append(data1[i])
#                     data3.remove(data1[i])
#
#
#
# data3=pd.DataFrame(data3)
#
# # data3=pd.DataFrame(data3)
# # data4=pd.DataFrame(data4)
#
# print(data3)
# print("\n")
# data3.to_excel(excel_writer=outpath1)





#数据清洗，将不符合vin码标准的清理，并将正确的放入列表里，用于取值
# for i in car_vin_unique:
#     if type(i)==str and len(i)==17  and i.isalnum and 'Ÿ' not in i and (i.isdigit() is False):  #字符串判断去除float的none，isalnum是字母或数字，没有非法字符，不是纯数字
#         row_list.append(i)
# print(len(row_list))
# with open(outpath+'.csv', 'ab') as f:
#     for i in row_list:
#         newdata = (data[data['vin_code'] == i])
#         if i[0].isdigit():
#             newdata['vin_code']=i[::-1]      #数据存在取反，实际是对的，需要将他逆序打印并将数据存储
#             i=i[::-1]
#         if os.path.getsize(outpath+'.csv'):
#             newdata.to_csv(f,header=False)
#             print(i)
#         else:
#             newdata.to_csv(f)
#             print(i)