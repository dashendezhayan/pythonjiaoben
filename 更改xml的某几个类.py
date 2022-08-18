import os
import glob
input_dir = glob.glob("F:/data/*.xml")  # xml文件所在的目录
#input_dir='allimage_1'  # xml文件所在的目录
shu=0

#
# new_name1='1'
# new_name2='2'
# new_name3='3'
# new_name4='4'
# new_name5='5'
# new_name6='6'
# new_name7='7'
# new_name8='8'
import xml.etree.ElementTree as ET
for file_path in input_dir:
    print(file_path)
    dom = ET.parse(file_path)
    root = dom.getroot()
    for obj in root.findall('object'):  # 获取object节点中的name子节点
        name= obj.find('name').text
        obj.find('name').text=str(int(name)-1)
        shu+=1
        # if obj.find('name').text== '0':
        #     obj.find('name').text=new_name1
        #     shu=shu+1
        #     #print("change %s to %s." % (yuan_name, new_name1))
        # elif obj.find('name').text== '1':
        #     obj.find('name').text = new_name2
        #     shu = shu + 1
        # elif obj.find('name').text== '2':
        #     obj.find('name').text= new_name3
        #     shu = shu + 1
  # 保存到指定文件
    dom.write(file_path, xml_declaration=True)
print("有%d个文件被成功修改。" % shu)
