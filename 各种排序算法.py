# -*- coding: utf-8 -*-
""" 
@Time    : 2021/9/7 8:18
@Author  : xuhaotian
@FileName: 各种排序算法.py
@SoftWare: PyCharm
"""
array=[1,5,6,9,2,3,40,25,68,7,1,3]

#冒泡算法
def maopao(array):                  #进行N-1次循环，每次将最大的或最小的排到最后，时间复杂度O(n^2)
    for i in range(1,len(array)):
        for j in range(0,len(array)-i):
            if array[j]>array[j+1]:
                array[j],array[j+1]=array[j+1],array[j]
    return array

#快速排序 递归方式
def quick(array):                 #数组切割成两部分，递归切割，左右和mid进行比较存放
    if len(array)>=2:
        left,right=[],[]
        mid=array[len(array)//2]
        array.remove(mid)
        for num in array:
            if num>=mid:
                right.append(num)
            else:
                left.append(num)
        return quick(left)+[mid]+quick(right)
    else:
        return array

#插入排序
def insert(array):              #第一个数暂定为最小的，打牌时最小的放在最左边，下一个数如果比他小，则赋最小值给它，一直往前比较，直到比他大，且无法往前比，将此值
                                #和第一个赋值。
    for i in range(1,len(array)):
        key=array[i]
        j=i
        while j>=0 and key<array[j-1]:
            array[j]=array[j-1]
            j-=1
        array[j]=key
    return array

#选择排序
def choose(array):                          #先暂时将起始定为最小，之后的数组与之比较，如果比最小还小，则将min标志换为当前的，确定好最小标志后，
    for i in range(len(array)):             #再将暂定的最小和min标志的最小进行交换
        min=i
        for j in range(i+1,len(array)):
            if array[min]>array[j]:
                min=j
        array[i],array[min]=array[min],array[i]
    return array


print(insert(array))