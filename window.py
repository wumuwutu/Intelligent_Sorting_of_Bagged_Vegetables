# # -*- coding: UTF-8 -*-
# """
# @Project : VegClassification
# @File    : window.py
# @Author  : 沕穆乌菟
# @Email   : 18392331353@163.com
# @Date    : 2023/9/14 21:28

import sys

import torch
import torchvision.models
from PIL import Image
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QTabWidget, QDesktopWidget, QTextEdit
from PyQt5.QtGui import QImage, QPixmap, QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog
from torchvision import transforms


class MainWindow(QTabWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("套袋蔬菜智能分类")
        self.img_path = None  # 选择的图片
        self.screen_geometry = QDesktopWidget().screenGeometry()

        # 初始化居中窗口
        self.aw = self.screen_geometry.width() * 2 // 3
        self.ah = self.screen_geometry.height() * 2 // 3
        self.ax = int((self.screen_geometry.width() - self.aw) / 2)
        self.ay = int((self.screen_geometry.height() - self.ah) / 2)
        self.setGeometry(self.ax, self.ay, self.aw, self.ah)

        # 两个项目栏
        self.tab1 = QWidget()
        self.tab2 = QWidget()

        # 项目栏名称
        self.addTab(self.tab1, "分类")
        self.addTab(self.tab2, "说明")

        # 设置展示图片的区域的样式
        self.img_label = QLabel(self.tab1)
        self.init_img_label()

        # 设置“选择图片”按钮的样式
        self.select_btn = QPushButton("选择图像", self.tab1)
        self.init_select_btn()

        # 设置“确认”按钮的样式
        self.commit_btn = QPushButton("识  别", self.tab1)
        self.init_commit_btn()

        # 设置“展示结果”文本框的样式
        self.result_text = QTextEdit(self.tab1)
        self.init_result_text()

        # 设置说明
        self.info_text = QTextEdit(self.tab2)
        self.init_info_text()

        # 加载模型
        self.device = torch.device("cpu")
        # self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.model = torch.load('resnet50_cls_13.pth')
        # self.model = torchvision.models.resnet50()
        # self.model.load_state_dict(torch.load("resnet50_model_29.pth"))

        # self.model = torch.jit.load("cls_3.pt")
        self.model.to(self.device)

        self.img_transforms = transforms.Compose([
                transforms.Resize(256),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            ])

        # 设置类别
        # self.class_names = ["西葫芦", "香菇", "红提"]
        self.class_names = ['西兰花', '卷心菜', '胡萝卜', '菜花', '西葫芦', '豇豆', '黄瓜', '茄子',
                            '绿南瓜', '香菇' '土豆', '螺丝椒', '西红柿']

    def init_img_label(self):
        self.img_label.setGeometry(int(self.ah / 7), int(self.ah / 12), int(self.ah / 1.5), int(self.ah / 1.5))
        self.img_label.setAlignment(Qt.AlignCenter)
        self.img_label.setStyleSheet("background-color: #F9F9F9; color: white; border:1px solid black")

    def init_select_btn(self):
        font = self.select_btn.font()
        font.setFamily("楷体")
        font.setPointSize(24)
        self.select_btn.setFont(font)
        self.select_btn.setGeometry(int(self.ah * 0.315), int(self.ah * 0.8), int(self.ah / 3),
                                    int(self.ah / 10))
        self.select_btn.clicked.connect(self.select_img)

    def init_commit_btn(self):
        font = self.commit_btn.font()
        font.setFamily("楷体")
        font.setPointSize(24)
        self.commit_btn.setFont(font)
        self.commit_btn.setGeometry(int(self.aw * 0.65), int(self.ah * 0.5), int(self.ah / 3),
                                    int(self.ah / 10))
        self.commit_btn.clicked.connect(self.analyse_img)

    def init_result_text(self):
        self.result_text.setStyleSheet("border: 1px solid #F9F9F9;"
                                       "background-color: #F9F9F9")
        font = QFont("楷体", 24)
        self.result_text.setFont(font)
        self.result_text.setPlainText("等待识别...")

        self.result_text.setAlignment(Qt.AlignCenter)

        self.result_text.setGeometry(int(self.aw * 0.6), int(self.ah * 0.3),
                                     int(self.ah / 2), int(self.ah / 10))

    def init_info_text(self):
        self.info_text.setStyleSheet("border: 1px solid #F9F9F9;"
                                     "background-color: #F9F9F9")
        font = QFont("楷体", 12)
        self.info_text.setFont(font)
        self.info_text.setGeometry(0, 0, int(self.aw), int(self.ah))
        with open("veg_info.txt", "r", encoding="utf-8") as f:
            msg = f.read()
        self.info_text.setPlainText(msg)

    def select_img(self):
        filename, _ = QFileDialog.getOpenFileName(self, "选择图像文件", "", "Image files (*.png *.jpg *.jpeg)")
        if filename:
            image = QImage(filename)
            self.img_path = filename
            # print(self.img_path)
            if not image.isNull():
                pixmap = QPixmap.fromImage(image)
                self.img_label.setPixmap(pixmap.scaled(int(self.ah/1.5), int(self.ah/1.5), Qt.KeepAspectRatio))

    def analyse_img(self):
        if self.img_path is not None:
            self.model.eval()
            img = Image.open(self.img_path)
            img = self.img_transforms(img)
            img = img.unsqueeze(0)
            img = img.to(self.device)
            output = self.model(img)
            idx = torch.argmax(output).item()
            self.result_text.setPlainText(self.class_names[idx])
            self.result_text.setAlignment(Qt.AlignCenter)
            # probs = torch.nn.functional.softmax(output[0], dim=0)

        else:
            self.result_text.setPlainText("请选择图片")
            self.result_text.setAlignment(Qt.AlignCenter)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
