import os
import glob
input_dir = glob.glob("F:/origin_dataset/*.xml")  # xml文件所在的目录
#input_dir='allimage_1'  # xml文件所在的目录
shu=0
label=[1,2,3,4,5,6,7,8,9]
import xml.etree.ElementTree as ET
for file_path in input_dir:
    print(file_path)
    dom = ET.parse(file_path)
    root = dom.getroot()
    for obj in root.findall('object'):  # 获取object节点中的name子节点
        name=obj.find('name').text
        if int(name) in label:
            shu+=1
  # 保存到指定文件
print("有%d个标签。" % shu)
