import serial
import binascii
from crcmodbus import crc16Add
ser = serial.Serial("COM3",9600,parity=serial.PARITY_NONE,timeout=0.5)
import time
#合闸 \xff\x05\x00\x01\xff\x00\xc8\x24
#\x01\x05\x00\x01\xff\x00\xdd\xfa
#分闸   \xff\x05\x00\x01\x00\x00\x89\xd4
#  \x01\x05\x00\x01\x00\x00\x9c\x0a
#修改地址 \x01\x10\x00\x00\x00\x04\x08\x00\x01\x25\x80\x00\x00\x00\x00\xA0\x51.
#读分合闸状态 \xff\x01\x00\x01\x00\x01\xb9\xd4      返回结果第四个字节01为合闸，00为分闸
#\x01\x01\x00\x01\x00\x01\xac\x0a

def test_DLQ(address,status):
    if status=='open':
        message_str=address+'050001ff00'
    elif status=='close':
        message_str = address + '0500010000'
    elif status=='status':
        message_str = address + '0100010001'
    message_str_all = crc16Add(message_str)
    message_hex = bytes.fromhex(message_str_all)     #字符串变成b'\x'十六进制
    print('发送指令：',message_str_all)
    ser.write(message_hex)
    receive_message = ser.readline()
    receive_message=binascii.b2a_hex(receive_message).decode()   #将十六进制b'\x'变为字符串
    print('返回报文：',receive_message)
    return receive_message
#修改地址 \x01\x10\x00\x00\x00\x04\x08\x00\x01\x25\x80\x00\x00\x00\x00\xA0\x51.
def change_add(old_address,new_address):
    message_str=old_address+'10000000040800'+new_address+'258000000000'
    message_str_all = crc16Add(message_str)
    message_hex = bytes.fromhex(message_str_all)
    print('发送指令：', message_str_all)
    ser.write(message_hex)
    receive_message = ser.readline()
    receive_message = binascii.b2a_hex(receive_message).decode()  # 将十六进制b'\x'变为字符串
    print('返回报文：', receive_message)
    return receive_message
#test_DLQ('01','open')#'open','close','status'
change_add('01','02')

# ser.write(b'\x02\x10\x00\x00\x00\x04\x08\x00\x01\x25\x80\x00\x00\x00\x00\xe3\x50')
# receive_message = (ser.readline())
# print(receive_message)
# data='01050001ff00ddfa'
# print(bytes.fromhex(data))
# ser.write(bytes.fromhex(data))
# receive_message = (ser.readline())
# receive_message=binascii.b2a_hex(receive_message)
# print(binascii.b2a_hex(b'\x01\x05\x00\x01\x00\x00')).decode())
# test_DLQ('01','open')#'open','close','status'