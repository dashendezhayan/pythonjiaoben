import os
import tqdm
import glob
path1 = glob.glob("D:/image/testdata/*.jpg")  # xml文件所在的目录
path2 =glob.glob("E:/图片1/*.jpg")        #要删除的文件夹
same=[]
path1=[i.split('\\')[-1] for i in path1]
for file2 in tqdm.tqdm(path2):  # 遍历文件夹
    filee=file2.split('\\')[-1]
    if filee in path1:
        os.remove(file2)

