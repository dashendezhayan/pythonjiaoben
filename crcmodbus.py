# -*- coding: utf-8 -*-
""" 
@Time    : 2021/7/28 9:57
@Author  : xuhaotian
@FileName: crcmodbus.py
@SoftWare: PyCharm
"""
from binascii import *
import binascii
import crcmod

#生成CRC16-MODBUS校验码
def crc16Add(read):
    if type(read)==bytes:#如果read为十六进制b'',转化为str
        read=binascii.b2a_hex(read).decode()
    elif type(read)==str:#如果read为str，不变
        read=read
    crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xFFFF, xorOut=0x0000)
    data = read.replace(" ", "") #消除空格
    readcrcout = hex(crc16(unhexlify(data))).upper()
    str_list = list(readcrcout)
    # print(str_list)
    if len(str_list) == 5:
        str_list.insert(2, '0')  # 位数不足补0，因为一般最少是5个
    crc_data = "".join(str_list) #用""把数组的每一位结合起来  组成新的字符串
    # print(crc_data)
    crc = read.strip() + crc_data[4:]  + crc_data[2:4] #把源代码和crc校验码连接起来
    return crc
#print(crc16Add('02 03 00 0a 00 02'))  #b'\x01\x05\x00\x01\xff\x00'



