import random
import os

Imgnum = int(input('请输入要打乱的图片的个数:'))
files = os.listdir("F:/allimage_2/")  # 获取图片目路径
i = 0
L = random.sample(range(0, Imgnum), Imgnum)
filetype = ".jpg"  # 文件类型
for filename in files:
    portion = os.path.splitext(filename)  # 将文件名拆成名字和后缀
    if portion[1] == filetype:  # 检查文件的后缀

        newname = str(L[i]) + filetype
        print(newname)
        os.rename(filename, newname)  # 修改名称
        i = i + 1