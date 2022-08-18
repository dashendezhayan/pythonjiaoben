# -*- coding: utf-8 -*-
""" 
@Time    : 2021/11/1 16:25
@Author  : xuhaotian
@FileName: httpserver.py
@SoftWare: PyCharm
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
import json
import base64
import datetime

class MessageHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # 1. How long was the message?
        length = int(self.headers.get('Content-length', 0))

        # 2. Read the correct amount of data from the request.
        data = self.rfile.read(length).decode()

        # 3. Extract the "message" field from the request data.
        message = parse_qs(data)
        message_type= message['type'][0]

        #判断信息类型
        if message_type=='heartbeat':
        #回复信息
            response_message={"error_num":"0","error_str":"no error","gpio_data":[{"ionum": "io2",
                                   "action": "on"}]}

        elif message_type=='online':
            response_message = {"error_num": "0", "error_str": "no error", "gpio_data":[{"ionum": "io1",
                                   "action": "on"}]}
            car_num=message['plate_num'][0]
            car_color=message['plate_color'][0]
            picture=message['picture'][0].replace("-","+").replace("_","/").replace(".","=")
            picture=base64.b64decode(picture)
            now_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            with open("D:/python脚本/"+now_time+car_num+".jpg", "wb")as f:  # wb是写二进制
                f.write(picture)
                f.close()
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(response_message).encode())




if __name__ == '__main__':
    server_address = ('192.168.0.222', 8888)
    httpd = HTTPServer(server_address, MessageHandler)
    httpd.serve_forever()
# from http.server import HTTPServer, BaseHTTPRequestHandler
# import json
#
# data = {"error_num":"0",
#         "error_str":"no error",
#         "passwd":'qQZEnVdp+nNh1+zGqj9tKA=='}
# host = ('192.168.55.222', 8888)
#
# class Resquest(BaseHTTPRequestHandler):
#     def do_get(self):
#         self.send_response(200)
#         self.send_header('Content-type', 'application/json')
#         self.end_headers()
#         self.wfile.write(json.dumps(data).encode())
#
# if __name__ == '__main__':
#     server = HTTPServer(host, Resquest)
#     print("Starting server, listen at: %s:%s" % host)
#     server.serve_forever()
