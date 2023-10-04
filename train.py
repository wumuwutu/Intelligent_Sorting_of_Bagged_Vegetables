# -*- coding: UTF-8 -*-
"""
@Project : VegClassification
@File    : train.py
@Author  : 沕穆乌菟
@Email   : 18392331353@163.com
@Date    : 2023/9/12 16:55 
"""
import os
import torch.cuda
from torch import nn, optim
from torch.optim.lr_scheduler import StepLR, CosineAnnealingLR
from torch.utils.data import DataLoader
from torchvision import transforms, datasets, models


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print(torch.cuda.is_available())

# 获取图片文件夹
data_path = os.getcwd()
data_path = os.path.join(data_path, "data")

# 超参设置
params = {
    "model": "aaa",                                                  # 模型名称
    "train_dir": os.path.join(data_path, "train"),                   # 训练集路径
    "val_dir": os.path.join(data_path, "val"),                       # 验证集路径
    "img_size": 224,                                                 # 图片输入大小
    "device": device,                                                # 训练设备
    "lr": 0.001,                                                      # 学习速率
    "batch_size": 64,                                                # 批次大小
    "epochs": 30,                                                    # 训练次数
    "pretrained": True,                                              # 预训练
    "num_class": len(os.listdir(os.path.join(data_path, "train"))),  # 训练门类
    "weight_decay": 0.00001,                                            # 学习衰减率
    "save_dir": "outputs"                                            # 保存路径
}

print(params["num_class"])

# 定义训练集和验证集的数据变换
data_transforms = {
    'train': transforms.Compose([
        transforms.RandomResizedCrop(224),                                  # 随机裁剪图像为大小为224x224
        transforms.RandomHorizontalFlip(p=0.2),                                  # 随机水平翻转图像
        transforms.ToTensor(),                                              # 转换图像为张量
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])  # 对图像进行归一化
    ]),
    'val': transforms.Compose([
        transforms.Resize(256),                                             # 调整图像大小为256x256
        transforms.CenterCrop(224),                                         # 中心裁剪图像为大小为224x224
        transforms.ToTensor(),                                              # 转换图像为张量
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])  # 对图像进行归一化
    ]),
}

# 加载训练集和验证集的数据
image_datasets = {
    'train': datasets.ImageFolder(params["train_dir"], transform=data_transforms["train"]),
    'val': datasets.ImageFolder(params["val_dir"], transform=data_transforms["val"])
}

# 创建数据加载器
dataloaders = {
    'train': DataLoader(image_datasets['train'], batch_size=params["batch_size"], shuffle=True),
    'val': DataLoader(image_datasets['val'], batch_size=params["batch_size"], shuffle=False)
}

# 加载模型
model = models.resnet50(pretrained=True)
# model = torch.load("./model/resnet50_res_1.pth")


# 冻结ResNet-50模型的所有参数
for param in model.parameters():
    param.requires_grad = False

# 替换最后一层全连接层，输出类别数为10  并 将模型移动到可用的设备（GPU或CPU）
num_ftrs = model.fc.in_features
model.fc = nn.Linear(num_ftrs, params["num_class"])
model.to(device)

# 定义损失函数
loss_fn = nn.CrossEntropyLoss()
loss_fn = loss_fn.to(device)

# 定义优化器
optimizer = optim.SGD(model.fc.parameters(), lr=params["lr"], momentum=0.9)  # momentum=0.9 只训练自定义的分类层

# 定义学习率调度器
# scheduler = StepLR(optimizer, step_size=30, gamma=0.001)
scheduler = CosineAnnealingLR(optimizer, T_max=50, eta_min=0)

# 训练次数
total_train_step = 0

# 验证次数
total_test_step = 0

# 输出标签
class_to_idx = image_datasets["train"].class_to_idx
print(class_to_idx)

# 训练模型
for i in range(params["epochs"]):
    running_loss = 0.0

    # 训练
    model.train()
    for data in dataloaders["train"]:
        images, targets = data
        images = images.to(device)
        targets = targets.to(device)
        outputs = model(images)

        # 优化模型
        optimizer.zero_grad()  # 梯度归零
        loss = loss_fn(outputs, targets)
        loss.backward()
        optimizer.step()
        scheduler.step()

        # 记录训练次数
        total_train_step += 1
        if total_train_step % 20 == 0:
            print("训练次数：{}， Loss:{}".format(total_train_step, loss))

        # 每个epoch的累计损失
        running_loss += loss.item() * images.size(0)

    # 每个epoch的平均损失
    epoch_loss = running_loss / len(image_datasets["train"])

    # 验证
    model.eval()
    val_loss = 0.0
    val_corrects = 0
    total_test_loss = 0
    total_accuracy = 0

    with torch.no_grad():
        for images, targets in dataloaders["val"]:
            images = images.to(device)
            targets = targets.to(device)
            outputs = model(images)

            _, index = torch.max(outputs, 1)
            loss = loss_fn(outputs, targets)

            val_loss += loss.item() * targets.size(0)
            val_corrects = torch.sum(index == targets.data)

            # temp
            total_test_loss += loss.item()
            total_accuracy += (outputs.argmax(1) == targets).sum()
    print("epoch：{}，整体测试集上的Loss：{}".format(i+1, total_test_loss), end="， ")
    print("整体测试集上的正确率：{}".format(total_accuracy / len(image_datasets["val"])))

    # val_loss = val_loss / len(image_datasets["val"])
    # val_accuracy = val_corrects.double() / len(image_datasets["val"])

    # print('Epoch [{}/{}], Train Loss: {:.4f}, Val Loss: {:.4f}, Val Acc: {:.4f}'
    #       .format(i + 1, params["epochs"], epoch_loss, val_loss, val_accuracy))

    # torch.save(model.state_dict(), 'resnet50_model.pth')

    file_name = "resnet50_model_" + str(i) + ".pth"
    torch.save(model, file_name)
    # torch.save(model.state_dict(), file_name)

print(torch.cuda.is_available())
