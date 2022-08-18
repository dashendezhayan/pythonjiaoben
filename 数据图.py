# matplotlib模块绘制直方图
# 读入数据
import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np
from scipy import stats
import seaborn as sns

IO = 'C:/Users/亿为徐浩天/Desktop/苏州苏ED31085.xlsx'
plt.rcParams['font.sans-serif']=['SimHei'] #显示中文标签
plt.rcParams['axes.unicode_minus']=False
#读取excel文件
Data = pd.read_excel(io=IO)
# Data = pd.ExcelFile('C:/Users/亿为徐浩天/Desktop/data(1).xlsx')
# #Data = pd.ExcelFile(os.path.join(File_path, '46个测点数据.xlsx'))
# Name = Data.sheet_names
print(Data.columns.to_list()[1:])#获取表头名
for table_name in Data.columns.to_list()[1:]:
    for table_name1 in Data.columns.to_list()[1:]:
        plt.figure()
        Data1_values=Data[table_name1].values[1:77]
        x1_data=Data[table_name].values[1:77]
        print(Data1_values)
        print(x1_data)

        Data2_values = Data[table_name1].values[79:145]
        x2_data = Data[table_name].values[79:145]
        print(x2_data)

        Data3_values = Data[table_name1].values[147:210]
        x3_data = Data[table_name].values[147:210]
        print(x3_data)

        Data4_values = Data[table_name1].values[214:279]
        x4_data = Data[table_name].values[214:279]


        plt.scatter(x1_data,Data1_values,linewidth = 1, color='blue', s=2**2,label='2021-06-18',marker='o')# 添加x轴和y轴标签
        plt.scatter(x2_data, Data2_values, linewidth=1, color='green', s=2**2,label='2021-06-25',marker='.')  # 添加x轴和y轴标签
        plt.scatter(x3_data, Data3_values, linewidth=1, color='cyan', s=2**2,label='2021-06-26',marker='o')  # 添加x轴和y轴标签
        plt.scatter(x4_data, Data4_values, linewidth=1, color='black', s=2**2,label='2021-06-29',marker='x')  # 添加x轴和y轴标签

        plt.xlabel(table_name)
        plt.ylabel(table_name1)
        plt.legend(loc=0, ncol=1)
        plt.savefig('C:/Users/亿为徐浩天/Desktop/6_30事故BSM分析/'+table_name+'_'+table_name1 + '.jpg')
        plt.show()
# 添加标题
# plt.title(Name[i])
# 显示图形

# plt.rcParams['font.sans-serif']=['SimHei'] #显示中文标签
# plt.rcParams['axes.unicode_minus']=False

# data = pd.read_excel(Data), sheet_name=Name[i])
# Name_1 = data.drop_duplicates(['测点名称'])
# plt_data = [[]]
# # plt_data[0] = data[data['测点名称'] == Name_1['测点名称'][0]]
# n = len(Name_1)
# for m in range(0, n):
#     label_name=Name_1['测点名称'][m]
#     data_2 = data[data['测点名称'] == Name_1['测点名称'][m]]
#     plt_data.append(data_2)
#     values=plt_data[m]['测点值'].values
#     print(values)
#     plt.hist(values, # 指定绘图数据
#              len(values),
#              [min(values),max(values)])
#     # 添加x轴和y轴标签
#     plt.xlabel(label_name)
#     plt.ylabel('频数')
#     # 添加标题
#     plt.title(Name[i])
#     # 显示图形
#     plt.savefig(label_name+'.jpg')
#     plt.show()



    # for data in df:
    #     print(data)
    #     plt_data=data[data['测点编码']=='P']
    #     print("1",plt_data)
    #     plt_data=plt_data['测点值'].values
    #     print("2",plt_data)
        #print(plt_data.describe(include = 'all'))
        # for i in range(len(plt_data)):
        #     print(plt_data[i])

        # for i in range(len(data)):
        #     if data['测点名称']=='35kV40T中频炉-C相电流':
        #         data['']

        #for i in range(len(data))
        #绘制直方图
        #sns.distplot(plt_data,bins=len(plt_data))  # bin控制直方图的竖直的长方形的数量
        # print(plt_data)



        # plt.hist(plt_data, # 指定绘图数据
        #          len(plt_data),
        #          [min(plt_data),max(plt_data)])
        # # 添加x轴和y轴标签
        # plt.xlabel(plt_data['测点名称'])
        # plt.ylabel('频数')
        # # 添加标题
        # plt.title(sheet_name)
        # # 显示图形
        # plt.show()