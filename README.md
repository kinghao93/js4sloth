# js4sloth
voc2007 xmls to sloth json

#### 1. Python中 使用XML2Dict 库
##### a lib to translate xml to dict of python
  object_dict.py xml2dict.py

#### 2. xml2json.py 
voc2007格式xml文件 逆向转换成 sloth中 标准json格式文件

#### 3.voc2007.py
将sloth 标注结果 *.Json 直接转换成 标准VOC2007格式数据集
##### 重要参数
  1. jsonPath: json 文件的绝对或相对路径
  2. imagePath： 给出脚本可以找到image的路径, <br/>
                 因为靠json中提供的路径, 脚本并不能保证一定可以访问到相应的image
  3. 按照不同比例划分数据集,在createMain函数调用时[eg: train:val:test=4:4:3 ]<br/>
     createMain(annos, pDir, rate_train=4, rate_val=4, rate_test=3)
