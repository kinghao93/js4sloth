# -*- coding: utf-8 -*-
import json
import os, glob, shutil
from os import path as opth
import cv2 as cv
import numpy as np

# 加载json,转换成list(dict)
def parseFromFile(fname):
    """
    Overwritten to read JSON files.
    """
    f = open(fname, "r")
    return json.load(f)

def serializeToFile(fname, annotations):
    """
    Overwritten to write JSON files.
    """
    f = open(fname, "w")
    json.dump(annotations, f, indent=4, separators=(',', ': '), sort_keys=True, ensure_ascii=False)
    f.write("\n")

def createDirs(pDir='.'):
    if os.path.exists(pDir + '/sample/'):
        os.system('rm -rf %s/sample/*' % pDir)
    else:
        os.system('mkdir -p %s/sample/' % pDir)

def getRandomPosition(pos, sw, sh, cw, ch):
    x = np.random.randint(0, sw-cw)
    y = np.random.randint(0, sh-ch)
    pos[0] = x
    pos[1] = y
    pos[2] = cw+x
    pos[3] = ch+y
    return pos

def havaIter(bb, BBGT):
    # intersection
    BBGT = np.array(BBGT)
    ixmin = np.maximum(BBGT[:, 0], bb[0])
    iymin = np.maximum(BBGT[:, 1], bb[1])
    ixmax = np.minimum(BBGT[:, 2], bb[2])
    iymax = np.minimum(BBGT[:, 3], bb[3])
    iw = np.maximum(ixmax - ixmin + 1., 0.)
    ih = np.maximum(iymax - iymin + 1., 0.)
    inters = np.max(iw * ih)
    return inters>=1.

if __name__ == '__main__':
    # voc2007 dataSet directory
    pDir = '.'
    """
    修改以下参数
    1. jsonPath: json 文件的绝对或相对路径
    2. imagePath： 给出脚本可以找到image的路径, 
       因为靠json中提供的路径, 脚本并不能保证一定可以访问到相应的image
    """
    jsonPath = '/home/wanghao/Desktop/newVOC/label_001-550.json' # '/home/wanghao/AL_5600-5710.json'
    imagePath = '/home/wanghao/Desktop/newVOC/VOC2007/JPEGImages' # '/home/wanghao/TFS/AL_1101-6000'
    cropPath = '/home/wanghao/Desktop/newVOC/crops' # 负样本子图扣件
    # save new image dir
    createDirs(pDir)
    annos = parseFromFile(jsonPath)
    croplist = glob.glob(cropPath+'/*.*')
    cind = 0 # cropImage 索引
    #　产生随机位置，并保存至annotations和image中
    for item in annos:
        annotation = item['annotations']
        filename = item['filename']
        print('filename: '+filename)
        name = opth.split(filename)[1]
        srcImage = cv.imread(opth.join(imagePath, name))
        sh, sw = srcImage.shape[0], srcImage.shape[1]
        BBGT = []
        for box in annotation:
            lx, ly, rx, ry = float(box['x']), float(box['y']), float(box['width']), float(box['height'])
            rx, ry = lx+rx, ly+ry
            BBGT += [[lx, ly, rx, ry]]
            print('lx, ly, rx, ry=(%f, %f, %f, %f)' % (lx, ly, rx, ry))
        for i in range(6):

            cropImage = cv.imread(croplist[cind])
            cind += 1
            ch, cw = cropImage.shape[0], cropImage.shape[1]
            pos = [0, 0, 0, 0]
            while havaIter(getRandomPosition(pos, sw, sh, cw, ch), BBGT): continue
            # modify src image
            srcImage[pos[1]:pos[3], pos[0]:pos[2], :] = cropImage
            # cv.imshow('cropImage', srcImage)
            # cv.waitKey()
            # modify annotations
            BBGT += [pos]
            class_name = 'C3'
            annotation += [{'class': class_name, 'x': float(pos[0]), 'y':  float(pos[1]),
                 'width': float(pos[2] - pos[0]), 'height': float(pos[3] - pos[1])}]

        # save2Xml(item, pDir, imagePath, imageCopy=True)
        print('~~~~~~~~~~~~~~~~~~~~~~~~~`')
        cv.imwrite(filename=opth.join('sample/', name), img=srcImage)

    # 保存修改后的图片和JSON信息
    savePath = opth.split(jsonPath)[1]
    serializeToFile(fname=savePath, annotations=annos)



