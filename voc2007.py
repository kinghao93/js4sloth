# -*- coding: utf-8 -*-
import json
import os, shutil
from PIL import Image
from random import shuffle

# 加载json,转换成list(dict)
def parseFromFile(fname):
    """
    Overwritten to read JSON files.
    """
    f = open(fname, "r")
    return json.load(f)

def createDirs(pDir='.'):
    if os.path.exists('VOC2007/'):
        os.system('rm -rf VOC2007/*')
    os.system('mkdir -p VOC2007/ImageSets/Main')
    os.system('mkdir VOC2007/Annotations')
    os.system('mkdir VOC2007/JPEGImages')

def save2Xml(item, pDir='.', imagePath='', imageCopy=False):
    # path.basename get file full name
    # path.splitext get file's name+ext
    img = os.path.basename(item['filename'])
    name, ext = os.path.splitext(img)
    # auto copy image files  to directory JPEGImages
    if imageCopy:
        shutil.copy(imagePath+'/'+img, pDir+'/VOC2007/JPEGImages/')
    im = Image.open((imagePath + '/' + img))
    width, height = im.size

    # write in xml file
    xml_file = open((pDir + '/VOC2007/Annotations/' + name + '.xml'), 'w')
    xml_file.write('<annotation>\n')
    xml_file.write('    <folder>VOC2007</folder>\n')
    xml_file.write('    <filename>' + img + '</filename>\n')
    xml_file.write('    <size>\n')
    xml_file.write('        <width>' + str(width) + '</width>\n')
    xml_file.write('        <height>' + str(height) + '</height>\n')
    xml_file.write('        <depth>3</depth>\n')
    xml_file.write('    </size>\n')

    # write the region of text on xml file
    for anno in item['annotations']:
        cls = anno['class']
        # cls = {'C1': 'l_faster', 'C2': 'r_faster'}[cls]
        cls = {'C1': 'positive', 'C2': 'positive', 'C3': 'negative'}[cls]
        xmin = anno['x']
        ymin = anno['y']
        xmax = anno['width'] + anno['x']
        ymax = anno['height'] + anno['y']

        xml_file.write('    <object>\n')
        xml_file.write('        <name>' + cls + '</name>\n')
        xml_file.write('        <pose>Unspecified</pose>\n')
        xml_file.write('        <truncated>0</truncated>\n')
        xml_file.write('        <difficult>0</difficult>\n')
        xml_file.write('        <bndbox>\n')
        xml_file.write('            <xmin>' + str(int(xmin)) + '</xmin>\n')
        xml_file.write('            <ymin>' + str(int(ymin)) + '</ymin>\n')
        xml_file.write('            <xmax>' + str(int(xmax)) + '</xmax>\n')
        xml_file.write('            <ymax>' + str(int(ymax)) + '</ymax>\n')
        xml_file.write('        </bndbox>\n')
        xml_file.write('    </object>\n')

    xml_file.write('</annotation>')

def createMain(annos=None, pDir='.', rate_train=0, rate_val=0, rate_test=0):
    # 计算 各类训练/验证/测试 数据 比例
    s = (rate_train + rate_val + rate_test) * 1.0
    r_train, r_val, r_test = rate_train / s, rate_val / s, rate_test / s
    r_train_val = 1.0 - r_test

    # 获取 image list
    images = []
    for item in annos:
        filename = os.path.basename(item['filename'])
        images += [os.path.splitext(filename)[0]]

    # 创建文件, 保存划分结果
    testText = open(pDir + '/VOC2007/ImageSets/Main/test.txt', 'w')
    trainvalText = open(pDir + '/VOC2007/ImageSets/Main/trainval.txt', 'w')
    trainText = open(pDir + '/VOC2007/ImageSets/Main/train.txt', 'w')
    valText = open(pDir + '/VOC2007/ImageSets/Main/val.txt', 'w')

    # 洗牌, 打乱顺序
    shuffle(images)
    images_len = len(images)
    train_val = int(images_len * r_train_val) # train_val部分 在images数组中 结束下标
    for test_image_name in sorted(images[train_val: ]):
        testText.write(test_image_name + '\n')
    for train_val_image_name in sorted(images[: train_val]):
        trainvalText.write(train_val_image_name + '\n')
    # shuffle(images)
    train = int(images_len * r_train)  # train部分 在images数组中 结束下标
    for train_image_name in sorted(images[: train]):
        trainText.write(train_image_name + '\n')
    for val_image_name in sorted(images[train: train_val]):
        valText.write(val_image_name + '\n')
    testText.close()
    trainvalText.close()
    trainText.close()
    valText.close()
    pass

if __name__ == '__main__':
    # voc2007 dataSet directory
    pDir = '.'
    """
    修改以下参数
    1. jsonPath: json 文件的绝对或相对路径
    2. imagePath： 给出脚本可以找到image的路径, 
       因为靠json中提供的路径, 脚本并不能保证一定可以访问到相应的image
    """
    jsonPath = '/home/wanghao/Desktop/GPU-SERVER/label_001-660.json' # '/home/wanghao/AL_5600-5710.json'
    imagePath = '/home/wanghao/Desktop/GPU-SERVER/sample' # '/home/wanghao/TFS/AL_1101-6000'
    # create voc2007 dirs
    createDirs(pDir)
    annos = parseFromFile(jsonPath)
    # 按照不同比例划分数据集
    createMain(annos, pDir, rate_train=4, rate_val=4, rate_test=3)
    #　生成标注 xml
    for item in annos:
        save2Xml(item, pDir, imagePath, imageCopy=True)

    # createMain(annos, rate_train=4, rate_val=4, rate_test=3)




