# -*- coding: utf-8 -*-
""" 
@Time    : 2021/9/8 8:43
@Author  : xuhaotian
@FileName: 排序算法练手.py
@SoftWare: PyCharm
"""
array=[25,13,60,3,4,7,98,32,45,32]
def maopao(array):
    for i in range(1,len(array)):
        for j in range(len(array)-i):
            if array[j]>array[j+1]:
                array[j],array[j+1]=array[j+1],array[j]
    return array


def quick(array):
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

def choose(array):
    for i in range(len(array)-1):
        min=i
        for j in range(i+1,len(array)):
            if array[j]<array[min]:
                min=j
        array[min],array[i]=array[i],array[min]
    return array
print(choose(array))
def insert(array):
    for i in range(1, len(array)):
        j=i
        key=array[i]
        while j >= 0 and key < array[j - 1]:
            array[j] = array[j - 1]
            j -= 1
        array[j] = key
    return array






