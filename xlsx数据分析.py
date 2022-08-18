# -*- coding: utf-8 -*-
""" 
@Time    : 2021/7/13 10:40
@Author  : xuhaotian
@FileName: xlsx数据分析.py
@SoftWare: PyCharm
"""
import pandas as pd
import matplotlib.pyplot as plt


IO = 'C:/Users/亿为徐浩天/Desktop/LNBSCC4H1KD788495.xlsx'
plt.rcParams['font.sans-serif']=['SimHei'] #显示中文标签
plt.rcParams['axes.unicode_minus']=False
#读取excel文件
Data = pd.read_excel(io=IO)

VIN='LNBSCC4H1KD788495 '


#获取时间
Date = Data['create_time']
Date_time=[]
for date in Date:
    if str(date).split(' ')[0] not in Date_time:
        Date_time.append(str(date).split(' ')[0])
print(Date_time)



name=Data.columns.to_list()[1:]#获取表头名

for table_name in ['current_soc','voltage_measurement']:
    for table_name1 in ['current_measurement','voltage_measurement','max_battery_temp','min_battery_temp']:
        plt.figure()
        x1=Data[table_name].values[1:31]
        y1=Data[table_name1].values[1:31]

        x2 = Data[table_name].values[32:375]
        y2 = Data[table_name1].values[32:375]
        x3 = Data[table_name].values[376:586]
        y3 = Data[table_name1].values[376:586]

        x4 = Data[table_name].values[587:837]
        y4 = Data[table_name1].values[587:837]
        x5 = Data[table_name].values[838:1078]
        y5 = Data[table_name1].values[838:1078]

        plt.scatter(x1, y1, linewidth=1, color='blue', s=2 ** 2, label='2021-06-23-5',
                    marker='o')  # 添加x轴和y轴标签
        plt.scatter(x2, y2, linewidth=1, color='green', s=2 ** 2, label='2021-06-23-9',
                    marker='o')  # 添加x轴和y轴标签
        plt.scatter(x3, y3, linewidth=1, color='cyan', s=2 ** 2, label='2021-06-29',
                    marker='o')  # 添加x轴和y轴标签
        plt.scatter(x4, y4, linewidth=1, color='black', s=2 ** 2, label='2021-06-30',
                    marker='o')  # 添加x轴和y轴标签
        plt.scatter(x5, y5, linewidth=1, color='pink', s=2 ** 2, label='2021-06-31',
                    marker='o')  # 添加x轴和y轴标签

        plt.xlabel(table_name)
        plt.ylabel(table_name1)
        plt.legend(loc=0, ncol=1)
        plt.savefig('C:/Users/亿为徐浩天/Desktop/LNBSCC4H1KD788495分析/' + table_name + '_' + table_name1 + '.jpg')
        plt.show()

#
#
#
# for i in range(len(Data)):
#      if str(Data['create_time'][i]).split(' ')[0]==date[0]:
#          data1.append(str(Data.loc[i].values))
#     # if Data['create_time'][1] !=None:
#     #     if data['vin_code'].values in VIN:
# print(data1[1])


