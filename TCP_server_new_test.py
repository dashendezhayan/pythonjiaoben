# -*- coding: utf-8 -*-
""" 
@Time : 2021/7/5 13:56
@Author : DingKun
@FileName: TCP_server.py
@SoftWare: PyCharm
"""
import datetime
import time
import binascii
import socket  # 导入 socket 模块
from threading import Thread
import crcmod
import calendar
from saveimgtosql import writesql
ADDRESS = ('192.168.0.36', 8888)  # 绑定地址

g_socket_server = None  # 负责监听的socket

clear_pool = [] #连接池去重

g_conn_pool = []  # 连接池

dict_conn_pool = {}  # 连接池字典映射

op_status_DLQ = {}

crc_message_DQL = []

dict_name_code={'西环路新庄地上站':'xinzhuang','百购商业广场地下站':'baigou','星海广场地下站':'xinghaigc','吴中科创园上站':'wuzhongkcy','花锦汇邻中心':'huajinhlzx','吴中公共文化中心':'wuzhongwhzx','友联新村':'youlianxc','星叶生活广场':'xingyeshgc','圆融时代广场':'yuanrongsdgc','斜塘老街':'xietanglj','吴江财智广场':'wuzhongczgc','联合广场':'lianheshgc','爱情海购物公园':'aiqinhai','SM生活广场':'SMshgc','圆融星座':'yuanrongxz','龙湖天街':'longhutj','嘉盛丽廷国际地下':'jiashenglt','兴贤商业广场':'xingxiansygc','昆山象屿':'kunshanxy','南浜村':'nanbangcun','昆山兆丰':'kunshanzf','玲珑88':'linglong88','昆山世茂':'kunshansm','昆山港龙':'kunshangl','昆山银都':'kunshanyd','润元':'runyuan','欧风':'oufeng'}

name_list = ['controller','controller01','controller02','controller03','controller04','baigou','xinghaigc','wuzhongkcy','jiashenglt',
          'yuanrongsdgc','youlianxc','huajinhlzx','wuzhongwhzx','xingyeshgc','xietanglj','xinzhuang','wuzhongczgc','lianheshgc',
          'aiqinhai','SMshgc','kunshanxy','longhutj','yuanrongxz','xinghaigc','nanbangcun','linglong88','kunshansm','kunshangl',
          'kunshanyd','oufeng','runyuan','kunshanzf',]

Magnification = {'baigou':200,'xingxiansygc':100,'jiashenglt':200,'huajinhlzx':160,'youlian':160,'wuzhongwhzx':200,'xingye':200,
'yuanrongsdgc':120,'xietanglj':200,'xinzhuang':1,'wuzhongczgc':1,'lianheshgc':120,'aiqinhai':100,'SMshgc':1,
'wuzhongkcy':200,'kunshanxy':200,'longhutj':1,'yuanrongxz':120,'xinghaigc':1,'nanbangcun':160,
'linglong88':200,'kunshansm':1,'kunshangl':1,'kunshanyd':1,'oufeng':1,'runyuan':1,'kunshanzf':1}

electricity_code = {'baigou':'03 01 56 00 02'}


close_code = '01 05 00 01 00 00 9C 0A'
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
    #print(days_in_month,now_time)
    #if now_time.split('-')[2]
    if now_time.split('-')[2] == 28:#days_in_month:
        return now_time
    else:
        return None

#电度数，单位kw/h
def Electric_degree(byte):
    data_16= byte[6:14]
    data_2=bin(int(data_16, 16))[2:]
    zhishu=int(data_2[0:8],2)
    weishu=int(data_2[8:],2)
    electric=pow(2,zhishu-127)*(1+weishu/pow(2,23))/1000#
    return electric

#生成CRC16-MODBUS校验码
def crc16Add(read):
    crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xFFFF, xorOut=0x0000)
    data = read.replace(" ", "") #消除空格
    readcrcout = hex(crc16(binascii.unhexlify(data))).upper()
    str_list = list(readcrcout)
    # print(str_list)
    if len(str_list) == 5:
        str_list.insert(2, '0')  # 位数不足补0，因为一般最少是5个
    crc_data = "".join(str_list) #用""把数组的每一位结合起来  组成新的字符串
    # print(crc_data)
    crc = read.strip() + ' ' + crc_data[4:] + ' ' + crc_data[2:4] #把源代码和crc校验码连接起来
    return crc

def accept_client():
    """
    接收新连接
    """
    while True:
        client, _ = g_socket_server.accept()  # 阻塞，等待客户端连接
        # 加入连接池
        #print('client', client)
        client.sendall("连接服务器成功!".encode(encoding='utf-8'))
        host_name = socket.gethostname()
        ip_address = socket.gethostbyname(host_name)
        #print('用户属性',ip_address)
        g_conn_pool.append(client)
        # 给每个客户端创建一个独立的线程进行管理
        thread = Thread(target=message_handle, args=(client,))
        # 设置成守护线程
        thread.setDaemon(True)
        thread.start()


def message_handle(client):
    """
    消息处理
    
    """
    global crc_message_DQL,name_position,DLQ_adress,DB_adress,decode_name, crc_message_recall_DQL,electricity
    #断路器状态
    op_status_DLQ['op_status'] = 0
    bytes = client.recv(1024)

    print('接入客户端名称为：',bytes.decode(encoding='utf-8'),type(bytes.decode(encoding='utf-8')))
    if bytes.decode(encoding='utf-8') in name_list:  ##首次连接时客户端上传的心跳包信息
        #print('接入名称',bytes.decode(encoding='utf-8'),type(bytes.decode(encoding='utf-8')))
        dict_conn_pool[bytes.decode(encoding='utf-8')] = client#g_conn_pool[-1]
        print('已使用的进程信息',dict_conn_pool)
    if '|' in bytes.decode(encoding='utf-8'):
        name_position = bytes.decode(encoding='utf-8').split('|')[0]
        DLQ_adress = bytes.decode(encoding='utf-8').split('|')[1]
        DB_adress = bytes.decode(encoding='utf-8').split('|')[2]
        if '_' in DLQ_adress:
            DLQ_adress = DLQ_adress.split('_')
        else:
            DLQ_adress = [DLQ_adress]
        if '_' in DB_adress:
            DB_adress = DB_adress.split('_')
        else:
            DB_adress = [DB_adress]
        dict_conn_pool[name_position] = client  # g_conn_pool[-1]
        print('已使用的进程信息', dict_conn_pool)

    while True:
        bytes = client.recv(1024)
 
        if 'DLQ' in str(bytes):  ## DLQ-断路器简写，表示操作指令与断路器相关

            ob_name = bytes.decode(encoding='utf-8').split('DLQ')[0]
            op_code = bytes.decode(encoding='utf-8').split('DLQ')[1]
            decode_name = dict_name_code[ob_name]
            print('被操作对象名称-->',decode_name)
            Connected_name = [i for i in dict_conn_pool.keys()]
            if decode_name in Connected_name:
                op_status_DLQ['op_status'] = 1  ##执行状态标识符，1-断开，0-复位
                message_DQL = [i+' '+op_code for i in DLQ_adress]
                message_recall_DQL = [i + ' ' + '01 00 01 00 01' for i in DLQ_adress]
                print('message',DLQ_adress,op_code,message_DQL)
                crc_message_DQL = [crc16Add(i) for i in message_DQL]
                crc_message_recall_DQL = [crc16Add(i) for i in message_recall_DQL]
                dict_conn_pool[decode_name].sendall(bytes.fromhex(crc_message_DQL[-1]))  ##执行断路器合闸操作
                print('*****************0', op_status_DLQ)
            else:
                #print('！！！！！！！！！！！！！！！！')
                client.sendall("操作对象未连接服务器!".encode(encoding='utf-8'))
                #print('********************************')    
        elif '\\x' in str(bytes): ##
            hex_bytes = binascii.b2a_hex(bytes)
            print('客户端反馈报文：',hex_bytes)
            #if
            ################################## 断路器状态查询
            if op_status_DLQ['op_status'] == 1:
                dict_conn_pool[decode_name].sendall(bytes.fromhex(crc_message_recall_DQL[-1]))
                op_status_DLQ['op_status'] = 0
                print('*****************1',op_status_DLQ)
            elif op_status_DLQ['op_status'] == 0:
                print('*****************2',op_status_DLQ)
                for i in dict_conn_pool.keys():
                      if 'controller' in i:
                          dict_conn_pool[i].sendall(bytes)
                crc_message_DQL.remove(crc_message_DQL[-1])
                crc_message_recall_DQL.remove(crc_message_recall_DQL[-1])
                time.sleep(0.5)
            ##################################电表电量返回值

        elif len(crc_message_DQL):
            dict_conn_pool[decode_name].sendall(bytes.fromhex(crc_message_DQL[-1]))
            op_status_DLQ['op_status'] = 1
        elif 'SeeConnectedName' in str(bytes): ##查询服务端中已连接的客户端
            Connected_name = [i for i in dict_conn_pool.keys()]
            Connected = '|'+Connected_name[0]+'|'
            for i in Connected_name[1:]:
                Connected += i + '|'
            #print('已连接站点信息',Connected)
            client.sendall(Connected.encode(encoding='utf-8'))
        elif 'exit' in str(bytes):
            del_ob = bytes.decode(encoding='utf8').split('-')[1]
            del dict_conn_pool[del_ob]
            client.close()
            # 删除连接
            g_conn_pool.remove(client)
            print(del_ob+"客户端下线了。") 
            break
        else:
            print("客户端心跳信息:", bytes.decode(encoding='utf-8'))
        ################################## 向DTU发送读取电度数报文
        Connected_position = [i for i in dict_name_code.keys()]  ## 站点名称列表
        if get_month_lastday() is not None and name_position in Connected_position: ## 判断当天是否为月末、线程是否为DTU客户端
            if get_month_lastday().split(' ')[-1]=='23-59-59':
                message_DB = [i + ' ' + electricity_code[name_position] for i in DB_adress]
                crc_message_DB = [crc16Add(i) for i in message_DB]
                time_now = get_month_lastday()
                dict_conn_pool[name_position].sendall(bytes.fromhex(crc_message_DB[-1]))
                now_electricity = electricity
                name_cn = [i for i in dict_name_code.keys() if dict_name_code[i] == name_position][0]
                infors = [name_cn,time_now,now_electricity,Magnification[name_position]]
                writesql(infors)
        ##################################
if __name__ == '__main__':
    init()
    # 新开一个线程，用于接收新连接
    thread = Thread(target=accept_client)
    thread.setDaemon(True)
    thread.start()
    # 主线程逻辑
    while True:

         cmd = input("""--------------------------
                        输入1:查看当前在线人数
                        输入2:给指定客户端发送消息,测试专用！！
                        输入3:查看当前接入用户名称
                        输入4:关闭服务端
                    """)
         if cmd == '1':
             print("--------------------------")
             print("当前在线人数：", len(dict_conn_pool))
         elif cmd == '2':
             print("--------------------------")
             name, msg = input("请输入“场站,操作指令”的形式：").split(",")
             dict_conn_pool[name].sendall(bytes.fromhex(msg))
         elif cmd == '3':
             Connected_name = [i for i in dict_conn_pool.keys()]
             Connected = '|'+Connected_name[0]+'|'
             for i in Connected_name[1:]:
                 Connected += i + '|'
             print('当前已连接场站信息','\n',Connected)
         elif cmd == '4':
             exit()
         #time.sleep(1)
         #print('Running……')

