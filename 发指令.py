# -*- coding: utf-8 -*-
""" 
@Time    : 2021/8/31 10:45
@Author  : xuhaotian
@FileName: 发指令.py
@SoftWare: PyCharm
"""
import serial
import binascii
from crcmodbus import crc16Add
ser = serial.Serial("COM3",9600,parity=serial.PARITY_NONE,timeout=0.5)
#ser.write(b'\x02\x03\x00\x47\x00\x02\x74\x2d ')#03 00 47 00 02
ser.write(b'\x05\x03\x01\x5e\x00\x02\xa5\xa1 ')
receive_message = (ser.readline())
receive_message=binascii.b2a_hex(receive_message)
print(receive_message)
