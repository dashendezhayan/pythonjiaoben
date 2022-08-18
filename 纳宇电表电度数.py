# -*- coding: utf-8 -*-
""" 
@Time    : 2021/7/29 13:32
@Author  : xuhaotian
@FileName: 纳宇电表电度数.py
@SoftWare: PyCharm
"""
#读取电度数指令
#地址 功能码 01 56 00 02 CRC
import serial
import binascii,crcmod
#电度数，单位kw/h



def crc16Add(read):
    if type(read)==bytes:   # 如果read为十六进制b'',转化为str
        read=binascii.b2a_hex(read).decode()
    elif type(read)==str:  # 如果read为str，不变
        read=read
    crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xFFFF, xorOut=0x0000)
    data = read.replace(" ", "")  # 消除空格
    readcrcout = hex(crc16(binascii.unhexlify(data))).upper()
    str_list = list(readcrcout)
    if len(str_list) == 5:
        str_list.insert(2, '0')  # 位数不足补0，因为一般最少是5个
    crc_data = "".join(str_list) # 用""把数组的每一位结合起来  组成新的字符串
    crc = read.strip() + crc_data[4:] + crc_data[2:4] # 把源代码和crc校验码连接起来
    return crc

def jiexi1(message):
    data_16= message[6:14]
    data_2=bin(int(data_16, 16))[2:]
    gaowei=int(data_2[0:8],2)
    diwei=int(data_2[8:],2)
    electric=(gaowei*65536+diwei)/1000#
    return electric
def jiexi2(message):                         #AMC72LE4C   1000101110101100110000000000000
    data_16 = message[6:14]
    print('十六进制',data_16)
    if data_16=='00000000':
        electric=0.0
        print(type(electric))

    else:
        data_2 = bin(int(data_16, 16))[2:]
        print('二进制', data_2)
        zhishu = int(data_2[0:8], 2)
        print(zhishu)
        weishu = int(data_2[8:], 2)

        electric = pow(2, zhishu - 127) * (1 + weishu / pow(2, 23))/1000
    return electric

def jiexi3(message):                     #AMC72LE4
    data_16 = message[6:14]
    electric = int(data_16, 16) / 100
    return electric
def jiexi4(message):                     #JZDTS125，nayu96K
    data_16 = message[6:14]
    electric = int(data_16, 16) / 10
    return electric

def linglong88(message):                         #AMC72LE4C
    data_16 = message[6:14]

    data_2 = bin(int(data_16, 16))[2:]
    zhishu = int(data_2[0:8], 2)
    weishu = int(data_2[8:], 2)
    electric = pow(2, zhishu - 127) * (1 + weishu / pow(2, 23))
    return electric

def jiexi5(message):                     #huadong
    data_16 = message[6:14]
    electric = int(data_16, 16) *0.8
    return electric
# #昆山兆丰，data='0203 00 47 00 02742D',0303 00 47 00 0275FC,04 0300000002C45E,0503015600022463
#
def jiexi6(message):
    data_16 = message[6:14]
    data_16 = data_16[4:8]+data_16[0:4]
    data_2 = bin(int(data_16, 16))[2:]
    print('二进制', data_2)
    zhishu = int(data_2[0:8], 2)
    print(zhishu)
    weishu = int(data_2[8:], 2)

    electric = pow(2, zhishu - 127) * (1 + weishu / pow(2, 23))
    return electric
#
data='06 03 00 00 00 02'      #玲珑88,0203008100029410
data=crc16Add(data)
print(data)
# message=bytes.fromhex(data)
# print(message)
# ser = serial.Serial("COM3",9600,parity=serial.PARITY_NONE,timeout=0.5)
# ser.write(message)
# receive_message = ser.readline()
# print(receive_message)
# print(binascii.b2a_hex(receive_message))

message='0903044E109390d605'        #02030400000000c933    03030445d660000507
print(linglong88(message))
print(jiexi1(message))
print('AMC72LE4C',jiexi2(message))   #AMC72LE4C
print(jiexi3(message))   #AMC72LE4
print(jiexi4(message))
print(jiexi5(message))
print(jiexi6(message))
print(linglong88(message))
#print(jiexi2('0203044e256ecce3e5'))   #12676.812     13072.712      693875456   71921

# print(bytes.fromhex('0203044d2bdd827766'))
# print(Nayu_Electric_degree(b'0403040001bb889a72'))
# print(b'\xff\x05\x00\x01\x00\x00\x89\xd4')
# print(binascii.b2a_hex(b'\xff\x05\x00\x01\x00\x00\x89\xd4'))