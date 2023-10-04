# Intelligent_Sorting_of_Bagged_Vegetables / 套袋蔬菜智能分类





### 1.项目目标

本项目是基于图像识别技术的套袋蔬菜智能识别系统，并部署到手机app。该系统能够自动识别套袋蔬菜的种类，用以代替人工分类，提高生产效率和分类准确率。



### 2.环境

#### 2.1软件

​		Pycharm:                2022.3.3

​        Python:                   3.8.5

​        Miniconda3-py39: 4.9.2

​        Pytorch:                  1.10.0

​		CUDA:                     11.3

#### 2.2硬件

​		CPU: i7-12700H

​		GPU: RTX 3070 Laptop



### 3.训练模型

#### 3.1 收集数据

​		对于需要的大量套袋蔬菜的照片，可以直接拍摄，也可以使用爬虫。

​		具体代码见：[data_get.py](ttps://github.com/wumuwutu/Intelligent_Sorting_of_Bagged_Vegetables/blob/master/data_get.py)

​		若使用爬虫，则每次爬取的同一类照片会存储在”download/类别名“下

​		若爬取的照片质量太差，需要手动删除

#### 3.2照片缩放

​		如果原始图片尺寸过大，需要将图片进行缩放操作

​		具体代码见：[data_zoom.py](https://github.com/wumuwutu/Intelligent_Sorting_of_Bagged_Vegetables/blob/master/data_zoom.py)

​		运行此程序，程序会将download下的每一类别的图片全部缩放到指定大小（由于会改变原有图片，请提前做好备份）

#### 3.3图片增多

​		如果原始数据过少，可以将每张图片进行变换生成其他图片来增加原始数据集的数量，例如：旋转、对称、调节对比度、锐化、调节亮度、增加噪声

​		具体代码见：[data_more.py](https://github.com/wumuwutu/Intelligent_Sorting_of_Bagged_Vegetables/blob/master/data_more.py)

​		你可以通过注释程序中的相关代码来选择是否增加某一类型的图片

​		如果你的数据集充足，那么就不需要进行此操作

#### 3.4图片清洗

​		此程序会将原始数据中的图片统一命名，并且可以根据你的选择决定是否保留原始数据集中的灰度图像、是否将彩色图片转换成灰度图片

​		具体代码见：[data_polish.py](https://github.com/wumuwutu/Intelligent_Sorting_of_Bagged_Vegetables/blob/master/data_polish.py)

​		清洗之后的图片放在”polish/“下

#### 3.5 图片分割

​		在开始训练模型之前，还需要划分数据集

​		在data文件夹下，按照train : val : test = 6 : 2 : 2的比例划分，也可以自己调节

​		具体代码见：[data_split.py](https://github.com/wumuwutu/Intelligent_Sorting_of_Bagged_Vegetables/blob/master/data_split.py)

​		你也可以在程序中选择是否将polish文件夹下的图片直接移动到data目录下以节省空间





​		
