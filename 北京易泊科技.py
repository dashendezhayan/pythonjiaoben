# -*- coding: utf-8 -*-
""" 
@Time    : 2022/2/21 10:22
@Author  : xuhaotian
@FileName: 北京易泊科技.py
@SoftWare: PyCharm
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
import json
import base64
import datetime

def picstr2pic(picstr):
    picture = picstr.replace("-", "+").replace("_", "/").replace(".", "=")
    picture = base64.b64decode(picture)
    return picture


class MessageHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # 1. How long was the message?
        length = int(self.headers.get('Content-Length', 0))

        # 2. Read the correct amount of data from the request.
        data = self.rfile.read(length).decode()
        # 3. 字符串数据转json
        result = json.loads(data)

        #处理结果得到车牌信息和图片
        self.Plate_Inf_Pic(result)


        #发送指令
        #response_message=
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain;charset=utf-8')
        self.end_headers()
        #self.wfile.write(json.dumps(response_message).encode())



    #车牌识别结果保存和图片保存
    def Plate_Inf_Pic(self,result):
        plateinfo={}
        if ([i for i in result.keys()][0]) =='AlarmInfoPlate':
            AlarmInfoPlate=result['AlarmInfoPlate']
            plate=AlarmInfoPlate['result']['PlateResult']
            platepic=plate['imageFile']
            car_num=plate['license']
            picture=picstr2pic(platepic)
            now_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            with open("D:/python脚本/车牌识别照片/"+now_time+car_num+".jpg", "wb")as f:  # wb是写二进制
                f.write(picture)
                f.close()
            plate.pop("imageFile")
            plate.pop('imageFragmentFile')

            plateinfo['devicenum'] = AlarmInfoPlate['deviceName']
            plateinfo['ip_addr'] = AlarmInfoPlate["ipaddr"]
            plateinfo['PlateResult'] = plate

            with open("D:/python脚本/车牌识别照片/"+now_time+car_num+".json", "w+")as f:
                json.dump(plateinfo,f,ensure_ascii=False)
                f.close()

        #print(response_message)

if __name__ == '__main__':
    server_address = ('192.168.0.222', 8888)
    httpd = HTTPServer(server_address, MessageHandler)
    httpd.serve_forever()





#response_message = {"Response": {"trigger_data": {"action": "on"}}}