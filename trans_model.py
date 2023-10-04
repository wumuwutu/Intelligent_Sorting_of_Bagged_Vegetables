# -*- coding: UTF-8 -*-
"""
@Project : VegClassification
@File    : trans_model.py
@Author  : 沕穆乌菟
@Email   : 18392331353@163.com
@Date    : 2023/9/22 16:12 
"""
import torch
import torchvision
from torch.utils.mobile_optimizer import optimize_for_mobile

model = torch.load("resnet50_cls_13.pth", map_location="cpu")  # 在手机的cpu上跑
model.eval()
example = torch.rand(1, 3, 224, 224)
traced_script_module = torch.jit.trace(model, example)
# optimized_traced_model = optimize_for_mobile(traced_script_module)
# optimized_traced_model._save_for_lite_interpreter("app/src/main/assets/model.ptl")
torch.jit.save(traced_script_module, "cls_13.pt")
