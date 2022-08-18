# -*- coding: utf-8 -*-
""" 
@Time    : 2021/9/6 8:48
@Author  : xuhaotian
@FileName: 道闸控制.py
@SoftWare: PyCharm
"""
import json
import requests
import hashlib
#import urllib2
import json
import urllib.request
from urllib.parse import urlparse
def http_post(url,data_json):
    jdata = json.dumps(data_json)
    jdata=urllib.parse.quote_plus(jdata).encode("utf-8")
    req = urllib.request.Request(url, jdata)
    response = urllib.request.urlopen(req)
    return response.read()

url = 'http://192.168.55.222:8888'
#headers = {'User-Agent': 'User-Agent:Mozilla/5.0'}
data_json ={"error_num":"0",
                     "error_str":"no error",
                     "passwd":'qQZEnVdp+nNh1+zGqj9tKA=='
                     }
resp = http_post(url,data_json)
print(resp)

# md5=hashlib.md5()
# md5.update(b'123abc')
# passwd=md5.hexdigest()
# print(passwd)
# url="http://192.168.55.100:8000"
# headers = {'Content-Type':'application/x-www-form-urlencoded'}
# datas = json.dumps({"error_num":"0",
#                     "error_str":"no error",
#                     "passwd":'qQZEnVdp+nNh1+zGqj9tKA==',
#                     })
# r = requests.post(headers=headers,url=url, data=datas)
# print(r.text)
# # #
# #
# import requests
# import json
#
#
# def requests_form():
#     url = 'http://httpbin.org/post'
#     data = {'k1': 'v1', 'k2': 'v2'}
#     response = requests.post(url, data)
#     return response
#
#
# def requests_json():
#     url = 'http://192.168.55.100:8000'
#     data  = json.dumps({"username":'admin','pwd':"123456","error_num":"0",
#                      "error_str":"noerror",
#                     "gpio_data":[{"ionum": "io1",
#                                    "action": "on"}]})
#     response = requests.post(url, data)
#     return response
#
#
# def requests_multipart():
#     url = 'http://httpbin.org/post'
#     files = {'file': open('requests.txt', 'rb')}  # requests.txt中包含一句“Hey requests”
#     response = requests.post(url, files=files)
#     return response
#
#
# if __name__ == "__main__":
#     #response1 = requests_form()
#     response2 = requests_json()
#     #response3 = requests_multipart()
#
#     #print("From形式提交POST请求：")
#     #print(response1.text)
#     print("Json形式提交POST请求：")
#     print(response2.text)
#     #print("Multipart形式提交POST请求：")
#     #print(response3.text)
