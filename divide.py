import os
import shutil
import math

path = input("请输入原始文件路径:\n")
folderPath = input("请输入要输出的路径:\n")
path = path.strip("\"")
folderPath = folderPath.strip("\"")


file_list = os.listdir(path) #源文件名称列表
number=int(len(file_list)/7) #每包文件数量
Number = 7 #目标文件夹数量
folderNumber = -1 #起始文件夹id ，-1是因为0 % 任意数 = 0
sort_folder_number = [x for x in range(0,Number)]

#  创建文件夹
for foldernumber in sort_folder_number:
    new_folder_path = os.path.join(folderPath,'%s'%foldernumber)#new_folder_path is ‘folderPath\number'

    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
        print("new a floder named "+str(foldernumber)+'at the path of '+ new_folder_path)

#分包
for i in range(0,len(file_list)):
    old_file = os.path.join(path, file_list[i])
    if os.path.isdir(old_file):
        '''if the path is a folder,program will pass it'''
        print('img does not exist ,path=' + old_file+' it is a dir' )
        pass
    elif not os.path.exists(old_file):
        '''if the path does not exist,program will pass it'''
        print('img does not exist ,path='+old_file)
        pass
    else:
        '''define the number,it decides how many imgs each people process'''
        if(0 == (i % number)): #导致folderNumber = -1 ： 0 % 任意数 = 0
            folderNumber += 1
        new_file_path = os.path.join(folderPath,'%s'%(folderNumber))
        if not os.path.exists(new_file_path):
            break
        shutil.move(old_file,new_file_path)
        print(old_file+'is successfully moved to '+new_file_path)
