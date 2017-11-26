# -*- coding: utf-8 -*-
import sys
from pprint import pprint
reload(sys)
sys.setdefaultencoding('utf8')
import json

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

if __name__ == '__main__':
    """截取指定对象的标注,生成新的文件
    """
    json_path = '/home/wanghao/Desktop/labels/labels_wanghao.json'
    namelist = ["illu_item10-_L_10.jpg",
                "illu_item10+_L_1.jpg","illu_item10+_L_2.jpg",
                "illu_item10+_L_3.jpg","illu_item10+_L_4.jpg",
                "illu_item10+_L_5.jpg","illu_item10-_LD_1.jpg",
                "illu_item10-_LD_2.jpg","illu_item10-_LD_3.jpg",
                "illu_item10-_LD_4.jpg","illu_item10-_LD_5.jpg",
                "illu_item10-_LD_6.jpg","illu_item10-_LD_7.jpg"]

    annos = parseFromFile(json_path)

    res = []
    for anno in annos:
        if anno['filename'] in namelist:
            res += [anno]
    pprint(res)
    serializeToFile("wh_lables.json", res)