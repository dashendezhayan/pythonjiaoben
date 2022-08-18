# -*- coding: utf-8 -*-
""" 
@Time    : 2021/7/15 13:20
@Author  : xuhaotian
@FileName: xlsx数据分析与画图.py
@SoftWare: PyCharm
"""
import pandas as pd
import matplotlib.pyplot as plt
import os
import copy
import numpy as np
from scipy import stats
import seaborn as sns

path = input('需要制图的BMS文件（绝对路径）：')
outpath=input('图片保存地址（绝对路径）：')
car_choice=input('请选择全部还是指定车辆（all或者车辆vim码（17位））：')
charge_times=input('输入指定充电次数的数据(all或者数字)：')

df = pd.read_csv(path,low_memory=False)
#name=Data.columns.to_list()[1:]#获取表头名
#获取时间
vin=df['vin_code'].unique()
Date = df['create_time'].values
if car_choice=='all':
    vin_code=vin
elif len(car_choice)==17:
    if car_choice.isalnum and car_choice not in vin:
        print("查询的vin码不存在")
    elif car_choice.isalnum and car_choice in vin:
        vin_code=car_choice
else:
    print('请输入正确的vin码')
if len(vin_code)>=1:
    for vin in vin_code:
        pic_path=outpath+'/'+vin
        if not os.path.exists(pic_path):
            os.mkdir(pic_path)
        print(vin)
        Data = (df[df['vin_code'] == vin])
        different_time = []
        time_index = {}
        for i in range(len(Data)):
            if charge_times!='all':
                if len(different_time)<int(charge_times):
                    if str(Data.iloc[i]['create_time']).split(' ')[0] not in different_time:
                        different_time.append(str(Data.iloc[i]['create_time']).split(' ')[0])
                        time_index[str(Data.iloc[i]['create_time']).split(' ')[0]] = []
                        time_index[str(Data.iloc[i]['create_time']).split(' ')[0]].append(i)
                    elif str(Data.iloc[i]['create_time']).split(' ')[0] in different_time:
                        time_index[str(Data.iloc[i]['create_time']).split(' ')[0]].append(i)
                else:
                    break
            else:
                if str(Data.iloc[i]['create_time']).split(' ')[0] not in different_time:
                    different_time.append(str(Data.iloc[i]['create_time']).split(' ')[0])
                    time_index[str(Data.iloc[i]['create_time']).split(' ')[0]] = []
                    time_index[str(Data.iloc[i]['create_time']).split(' ')[0]].append(i)
                elif str(Data.iloc[i]['create_time']).split(' ')[0] in different_time:
                    time_index[str(Data.iloc[i]['create_time']).split(' ')[0]].append(i)

        color=['black','blue','yellow','red','brown','green','cyan','deeppink','brown','crimson',
               'darkblue','#FF00FF','#228B22','gold','gray','honeydew','hotpink','indianred',
               'lavender','lightpink','mintcream','peachpuff','slateblue','snow','teal',
               'mediumaquamarine','mediumblue','mediumorchid','mediumpurple','mediumseagreen',
               'mediumslateblue','mediumspringgreen','mediumturquoise','mediumvioletred',
               'lightblue','lightcoral','lightcyan','lightgoldenrodyellow','lightgray',
               'lightsalmon','lightskyblue','lightslategray','lightyellow','limegreen',
               'linen']

        for table_name in ['current_soc', 'voltage_measurement']:
            for table_name1 in ['current_measurement', 'voltage_measurement', 'max_battery_temp', 'min_battery_temp']:
                if table_name==table_name1:
                    continue
                plt.figure(dpi=500)
                color_id = 0
                print(table_name,table_name1)
                for k,v in time_index.items():

                    x=Data.iloc[v][table_name]
                    y=Data.iloc[v][table_name1]
                    print(len(x),len(y),len(time_index),len(color))
                    plt.scatter(x, y, linewidth=1, color=color[color_id], s=2 ** 2, label=k,
                                marker='o')  # 添加x轴和y轴标签

                    plt.xlabel(table_name)
                    plt.ylabel(table_name1)
                    plt.legend(loc=0, ncol=1)
                    color_id += 1
                plt.savefig(pic_path+'/' + table_name + '_' + table_name1 + '.jpg')
                plt.show()

# for date in Date:
#     if str(date).split('T')[0] not in Date_time:
#         Date_time.append(str(date).split('T')[0])
# print(Date_time)
#
# data=[[],[],[],[]]
# for i in range(len(Date_time)):
#     for j in range(len(Data)):
#         print( str(Data.loc[j,'create_time']).split(' ')[0],Date_time[i])
#         if str(Data.loc[j,'create_time']).split(' ')[0] == Date_time[i]:
#             data[i][j]=Data.loc[j,:]
# print(data[0][0])


# print(Date_time.loc[1])

# for i in range(len(Date_time)):
#
#     for j in range(len(Data)):
#         # print(Data['create_time'])
#         # print(Date_time.loc[i]
#         # print(str(Data.loc[j]['create_time']).split(' ')[0])
#         new_Data.loc[j]['create_time']=str(new_Data.loc[j]['create_time']).split(' ')[0])
#
#         if Data.loc[j]['create_time'] == str(Date_time.loc[i]):
#             print(1)
#             # data =Data.loc[j]
# # print(data)

#print(data1)


#name=Data.columns.to_list()[1:]#获取表头名