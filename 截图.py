import cv2
import re
import glob
import time
url = "rtsp://192.168.0.6/stream1"#a12345678,yiwei666
cap = cv2.VideoCapture(url)
ret, frame = cap.read()
n=1
def PHOTO_num():
    image_files = glob.glob('D:/image/xinzhuang/11111/*.jpg')
    print(image_files)
    image_files = [i.split('\\')[1] for i in image_files]
    image_files.sort(key=lambda i: int(re.match(r'(\d+)', i).group()))
    #print(image_files)
    if len(image_files) != 0 :
        #image_files.sort()
        #print(image_files[-1].split('\\')[1][:-4])
        jpg_Num = int(image_files[-1].split('.')[0])
    else:
        jpg_Num = 0

    return jpg_Num
#num_1  = PHOTO_num()
#print(num_1)
num_2 = 1
ret, frame = cap.read()
cv2.imwrite("1.jpg",frame)
# while ret:
#     ret, frame = cap.read()
#     #cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
#     #cv2.imshow("frame", frame)
#
#     keypress = cv2.waitKey(1)
#     if  keypress & 0xFF == ord('y'):
#         cv2.imwrite("D:/image/xinzhuang/11111/"+str(num_1+num_2)+".jpg",frame)
#     if  keypress & 0xFF == ord('q'):
#         break
#     num_2 += 1
#     print(n)
cv2.destroyAllWindows()
cap.release()

