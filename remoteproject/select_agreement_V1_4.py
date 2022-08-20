# -*- coding: utf-8 -*-
""" 
@Time : 2021/8/16 10:48
@Author : DingKun
@FileName: select_agreement_V1.3.py
@SoftWare: PyCharm
"""
import crcmod, binascii, copy ,serial

# 生成CRC16-MODBUS校验码

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
    #print(index_list)
    return index_list

def crc16Add(read):
    if type(read)==bytes:#如果read为十六进制b'',转化为str
        read=binascii.b2a_hex(read).decode()
    elif type(read)==str:#如果read为str，不变
        read=read
    crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xFFFF, xorOut=0x0000)
    data = read.replace(" ", "") #消除空格
    readcrcout = hex(crc16(binascii.unhexlify(data))).upper()
    str_list = list(readcrcout)
    # print(str_list)
    if len(str_list) == 5:
        str_list.insert(2, '0')  # 位数不足补0，因为一般最少是5个
    crc_data = "".join(str_list) #用""把数组的每一位结合起来  组成新的字符串
    # print(crc_data)
    crc = read.strip() + crc_data[4:] + crc_data[2:4] #把源代码和crc校验码连接起来
    return crc

# 将报文和CRC校验码组合
def message_combination(bit_of_data, address_code):
    opcode = address_code + ' ' + bit_of_data
    complete_message = crc16Add(opcode)
    return complete_message

#############################################################电表报文匹配
class agreement_DB(object):
    def __init__(self, device_name):
        self.device_name = device_name

    def combination_message(self, address_code, function_name):
        #print(self.device_name)
        if 'AMC' in self.device_name:
            return self.ankerui(function_name).combination_type(address_code, self.device_name)
        elif 'HN' in self.device_name:
            return self.huanuo(function_name).combination_type(address_code, self.device_name)
        elif 'YADA' in self.device_name:
            return self.yadadtsd(function_name).combination_type(address_code, self.device_name)
        elif 'NAYU' in self.device_name:
            return self.nayu(function_name).combination_type(address_code, self.device_name)
        elif 'HT' in self.device_name:
            return self.huatong(function_name).combination_type(address_code, self.device_name)
        elif 'SHD' in self.device_name:
            return self.huadong(function_name).combination_type(address_code, self.device_name)


    def analysis_message(self, combination_message, recv_message, function_name):
        if 'AMC' in self.device_name:
            return self.ankerui(function_name).analysis_type(combination_message, recv_message, self.device_name)
        elif 'HN' in self.device_name:
            return self.huanuo(function_name).analysis_type(combination_message, recv_message, self.device_name)
        elif 'YADA' in self.device_name:
            return self.yadadtsd(function_name).analysis_type(combination_message, recv_message, self.device_name)
        elif 'NAYU' in self.device_name:
            return self.nayu(function_name).analysis_type(combination_message, recv_message, self.device_name)
        elif 'HT' in self.device_name:
            return self.huatong(function_name).analysis_type(combination_message, recv_message, self.device_name)
        elif 'SHD' in self.device_name:
            return self.huadong(function_name).analysis_type(combination_message, recv_message, self.device_name)

    ######安科瑞
    class ankerui():
        def __init__(self, function_name):
            self.function_name = function_name
        ##########################################生成完整的待发送报文数据
        ##选择发送报文类型
        def combination_type(self, address_code, device_name):
            if device_name == 'AMC72LE4C' or device_name == 'AMCPZ80':
                if self.function_name == 'DDS':
                    bit_of_data = '03 00 47 00 02'
                    return message_combination(bit_of_data, address_code)
            elif device_name == 'AMC72LE4':
                if self.function_name == 'DDS':
                    bit_of_data = '03 00 70 00 02'
                    return message_combination(bit_of_data, address_code)
            elif device_name == 'AMCDTSD1352':
                if self.function_name == 'DDS':
                    bit_of_data = '03 00 0A 00 02'
                    return message_combination(bit_of_data, address_code)
            elif device_name == 'AMCADL400':
                if self.function_name == 'DDS':
                    bit_of_data = '03 00 00 00 02'
                    return message_combination(bit_of_data, address_code)
            elif device_name == 'AMC72LE4Cpow':
                if self.function_name == 'DDS':
                    bit_of_data = '03 00 31 00 18'
                    return message_combination(bit_of_data, address_code)
            else:
                return -1

        ##########################################根据接收到的报文解析数据
        def analysis_type(self, combination_message, recv_message, device_name):
            # 解析电表度数 字符长度18
            judge_messg_position = combination_message.replace(' ','')[:4] + '04'   ##04是字节数
            if len(recv_message) == 18 and recv_message[:6] == judge_messg_position:
                recv_message = recv_message
            elif recv_message.find(judge_messg_position) != -1:
                correct_position = get_index(judge_messg_position, recv_message)[-1]
                recv_message = recv_message[correct_position:correct_position+18]
            else:
                recv_message = 'error message'

            if recv_message != 'error message':
                if device_name == 'AMC72LE4C':
                    if self.function_name == 'DDS':
                        data_16 = recv_message[6:14]
                        if data_16=='00000000':
                            electric=0.0
                        else:
                            data_2 = bin(int(data_16, 16))[2:]
                            zhishu = int(data_2[0:8], 2)
                            weishu = int(data_2[8:], 2)
                            electric = pow(2, zhishu - 127) * (1 + weishu / pow(2, 23)) / 1000  #
                        return [electric]
                elif device_name == 'AMCPZ80':
                    if self.function_name == 'DDS':
                        data_16 = recv_message[6:14]
                        if data_16=='00000000':
                            electric=0.0
                        else:
                            data_2 = bin(int(data_16, 16))[2:]
                            zhishu = int(data_2[0:8], 2)
                            weishu = int(data_2[8:], 2)
                            electric = pow(2, zhishu - 127) * (1 + weishu / pow(2, 23))  #
                        return [electric]
                elif device_name == 'AMC72LE4' or device_name == 'AMCDTSD1352' or device_name=='AMCADL400':
                    if self.function_name == 'DDS':
                        data_16 = recv_message[6:14]
                        electric = int(data_16, 16) / 100
                        return [electric]
                elif device_name=='AMC72LE4Cpow':
                    if self.function_name == 'DDS':
                        data_power = recv_message[6:10]
                        data_electric = recv_message[-12:4]
                        power = int(data_power, 16) / 10
                        if data_electric == '00000000':
                            electric = 0.0
                        else:
                            data_2 = bin(int(data_electric, 16))[2:]
                            zhishu = int(data_2[0:8], 2)
                            weishu = int(data_2[8:], 2)
                            electric = pow(2, zhishu - 127) * (1 + weishu / pow(2, 23)) / 1000  #
                        return [electric, power]
                else:
                    return None
            else:
                return -1
    ######################################
    class huanuo():
        def __init__(self, function_name):
            self.function_name = function_name

        ##########################################生成完整的待发送报文数据
        ##选择发送报文类型
        def combination_type(self, address_code, device_name):
            if device_name == 'HN70E7S3':
                if self.function_name == 'DDS':
                    bit_of_data = '03 00 34 00 02'
                    return message_combination(bit_of_data, address_code)
            else:
                return 'No this device agreement!!'


        ##########################################根据接收到的报文解析数据
        def analysis_type(self, combination_message, recv_message, device_name):
            # 解析电表度数 字符长度18
            judge_messg_position = combination_message.replace(' ', '')[:4] + '04'
            if len(recv_message) == 18 and recv_message[:6] == judge_messg_position:
                recv_message = recv_message
            elif recv_message.find(judge_messg_position) != -1:
                correct_position = get_index(judge_messg_position, recv_message)[-1]
                recv_message = recv_message[correct_position:correct_position + 18]
            else:
                recv_message = 'error message'

            if recv_message != 'error message':
                if self.function_name == 'DDS':
                    recv_message = recv_message[:6] + recv_message[10:14] + recv_message[6:10]
                    #print(recv_message)
                    data_16 = recv_message[6:14]
                    if data_16 == '00000000':
                        electric = 0.0
                    else:
                        data_2 = bin(int(data_16, 16))[2:]
                        zhishu = int(data_2[0:8], 2)
                        weishu = int(data_2[8:], 2)
                        electric = pow(2, zhishu - 127) * (1 + weishu / pow(2, 23))  #
                    return [electric]
                else:
                    return None
            else:
                return -1
    ######################################
    class yadadtsd():
        def __init__(self, function_name):
            self.function_name = function_name

        ##########################################生成完整的待发送报文数据
        ##选择发送报文类型
        def combination_type(self, address_code, device_name):
            if device_name == 'YADA336D':
                if self.function_name == 'DDS':
                    bit_of_data = '03 00 00 00 02'
                    return message_combination(bit_of_data, address_code)
            else:
                return 'No this device agreement!!'

        ##########################################根据接收到的报文解析数据
        def analysis_type(self, combination_message, recv_message, device_name):
            # 解析电表度数 字符长度18
            judge_messg_position = combination_message.replace(' ', '')[:4] + '04'   ##04是字节数
            #print('***********'+len(recv_message),recv_message[:6],judge_messg_position)
            if len(recv_message) == 18 and recv_message[:6] == judge_messg_position:
                recv_message = recv_message
            elif recv_message.find(judge_messg_position) != -1:
                correct_position = get_index(judge_messg_position, recv_message)[-1]
                recv_message = recv_message[correct_position:correct_position + 18]
            else:
                recv_message = 'error message'

            if recv_message != 'error message':
                if self.function_name == 'DDS':
                    data_16 = recv_message[6:14]#
                    electric = int(data_16, 16) / 100#
                    return [electric]
                else:
                    return None
            else:
                return -1
    ######################################

##########################################纳宇电表
    class nayu():
        def __init__(self,function_name):
            self.function_name=function_name

        # 发送相应功能码的报文
        def combination_type(self, address_code, device_name):
            if device_name == 'NAYUJZDTS125':
                if self.function_name == 'DDS':
                    bit_of_data = '03 01 56 00 02'
                    return message_combination(bit_of_data, address_code)
            elif device_name == 'NAYUDTS96K':
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
                        electric = int(data_16, 16) / 10
                        return [electric]
                    elif device_name == 'NAYUDTS96K':
                        data_16 = recv_message[6:14]
                        electric = int(data_16, 16) / 10
                        return [electric]
                    else:
                        return None
                else:
                    return -1

###################华通
    class huatong():
        def __init__(self, function_name):
            self.function_name = function_name

        ##########################################生成完整的待发送报文数据
        ##选择发送报文类型
        def combination_type(self, address_code, device_name):
            if device_name == 'HTBR963E':
                if self.function_name == 'DDS':
                    bit_of_data = '03 00 81 00 02'
                    return message_combination(bit_of_data, address_code)
            else:
                return 'No this device agreement!!'

        ##########################################根据接收到的报文解析数据
        def analysis_type(self, combination_message, recv_message, device_name):
            # 解析电表度数 字符长度18
            judge_messg_position = combination_message.replace(' ', '')[:4] + '04'   ##04是字节数
            #print('***********'+len(recv_message),recv_message[:6],judge_messg_position)
            if len(recv_message) == 18 and recv_message[:6] == judge_messg_position:
                recv_message = recv_message
            elif recv_message.find(judge_messg_position) != -1:
                correct_position = get_index(judge_messg_position, recv_message)[-1]
                recv_message = recv_message[correct_position:correct_position + 18]
            else:
                recv_message = 'error message'

            if recv_message != 'error message':
                if self.function_name == 'DDS':
                    data_16 = recv_message[6:14]
                    if data_16=='00000000':
                        electric=0.0
                    else:
                        data_2 = bin(int(data_16, 16))[2:]
                        zhishu = int(data_2[0:8], 2)
                        weishu = int(data_2[8:], 2)
                        electric = pow(2, zhishu - 127) * (1 + weishu / pow(2, 23))
                    return [electric]
                else:
                    return None
            else:
                return -1
###############华东
    class huadong():
        def __init__(self, function_name):
            self.function_name = function_name

        ##########################################生成完整的待发送报文数据
        ##选择发送报文类型
        def combination_type(self, address_code, device_name):
            if device_name == 'SHD963E':
                if self.function_name == 'DDS':
                    bit_of_data = '03 00 1D 00 02'
                    return message_combination(bit_of_data, address_code)
            else:
                return 'No this device agreement!!'


        ##########################################根据接收到的报文解析数据
        def analysis_type(self, combination_message, recv_message, device_name):
            # 解析电表度数 字符长度18
            judge_messg_position = combination_message.replace(' ', '')[:4] + '04'
            if len(recv_message) == 18 and recv_message[:6] == judge_messg_position:
                recv_message = recv_message
            elif recv_message.find(judge_messg_position) != -1:
                correct_position = get_index(judge_messg_position, recv_message)[-1]
                recv_message = recv_message[correct_position:correct_position + 18]
            else:
                recv_message = 'error message'

            if recv_message != 'error message':
                if self.function_name == 'DDS':
                    #print(recv_message)
                    data_16 = recv_message[6:14]
                    electric = int(data_16, 16) *0.8
                    return [electric]
                else:
                    return None
            else:
                return -1


#######################################################断路器报文匹配
class agreement_DLQ(object):
    def __init__(self, device_name):
        self.device_name = device_name

    def combination_message(self, address_code, function_name):
        if 'MDQ' in self.device_name:
            return self.maiduoqi(function_name).combination_type(address_code, self.device_name)

    def analysis_message(self, recv_message, function_name):
        if 'MDQ' in self.device_name:
            return self.maiduoqi(function_name).analysis_type(recv_message, self.device_name)

    class maiduoqi():
        def __init__(self, function_name):
            self.function_name = function_name
        ##########################################生成完整的待发送报文数据
        ##选择发送报文类型
        def combination_type(self, address_code, device_name):
            if device_name == 'MDQ':
                if self.function_name == 'cut':
                    bit_of_data = '05 00 01 FF 00'
                    return message_combination(bit_of_data, address_code)
                elif self.function_name == 'open':
                    bit_of_data = '05 00 01 00 00'
                    return message_combination(bit_of_data, address_code)
                elif self.function_name == 'status':
                    bit_of_data = '01 00 01 00 01'
                    return message_combination(bit_of_data, address_code)
                else:
                    return None
            else:
                return -1


        ##########################################根据接收到的报文解析数据
        ##解析断路器状态
        def analysis_type(self, recv_message, device_name):
            if device_name == 'MDQ':
                if self.function_name == 'status':
                    status = recv_message[6:8]
                    return status
            else:
                return -1

#7,9,10,12,16,
# crc = crc16Add('070300340002')
# print('crc',crc)
# ser = serial.Serial("COM4", 9600, parity=serial.PARITY_NONE,timeout=0.5)
# ser.write(b'\x07\x03\x00\x34\x00\x02\x85\xa3')
# receive_message = (ser.readline())
# receive_message=binascii.b2a_hex(receive_message)
#
# print('receive_message',receive_message)
# d = receive_message
# d = d.decode()
# a = agreement_DB('YADADTS336D') #设备协议类初始化----
# b = a.combination_message('05', 'DDS')  # 根据功能和地址获取完整的报文数据
# print('combination',b)
#c = a.analysis_message(b, d, 'DDS')
#print('analysis',c)