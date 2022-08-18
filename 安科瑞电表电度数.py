# -*- coding: utf-8 -*-
""" 
@Time    : 2021/7/29 9:15
@Author  : xuhaotian
@FileName: 安科瑞电表电度数.py
@SoftWare: PyCharm
"""
import serial
import binascii
from crcmodbus import crc16Add
#ser = serial.Serial("COM3",9600,parity=serial.PARITY_NONE,timeout=0.5)
#地址 功能码 00 47 00 02 CRClo CRChi
#地址 功能码 00 70 00 02 CRClo CRChi     圆融星座AMC72L-E4,电能70H：0201，71H：dc50 ，数据0x0201dc50   yuanrongxz,02 03 00 70 00 02 c5 e3 回复：0203040201dc50c1b7
                                                                                          #常熟塔弄  28,02 03 00 47 00 02 74 2d

#电度数，单位kw/h
def AMC72L_E4_c_Electric_degree(byte):
    data_16= byte[6:14]
    data_2=bin(int(data_16, 16))[2:]
    if len(data_2)%2==1:
        zhishu=int(data_2[0:8],2)
        weishu=int(data_2[8:],2)
        electric=pow(2,zhishu-127)*(1+weishu/pow(2,23))/1000#
        return electric
    else:
        zhishu = int(data_2[1:9], 2)
        weishu = int(data_2[9:], 2)
        electric = (-1)*pow(2, zhishu - 127) * (1 + weishu / pow(2, 23)) /1000   #
        return electric

def AMC72L_E4_Electric_degree(byte):
    data_16 = byte[6:14]
    electric=int(data_16, 16)/100
    return electric



#def query_JZ_DTS125(address):   #status:baud,改波特率；status:electric，查电度数
    # message_str = address + '03015e0002'
    # message_str_all = crc16Add(message_str)
    # message_hex = bytes.fromhex(message_str_all)
    # print('发送指令：', message_str_all)
    # ser.write(message_hex)
    # receive_message = ser.readline()
    # receive_message = binascii.b2a_hex(receive_message).decode()  # 将十六进制b'\x'变为字符串
    # electric_degree=AMC72L_E4_Electric_degree(receive_message)
    # print('返回报文及电度数：', receive_message,electric_degree)
    # return receive_message,electric_degree
#query_JZ_DTS125('01')
print(AMC72L_E4_c_Electric_degree('03030448d7a000066b'))


#33  0304   0015003f   b824