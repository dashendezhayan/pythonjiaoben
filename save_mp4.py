import numpy as np
import cv2
import cv2
import re
import glob
import time
url = "rtsp://admin:a12345678@192.168.3.111/Streaming/Channels/1"
cap = cv2.VideoCapture(url)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')

def Video_num():
    image_files = glob.glob('*.mp4')
    print(image_files)
    #image_files = [i.split('\\')[1] for i in image_files]
    image_files.sort(key=lambda i: int(re.match(r'(\d+)', i).group()))
    #print(image_files)
    if len(image_files) != 0 :
        #image_files.sort()
        #print(image_files[-1].split('\\')[1][:-4])
        jpg_Num = int(image_files[-1].split('.')[0])
    else:
        jpg_Num = 0

    return jpg_Num
num_1  = Video_num()
print(num_1)
num_2 = 1
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# 获取视频高度
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
out = cv2.VideoWriter(str(num_1+num_2)+'.mp4', fourcc, 25.0, (frame_width, frame_height), True)
while (cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
        cv2.imshow('frame', frame)
        #out.write(frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
out.release()
cv2.destroyAllWindows()
