# -*- coding: utf-8 -*-
""" 
@Time : 2021/7/29 11:01
@Author : DingKun
@FileName: select_agreement.py
@SoftWare: PyCharm
"""
import crcmod, binascii


# 生成CRC16-MODBUS校验码
def crc16Add(agreement_str):
    crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xFFFF, xorOut=0x0000)
    data = agreement_str.replace(" ", "")  # 消除空格
    readcrcout = hex(crc16(binascii.unhexlify(data))).upper()
    str_list = list(readcrcout)
    # print(str_list)
    if len(str_list) == 5:
        str_list.insert(2, '0')  # 位数不足补0，因为一般最少是5个
    crc_data = "".join(str_list)  # 用""把数组的每一位结合起来  组成新的字符串
    # print(crc_data)
    crc = agreement_str.strip() + ' ' + crc_data[4:] + ' ' + crc_data[2:4]  # 把源代码和crc校验码连接起来
    return crc
#############################################################电表报文匹配
class agreement_DB(object):
    def __init__(self, device_name):
        self.device_name = device_name

    def combination_message(self, address_code, function_name):
        if self.device_name == 'AKR':

            details_method = self.ankerui(function_name).combination_type(address_code)

            return details_method

    def analysis_message(self, recv_message, function_name):
        if self.device_name == 'AKR':
            if function_name == 'DDS':
                return self.ankerui(function_name).Electric_degree(recv_message)

    class ankerui():
        def __init__(self, function_name):
            self.function_name = function_name
        ##########################################生成完整的待发送报文数据
        ##选择发送报文类型
        def combination_type(self, address_code):
            if self.function_name == 'DDS':
                bit_of_data = '03 00 47 00 02'
                return self.message_combination(bit_of_data, address_code)

        ##根据报文地址位+功能位+数据位生成校验码
        def message_combination(self, bit_of_data, address_code):
            opcode = address_code + ' ' + bit_of_data
            Complete_message = crc16Add(opcode)
            return Complete_message

        ##########################################根据接收到的报文解析数据
        ##解析电表度数
        def Electric_degree(self, recv_message):
            data_16 = recv_message[6:14]
            data_2 = bin(int(data_16, 16))[2:]
            zhishu = int(data_2[0:8], 2)
            weishu = int(data_2[8:], 2)
            electric = pow(2, zhishu - 127) * (1 + weishu / pow(2, 23)) / 1000  #
            return electric
#######################################################断路器报文匹配
class agreement_DLQ(object):
    def __init__(self, device_name):
        self.device_name = device_name

    def combination_message(self, address_code, function_name):
        if self.device_name == 'MDQ':

            details_method = self.maiduoqi(function_name).combination_type(address_code)

            return details_method

    def analysis_message(self, recv_message, function_name):
        if self.device_name == 'MDQ':
            if function_name == 'status':
                return self.maiduoqi(function_name).status_infors(recv_message)

    class maiduoqi():
        def __init__(self, function_name):
            self.function_name = function_name
        ##########################################生成完整的待发送报文数据
        ##选择发送报文类型
        def combination_type(self, address_code):
            if self.function_name == 'close':
                bit_of_data = '05 00 01 FF 00'
                return self.message_combination(bit_of_data, address_code)
            elif self.function_name == 'open':
                bit_of_data = '05 00 01 00 00'
                return self.message_combination(bit_of_data, address_code)
            elif self.function_name == 'status':
                bit_of_data = '01 00 01 00 01'
                return self.message_combination(bit_of_data, address_code)
            else:
                return None

        ##根据报文地址位+功能位+数据位生成校验码
        def message_combination(self, bit_of_data, address_code):
            opcode = address_code + ' ' + bit_of_data
            Complete_message = crc16Add(opcode)
            return Complete_message

        ##########################################根据接收到的报文解析数据
        ##解析断路器状态
        def status_infors(self, recv_message):
            status = recv_message[6:8]
            return status





############example
a = agreement_DB('AKR')

b = a.combination_message('01', 'DDS')

c = a.analysis_message('0403044a31a26091ac', 'DDS')

print(b, c)

d = agreement_DLQ('MDQ')

e = d.combination_message('01','open')

f = d.combination_message('01','close')

g = d.combination_message('01','status')

h = d.analysis_message('010101019048', 'status')

print(e,'\n',f,'\n',g,'\n',h)
############