# -*- coding: utf-8 -*-
""" 
@Time    : 2021/12/27 13:05
@Author  : xuhaotian
@FileName: 远程断电加解密.py
@SoftWare: PyCharm
"""

k = '(--*dsadasdasd#$#%！#￥%…………&&&'
def enctry(s,k):

    encry_str = ""
    for i, j in zip(s, k):
        # i为字符，j为秘钥字符
        temp = str(ord(i) + ord(j)) + '_'  # 加密字符 = 字符的Unicode码 + 秘钥的Unicode码
        encry_str = encry_str + temp
    return encry_str


# 解密
def dectry(p,k):
    dec_str = ""
    for i, j in zip(p.split("_")[:-1], k):
        # i 为加密字符，j为秘钥字符
        temp = chr(int(i) - ord(j))  # 解密字符 = (加密Unicode码字符 - 秘钥字符的Unicode码)的单字节字符
        dec_str = dec_str + temp
    return dec_str


data = "yiwei"
print(bytes.fromhex(data))
print("原始数据为：", data)
enc_str = enctry(data,k)
print("加密数据为：", enc_str)
dec_str = dectry(enc_str,k)
print("解密数据为：", dec_str)