import cv2
import os
import numpy as np
rootdir = 'D:/image/hunman_in/'
list = os.listdir(rootdir)
for i in range(0,len(list)):
    img=cv2.imread(rootdir+list[i])
    img_new=cv2.resize(img,(416,416),interpolation=cv2.INTER_AREA).astype(np.uint8)
    cv2.imwrite(rootdir+"/resize/"+list[i],img_new)  # 写入图片
    #cv2.imshow('image',dst)

#关闭
cv2.waitKey(0)
cv2.destroyAllWindows()