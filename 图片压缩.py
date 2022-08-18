# -*- coding: utf-8 -*-
""" 
@Time    : 2022/6/7 9:10
@Author  : xuhaotian
@FileName: 图片压缩.py
@SoftWare: PyCharm
"""
import PIL
from PIL import Image
from tkinter.filedialog import *
fl=askopenfilenames()
img = Image.open(fl[0])
img.save("result.jpg", "JPEG", optimize = True, quality = 10)

