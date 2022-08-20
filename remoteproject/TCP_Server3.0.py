# coding=UTF-8
import datetime
import socket
import threading
import time
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
import calendar
import pymysql
from threading import Thread
import inspect
import ctypes, sys, os
from send_email import send_email
from PropertiesUtil import Properties
from saveimgtosql import writesql, writesql_position_status, connectMysql, position_status_init
from select_agreement_V1_4 import agreement_DB, agreement_DLQ
from En_DE_cryption import *

def refresh_position():
    t1 = time.time()
    position_device_infos = {}
    conn, cursor = connectMysql()
    sql = "SELECT * FROM position_device"
    cursor.execute(sql)
    conn.commit()
    results = cursor.fetchall()
    position_device_infos['all_position'] = []
    for position_infus in results:
        position_device_infos[str(position_infus[0])] = position_infus[1]  # 场站拼音对应中文名称
        position_device_infos[position_infus[1]] = {}  # 场站内的DTU、电表的设备型号、RS485地址
        if '_' in position_infus[2]:
            DLQ_infos = [j for j in position_infus[2].split('_') if 'XX' not in j]
            position_device_infos[position_infus[1]]['DLQ'] = DLQ_infos
        elif 'XX' not in position_infus[2]:
            position_device_infos[position_infus[1]]['DLQ'] = [position_infus[2]]
        else:
            position_device_infos[position_infus[1]]['DLQ'] = []
        if '_' in position_infus[3]:
            DB_infos = [j for j in position_infus[3].split('_') if 'XX' not in j]
            position_device_infos[position_infus[1]]['Strong_DB'] = DB_infos
        elif 'XX' not in position_infus[3]:
            position_device_infos[position_infus[1]]['Strong_DB'] = [position_infus[3]]
        else:
            position_device_infos[position_infus[1]]['Strong_DB'] = []
        if '_' in position_infus[4]:
            DB_infos = [j for j in position_infus[4].split('_') if 'XX' not in j]
            position_device_infos[position_infus[1]]['Weak_DB'] = DB_infos
        elif 'XX' not in position_infus[4]:
            position_device_infos[position_infus[1]]['Weak_DB'] = [position_infus[4]]
        else:
            position_device_infos[position_infus[1]]['Weak_DB'] = []
        position_device_infos[position_infus[1]]['Magnification'] = position_infus[5]
        position_device_infos['all_position'].append(position_infus[1])
    print("初始化场站设备耗时", time.time() - t1)
    t2 = time.time()
    sql2 = "SELECT * FROM count"
    cursor.execute(sql2)
    conn.commit()
    res = cursor.fetchall()
    Controller_list = [j[0] for j in res]
    cursor.close()
    # # 关闭数据库连接
    conn.close()
    print("查询控制端账号名称耗时", time.time() - t2)

    return position_device_infos, Controller_list

def client_infos_init(first_mesg, sock):
    client_name = ''
    end_flag = 0
    try:
        first_mesg.decode(encoding='utf-8')  # 客户端发送的心跳包内容是否能够进行utf-8解码
    except:
        print('非法接入，已删除#1：', first_mesg)
        #sock.close()
        del client_thread_dict[sock]
        end_flag = -1
        print('非法接入，已删除#2' + ",当前线程数目-------->", len(threading.enumerate()))
    else:
        # 只包含站点的心跳包信息
        if first_mesg.decode(encoding='utf-8') in position_device_infos.keys():
            print('接入客户端名称为（已进行utf编码）：', position_device_infos[first_mesg.decode(encoding='utf-8')],
                  type(first_mesg.decode(encoding='utf-8')))
            client_name = position_device_infos[first_mesg.decode(encoding='utf-8')]
            # if client_name in client_thread_dict:
            #     print(client_name + "重复连接，重置线程")
            #     client_thread_dict[client_name][1].shutdown(2)
            #     client_thread_dict[client_name][1].close()
            #     #time.sleep(1)
            #     print(client_name + "线程已重置")
            #     client_thread_dict[client_name] = client_thread_dict[sock]  # client_thread_dict[sock] = [thread, sock]
            #     client_thread_dict[client_name][0].setName(client_name)
            #     del client_thread_dict[sock]
            #     print(client_name + "重置线程接入后当前线程数目-------->", len(threading.enumerate()))
            # else:
            # #  重置sock连接对应的站点名称
            client_thread_dict[client_name] = client_thread_dict[sock]  # client_thread_dict[sock] = [thread, sock]
            client_thread_dict[client_name][0].setName(client_name)
            del client_thread_dict[sock]
            print(client_name + "首次接入后当前线程数目-------->", len(threading.enumerate()))
            # 只包含控制端的心跳包信息
        elif first_mesg.decode(encoding='utf-8') in Controller_list:
            print('接入客户端名称为（已进行utf编码）：', first_mesg.decode(encoding='utf-8'),
                  type(first_mesg.decode(encoding='utf-8')))
            #  重置sock连接对应的控制端名称
            print(client_name + "接入后当前线程数目-------->", len(threading.enumerate()))
            client_name = first_mesg.decode(encoding='utf-8')
            client_thread_dict[client_name] = client_thread_dict[sock]
            client_thread_dict[client_name][0].setName(client_name)
            del client_thread_dict[sock]
        else:
            print('非法接入，已删除#2:', first_mesg, first_mesg.decode(encoding='utf-8'))
            print('非法接入，已删除#2' + ",当前线程数目-------->", len(threading.enumerate()))
            #sock.close()
            del client_thread_dict[sock]
            end_flag = -1

    return end_flag, client_name

def first_send_DLQ_mesg(client_name, data, mesg_combin_DQL): # op_name-操作者名称, ob_name-站点名称, op_code-操作指令
    control_DLQ_infos[data.decode(encoding='utf-8').split('DLQ')[0]] = {}
    control_DLQ_infos[data.decode(encoding='utf-8').split('DLQ')[0]]['ob_name'] = data.decode(encoding='utf-8').split('DLQ')[0]  # 将要操作的场站
    control_DLQ_infos[data.decode(encoding='utf-8').split('DLQ')[0]]['op_code'] = pc.decrypt(data.decode(encoding='utf-8').split('DLQ')[1])  # 将要执行的功能
    control_DLQ_infos[data.decode(encoding='utf-8').split('DLQ')[0]]['control_name'] = client_name
    ob_name, op_code = control_DLQ_infos[data.decode(encoding='utf-8').split('DLQ')[0]]['ob_name'], control_DLQ_infos[data.decode(encoding='utf-8').split('DLQ')[0]]['op_code']
    print('被操作对象名称-->', ob_name)
    if ob_name in client_thread_dict:  # 判断操作对象是否在当前线程池中
        mesg_combin_DQL[ob_name] = {}
        mesg_combin_DQL[ob_name]['action_mesg'] = [agreement_DLQ(i.split('-')[0]).combination_message(i.split('-')[1], op_code) for i
                          in position_device_infos[ob_name]['DLQ']]  # 断路器动作执行报文，”cut“-合闸，”off“-分闸（保留）
        mesg_combin_DQL[ob_name]['status_mesg'] = [agreement_DLQ(i.split('-')[0]).combination_message(i.split('-')[1], 'status') for i
                          in position_device_infos[ob_name]['DLQ']]  # 断路器状态查询报文，”status“-查询断路器状态
        client_thread_dict[ob_name][1].sendall(bytes.fromhex(mesg_combin_DQL[ob_name]['action_mesg'][-1]))  # 执行断路器合闸操作
        client_thread_dict[client_name][1].sendall(bytes(ob_name + '断电指令发送成功！', encoding="utf-8"))
    else:  # 操作对象不在当前线程池中，则判断为未连接至服务器
        print('已连接信息', list(client_thread_dict.keys()))
        client_thread_dict[client_name][1].sendall(bytes(ob_name + '通讯设备处于离线状态！', encoding="utf-8"))

def sendall_DLQ_action_mesg(client_name, data, mesg_combin_DQL):
    control_DLQ_infos[data.decode(encoding='utf-8').split('DLQ')[0]] = {}
    control_DLQ_infos[data.decode(encoding='utf-8').split('DLQ')[0]]['ob_name'] = \
    data.decode(encoding='utf-8').split('DLQ')[0]  # 将要操作的场站
    control_DLQ_infos[data.decode(encoding='utf-8').split('DLQ')[0]]['op_code'] = pc.decrypt(
        data.decode(encoding='utf-8').split('DLQ')[1])  # 将要执行的功能
    control_DLQ_infos[data.decode(encoding='utf-8').split('DLQ')[0]]['control_name'] = client_name
    ob_name, op_code = control_DLQ_infos[data.decode(encoding='utf-8').split('DLQ')[0]]['ob_name'], \
                       control_DLQ_infos[data.decode(encoding='utf-8').split('DLQ')[0]]['op_code']
    print('被操作对象名称-->', ob_name)
    if ob_name in client_thread_dict:  # 判断操作对象是否在当前线程池中
        mesg_combin_DQL[ob_name] = {}
        mesg_combin_DQL[ob_name]['action_mesg'] = [
            agreement_DLQ(i.split('-')[0]).combination_message(i.split('-')[1], op_code) for i
            in position_device_infos[ob_name]['DLQ']]  # 断路器动作执行报文，”cut“-合闸，”off“-分闸（保留）
        mesg_combin_DQL[ob_name]['status_mesg'] = [
            agreement_DLQ(i.split('-')[0]).combination_message(i.split('-')[1], 'status') for i
            in position_device_infos[ob_name]['DLQ']]  # 断路器状态查询报文，”status“-查询断路器状态
        mesg_combin_DQL[ob_name]['handle_status'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for ID in mesg_combin_DQL[ob_name]['action_mesg'][::-1]:
            client_thread_dict[ob_name][1].sendall(bytes.fromhex(ID))  # 执行断路器合闸操作
            time.sleep(1)
        mesg_combin_DQL[ob_name]['handle_status'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        mesg_combin_DQL[ob_name]['handle_nums'] = []
        del mesg_combin_DQL[ob_name]['action_mesg']
        client_thread_dict[client_name][1].sendall(bytes(ob_name + '断电指令发送成功！', encoding="utf-8"))
        time.sleep(1)
        mesg_combin_DQL[ob_name]['handle_status'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        client_thread_dict[ob_name][1].sendall(bytes.fromhex(mesg_combin_DQL[ob_name]['status_mesg'][-1]))  # 执行断路器状态查询操作
    else:  # 操作对象不在当前线程池中，则判断为未连接至服务器
        print('已连接信息', list(client_thread_dict.keys()))
        client_thread_dict[client_name][1].sendall(bytes(ob_name + '通讯设备处于离线状态！', encoding="utf-8"))


def all_DLQ_status_judge(client_name, hex_bytes, mesg_combin_DQL, control_DLQ_infos):
    ob_name = control_DLQ_infos[client_name]['ob_name']
    control_name = control_DLQ_infos[client_name]['control_name']
    hex_bytes_handle = hex_bytes.decode().upper()
    total_control_nums = len(position_device_infos[ob_name]['DLQ'])
    current_which_one = str(hex_bytes_handle[1:2])
    if (hex_bytes_handle[:2] == mesg_combin_DQL[ob_name]['status_mesg'][-1].replace(' ', '')[:2]) and (hex_bytes_handle[6:8] == '01'):
        mesg_combin_DQL[ob_name]['handle_status'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        mesg_combin_DQL[ob_name]['handle_nums'].append(current_which_one)
        time.sleep(2)
        send_mesg = ob_name + '当前第' + current_which_one + '/' + str(total_control_nums) + '个断路器已合闸!'
        print(send_mesg)
        mesg_combin_DQL[ob_name]['handle_status'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        client_thread_dict[control_name][1].sendall(bytes(send_mesg, encoding="utf-8"))
        mesg_combin_DQL[ob_name]['status_mesg'].remove(mesg_combin_DQL[ob_name]['status_mesg'][-1])
        if len(mesg_combin_DQL[ob_name]['status_mesg']):  # 循环执行剩余的断路器状态操作
            time.sleep(2)
            mesg_combin_DQL[ob_name]['handle_status'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            client_thread_dict[ob_name][1].sendall(bytes.fromhex(mesg_combin_DQL[ob_name]['status_mesg'][-1]))  # 执行断路器状态查询操作
        else:
            time.sleep(2)
            mesg_combin_DQL[ob_name]['handle_status'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            send_messg = ob_name + '所有断电操作全部完成！'
            client_thread_dict[control_name][1].sendall(bytes(send_messg, encoding="utf-8"))
            del mesg_combin_DQL[ob_name]
            del control_DLQ_infos[ob_name]

def analytical_DLQ_mesg(client_name, hex_bytes, mesg_combin_DQL, control_DLQ_infos):
    ob_name = control_DLQ_infos[client_name]['ob_name']
    control_name = control_DLQ_infos[client_name]['control_name']
    hex_bytes_handle = hex_bytes.decode().upper()
    if hex_bytes_handle == mesg_combin_DQL[ob_name]['action_mesg'][-1].replace(' ', ''):
        print('已检测到' + ob_name + '断电回传报文，开始执行状态查询操作……')
        current_which_one = str(hex_bytes_handle[:2])
        mesg = '已检测到' + ob_name + '第' + current_which_one + '个断路器的断电回传报文，开始执行状态查询操作……'
        print(mesg)
        mesg_combin_DQL[ob_name]['handle_status'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        time.sleep(2)
        client_thread_dict[ob_name][1].sendall(bytes.fromhex(mesg_combin_DQL[ob_name]['status_mesg'][-1]))
        mesg_combin_DQL[ob_name]['handle_status'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 判断是否为断路器回传的状态报文
    elif (len(hex_bytes_handle) == 12) and (hex_bytes_handle[:2] == mesg_combin_DQL[ob_name]['status_mesg'][-1].replace(' ', '')[:2]):
        #  移除已成功断电的断路器动作报文
        mesg_combin_DQL[ob_name]['handle_status'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        mesg_combin_DQL[ob_name]['action_mesg'].pop(-1)
        mesg_combin_DQL[ob_name]['status_mesg'].pop(-1)
        assert len(mesg_combin_DQL[ob_name]['action_mesg']) == len(mesg_combin_DQL[ob_name]['status_mesg'])
        total_control_nums = len(position_device_infos[ob_name]['DLQ'])
        current_which_one = str(hex_bytes_handle[:2])
        mesg_combin_DQL[ob_name]['handle_status'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        time.sleep(2)
        mesg_combin_DQL[ob_name]['handle_status'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        send_mesg = ob_name + '当前第' + current_which_one + '/' + str(total_control_nums) + '个断路器已合闸!'
        print(send_mesg)
        client_thread_dict[control_name][1].sendall(bytes(send_mesg, encoding="utf-8"))
        mesg_combin_DQL[ob_name]['handle_status'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(client_name + '发送断路器状态报文操作完毕')
        print(client_name +'判断所有断电操作是否全部完成……')
        if len(mesg_combin_DQL[ob_name]['action_mesg']):  # 循环执行剩余的断电操作
            print(ob_name + '断电操作有未完成项，继续执行断电操作……')
            mesg_combin_DQL[ob_name]['handle_status'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            time.sleep(1)
            mesg_combin_DQL[ob_name]['handle_status'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            client_thread_dict[ob_name][1].sendall(bytes.fromhex(mesg_combin_DQL[ob_name]['action_mesg'][-1]))
        else:
            mesg_combin_DQL[ob_name]['handle_status'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            time.sleep(2)
            mesg_combin_DQL[ob_name]['handle_status'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(ob_name + '所有断电操作全部完成!')
            send_messg = ob_name + '所有断电操作全部完成！'
            client_thread_dict[control_name][1].sendall(bytes(send_messg, encoding="utf-8"))
            del mesg_combin_DQL[ob_name]
            del control_DLQ_infos[ob_name]


def analytical_DB(hex_bytes, client_name):
    judge_message = agreement_DB(Electric_data[client_name]['DB_name'][-1]).analysis_message(
        Electric_data[client_name]['action_message_DB'][-1],
        hex_bytes, 'DDS')
    if judge_message != -1:  # 电表回传报文解析成功
        if Electric_data[client_name]['Weak_num'] != 0:
            Electric_data[client_name]['Weak_electricity'].append(judge_message[0])
            Electric_data[client_name]['Weak_num'] -= 1
        else:
            if len(judge_message) == 2:
                Electric_data[client_name]['power'].append(judge_message[1])
            Electric_data[client_name]['electricity'].append(judge_message[0])
        assert len(Electric_data[client_name]['action_message_DB']) == len(
            Electric_data[client_name]['DB_name'])

        Electric_data[client_name]['action_message_DB'].pop(-1)
        Electric_data[client_name]['DB_name'].pop(-1)
        if len(Electric_data[client_name]['action_message_DB']):  # 循环执行剩余的抄表操作
            client_thread_dict[client_name][1].sendall(
                bytes.fromhex(Electric_data[client_name]['action_message_DB'][-1]))  ##执行抄表操作
        else:
            now_electricity = sum(Electric_data[client_name]['electricity'])
            now_Weak_electricity = sum(Electric_data[client_name]['Weak_electricity'])
            now_power = sum(Electric_data[client_name]['power'])
            print(client_name,Electric_data[client_name]['electricity'],Electric_data[client_name]['Weak_electricity'])
            time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            infors = [client_name, time_now, now_electricity, now_Weak_electricity,
                      position_device_infos[client_name]['Magnification'],now_power]
            try:
                writesql(infors)
            except:
                print(client_name + "电表数据写入数据库超时！")
            else:
                pass

    elif judge_message == -1:  # 电表回传报文解析失败，再次发送
        # print(name_position + '当前报文组合3', names[name_position + 'action_message_DB'])
        client_thread_dict[client_name][1].sendall(
            bytes.fromhex(Electric_data[client_name]['action_message_DB'][-1]))

def send_DB_query_mesg(time_point, client_name):
    connected_position = list(client_thread_dict.keys())
    if (client_name not in Controller_list) and (client_name in connected_position):
        if len(position_device_infos[client_name]['Strong_DB'] + position_device_infos[client_name]['Weak_DB']):
            time_point_init = ['00', '10', '20', '30', '40', '50']
            #time_point_init = [str(i) for i in range(1, 60)]
            if datetime.datetime.now().strftime('%M') in time_point:
                exclude_time = time_point_init[time_point_init.index(datetime.datetime.now().strftime('%M'))]
                time_point_init.remove(exclude_time)
                time_point = time_point_init
                Electric_data[client_name] = {}
                Electric_data[client_name]['action_message_DB'] = []
                Electric_data[client_name]['electricity'] = []
                Electric_data[client_name]['power'] = []
                Electric_data[client_name]['Weak_electricity'] = []
                Electric_data[client_name]['Weak_num'] = len(position_device_infos[client_name]['Weak_DB'])
                Electric_data[client_name]['action_message_DB'] = [agreement_DB(i.split('-')[0]).combination_message(i.split('-')[1], 'DDS')
                    for i in (position_device_infos[client_name]['Strong_DB'] + position_device_infos[client_name]['Weak_DB'])]
                Electric_data[client_name]['DB_name'] = [j.split('-')[0] for j in (position_device_infos[client_name]['Strong_DB'] +
                                                                                   position_device_infos[client_name]['Weak_DB'])]
                client_thread_dict[client_name][1].sendall(bytes.fromhex(Electric_data[client_name]['action_message_DB'][-1]))
    return time_point

def tcplink(sock, addr):
    #print('Accept new connection from %s:%s...' % addr)
    sock.send(bytes('连接成功！', encoding="utf-8"))
    t1 = time.time()
    #sock.settimeout(20)
    try:
        first_mesg = sock.recv(1024)
        print("心跳间隔", time.time()-t1)
        print('first_mesg', first_mesg)
        end_flag, client_name = client_infos_init(first_mesg, sock)
    except:
        print("心跳包上传失败")
        pass
        #client_thread_dict[client_name][1].close()
    else:
        if end_flag == -1:
            pass
        else:
            #  站点抄表时间点设置
            #time_point =[str(i) for i in range(1,60)]
            time_point = ['00','10', '20', '30', '40', '50']
            while True:
                try:
                    # now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    # if now_time[-8:-3] == '01:01':  # 客户端定时断开的时间点
                    #     if client_name in control_DLQ_infos:
                    #         del control_DLQ_infos[client_name]
                    #     if client_name in client_thread_dict:
                    #         del client_thread_dict[client_name]
                    #     break
                    data = sock.recv(1024)
                    client_thread_dict[client_name][2] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                except:
                    if client_name in control_DLQ_infos:
                        del control_DLQ_infos[client_name]
                    if client_name in client_thread_dict:
                        del client_thread_dict[client_name]
                    print(client_name + "连接异常！服务端已断开通讯连接"+ '\n' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                    print(client_name + "服务端已断开通讯连接后,当前线程数目-------->", len(threading.enumerate()))
                    break
                else:
                    #print("心跳信息", data)
                    if not data or ('exit' in str(data)):
                        print(client_name + "sock连接中断或客户端主动退出" + '\n' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                        print(client_name + "sock连接中断或客户端主动退出,当前线程数目-------->", len(threading.enumerate()))
                        if client_name in control_DLQ_infos:
                            del control_DLQ_infos[client_name]
                        if client_name in client_thread_dict:
                            del client_thread_dict[client_name]
                        break
                    # 断路器根据接收到的控制端的报文指令进行对应的动作，DLQ-断路器简写，表示操作指令与断路器相关
                    elif ('DLQ' in str(data)) and (pc.decrypt(data.decode(encoding='utf-8').split('DLQ')[1]) == 'cut'):
                        #first_send_DLQ_mesg(client_name, data, mesg_combin_DQL)
                        sendall_DLQ_action_mesg(client_name, data, mesg_combin_DQL)
                    elif (client_name in mesg_combin_DQL) and (len(b2a_hex(data).decode()) == 12):  # 判断是否为断路器设备返回的报文
                        hex_bytes = b2a_hex(data)  # 字节流信息转换为十六进制
                        print(control_DLQ_infos[client_name]['ob_name'] + 'RS485设备返回的报文', [data, hex_bytes])
                        # analytical_DLQ_mesg(client_name, hex_bytes, mesg_combin_DQL, control_DLQ_infos) # 断路器动作结果校验操作
                        all_DLQ_status_judge(client_name, hex_bytes, mesg_combin_DQL, control_DLQ_infos)
                    elif (client_name in Electric_data) and (len(Electric_data[client_name]['action_message_DB'])):  # 判断是否为智能电表设备返回的报文
                        hex_bytes = b2a_hex(data).decode()
                        analytical_DB(hex_bytes, client_name)
                    else:
                        # print("客户端心跳信息", name_position + '->' + bytes_data.decode(encoding='utf-8'))
                        pass
                    if client_name in control_DLQ_infos:
                        ob_name = control_DLQ_infos[client_name]['ob_name']
                        control_name = control_DLQ_infos[client_name]['control_name']
                        if len(mesg_combin_DQL[ob_name]['handle_status']):
                            start = mesg_combin_DQL[ob_name]['handle_status']
                            end = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            if calc_timeDifference(start, end, 'second') > 5:
                                print(ob_name + '断路器开关状态查询超时')
                                send_messg = ob_name + '断路器开关状态查询超时'
                                client_thread_dict[client_name][1].sendall(
                                    bytes(send_messg, encoding="utf-8"))
                                del control_DLQ_infos[client_name]
                                del mesg_combin_DQL[ob_name]
                    time_point = send_DB_query_mesg(time_point, client_name)
    if "closed" in str(sock):
        pass
    else:
        #sock.shutdown(2)
        sock.close()

def accept_client(s):
    while True:
        #print('Waiting for connection...')
        # 接受一个新连接:
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        #if now_time[-8:-3] != '01:01':  # 客户端在能定时断开时间点之外进行连接
        sock, addr = s.accept()
        # 创建新线程来处理TCP连接:
        t = threading.Thread(target=tcplink, args=(sock, addr))
        t.setName(str(sock))
        client_thread_dict[sock] = [t, sock, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
        t.setDaemon(True)
        t.start()

def calc_timeDifference(start, end, mode):
    old_time = datetime.datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
    new_time = datetime.datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
    days = (new_time - old_time).days
    sec = (new_time - old_time).seconds
    if mode == 'second':
        total_secs = round(days * 24 * 60 * 60 + sec, 1)
        return total_secs
    elif mode == 'hours':
        total_hours = round(days * 24  + sec/3600, 1)
        return total_hours
    elif mode == 'min':
        total_mins = round(days * 24 * 60  + sec/60, 1)
        return total_mins

def connectMysql2():
    accountInfo = "accountInfo.properties"
    info = Properties(accountInfo).getProperties()
    host = info['host']  # 主机ip地址
    user = info['user']  # 用户名
    passwd = info['passwd']  # 密码
    db = info['db']  # 数据库名
    charset = info['charset']  # 字符集
    # 建立一个MySQL连接（不使用配置文件，直接填入数据库连接信息）
    conn = pymysql.connect(host=host, user=user, passwd=passwd, database=db, charset=charset)
    # 创建游标,给数据库发送sql指令,id已经设置为自增
    cursor = conn.cursor()
    return conn, cursor

def get_offline_time():
    online_position = dict()
    offline_position = dict()
    time_flage = dict()
    offline_devices = dict()
    online_devices = dict()
    while True:
        all_position_status = [[], []]  # 0-初始化站点名称，1-站点状态发生变化
        for name in position_device_infos['all_position']:
            if name not in client_thread_dict:  # 未连接
                offline_position[name] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 添加离线站点
                all_position_status[0].append(name)  # 首次启动，站点状态初始化为离线状态
            elif name in client_thread_dict:  # 已连接
                online_position[name] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 添加连线站点
            if (name in online_position) and (name in offline_position):
                if datetime.datetime.strptime(online_position[name], '%Y-%m-%d %H:%M:%S') < datetime.datetime.strptime(offline_position[name], '%Y-%m-%d %H:%M:%S'):  # 设备上线后发生离线
                    if name in time_flage:
                        print(name+"！设备离线！" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                        print(name + "设备离线,当前线程数目-------->", len(threading.enumerate()))
                        offline_devices[name] = offline_position[name]
                        del time_flage[name]
                        all_position_status[1].append([name, offline_devices[name], "off"])
                else:   # 首次连线
                    if name not in time_flage:
                        print(name + '已上线！'+ '\n' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                        #print(name + "设备上线,当前线程数目-------->", len(threading.enumerate()))
                        online_devices[name] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        time_flage[name] = 1
                        all_position_status[1].append([name, online_devices[name], "on"])
        if len(all_position_status[0]) or len(all_position_status[1]):
            try:
                conn, cursor = connectMysql2()
            except:
                print("连接数据库超时！")
            else:
                if len(all_position_status[0]):
                    position_status_init(all_position_status[0], conn, cursor)
                if len(all_position_status[1]):
                    writesql_position_status(all_position_status[1], conn, cursor)
                # 关闭游标
                cursor.close()
                # # 关闭数据库连接
                conn.close()


key = 'Aslkfsjlsd5SA@#$%sd151dsf!'
AES_LENGTH = 16
pc = prpcrypt(key)
position_device_infos, Controller_list = refresh_position()
client_thread_dict = {} #  存储socket连接完成之后对应的线程以及sock对象
control_DLQ_infos = {}  # 存储接收到的断电信息
mesg_combin_DB = {}  # 存储组合后的电表报文
mesg_combin_DQL = {} # 存储组合后的断路器报文
Electric_data = {}
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 取消端口保护机制，因为服务器进程终止后，操作系统会保留几分钟它的端口，从而防止其他进程占用
s.bind(('192.168.0.36', 8888))
s.listen(5)
#s.settimeout(30.0)  ## 连接超时设置
# 启动socket连接子线程
thread_main = threading.Thread(target=accept_client, args=(s,))
thread_main.setName("客户端连接主线程")
thread_main.setDaemon(True)
thread_main.start()
# 新开一个线程，用于监控通讯连接状态
thread1 = Thread(target=get_offline_time)
thread1.setName("客户端连接状态判断线程")
thread1.setDaemon(True)
thread1.start()
# 启动主线程、检测子线程状态、线程数变化
# while True:
#         cmd = input("""--------------------------
#                         输入1:查看当前在线人数
#                         输入2:给指定客户端发送消息,测试专用！！
#                         输入3:查看当前接入用户名称
#                         输入4:关闭服务端
#                     """)
#         if cmd == '1':
#             print("--------------------------")
#             print("当前在线人数：", len(client_thread_dict))
#         elif cmd == '2':
#             print("--------------------------")
#             name, msg = input("请输入“场站,操作指令”的形式：").split(",")
#             dict_conn_pool[name].sendall(bytes.fromhex(msg))
#         elif cmd == '3':
#             Connected_name = list(client_thread_dict.keys())
#             print(Connected_name)
#             Connected = '|' + Connected_name[0] + '|'
#             for i in Connected_name[1:]:

time_num = 0
while True:

    time_num += 1
    all_thread_status = {}
    for i in threading.enumerate():
        all_thread_status[i.name] = i.is_alive()
    #print("thread nums is ", len(threading.enumerate()), "connect time", time_num+1, all_thread_status)
    all_thread = list(client_thread_dict.keys())
    for key in all_thread:
            end = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            start = client_thread_dict[key][-1]
            time_difference = calc_timeDifference(start, end, 'second')
            #print(str(key) + 'heart time-difference', time_difference)
            if key in client_thread_dict:
                # if (time_difference > 300) and (type(key) is str) and ('-1' not in str(client_thread_dict[key][1])) and (client_thread_dict[key][0].is_alive())  and (key not in Controller_list):
                #     send_part, receive_part, filepath = '58475885@163.com', 'haotian.xu@shellwofe.com', 'TCP_Server3.0.log'
                #     subject_infos = [key + '心跳包刷新超时！' + "设备离线_" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '']
                #     print(key + '心跳包刷新超时！'+ "设备离线,当前线程数目-------->", len(threading.enumerate()))
                #     try:
                #        send_email('163', ['58475885@163.com', 'TGAJYHTIJAIXLSCD'],
                #                   ['1193358516@qq.com', '954825786@qq.com'],
                #                   'TCP_Server3.0.log', subject_infos)
                #     except smtplib.SMTPException as e:
                #        print('邮件发送失败:', e)
                #     else:
                #        print(key + '离线邮件发送成功')
                #     client_thread_dict[key][1].shutdown(2)
                #     client_thread_dict[key][1].close()
                #     time.sleep(1)
                if (time_difference > 120) and (type(key) is str) and ('-1' not in str(client_thread_dict[key][1])) and (client_thread_dict[key][0].is_alive()) and (key in Controller_list):
                    send_messg = '长时间未操作，已断开与服务器连接'
                    client_thread_dict[key][1].sendall(
                        bytes(send_messg, encoding="utf-8"))
                    client_thread_dict[key][1].shutdown(2)
                    client_thread_dict[key][1].close()
                # if (time_difference > 300) and (type(key) is not str) and ('-1' not in str(client_thread_dict[key][1])) and (client_thread_dict[key][0].is_alive()) and (key not in Controller_list):
                #     client_thread_dict[key][1].shutdown(2)
                #     client_thread_dict[key][1].close()
                #     time.sleep(1)
                #     print(str(key) + "心跳包刷新超时！服务端已断开通讯连接")
                #     print(str(key) + '心跳包刷新超时！' + "设备离线,当前线程数目-------->", len(threading.enumerate()))
    time.sleep(1)

