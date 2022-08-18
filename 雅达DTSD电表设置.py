# -*- coding: utf-8 -*-
""" 
@Time    : 2021/10/26 17:49
@Author  : xuhaotian
@FileName: 雅达DTSD电表设置.py
@SoftWare: PyCharm
"""
import serial
import binascii
from crcmodbus import crc16Add
ser = serial.Serial("COM3",9600,parity=serial.PARITY_NONE,timeout=0.5)   #雅达电表初始波特率为2400，偶校验
                                                                        #更改完成后，需要更改波特率9600，parity=serial.PARITY_NONE

#修改地址 \x01\x10\x00\x00\x00\x04\x08\x00\x01\x25\x80\x00\x00\x00\x00\xA0\x51.
def query_DTSD(address,status):   #status:baud,改波特率；status:electric，查电度数
    if status=='baud':
        message_str = address + '0602260140'
    elif status=='electric':
        message_str = address + '0300000002'
    message_str_all = crc16Add(message_str)
    message_hex = bytes.fromhex(message_str_all)
    print('发送指令：', message_str_all)
    ser.write(message_hex)
    receive_message = ser.readline()
    receive_message = binascii.b2a_hex(receive_message).decode()  # 将十六进制b'\x'变为字符串
    print('返回报文：', receive_message)
    return receive_message

def change_add(old_address,new_address):
    message_str=old_address+'0601fb00'+new_address
    message_str_all = crc16Add(message_str)
    message_hex = bytes.fromhex(message_str_all)
    print('发送指令：', message_str_all)
    ser.write(message_hex)
    receive_message = ser.readline()
    receive_message = binascii.b2a_hex(receive_message).decode()  # 将十六进制b'\x'变为字符串
    print('返回报文：', receive_message)
    return receive_message
query_DTSD('04','electric')
#change_add('01','04')

