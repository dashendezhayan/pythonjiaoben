# -*- coding: utf-8 -*-
""" 
@Time    : 2022/4/26 13:34
@Author  : xuhaotian
@FileName: linux485.py
@SoftWare: PyCharm
"""
import time
#电度数，单位kw/h
import serial
import binascii
ser = serial.Serial("/dev/ttyS0",9600,parity=serial.PARITY_NONE,timeout=0.5)
message='6804000408'

message_hex = bytes.fromhex(message)
ser.write(message_hex)
receive_message = (ser.readline())
receive_message=binascii.b2a_hex(receive_message)

print(receive_message)
# n=10000
# while n>0:
#     ser.write(message_hex)
#
#     receive_message = (ser.readline())
#     receive_message=binascii.b2a_hex(receive_message)
#     n-=1
#     print(receive_message)
#     time.sleep(0.5)
#print(bytes.fromhex('00 01 02 03 04 05'))
#print(xinling_Electric_degree(b'0403040001bb889a72'))
# print(b'\xff\x05\x00\x01\x00\x00\x89\xd4')
# print(binascii.b2a_hex(b'\xff\x05\x00\x01\x00\x00\x89\xd4'))