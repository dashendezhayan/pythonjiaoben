# -*- coding: utf-8 -*-
""" 
@Time    : 2021/11/12 9:40
@Author  : xuhaotian
@FileName: 全电表设置.py
@SoftWare: PyCharm
"""
import binascii, copy,serial,crcmod

def get_index(ob, data):
    '''

    :param ob: 待检索目标字符串
    :param data: 待检索目标对象
    :return: 目标字符串在目标对象中的重复出现位置
    '''
    index_list = []
    copy_data = copy.deepcopy(data)
    while True:
        if copy_data.find(ob) != -1:
            index_list.append(copy_data.find(ob))
            copy_data = copy_data[:copy_data.find(ob)] + 'X'*len(ob) + copy_data[copy_data.find(ob) + len(ob):]
        else:
            break
    return index_list

# CRC校验码
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


# 将报文和CRC校验码组合
def message_combination(bit_of_data, address_code):
    opcode = address_code + ' ' + bit_of_data
    complete_message = crc16Add(opcode)
    return complete_message

class DB(object):
    def __init__(self,device_name):
        self.device_name=device_name

    # 组合报文，根据所需的功能进行发送
    def combination_message(self, address, function_name,new_address='01'):
        print(self.device_name)
        # 安科瑞
        if 'AMC' in self.device_name:
            return self.ankerui(function_name).combination_type(address, self.device_name)
        # 纳宇
        elif 'NAYU' in self.device_name:
            return self.nayu(function_name).combination_type(address, self.device_name)
        # 华诺
        elif 'HN' in self.device_name:
            return self.huanuo(function_name).combination_type(address, self.device_name)
        # 雅达
        elif 'YADA' in self.device_name:
            return self.yada(function_name,new_address).combination_type(address, self.device_name)
        # 欣灵
        elif 'CLIN' in self.device_name:
            return self.xinling(function_name).combination_type(address, self.device_name)

    # 对电表返回的报文进行类型分析和解析
    def analysis_message(self, combination_message, recv_message, function_name):
        # 安科瑞
        if 'AMC' in self.device_name:
            return self.ankerui(function_name).analysis_type(combination_message, recv_message, self.device_name)
        # 纳宇
        elif 'NAYU' in self.device_name:
            return self.nayu(function_name).analysis_type(combination_message, recv_message, self.device_name)
        # 华诺
        elif 'HN' in self.device_name:
            return self.huanuo(function_name).analysis_type(combination_message, recv_message, self.device_name)

        # 雅达
        elif 'YADA' in self.device_name:
            return self.yada(function_name).analysis_type(combination_message, recv_message, self.device_name)
        # 欣灵
        elif 'CLIN' in self.device_name:
            return self.xinling(function_name).analysis_type(combination_message, recv_message, self.device_name)

    # 安科瑞类，包含发送报文，解析报文
    class ankerui():
        def __init__(self,function_name):
            self.function_name=function_name

        # 发送相应功能码的报文
        def combination_type(self, address_code, device_name):
            if device_name == 'AMC72LE4C':
                if self.function_name == 'DDS':
                    bit_of_data = '03 00 47 00 02'
                    return message_combination(bit_of_data, address_code)
            elif device_name == 'AMC72LE4':
                if self.function_name == 'DDS':
                    bit_of_data = '03 00 70 00 02'
                    return message_combination(bit_of_data, address_code)
            else:
                return 'No this device agreement!!'

        # 解析相应功能码的报文
        def analysis_type(self, combination_message, recv_message,device_name):
            if self.function_name=='DDS':
                judge_messg_position = combination_message.replace(' ', '')[:4] + '04'
                if len(recv_message) == 18 and recv_message[:6] == judge_messg_position:
                    recv_message = recv_message
                elif recv_message.find(judge_messg_position) != -1:
                    correct_position = get_index(judge_messg_position, recv_message)[-1]
                    recv_message = recv_message[correct_position:correct_position + 18]
                else:
                    recv_message = 'error message'
                if recv_message != 'error message':
                    if device_name == 'AMC72LE4C':
                        data_16 = recv_message[6:14]
                        data_2 = bin(int(data_16, 16))[2:]
                        zhishu = int(data_2[0:8], 2)
                        weishu = int(data_2[8:], 2)
                        electric = pow(2, zhishu - 127) * (1 + weishu / pow(2, 23))/1000
                        return electric
                    elif device_name == 'AMC72LE4':
                        data_16 = recv_message[6:14]
                        electric = int(data_16, 16) / 100
                        return electric
                    else:
                        return None
                else:
                    return -1
    # 纳宇类，包括发送报文，解析报文
    class nayu():
        def __init__(self,function_name):
            self.function_name=function_name

        # 发送相应功能码的报文
        def combination_type(self, address_code, device_name):
            if device_name == 'NAYUJZDTS125':
                if self.function_name == 'DDS':
                    bit_of_data = '03 01 56 00 02'
                    return message_combination(bit_of_data, address_code)
            elif device_name == 'NAYUHBD380':
                if self.function_name == 'DDS':
                    bit_of_data = '03 01 56 00 02'
                    return message_combination(bit_of_data, address_code)
            else:
                return 'No this device agreement!!'

        # 解析相应功能码的报文
        def analysis_type(self, combination_message, recv_message,device_name):
            if self.function_name=='DDS':
                judge_messg_position = combination_message.replace(' ', '')[:4] + '04'
                if len(recv_message) == 18 and recv_message[:6] == judge_messg_position:
                    recv_message = recv_message
                elif recv_message.find(judge_messg_position) != -1:
                    correct_position = get_index(judge_messg_position, recv_message)[-1]
                    recv_message = recv_message[correct_position:correct_position + 18]
                else:
                    recv_message = 'error message'
                if recv_message != 'error message':
                    if device_name == 'NAYUJZDTS125':
                        data_16 = recv_message[6:14]
                        electric = int(data_16, 16) / 100
                        return electric
                    elif device_name == 'NAYUHBD380':
                        data_16 = recv_message[6:14]
                        data_2 = bin(int(data_16, 16))[2:]
                        zhishu = int(data_2[0:8], 2)
                        weishu = int(data_2[8:], 2)
                        electric = pow(2, zhishu - 127) * (1 + weishu / pow(2, 23))  #
                        return electric
                    else:
                        return None
                else:
                    return -1

    # 华诺类，包含发送报文，解析报文
    class huanuo():
        def __init__(self,function_name):
            self.function_name=function_name

        # 发送相应功能码的报文
        def combination_type(self, address_code, device_name):
            if device_name == 'HN70E7S3':
                if self.function_name == 'DDS':
                    bit_of_data = '03 00 34 00 02'
                    return message_combination(bit_of_data, address_code)
            else:
                return 'No this device agreement!!'

        # 解析相应功能码的报文
        def analysis_type(self, combination_message, recv_message,device_name):
            if self.function_name=='DDS':
                judge_messg_position = combination_message.replace(' ', '')[:4] + '04'
                if len(recv_message) == 18 and recv_message[:6] == judge_messg_position:
                    recv_message = recv_message
                elif recv_message.find(judge_messg_position) != -1:
                    correct_position = get_index(judge_messg_position, recv_message)[-1]
                    recv_message = recv_message[correct_position:correct_position + 18]
                else:
                    recv_message = 'error message'
                if recv_message != 'error message':
                    if device_name == 'HN70E7S3':
                        data_16 = recv_message[6:14]
                        data_2 = bin(int(data_16, 16))[2:]
                        zhishu = int(data_2[0:8], 2)
                        weishu = int(data_2[8:], 2)
                        electric = pow(2, zhishu - 127) * (1 + weishu / pow(2, 23))
                        return electric
                    else:
                        return None
                else:
                    return -1

    # 雅达类，包括发送报文，解析报文
    class yada():
        def __init__(self,function_name,new_address):
            self.function_name=function_name
            self.new_address=new_address

        # 发送相应功能码的报文
        def combination_type(self, address_code, device_name):
            if device_name == 'YADA336D':
                # 询电度数
                if self.function_name == 'DDS':
                    bit_of_data = '03 00 00 00 02'
                    return message_combination(bit_of_data, address_code)
                # 设置通信参数，波特率和校验位
                elif self.function_name == 'SETcomm':
                    bit_of_data = '06 02 26 01 40'
                    return message_combination(bit_of_data, address_code)
                elif self.function_name == 'SETaddress':
                    bit_of_data = '06 01 fb 00 '+self.new_address
                    return message_combination(bit_of_data, address_code)
            else:
                return 'No this device agreement!!'

        # 解析相应功能码的报文
        def analysis_type(self, combination_message, recv_message,device_name):
            if self.function_name == 'DDS':
                judge_messg_position = combination_message.replace(' ', '')[:4] + '04'
                if len(recv_message) == 18 and recv_message[:6] == judge_messg_position:
                    recv_message = recv_message
                elif recv_message.find(judge_messg_position) != -1:
                    correct_position = get_index(judge_messg_position, recv_message)[-1]
                    recv_message = recv_message[correct_position:correct_position + 18]
                else:
                    recv_message = 'error message'
                if recv_message != 'error message':
                    if device_name == 'YADA336D':
                        data_16 = recv_message[6:14]
                        electric = int(data_16, 16) / 100
                        return electric
                    else:
                        return None
                else:
                    return -1
            elif self.function_name == 'SETcomm':
                if combination_message==recv_message:
                    print("通信参数设置成功")
                else:
                    print("通信参数设置失败")
            elif self.function_name == 'SETaddress':
                if combination_message==recv_message:
                    print("地址设置成功")
                else:
                    print("地址设置失败")

    # 欣灵类，包含发送报文，解析报文
    class xinling():
        def __init__(self,function_name):
            self.function_name=function_name

        # 发送相应功能码的报文
        def combination_type(self, address_code, device_name):
            if device_name == 'CLINHCD1949S4':
                if self.function_name == 'DDS':
                    bit_of_data = '03 00 37 00 04'
                    return message_combination(bit_of_data, address_code)
            else:
                return 'No this device agreement!!'

        # 解析相应功能码的报文
        def analysis_type(self, combination_message, recv_message,device_name):
            if self.function_name=='DDS':
                judge_messg_position = combination_message.replace(' ', '')[:4] + '08'
                if len(recv_message) == 18 and recv_message[:6] == judge_messg_position:
                    recv_message = recv_message
                elif recv_message.find(judge_messg_position) != -1:
                    correct_position = get_index(judge_messg_position, recv_message)[-1]
                    recv_message = recv_message[correct_position:correct_position + 18]
                else:
                    recv_message = 'error message'
                if recv_message != 'error message':
                    if device_name == 'CLINHCD1949S4':
                        data_16 = recv_message[6:14]
                        data_2 = bin(int(data_16, 16))[2:]
                        zhishu = int(data_2[0:8], 2)
                        weishu = int(data_2[8:], 2)
                        electric = pow(2, zhishu - 127) * (1 + weishu / pow(2, 23))  #
                        return electric
                    else:
                        return None
                else:
                    return -1

'''
参数1：电表：AMC72LE4C, AMC72LE4, NAYUJZDTS125, NAYUHBD380, HN70E7S3, YADA336D
参数2：DDS:查询电度数, SETaddress:设置通信地址, SETcomm:设置波特率9600，无校验码
参数3：通信地址
'''
ser = serial.Serial("COM3",9600,parity=serial.PARITY_NONE,timeout=0.5)

a=DB('AMC72LE4C')
b=a.combination_message('02','DDS')
print(b)
#发报文
b=bytes.fromhex(b)
ser.write(b)
receive_message = (ser.readline())
receive_message=binascii.b2a_hex(receive_message)
print(receive_message)
#解析报文
print(DB.analysis_message('',receive_message))
