# -*- coding: utf-8 -*-
""" 
@Time    : 2022/3/3 16:50
@Author  : xuhaotian
@FileName: 接口测试.py
@SoftWare: PyCharm
"""
# -*- coding:utf-8 -*-
#发送cookie到服务器
import requests
import json

host = "http://123.60.71.211/EdgeBoardServer/a/login;JSESSIONID=d53139dbad874ac4a6e501c06d5f23b5"
endpoint = "cookies"

url = ''.join([host,endpoint])
#方法一：简单发送
cookies = {"aaa":"bbb"}
r = requests.get(url,cookies=cookies)
print (r.text)

#方法二：复杂发送
# s = requests.session()
# c = requests.cookies.RequestsCookieJar()
# c.set('c-name','c-value',path='/xxx/uuu',domain='.test.com')
# s.cookies.update(c)