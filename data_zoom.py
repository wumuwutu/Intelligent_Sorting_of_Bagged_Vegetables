# -*- coding: utf-8 -*-
# @Time    : 2023/9/12
# @Author  : wumuwutu
# @Email   : 18392331353@163.com
# @File    : data_more.py
# @Software: Pycharm2022.3.3
# @Function: Symmetric, rotate, adjust contrast, and more operations on the image
import os

import imageio.v2 as iio
import numpy as np
from PIL import Image, ImageOps, ImageEnhance
from tqdm import tqdm

# all images
total_num = 0

params = {
    "source": 0,  # 0: default source("./download/"), 1: custom path
    "source_path": "D:/VegClassification/download/",  # custom source path(use absolute address)
    "zoom_size": 512
}


def main():
    # get the source path
    data_path = os.getcwd()
    data_path = os.path.join(data_path, "download")
    if params["source"]:
        data_path = params["source_path"]

    # operate on each directory
    directories = os.listdir(data_path)
    for directory in directories:

        # directory name
        dir_name = os.path.join(data_path, directory)

        # operator on each img
        images = os.listdir(dir_name)
        with tqdm(total=len(images), colour="green") as pbar:
            for img_name in images:
                img_path = os.path.join(dir_name, img_name)

                img = Image.open(img_path)
                w, h = img.size
                if h > w:
                    new_h, new_w = params["zoom_size"] * h / w, params["zoom_size"]
                else:
                    new_h, new_w = params["zoom_size"], params["zoom_size"] * w / h
                img = img.resize((int(new_w), int(new_h)))


                # img = img.resize(params["zoom_size"])
                img.save(img_path)

                pbar.update(1)


if __name__ == "__main__":
    main()
