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

​		清洗之后的图片放在polish文件夹下

#### 3.5 图片分割

​		在开始训练模型之前，还需要划分数据集

​		在data文件夹下，按照train : val : test = 6 : 2 : 2的比例划分，也可以自己调节

​		具体代码见：[data_split.py](https://github.com/wumuwutu/Intelligent_Sorting_of_Bagged_Vegetables/blob/master/data_split.py)

​		你也可以在程序中选择是否将polish文件夹下的图片直接移动到data目录下以节省空间

#### 3.6 模型训练

​		具体步骤和一般的深度训练步骤类似。

​		具体代码见：[train.py](https://github.com/wumuwutu/Intelligent_Sorting_of_Bagged_Vegetables/blob/master/train.py)

​		你可以在params中进行超参设置

​		每次训练出的模型都会保存在当前目录下，你根据每次模型的正确率保留最高的模型

#### 3.7测试

​		对训练好的模型进行测试

​		具体代码见：[test.py](https://github.com/wumuwutu/Intelligent_Sorting_of_Bagged_Vegetables/blob/master/test.py)和[test2.py](https://github.com/wumuwutu/Intelligent_Sorting_of_Bagged_Vegetables/blob/master/test.py)

​		前者针对data/test下的所有图片一次性进行测试，并输出预测结果、标签和概率

​		后者只针对选择的某一张图片进行测试

#### 3.8图形化界面

​		通过可视化界面，更好的进行测试操作

​		具体代码见：[window.py](https://github.com/wumuwutu/Intelligent_Sorting_of_Bagged_Vegetables/blob/master/window.py)

![效果](https://github.com/wumuwutu/Intelligent_Sorting_of_Bagged_Vegetables/blob/master/Res_imgs/img1.png)





### 4.部署



#### 4.1模型转换

​		需要将训练好的.pth模型转换成.pt模型

​		具体代码见：[trans_model.py](https://github.com/wumuwutu/Intelligent_Sorting_of_Bagged_Vegetables/blob/master/trans_model.py)

#### 4.2创建Android Studio项目

​		在这个项目中，对界面的按键布局、响应逻辑和界面美化等进行了编辑

​		具体代码可以打开项目：[Mycls](https://github.com/wumuwutu/Intelligent_Sorting_of_Bagged_Vegetables/tree/master/MyCls)

​		最终实现的界面效果如下：

![效果](https://github.com/wumuwutu/Intelligent_Sorting_of_Bagged_Vegetables/blob/master/Res_imgs/img0.jpg)



​		ps：美观不美观能用就行（相册和相机的图片还是从Huawei手机上扣的(/≧▽≦)/~┴┴）

#### 4.3项目中的几个注意事项

​		①如果直接将拍的照片输入给模型，手机cpu可能会因为算力不足而卡死，所以需要进行预处理，将图片缩放到512\*512或256\*256（建议和训练时的参数保持一致）

​		②由于手机的cpu和电脑cpu的算力差距以及精度差距，在某些情况下可能会出现预测结果不太准确的可能

​		③构建好的apk文件在MyCls\app\build\outputs\apk\debug下

​		④可以在代码中修改是否展示预测的概率，也可以设置展示概率最大的，还是展示概率排在前两位的



### 5.补充

本项目所有数据均为拍摄收集，共计4.7G

要获取数据集或想要咨询其他事项，可以联系我18392331353@163.com





​		





​		
