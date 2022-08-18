# -*- coding: utf-8 -*-
""" 
@Time    : 2021/7/2 10:48
@Author  : xuhaotian
@FileName: 远程连接云服务器.py
@SoftWare: PyCharm
"""
import paramiko

ssh = paramiko.SSHClient()  # 创建SSH对象
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 允许连接不在know_hosts文件中的主机
ssh.connect(hostname='123.60.71.211', port=22, username='root', password='yiweixny.666')  # 连接服务器

stdin, stdout, stderr = ssh.exec_command('whoami')  # 执行命令并获取命令结果
# stdin为输入的命令
# stdout为命令返回的结果
# stderr为命令错误时返回的结果
res, err = stdout.read(), stderr.read()
result = res if res else err
print(result)
ssh.close()  # 关闭连接