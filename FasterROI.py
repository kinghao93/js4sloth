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
    json.dump(annotations, f, indent=4, separators=(',', ': '), sort_keys=True) #, ensure_ascii=False)
    f.write("\n")

def createDirs(pDir='.'):
    if os.path.exists(pDir + '/roi/'):
        os.system('rm -rf %s/roi/*' % pDir)
    else:
        os.system('mkdir -p %s/roi/' % pDir)


if __name__ == '__main__':
    # voc2007 dataSet directory
    pDir = '.'
    """
    修改以下参数
    1. jsonPath: json 文件的绝对或相对路径
    2. imagePath： 给出脚本可以找到image的路径, 
       因为靠json中提供的路径, 脚本并不能保证一定可以访问到相应的image
    """
    jsonPath = '/home/wanghao/Desktop/hy-cs/RM.json' # '/home/wanghao/AL_5600-5710.json'
    imagePath = '/home/wanghao/Desktop/hy-cs/RM' # '/home/wanghao/TFS/AL_1101-6000'
    # save new image dir
    createDirs(pDir)
    annos = parseFromFile(jsonPath)
    cind = 0 # cropImage 索引
    #　产生随机位置，并保存至annotations和image中
    for item in annos:
        annotation = item['annotations']
        filename = item['filename']
        print('filename: '+filename)
        name = opth.split(filename)[1]
        srcImage = cv.imread(opth.join(imagePath, name))
        for box in annotation:
            lx, ly, rx, ry = float(box['x']), float(box['y']), float(box['width']), float(box['height'])
            lx, ly, rx, ry = int(lx), int(ly), int(lx+rx), int(ly+ry)
            print('lx, ly, rx, ry=(%f, %f, %f, %f)' % (lx, ly, rx, ry))
            cind += 1
            cv.imwrite(filename=(pDir + '/roi/%05d.JPG') % cind, img=srcImage[ly:ry+1, lx:rx+1, :])
            # cv.imshow('cropImage', srcImage[ly:ry+1, lx:rx+1, :])
            # cv.waitKey()

        # save2Xml(item, pDir, imagePath, imageCopy=True)
        print('~~~~~~~~~~~~~~~~~~~~~~~~~`')

    # 保存修改后的图片和JSON信息
    # savePath = opth.split(jsonPath)[1]
    # serializeToFile(fname=savePath, annotations=annos)



