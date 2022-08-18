# -*- coding: utf-8 -*-
import os
import tqdm
def rename():
    count_pic=1 #初始文件编号为1
    count_xml=1
    count_mp4=1
    path='F:/图像数据库/烟雾相关/' #需要重命名的文件目录，注意目录的写法
    filelist=os.listdir(path) #返回指定的文件夹包含的文件或文件夹的名字的列表。这个列表以字母顺序。
    for files in tqdm(filelist):  #循环列出文件
        Olddir=os.path.join(path,files)  #将多个路径组合后返回
        if os.path.isdir(Olddir): #判断路径是否为目录，isfile判断是否为文件
            continue #是的话继续
        filename=os.path.splitext(files)[0]  #文件名
        filetype=os.path.splitext(files)[1]  #文件后缀
        if filetype=='.jpg' or filetype=='.png':
            Newdir=os.path.join(path,'fire_smoke_4_922_'+str(count_pic)+filetype)
            os.rename(Olddir,Newdir)  #重命名文件或目录
            count_pic+=1
        elif filetype=='.xml':
            Newdir = os.path.join(path, 'fire_4_922_' + str(count_xml) + filetype)
            os.rename(Olddir, Newdir)  # 重命名文件或目录
            count_xml += 1
        elif filetype == '.mp4':
            Newdir = os.path.join(path, 'fire_4_922_' + str(count_mp4) + filetype)
            os.rename(Olddir, Newdir)  # 重命名文件或目录
            count_mp4 += 1
           #文件编号加1
rename()
