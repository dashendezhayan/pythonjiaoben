import cv2
import re
import glob
import time
import os

path='F:\\国网充电站数据\\'
mp4_path=glob.glob(os.path.join(path,'*.mp4'))

#print(mp4_path)

for files in mp4_path:  #循环列出文件
    print(files)
    capture = cv2.VideoCapture(files)

    #ret, frame = capture.read()
    frame_number= int(capture.get(7))
    filename=files.split(".")[0].split("\\")[-1]
    print(filename)
    #print("文件名：",filename)
    rate = 25#capture.get(5)  # 帧速率
    time=frame_number/rate/60
    jiange=60*10  # 帧速率/视频总帧数 是时间，除以60之后单位是分钟
    print("时长：",time)
    print("帧速率：",rate)
    print("总帧数：",frame_number)
    print("截图间隔：",jiange,"分钟")
    print("截图步长：",frame_number/jiange)
    a = 1
    b = 00000
    for i in range(1,frame_number):
        a+=1
        capture.set(cv2.CAP_PROP_POS_FRAMES, float(i))
        if capture.isOpened():  # 判断是否正常打开
            rval, frame = capture.read()
            if rval:
                cv2.imwrite(path+ filename + str(a) + ".jpg", frame)###路径要全英文

    # while(True):
    #     ret, frame = capture.read()
    #
    #     if ret:
    #         framerate=jiange*int(rate)
    #         if (a%10==0):
    #             print(path+ filename+str(a) + ".jpg")
    #             # cv2.namedWindow('img',cv2.WINDOW_NORMAL)
    #             # cv2.imshow('img',frame)
    #
    #             #print(frame)
    #             cv2.imwrite(path+ filename+str(a) + ".jpg", frame)
    #             print(path + filename + str(a) + ".jpg")
    #             # cv2.waitKey(0)
    #         a+=1
    #     else:
    #         break

# while ret:
#     ret, frame = cap.read()
#     # print('2')
#     cv2.namedWindow('frame', cv2.WINDOW_NORMAL|cv2.WINDOW_KEEPRATIO)
#     cv2.imshow("frame", frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
# cv2.destroyAllWindows()
# cap.release()