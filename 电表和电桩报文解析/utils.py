# -*- coding: utf-8 -*-
""" 
@Time    : 2022/8/18 13:23
@Author  : xuhaotian
@FileName: utils.py
@SoftWare: PyCharm
"""
import binascii, crcmod

# CRC计算，输入：str or byte，输出：str + CRC
def crc(read):
    # 如果read为十六进制b'',转化为str
    if type(read) == bytes:
        read = binascii.b2a_hex(read).decode()
    # 如果read为str，不变
    elif type(read) == str:
        read = read
    crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xFFFF, xorOut=0x0000)
    # 消除空格
    data = read.replace(" ", "")
    readcrcout = hex(crc16(binascii.unhexlify(data))).upper()
    str_list = list(readcrcout)
    print(readcrcout)
    # 位数不足补0，因为一般最少是5个
    if len(str_list) == 5:
        str_list.insert(2, '0')
    # 用""把数组的每一位结合起来  组成新的字符串
    crc_data = "".join(str_list)
    crc = data + crc_data[4:] + crc_data[2:4]  # 把源代码和crc校验码连接起来
    return crc

# 读取txt文本，输入：str(文件地址)，输出：str(文本内容)
def read_txt(txt):
    f = open(txt, encoding="utf-8")
    txt_message= f.readlines()
    return txt_message


print(read_txt('S04_AMC72L.config')[0].split(',')[0])
print(read_txt('S04_AMC72L.config')[0].split(',')[0])
print(read_txt('S04_AMC72L.config')[0].split(',')[0])
print(read_txt('S04_AMC72L.config')[0].split(',')[0])

