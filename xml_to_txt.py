import os, re
import xml.etree.ElementTree as ET


def getbox(box, w, h):
    xmin = float(box.find("xmin").text) / w
    ymin = float(box.find("ymin").text) / h
    xmax = float(box.find("xmax").text) / w
    ymax = float(box.find("ymax").text) / h
    return ((xmin + xmax) / 2, (ymin + ymax) / 2, xmax - xmin, ymax - ymin)


def convert(inpath=".", outpath="txt"):
    if not os.path.exists(outpath):
        os.makedirs(outpath)
    filelist = os.listdir(inpath)
    regex = re.compile("(.+)\\.xml")
    for file in filelist:
        filename = regex.match(file)
        if (filename):
            txtfile = open(outpath + "/" + filename.group(1) + ".txt", "w")
            root = ET.parse(inpath + "/" + file).getroot()
            size = root.find("size")
            width = int(size.find("width").text)
            height = int(size.find("height").text)
            for obj in root.iter("object"):
                name = obj.find("name").text
                box = getbox(obj.find("bndbox"), width, height)
                txtfile.write("%s %.6f %.6f %.6f %.6f\n" % (name, *box))
            txtfile.close()
        print(file, "converted")


xmlPath = "H:/TRAIN/together/train/"

convert(inpath=xmlPath, outpath=xmlPath + "txt")