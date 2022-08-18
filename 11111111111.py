# -*- coding: utf-8 -*-
""" 
@Time    : 2022/2/22 23:17
@Author  : xuhaotian
@FileName: 11111111111.py
@SoftWare: PyCharm
"""


# 定义排列组合的C(m, n)
def func(m,n):
    a=b=result=1
    if m<n:
        return 0
    else:
        minNI=min(n,m-n)#使运算最简便
        for j in range(0,minNI):
        #使用变量a,b 让所用的分母相乘后除以所有的分子
            a=a*(m-j)
            b=b*(minNI-j)
            result=a//b #在此使用“/”和“//”均可，因为a除以b为整数
        return result
print(func(3,2))  #结果为6
