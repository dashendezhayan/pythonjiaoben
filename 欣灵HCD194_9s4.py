# -*- coding: utf-8 -*-
""" 
@Time    : 2021/7/29 13:32
@Author  : xuhaotian
@FileName: 纳宇电表电度数.py
@SoftWare: PyCharm
"""
def xinling_Electric_degree(byte):
    data_16= byte[6:22]
    data_2=bin(int(data_16, 16))[2:]
    gaowei=int(data_2[0:8],2)
    diwei=int(data_2[8:],2)
    electric=(gaowei*10+diwei)/1000#
    return electric
#读取电度数指令
#地址 功能码 01 56 00 02 CRC
#兴贤 04 03 00 37 00 04F592
#04 03 08 00 00 00 00 00 00 00 00
import binascii
#电度数，单位kw/h
import serial
import binascii
from crcmodbus import crc16Add
ser = serial.Serial("COM3",2400,parity=serial.PARITY_EVEN,timeout=0.5)

ser.write(b'\x01\x10\x04\x06\x00\x01\x03\xb9\x89')
#b'\x01\x10\x04\x04\x00\x01\x03\xb8\x31'
receive_message = (ser.readline())
receive_message=binascii.b2a_hex(receive_message)
print(receive_message)
#print(bytes.fromhex('00 01 02 03 04 05'))
#print(xinling_Electric_degree(b'0403040001bb889a72'))
# print(b'\xff\x05\x00\x01\x00\x00\x89\xd4')
# print(binascii.b2a_hex(b'\xff\x05\x00\x01\x00\x00\x89\xd4'))