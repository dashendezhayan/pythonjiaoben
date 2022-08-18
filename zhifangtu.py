# matplotlib模块绘制直方图
# 读入数据
import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np
from scipy import stats
import seaborn as sns


File_path = 'C:/Users/亿为徐浩天/Desktop/数据分析/46个测点'
#Data = pd.ExcelFile(os.path.join(File_path, '46个测点数据.xlsx'))
#Name = Data.sheet_names
plt.rcParams['font.sans-serif']=['SimHei'] #显示中文标签
plt.rcParams['axes.unicode_minus']=False


data = pd.read_excel(os.path.join(File_path, '46个测点数据.xlsx'), sheet_name='35kV40T中频炉')
for name in data['测点名称']:
    plt_data = data[data['测点名称'] == name]
    plt_data=plt_data['测点值'].values
    plt.hist(plt_data,  # 指定绘图数据
             30,
             [min(plt_data), max(plt_data)])
    # 添加x轴和y轴标签
    plt.xlabel(name)
    plt.ylabel('频数')
    # 添加标题
    #plt.title(name)
    # 显示图形
    plt.savefig('C:/Users/亿为徐浩天/Desktop/数据分析/图片/'+'35kV40T中频炉'+name+'.png')
    plt.show()
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
