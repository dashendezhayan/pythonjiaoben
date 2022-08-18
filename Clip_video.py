import numpy as np
import cv2
import cv2
import re
import glob
import time
path='D:/yiwei_company/CAMERA/Human-Falling-Detect-Tracks-master(GPU)/Data/dataset/2021_4_20_video/2021_4_20_27.mp4'
cap = cv2.VideoCapture(path)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
# 获取视频高度
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
new_path=path.split("/")[-1].split(".")[0]+'_new'+'.mp4'
print(new_path)
out = cv2.VideoWriter(new_path, fourcc, 25.0, (frame_width, frame_height), True)
n=1
while (cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
        cv2.imshow('frame', frame)
        keypress = cv2.waitKey(5)
        if n>=50:#keypress & 0xFF == ord('s'):
            out.write(frame)
            print("success")

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
        n+=1
    else:
        break

cap.release()
out.release()
cv2.destroyAllWindows()
