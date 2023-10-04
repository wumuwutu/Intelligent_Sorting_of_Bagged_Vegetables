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
    "source_path": "D:/VegClassification/download/"  # custom source path(use absolute address)
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
                # open the image
                img = Image.open(os.path.join(dir_name, img_name))

                # part name of transformed image
                part_name = os.path.join(dir_name, img_name[:-4])

                # # rotate 90°
                img_rotate_90 = img.rotate(90)
                img_rotate_90_name = part_name + "_rotate_90.jpg"
                img_rotate_90.save(img_rotate_90_name)

                # # rotate 180°
                img_rotate_180 = img.rotate(180)
                img_rotate_180_name = part_name + "_rotate_180.jpg"
                img_rotate_180.save(img_rotate_180_name)

                # # rotate 270°
                img_rotate_270 = img.rotate(270)
                img_rotate_270_name = part_name + "_rotate_270.jpg"
                img_rotate_270.save(img_rotate_270_name)

                # Horizontal symmetry
                img_horizontal = ImageOps.mirror(img)
                img_horizontal_name = part_name + "_hor.jpg"
                img_horizontal.save(img_horizontal_name)

                # Vertical symmetry
                img_vertical = img.transpose(Image.FLIP_TOP_BOTTOM)
                img_vertical_name = part_name + "_ver.jpg"
                img_vertical.save(img_vertical_name)

                enhancer = ImageEnhance.Contrast(img)

                # Low contrast
                contrast_factor = 0.5
                img_low_con = enhancer.enhance(contrast_factor)
                img_low_con_name = part_name + "_low_con.jpg"
                img_low_con.save(img_low_con_name)

                # High contrast
                contrast_factor = 1.5
                img_high_con = enhancer.enhance(contrast_factor)
                img_high_con_name = part_name + "_high_con.jpg"
                img_high_con.save(img_high_con_name)

                enhancer = ImageEnhance.Sharpness(img)

                # # Low sharpness
                sharpness_factor = 0.2
                img_low_sha = enhancer.enhance(sharpness_factor)
                img_low_sha_name = part_name + "_low_sha.jpg"
                img_low_sha.save(img_low_sha_name)

                # High sharpness
                sharpness_factor = 5.0
                img_high_sha = enhancer.enhance(sharpness_factor)
                img_high_sha_name = part_name + "_high_sha.jpg"
                img_high_sha.save(img_high_sha_name)

                enhancer = ImageEnhance.Brightness(img)

                # Low brightness
                brightness_factor = 0.6
                img_low_bri = enhancer.enhance(brightness_factor)
                img_low_bri_name = part_name + "_low_bri.jpg"
                img_low_bri.save(img_low_bri_name)

                # High brightness
                brightness_factor = 1.3
                img_high_bri = enhancer.enhance(brightness_factor)
                img_high_bri_name = part_name + "_high_bri.jpg"
                img_high_bri.save(img_high_bri_name)

                # Gaussian noise
                img = iio.imread(os.path.join(dir_name, img_name))
                mean = 0
                stddev = 10
                noise = np.random.normal(mean, stddev, img.shape)
                img_gau = np.clip((img + noise).astype(np.uint8), 0, 255)
                img_gau_name = part_name + "_gau.jpg"
                iio.imsave(img_gau_name, img_gau)

                pbar.update(1)


if __name__ == "__main__":
    main()
