# -*- coding: UTF-8 -*-
"""
@Project : VegClassification
@File    : test.py
@Author  : 沕穆乌菟
@Email   : 18392331353@163.com
@Date    : 2023/9/14 16:21 
"""

import torch
import torchvision
from torch.utils.data import DataLoader
from torchvision.transforms import transforms

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 定义变换
transform = transforms.Compose([
    transforms.Resize((474, 474)),
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

# 加载测试数据集
test_dataset = torchvision.datasets.ImageFolder("./data/test", transform=transform)
test_loader = DataLoader(test_dataset, batch_size=1, shuffle=True)

# 数据集名称
class_name = ['broccoli', 'cabbage', 'carrot', 'cauliflower', 'courgette', 'cowpea', 'cucumber', 'eggplant',
              'green_pumpkin', 'lentinula_edodes' 'potato', 'screw_pepper', 'tomato']

# 加载已经训练好的模型
model = torch.load('resnet50_cls_13.pth')
model = model.to(device)
model.eval()

# 进行测试
correct = 0
total = 0

i = 0
error_idx = []
probabilities = []
with torch.no_grad():
    for images, labels in test_loader:
        images = images.to(device)
        labels = labels.to(device)
        outputs = model(images)

        probabilities_batch = torch.softmax(outputs, dim=1)
        probabilities.append(probabilities_batch)

        _, predicted = torch.max(outputs.data, 1)

        if labels.item() != predicted.item():
            error_idx.append(i)
        i += 1

# 输出每个图像属于每个类别的概率和目标值
for idx, (probs, labels) in enumerate(zip(probabilities, test_loader.dataset.targets)):
    print(f"Image index: {idx}")
    for class_idx, prob in enumerate(probs.squeeze()):
        class_name = test_loader.dataset.classes[class_idx]
        print(f"{class_name}: {prob.item()}")

    target_class = test_loader.dataset.classes[labels]
    print("Target:", target_class)

# 输出错误分类的图像索引和数量
print("Error image indices:", error_idx)
print("Number of errors:", len(error_idx))

# import torch
# import torchvision
# from torch import nn
# from torch.autograd.grad_mode import F
# from torch.utils.data import DataLoader
# from torchvision.transforms import transforms
#
# # 设置使用的设备
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#
# # 定义变换
# transform = transforms.Compose([
#     transforms.Resize((474, 474)),
#     transforms.ToTensor(),
#     transforms.Normalize((0.5,), (0.5,))
# ])
#
# # 加载测试数据集
# test_dataset = torchvision.datasets.ImageFolder("./data/test", transform=transform)
# test_loader = DataLoader(test_dataset, batch_size=1, shuffle=True)
#
# # 数据集名称
# # class_name = ['broccoli', 'cucumber', 'potato', 'spinach', 'tomato']
# class_name = ['courgette', 'lentomila_edodes', 'red_grape']
#
# # 加载已经训练好的模型
# model = torch.load('resnet50_model.pth')
# model = model.to(device)
# model.eval()
#
# # 进行测试
# correct = 0
# total = 0
#
# i = 0
# error_idx = []
# with torch.no_grad():
#     for images, labels in test_loader:
#         images = images.to(device)
#         labels = labels.to(device)
#         outputs = model(images)
#
#         _, predicted = torch.max(outputs.data, 1)
#
#         if labels.item() != predicted.item():
#             error_idx.append(i)
#         i += 1
#
# # 计算准确率
# accuracy = 100 * (1 - len(error_idx)/i)
# print(f'Test Accuracy: {accuracy:.2f}%')
# print(error_idx)
# print("error_num：{}".format(len(error_idx)))