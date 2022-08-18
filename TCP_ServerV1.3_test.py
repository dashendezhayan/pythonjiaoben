# -*- coding: utf-8 -*-
""" 
@Time : 2021/8/16 11:25
@Author : DingKun
@FileName: TCP_ServerV1.3_test.py
@SoftWare: PyCharm
"""
import datetime
import time
import binascii
import socket  # 导入 socket 模块
import threading
from threading import Thread
import crcmod
import calendar
from saveimgtosql import writesql
from select_agreement_V1_3 import agreement_DB, agreement_DLQ, get_index
import inspect
import ctypes

def _async_raise(tid, exctype):
  """raises the exception, performs cleanup if needed"""
  tid = ctypes.c_long(tid)
  if not inspect.isclass(exctype):
    exctype = type(exctype)
  res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
  if res == 0:
    raise ValueError("invalid thread id")
  elif res != 1:
    # """if it returns a number greater than one, you're in trouble,
    # and you should call it again with exc=NULL to revert the effect"""
    ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
    raise SystemError("PyThreadState_SetAsyncExc failed")
def stop_thread(thread):
  _async_raise(thread.ident, SystemExit)


names = globals()
client_threading = {}
position_threading = {}
threading_list = []
locker = threading.Lock()
ADDRESS = ('192.168.0.36', 8888)  # 绑定地址

g_socket_server = None  # 负责监听的socket
dict_conn_pool = {}  # 连接池字典映射
client_heart = []
dict_name_code = {'西环路新庄地上站': '1', '百购商业广场地下站': '2', '星海广场地下站': '3', '吴中科创园上站': '4',
                  '花锦汇邻中心': '5', '吴中公共文化中心': '6', '友联新村': '07', '星叶生活广场': '8',
                  '圆融时代广场': '09', '斜塘老街': '10', '吴江财智广场': '11', '联合广场': '12',
                  '爱琴海': '13', 'SM生活广场': '14', '龙湖天街': '16', '圆融星座': '15',
                  '嘉盛丽廷国际地下站': '17', '兴贤商业广场': '18', '昆山象屿': '19', '南浜村': '20',
                  '昆山兆丰': '21', '玲珑88': '22', '昆山世茂': '23', '昆山港龙': '24',
                  '昆山银都': '25', '润元': '26', '欧风': '27', '常熟塔弄': '28', '常熟嘉安': '29', '常熟好得家': '30',
                  '常熟禾盛': '31', '盛安广场': '32'}  # '常熟塔弄':'28'

name_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13',
             '14', '16', '17', '18', '19', '20', '15', '21', '22', '23', '24', '25',
             '26', '27', '28', '29', '30', '31', '32']

Magnification = {'百购商业广场地下站': 200, '兴贤商业广场': 100, '嘉盛丽廷国际地下站': 200, '花锦汇邻中心': 160, '友联新村': 160,
                 '吴中公共文化中心': 200, '星叶生活广场': 200, '圆融时代广场': 120, '斜塘老街': 200, '西环路新庄地上站': 1, '吴江财智广场': 1,
                 '联合广场': 120, '爱琴海': 100, 'SM生活广场': 1, '吴中科创园上站': 200, '昆山象屿': 200, '龙湖天街': 1, '圆融星座': 120,
                 '星海广场地下站': 1, '南浜村': 160, '玲珑88': 200, '昆山世茂': 1, '昆山港龙': 1, '昆山银都': 1, '欧风': 1, '润元': 1,
                 '昆山兆丰': 1, '常熟塔弄': 1, '常熟嘉安': 1, '常熟好得家': 1, '常熟禾盛': 1, '盛安广场': 1, }

position_device = {'28': '常熟塔弄|MDQ-01|AMC72LE4C-02', '29': '常熟嘉安|MDQ-01|AMC72LE4C-02',
                   '30': '常熟好得家|MDQ-01|AMC72LE4C-02',
                   '31': '常熟禾盛|MDQ-01|AMC72LE4C-03|', '32': '盛安广场|MDQ-01|AMC72LE4C-02', '27': '欧风|MDQ-01|AMC72LE4C-XX',
                   '8': '星叶生活广场|MDQ-01|AMC72LE4C-02', '12': '联合广场|MDQ-01|AMC72LE4-02', '13': '爱琴海|MDQ-01|AMC72LE4C-XX',
                   '15': '圆融星座|MDQ-01|AMC72LE4-02', '26': '润元|MDQ-01|AMC72LE4C-02',
                   '17': '嘉盛丽廷国际地下站|MDQ-01|AMC72LE4C-XX',
                   '6': '吴中公共文化中心|MDQ-01|DTSD1352-02', '5': '花锦汇邻中心|MDQ-01_MDQ-02|AMC72LE4-XX',
                   '16': '龙湖天街|MDQ-01|AMC72LE4C-02',
                   '14': 'SM生活广场|MDQ-01|AMC72LE4-02', '11': '吴江财智广场|MDQ-01|AMC72LE4C-02_AMC72LE4C-03_AMC72LE4C-04',
                   '18': '兴贤商业广场|MDQ-01_MDQ-02|AMC72LE4-03_AMC72LE4-XX', '24': '昆山港龙|MDQ-01|AMC72LE4C-02',
                   '25': '昆山银都|MDQ-01|AMC72LE4C-02',
                   '23': '昆山世茂|MDQ-01|AMC72LE4C-02', '19': '昆山象屿|MDQ-01|AMC72LE4C-02',
                   '3': '星海广场地下站|MDQ-01|AMC72LE4C-04', '2': '百购商业广场地下站|MDQ-01_MDQ-02_MDQ-03|AMC72LE4C-XX',
                   '1': '西环路新庄地上站|MDQ-01|HN70E7S3-07', '20':'南浜村|MDQ-01|HN70E7S3-02', '4': '吴中科创园上站|MDQ-01|AMC72LE4C-XX'}


def init():
    """
    初始化服务端
    """
    global g_socket_server
    g_socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建 socket 对象
    g_socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    g_socket_server.bind(ADDRESS)
    g_socket_server.listen(5)  # 最大等待数（有很多人理解为最大连接数，其实是错误的）
    print("服务端已启动，等待客户端连接...")


def get_month_lastday():
    # 获得当月1号的日期
    start_date = datetime.date.today().replace(day=1)
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # 获得当月一共有多少天（也就是最后一天的日期）
    _, days_in_month = calendar.monthrange(start_date.year, start_date.month)

    # if now_time.split(' ')[0].split('-')[2] == '23':  # days_in_month:
    #     return now_time
    # else:
    #     return None
    return now_time

def accept_client():
    """
    接收新连接
    """
    while True:
        client, _ = g_socket_server.accept()  # 阻塞，等待客户端连接
        if 'raddr' in str(client):
            # 加入连接池
            # print('client', client)
            client.sendall(bytes('连接至服务器！', encoding="utf-8"))
            host_name = socket.gethostname()
            ip_address = socket.gethostbyname(host_name)
            # print('用户属性',ip_address)
            # 给每个客户端创建一个独立的线程进行管理
            thread = Thread(target=message_handle, args=(client,))
            threading_list.append(thread)
            client_threading[client] = thread
            # 设置成守护线程
            thread.setDaemon(True)
            thread.start()


def get_device_infors(bytes):
    name_position = position_device[bytes.decode(encoding='utf-8')].split('|')[0]
    DLQ_device_adress = position_device[bytes.decode(encoding='utf-8')].split('|')[1]
    DB_device_adress = position_device[bytes.decode(encoding='utf-8')].split('|')[2]
    if '_' in DLQ_device_adress:
        DLQ_device_adress = DLQ_device_adress.split('_')
    else:
        DLQ_device_adress = [DLQ_device_adress]
    if '_' in DB_device_adress:
        DB_device_adress = DB_device_adress.split('_')
    else:
        DB_device_adress = [DB_device_adress]
    return name_position, DLQ_device_adress, DB_device_adress


def message_handle(client):
    """
    消息处理
    """
    global action_message_DQL, status_message_DQL
    global ob_name

    # global locker
    action_message_DQL = []
    status_message_DQL = []

    bytes_data_once = client.recv(1024)
    name_position = -1
    try:
        bytes_data_once.decode(encoding='utf-8')
    except:
        print('接入客户端名称为：', bytes_data_once)
    else:
        print('接入客户端名称为：', bytes_data_once.decode(encoding='utf-8'), type(bytes_data_once.decode(encoding='utf-8')))
        ##首次连接时客户端上传的心跳包信息
        if bytes_data_once.decode(encoding='utf-8') in name_list:  ##只包含站点的心跳包信息
            DTU_infors = get_device_infors(bytes_data_once)
            name_position = DTU_infors[0]
            if name_position not in position_threading:
                position_threading[name_position] = client_threading[client]
            # else:
            #     print(name_position+'TCP重连，线程已重置！')
            #     print(position_threading[name_position], client_threading[client])
            #     stop_thread(position_threading[name_position])
            names[name_position + '_DLQ_device_adress'], names[name_position + '_DB_device_adress'] = DTU_infors[1], \
                                                                                                      DTU_infors[2]
            # print(name_position+'DLQ_device_adress', DLQ_device_adress)
            dict_conn_pool[name_position] = client  # g_conn_pool[-1]

            print('已使用的进程信息', dict_conn_pool)

        elif 'controller' in bytes_data_once.decode(encoding='utf-8'):  ##控制端上传的首次心跳信息
            name_position = bytes_data_once.decode(encoding='utf-8').split('-')[0]
            if name_position not in position_threading:
                position_threading[name_position] = client_threading[client]
            dict_conn_pool[name_position] = client  # g_conn_pool[-1]
            print('已使用的进程信息', dict_conn_pool)
        else:
            pass
    point = ['00','01','02','03','04','05','06','07','08','09']
    time_point = point + [str(i) for i in range(10, 60)]
    # time_point = ['09', '19', '29', '39', '49', '59']
    charge_positon_name = [i for i in dict_conn_pool.keys()]
    names[name_position + 'action_message_DB'] = []
    ####################################
    while True:  ##单个线程循环

        if name_position != -1:  ## 判断接入客户端是否为合法用户
            # locker.acquire()
            try:
                bytes_data = client.recv(1024)
            #     #print(bytes_data)
            except:
                del dict_conn_pool[name_position]
                del position_threading[name_position]
                stop_thread(client_threading[client])
                client.close()
                print(name_position + "客户端下线了。")
                break
            else:
                ## 处理断路器操作请求
                if 'DLQ' in str(bytes_data):  ## DLQ-断路器简写，表示操作指令与断路器相关
                    # print(name_position+'DLQ_device_adress_test', DLQ_device_adress)
                    ob_name = bytes_data.decode(encoding='utf-8').split('DLQ')[0]
                    op_code = bytes_data.decode(encoding='utf-8').split('DLQ')[1]
                    # decode_name = dict_name_code[ob_name]
                    print('被操作对象名称-->', ob_name)
                    Connected_name = [i for i in dict_conn_pool.keys()]
                    if ob_name in Connected_name:  # 判断操作对象是否在当前线程池中
                        # op_status_DLQ['op_status'] = 1  #执行状态标识符，1-断开，0-复位
                        # DTU_infors = get_device_infors(bytes(dict_name_code[ob_name], encoding="utf-8"))
                        # _, DLQ_device_adress, _ = DTU_infors[0], DTU_infors[1], DTU_infors[2]
                        action_message_DQL = [
                            agreement_DLQ(i.split('-')[0]).combination_message(i.split('-')[1], op_code) for i
                            in names[ob_name + '_DLQ_device_adress']]
                        status_message_DQL = [
                            agreement_DLQ(i.split('-')[0]).combination_message(i.split('-')[1], 'status') for i
                            in names[ob_name + '_DLQ_device_adress']]
                        print('message', names[ob_name + '_DLQ_device_adress'], action_message_DQL, status_message_DQL)
                        dict_conn_pool[ob_name].sendall(bytes.fromhex(action_message_DQL[-1]))  ##执行断路器合闸操作
                        client.sendall(bytes('报文发送成功！', encoding="utf-8"))
                    else:  # 操作对象不在当前线程池中，则判断为未连接至服务器
                        print('已连接信息', Connected_name)
                        client.sendall(bytes('操作对象未连接至服务器！', encoding="utf-8"))

                elif '\\x' in str(bytes_data):
                    ## 判断是否为RS485设备返回的报文
                    hex_bytes = binascii.b2a_hex(bytes_data)
                    print(name_position + 'RS485设备返回的报文', hex_bytes)
                    ##判断是否为断路器回传的操作报文
                    if len(action_message_DQL):  ## 第一次循环
                        hex_bytes = binascii.b2a_hex(bytes_data).decode().upper()
                        if hex_bytes == action_message_DQL[-1].replace(' ', ''):
                            print('已检测到断电回传报文，开始执行状态查询操作……')
                            time.sleep(2)
                            dict_conn_pool[ob_name].sendall(bytes.fromhex(status_message_DQL[-1]))
                            print('执行状态查询操作完毕，开始检测状态报文回传信息……')
                        elif len(hex_bytes) == 12:  ##判断是否为断路器回传的状态报文
                            print('已检测到状态查询回传报文，开始向控制端发送状态报文……')
                            action_message_DQL.remove(action_message_DQL[-1])
                            status_message_DQL.remove(status_message_DQL[-1])
                            assert len(action_message_DQL) == len(status_message_DQL)
                            total_control_code = len(names[ob_name + '_DLQ_device_adress'])
                            current_control_code = hex_bytes[:2]
                            send_messg = str(total_control_code) + '_' + current_control_code + '_' + hex_bytes
                            for i in dict_conn_pool.keys():
                                if 'controller' in i:
                                    dict_conn_pool[i].sendall(bytes(send_messg, encoding="utf-8"))
                            print('向控制端发送状态报文操作完毕')
                            print('判断所有断电操作是否全部完成……')
                            if len(action_message_DQL):  # 循环执行剩余的断电操作
                                print('断电操作有未完成项，继续执行断电操作……')
                                # time.sleep(0.5)
                                dict_conn_pool[ob_name].sendall(bytes.fromhex(action_message_DQL[-1]))  ##执行断路器合闸操作
                            else:
                                print('所有断电操作全部完成！')
                                action_message_DQL = []
                                status_message_DQL = []
                                ob_name = None
                        # else: ##设备断电执行失效，开始执行剩余设备的断电操作
                        #     action_message_DQL.remove(action_message_DQL[-1])
                        #     status_message_DQL.remove(status_message_DQL[-1])
                        #     print('判断所有断电操作是否全部完成……')
                        #     if len(action_message_DQL):  # 循环执行剩余的断电操作
                        #         print('断电操作有未完成项，继续执行断电操作……')
                        #         time.sleep(1)
                        #         dict_conn_pool[ob_name].sendall(bytes.fromhex(action_message_DQL[-1]))  ##执行断路器合闸操作

                    #################解析电表数据
                    elif len(names[name_position + 'action_message_DB']):
                        print(name_position + '电表报文解析中……')
                        hex_bytes = binascii.b2a_hex(bytes_data).decode()
                        judge_message = agreement_DB(names[name_position + 'DB_name'][-1]).analysis_message(names[name_position + 'action_message_DB'][-1],
                                                                                                hex_bytes, 'DDS')
                        ##############
                        if judge_message != -1: #电表回传报文解析成功
                            names[name_position + 'electricity'].append(judge_message)
                            # electricity = agreement_DB(names[name_position + 'DB_name'][-1]).analysis_message(hex_bytes, 'DDS')
                            print(name_position + names[name_position + 'DB_name'][-1] + '电度数：',
                                  names[name_position + 'electricity'])
                            assert len(names[name_position + 'action_message_DB']) == len(names[name_position + 'DB_name'])
                            names[name_position + 'action_message_DB'].remove(
                                names[name_position + 'action_message_DB'][-1])
                            names[name_position + 'DB_name'].remove(names[name_position + 'DB_name'][-1])
                            if len(names[name_position + 'action_message_DB']):  # 循环执行剩余的抄表操作
                                print('电表抄表有未完成项，继续执行抄表操作……')
                                time.sleep(2)
                                print(name_position + '当前报文组合2', names[name_position + 'action_message_DB'])
                                dict_conn_pool[name_position].sendall(
                                    bytes.fromhex(names[name_position + 'action_message_DB'][-1]))  ##执行抄表操作
                            else:
                                now_electricity = sum(names[name_position + 'electricity'])
                                time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                print(name_position + '总电度数：', names[name_position + 'electricity'])
                                infors = [name_position, time_now, now_electricity, Magnification[name_position]]
                                writesql(infors)
                                print(name_position + '所有电表抄表全部完成！')
                        elif judge_message == -1: #电表回传报文解析失败，再次发送
                            print(name_position + '当前报文组合3', names[name_position + 'action_message_DB'])
                            dict_conn_pool[name_position].sendall(
                                bytes.fromhex(names[name_position + 'action_message_DB'][-1]))
                        ##############
                    #################

                elif 'SeeConnectedName' in str(bytes_data):
                    Connected_name = [i for i in dict_conn_pool.keys()]
                    Connected = '|' + Connected_name[0] + '|'
                    for i in Connected_name[1:]:
                        Connected += i + '|'
                        # print('已连接站点信息',Connected)
                    dict_conn_pool[name_position].sendall(Connected.encode(encoding='utf-8'))
                elif 'exit' in str(bytes_data):
                    # del_ob = bytes_data_once.decode(encoding='utf8').split('-')[0]
                    del dict_conn_pool[name_position]
                    del position_threading[name_position]
                    stop_thread(client_threading[client])
                    # 删除连接
                    # g_conn_pool.remove(client)
                    client.close()
                    print(name_position + "客户端下线了。")
                    break
                else:
                    #print("客户端心跳信息:", name_position + '->' + bytes_data.decode(encoding='utf-8'))
                    pass
                ################发送读电表数据报文
                if len(time_point) == 0:
                    point = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09']
                    time_point = point + [str(i) for i in range(10, 60)]

                if name_position in charge_positon_name and 'controller' not in name_position:  ## 判断当天是否为月末、线程是否为DTU客户端
                    DB_adress = [i.split('-')[-1] for i in names[name_position+'_DB_device_adress']]
                    if 'XX' not in DB_adress:

                        if get_month_lastday().split(' ')[1].split(':')[-2] in time_point:
                            print(get_month_lastday().split(' ')[1])
                            print(name_position + "开始执行电表读取任务1……")
                            names[name_position + 'electricity'] = []
                            names[name_position + 'action_message_DB'] = [agreement_DB(i.split('-')[0]).combination_message(i.split('-')[1], 'DDS')
                                             for i in names[name_position+'_DB_device_adress']] ##报文组合
                            names[name_position + 'DB_name'] = [i.split('-')[0] for i in names[name_position+'_DB_device_adress']]  ##电表名称
                            time_point.remove(get_month_lastday().split(' ')[1].split(':')[-2])
                            print(name_position + "开始执行电表读取任务2……")
                            print(name_position+'当前报文组合1', names[name_position+'_DB_device_adress'], names[name_position + 'action_message_DB'])
                            dict_conn_pool[name_position].sendall(bytes.fromhex(names[name_position + 'action_message_DB'][-1]))
                ###############


if __name__ == '__main__':
    init()
    # 新开一个线程，用于接收新连接
    thread = Thread(target=accept_client)
    thread.setDaemon(True)
    thread.start()

    # 主线程逻辑
    while True:
        print('当前线程数目——————————————————>', len(threading.enumerate()))
        # print('当前线程目录——————————————————>', threading_list)
        time.sleep(5)
        continue
    # while True:
    #     cmd = input("""--------------------------
    #                     输入1:查看当前在线人数
    #                     输入2:给指定客户端发送消息,测试专用！！
    #                     输入3:查看当前接入用户名称
    #                     输入4:关闭服务端
    #                 """)
    #     if cmd == '1':
    #         print("--------------------------")
    #         print("当前在线人数：", len(dict_conn_pool))
    #     elif cmd == '2':
    #         print("--------------------------")
    #         name, msg = input("请输入“场站,操作指令”的形式：").split(",")
    #         dict_conn_pool[name].sendall(bytes.fromhex(msg))
    #     elif cmd == '3':
    #         Connected_name = [i for i in dict_conn_pool.keys()]
    #         Connected = '|' + Connected_name[0] + '|'
    #         for i in Connected_name[1:]:
    #             Connected += i + '|'
    #         print('当前已连接场站信息', '\n', Connected)
    #     elif cmd == '4':
    #         exit()