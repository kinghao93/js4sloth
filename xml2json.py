# -*- coding: utf-8 -*-
from xml2dict import XML2Dict
import json
import glob


def serializeToFile(fname, annotations):
    """
    Overwritten to write JSON files.
    """
    f = open(fname, "w")
    json.dump(annotations, f, indent=4, separators=(',', ': '), sort_keys=True)
    f.write("\n")

def getAnnos(file_name="", prefix=''):
    xml = XML2Dict()
    root = xml.parse(file_name)
    # get a dict object
    anno = root.annotation
    image_name = anno.filename
    item = {'filename': prefix + image_name, 'class': 'image', 'annotations': []}

    for obj in anno.object:

        cls = {'l_faster': 'C1', 'r_faster': 'C2'}[obj.name]
        box = obj.bndbox
        x, y, width, height = int(box.xmin), int(box.ymin), int(box.xmax) - int(box.xmin), int(box.ymax) - int(box.ymin)
        item['annotations'] += [{
                "class": cls,
                "height": height,
                "width": width,
                "x": x,
                "y": y
            }]
    return item

if __name__ == '__main__':
    annotations = []
    anno_name = 'AR_001-550.json'
    files = glob.glob('Annotations/AR_*.xml')
    files = sorted(files)
    # print files.sort()
    for filename in files:
        item = getAnnos(filename, prefix='TFS/JPEGImages/')
        print item
        print '-----------------'
        annotations += [item] #"xmls/AL_00001.xml"
    serializeToFile(anno_name, annotations)


