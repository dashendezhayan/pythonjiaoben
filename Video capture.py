# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 15:34:26 2020

@author: sheld
"""
import cv2
url = "rtsp://admin:123456@192.168.55.100/Streaming/Channels/1"
vc = cv2.VideoCapture(url)
c=1
 
if vc.isOpened(): #判断是否正常打开
    rval , frame = vc.read()
else:
    rval = False

timeF = 200 #视频帧计数间隔频率
 
while rval:   #循环读取视频帧
    rval, frame = vc.read()
    cv2.imshow("frame", frame)
    if(c%timeF == 0): #每隔timeF帧进行存储操作
        cv2.imwrite('D:/image/new'+'img' + str(c) + '.jpg',frame) #存储为图像
    c = c + 1
    print(c)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    cv2.waitKey(0)
cv2.destroyAllWindows()
cap.release()