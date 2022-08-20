# encoding: utf-8
import pymysql
from PropertiesUtil import Properties
from decimal import *
from datetime import datetime
# 使用配置文件获取数据库连接信息

def connectMysql():
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


def writesql(infors):
    """
    infors =
    """
    # global old_electricity, consumption, recall
    conn, cursor = connectMysql()
    name_cn = infors[0]  # 场站名称
    time_now = infors[1]  # 时间
    if name_cn=='吴中科创园地面站配电房' or name_cn=='吴中科创园地面站室外':
        power = infors[-1]
    else:
        power = 0
    if name_cn=='西环路新庄地面站':
        now_Weak_electricity=infors[3]-infors[2]  # 新庄站的弱电是总表减去桩表
        now_electricity = infors[2]               # 新庄站经营用电
    # elif name_cn=='爱琴海' or name_cn=='嘉盛丽廷国际地下站':
    #     now_Weak_electricity=infors[3]            # 爱琴海弱电
    #     now_electricity = infors[2]-infors[3]     # 爱琴海和嘉盛的经营电是总表减去经营
    elif name_cn=='吴中公共文化中心地下站':
        now_Weak_electricity = infors[3]          # 吴中公共文化中心弱电
        now_electricity = infors[2]*200
    else:
        now_Weak_electricity = infors[3]          # 当前其他用电
        now_electricity = infors[2]               # 当前经营电用电
    Magnification = infors[-1]  # 倍率
    #print('当前站点', name_cn)
    sql = "SELECT * FROM electricity_new WHERE 站点 = %s" % ('\'' + name_cn + '\'')
    #######################查询上月月末电度数
    try:
        # 执行SQL语句
        cursor.execute(sql)
        results = cursor.fetchall()
        #print(name_cn + '********' + str(results))
        assert len(results) != 0
    except:
        print(name_cn + "warning: no history data!" + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        recall = False
        old_electricity = now_electricity
        old_Weak_electricity = now_Weak_electricity
    else:
        # 获取上月电度数
        old_electricity = results[-1][4]
        old_Weak_electricity = results[-1][5]
        recall = True
    #######################
    #######################插入本月用电量数据
    try:
        if recall == True:
            #print('追加抄表数据，开始写入数据库……')
            #print(name_cn + '当月电度数', now_electricity, old_electricity, now_electricity - old_electricity)
            consumption = (now_electricity - old_electricity)
            Weak_consumption = (now_Weak_electricity - old_Weak_electricity)
            sql = "insert into electricity_new(站点,抄表时间,上次经营总电表读数,上次其他电表读数, 本次经营总电表读数,本次其他电表读数,本阶段经营使用电量,本阶段其他使用电量,倍率,功率) values  (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"
            # print(name_cn, now_electricity, old_electricity )
            args = (name_cn, time_now, old_electricity, old_Weak_electricity, now_electricity, now_Weak_electricity,
                    consumption, Weak_consumption, Magnification, power)
            cursor.execute(sql, args)
            conn.commit()
        if recall == False:
            #print('第一次抄表，开始写入数据库……')
            consumption = 0
            Weak_consumption = 0
            sql = "insert into electricity_new(站点,抄表时间, 上次经营总电表读数,上次其他电表读数,本次经营总电表读数,本次其他电表读数,本阶段经营使用电量,本阶段其他使用电量,倍率,功率) values  (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"
            args = (name_cn, time_now, old_electricity, old_Weak_electricity, now_electricity, now_Weak_electricity,
                    consumption, Weak_consumption, Magnification, power)
            cursor.execute(sql, args)
            conn.commit()

    except Exception as e:
        print(e, '\n', name_cn + '电表写入数据库失败！-' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    else:
        pass
    #######################

    # 关闭游标
    cursor.close()
    # # 关闭数据库连接
    conn.close()

def writesql_position_status(infos,conn, cursor):
    # global old_electricity, consumption, recall
    #conn, cursor = connectMysql()
    for data in infos:
        position = data[0]
        time_content = data[1]
        if "on" in data:
            try:
                sql = "insert into position_status_history(站点,上线时间) values  (%s, %s)"
                args = (position, time_content)
                cursor.execute(sql, args)
                cursor.execute("update position_status set 上线时间=%s where 站点=%s", (time_content,  position))
                cursor.execute("update position_status set 当前状态=%s where 站点=%s", ("在线",  position))
            except Exception as e:
                print(e,'\n', position + '上线时间刷新失败-' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            else:
                pass#print("数据保存成功")

        elif "off" in data:
            try:
                # 查询最近一次上线时间
                sql_query = "SELECT * FROM position_status_history WHERE 站点 = %s" % ('\'' + position + '\'')
                cursor.execute(sql_query)
                last_onTime = cursor.fetchall()[-1][2]
                #  更新站点状态
                cursor.execute("update position_status_history set 离线时间=%s where 上线时间=%s and 站点=%s", (time_content,  last_onTime,  position))
                cursor.execute("update position_status_history set 在线时长=%s where 上线时间=%s and 站点=%s", (calc_hours(last_onTime,time_content),  last_onTime,  position))
                cursor.execute("update position_status set 当前状态=%s where 上线时间=%s and 站点=%s", ("离线", last_onTime, position))
            except Exception as e:
                print(e,'\n', position + '离线时间刷新失败-' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            else:
                pass#print("数据保存成功")
    try:
        conn.commit()
    except Exception as e:
        print(e,'\n', position + '设备状态刷新失败-' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    else:
        pass
def position_status_init(position, conn, cursor):
    positons = [i for i in position]
    try:
        for position in positons:
            cursor.execute("update position_status set 当前状态=%s where 站点=%s", ("离线",  position))
        conn.commit()
    except Exception as e:
        print(e,'\n', position + '设备初始化状态刷新失败-' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    else:
        pass#print("数据保存成功") 

def calc_hours(start, end):
    old_time = datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
    new_time = datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
    days = (new_time - old_time).days
    sec = (new_time - old_time).seconds
    hours = days * 24 + round(sec/3600, 3)
    return str(hours) + "小时"
# position = "常熟好得家"
# sql = "SELECT * FROM position_status WHERE 站点 = %s" % ('\'' + position + '\'')
# #######################查询上月月末电度数
# conn,cursor = connectMysql()
# cursor.execute(sql)
# results = cursor.fetchall()[-1][1]
# time_content = results
# print(results)

