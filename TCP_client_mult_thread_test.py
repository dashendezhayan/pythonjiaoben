# -*- coding: utf-8 -*-
""" 
@Time : 2021/8/3 13:36
@Author : DingKun
@FileName: TCP_client_mult_thread_test.py
@SoftWare: PyCharm
"""
import binascii
import socket
import time
from color2cmd import Color
from threading import Thread
def get_NameCode(display_content):
    name_code = {'001':'',
                 '003':'',
                 '002': ''}

    if display_content == 1:
        for i in name_code.keys():
            clr.print_green_text(name_code[i]+': '+i)
    elif display_content == 0:
        return name_code
clr = Color()
################客户端##################
op_code = {}
op_code['3'] = 'SeeConnectedName'
# # 创建socket对象
client_send = socket.socket()
client_name = 'controller02-'
# 确定IP
ip_port = ("123.60.71.211", 8888)
#检验是否含有中文字符
def is_contains_chinese(strs):
    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            return True
    return False
# 建立客户端链接
def is_connect():
    try:
        client_send.connect(ip_port)

    except:
        clr.print_green_text('当前用户：'+client_name)
        clr.print_red_text('服务器未启动!!')
        return False

    else:
        clr.print_green_text('当前用户：' + client_name)
        data = client_send.recv(1024)
        clr.print_green_text('服务端消息：'+str(data.decode(encoding='utf8')))#print('服务端消息：', data.decode(encoding='utf8'))
        client_send.sendall(bytes(client_name, encoding="utf-8"))
        return True


def message_handle(client_send):
    """
    消息处理

    """
    while True:
        data = client_send.recv(1024)
        if data == b'':
            clr.print_red_text('服务端已退出！！')
            break

        else:
            data = data.decode(encoding='utf-8')
            if '_' in data: #服务器回传的
                total_control_code = data.split('_')[0]
                current_control_code = int(data.split('_')[1])
                message = data.split('_')[2]
                value = message[6:8]
                clr.print_green_text('共计' + total_control_code + '个断路器')
                if value == '01':
                    clr.print_green_text('当前第'+str(current_control_code)+'个断路器合闸成功！！')
                elif value == '00':
                    clr.print_green_text('当前第'+str(current_control_code)+'个断路器分闸成功！！')
                else:
                    clr.print_red_text('当前第' + str(current_control_code) + '个断路器分闸失败！！')
            else:
                clr.print_green_text('服务端消息：' + data)


if __name__ == '__main__':
    if is_connect():
        ##############消息接收线程
        thread = Thread(target=message_handle, args=(client_send,))
        # 设置成守护线程
        thread.setDaemon(True)
        thread.start()
        ##############
        while True:
            msg = input('''
    步骤1---->输入1：查看现有场站名称编码
    步骤2---->输入2：开始执行控制操作
    其他 ---->输入3：查看已连接至服务器的场站信息
    其他 ---->输入exit：退出控制程序
    输入后请按下回车键或Enter键完成此步操作！！！
                        ''')
            if msg == '1':
                get_NameCode(display_content=1)
                continue
            elif msg == '2':

                code = input('''
    请输入将要断电的充电站名称编码
    输入后请按下回车键或Enter键完成此步操作！！！    
                            ''')
                #print(code.rjust(40))
                code_list = [i for i in get_NameCode(display_content=0).keys()]
                #print(code_list)
                if code not in code_list:
                    while code not in code_list:
                        clr.print_red_text('输入场站的编码有误，请查看以下编码内容重新确认')
                        get_NameCode(display_content=1)
                        code =  input('''
    请输入将要断电的充电站名称编码……
    输入后请按下回车键或Enter键完成此步操作！！！    
                                ''')
                        #print(code.rjust(40))
                if code in code_list:
                    name = get_NameCode(display_content=0)[code]
                    clr.print_red_text('您当前选择的断电执行对象为：' + name)#print('您当前选择的断电执行对象为：', name)#print('您当前选择的断电执行对象为：', Fore.BLACK+Back.YELLOW+name+Style.RESET_ALL)
                    result_list = ['cut','do nothing','open']
                    result = input('''
    输入cut：立即执行断电操作
    输入do nothing：撤销断电进程
    输入后请按下回车键或Enter键完成此步操作！！！    
                                        ''')
                    #print(result.rjust(40))
                    if result not in result_list:
                        while result not in result_list:
                            clr.print_red_text('控制指令输入有误，请查看控制指令确认后重新输入')#print('控制指令输入有误，请查看控制指令确认后重新输入')
                            result = input('''
    输入cut：立即执行断电操作
    输入do nothing：撤销断电进程3
    输入后请按下回车键或Enter键完成此步操作！！！    
                                            ''')
                            #print(result.rjust(40))
                    if result in result_list:
                        if result  == 'open' or result  == 'cut':
                            clr.print_red_text('开始对'+name+'执行合闸操作……')#print("开始对",name,'执行断电操作')#print("开始对",Fore.BLACK+Back.YELLOW+name+Style.RESET_ALL,'执行断电操作')
                            control_code = name +'DLQ' + result
                            client_send.sendall(bytes(control_code, encoding="utf-8"))
                            #time.sleep(0.5)
                        elif result == 'do nothing':
                            continue
            elif msg == "exit":
                client_send.sendall(bytes(msg+'-'+client_name, encoding="utf-8"))
                client_send.close()
                break
            elif msg == '3':
                op = op_code['3']
                client_send.sendall(bytes(op, encoding="utf-8"))
            elif msg not in ['1', '2', '3',"exit"]:
                clr.print_red_text('输入指令有误，请重新输入！！！')#print('输入指令有误，请重新输入！！！')
                continue
    else:
        time_all = 8
        while time_all > 1:
            clr.print_green_text('程序将在%s秒后退出' % (time_all - 1))
            time.sleep(1)
            time_all = time_all - 1