import cv2
import os
import tqdm
path='G:/video_display/bulue/'

#path = input('图片路径(E:/.../)：')
video_name = path+'73'#input('合成视频名称:')#
# 读取时序图中的第一张图片E:\example\exp193
files = os.listdir(path)
print(path+files[0])
img = cv2.imread(path+files[0])
# 设置每秒读取多少张图片E:\example\exp193
fps = 10
imgInfo = img.shape

# 获取图片宽高度信息
size = (imgInfo[1], imgInfo[0])
fourcc = cv2.VideoWriter_fourcc(*"MJPG")

# 定义写入图片的策略
videoWrite = cv2.VideoWriter(video_name+'.mp4', fourcc, fps, size)
out_num = len(files)
for i in tqdm.tqdm(range(0, out_num)):
    # 读取所有的图片
    # fileName = path + 'in' + str(i).zfill(6)+'.jpg'
    fileName = path + str(i)+'.jpg'
    img = cv2.imread(fileName)
    #print(fileName)
    # 将图片写入所创建的视频对象
    videoWrite.write(img)

videoWrite.release()
print('finish')