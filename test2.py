# -*- coding: UTF-8 -*-
"""
@Project : VegClassification
@File    : test2.py
@Author  : 沕穆乌菟
@Email   : 18392331353@163.com
@Date    : 2023/9/22 18:03 
"""
import torch
from PIL import Image
from torchvision.transforms import transforms

class_names = ['cabbage', 'cauliflower', 'courgette', 'cowpea', 'eggplant', 'green_pumpkin',
                           'lentinula_edodes', 'potato', 'screw_pepper', 'tomato']


def main():
    # device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    device = torch.device("cpu")
    img_path = "D:\\VegClassification\\download\\screw_pepper\\IMG_20230930_130528.jpg"
    img = Image.open(img_path)

    transform = transforms.Compose([
        transforms.Resize((474, 474)),
        transforms.ToTensor(),
        transforms.Normalize((0.5,), (0.5,))
    ])
    tensor_img = transform(img)
    tensor_img = tensor_img.to(device)
    tensor_img = tensor_img.unsqueeze(0)

    model = torch.jit.load("cls_10_3.pt")

    output = model(tensor_img)

    idx, pred = output.max(1)
    print(class_names[pred])
    print(idx)
    print(output)


if __name__ == "__main__":
    main()