# -*- coding: utf-8 -*-
# @Time    : 2023/6/24
# @Author  : wumuwutu
# @Email   : 18392331353@163.com
# @File    : data_polish.py
# @Software: Pycharm2022.3.3
# @Function: Optimize the downloaded images
"""

    You can run this program directly without making any params adjustments, unless you need to customize it.
    Here are descriptions of several important params:
        source_Path: This directory contains folders of images that have been categorized.
        target_Path: This directory stores folders of images that have been optimized.

"""

import os
import shutil
from tqdm import tqdm
import re
import time
import cv2
import numpy as np

params = {
    "source": 0,  # 0: default source("./download/"), 1: custom path
    "source_Path": "D:/VegClassification/download - 副本/",  # custom source path(use absolute address)
    "target": 0,  # 0: default storage location("./polished/"), 1: custom storage location
    "target_Path": "D:/VegClassification/polished/",  # custom storage path(use absolute address)
    "type": 1,  # 1: default(use colour images), 0: use grayscale images
    "remove": 1,  # 1: discard grayscale images in source images, 0: retain grayscale image
}


def input_dir(directory):
    """

    Args:
        directory: the initial directory

    Returns: modified directory

    """
    name = input("文件夹 {} 非英文， 请修改为英文：".format(directory))
    if re.match(r"^[A-Za-z_]+$", name):
        return name
    else:
        return input_dir(name)


def cv_imread(source_path):
    """

    Args:
        source_path: image's location

    Returns:
        decoded image information

    """
    # support Chinese path
    return cv2.imdecode(np.fromfile(source_path, dtype=np.uint8), -1)  # read and return the image


def cv_imwrite(save_path, cv_img):
    """

    Args:
        save_path: the location of the image to store with image name
        cv_img: image

    Returns:
        None

    """
    if params["type"] == 1:
        pass  # keep colour
    else:
        if len(cv_img.shape) == 3:  # convert colour image to grayscale image
            cv_img = 0.21*cv_img[:, :, 0] + 0.71*cv_img[:, :, 1] + 0.07*cv_img[:, :, 2]
    cv2.imencode(save_path[-4:], cv_img)[1].tofile(save_path)  # store(image suffix, img_info, full path of the image)


def main():
    """

    Returns: None

    """

    # get the Source Path and Target Path
    initial_path = os.getcwd()
    initial_source_path = initial_path + "/download/"
    initial_target_path = initial_path + "/polished/"
    if params["source"] == 1:
        initial_source_path = params["source_Path"]
    if params["target"] == 1:
        initial_target_path = params["target_Path"]

    # verify the target directory
    if os.path.isdir(initial_target_path):
        pass
    else:
        os.mkdir(initial_target_path)

    directories = os.listdir(initial_source_path)
    for directory in directories:

        temp_source_path = initial_source_path + directory
        if os.path.isdir(temp_source_path):

            # Change directory to English if it's not English
            if re.match(r"^[A-Za-z_]+$", directory):
                source_path = temp_source_path
            else:
                directory = input_dir(directory)
                source_path = initial_source_path + directory
                os.rename(temp_source_path, source_path)  # change source directory name to English

            target_path = initial_target_path + directory + "\\"
            if os.path.isdir(target_path):
                shutil.rmtree(target_path)
            os.mkdir(target_path)  # Don't forget to mkdir, it's critical.

            # optimize on images in source_path
            images = os.listdir(source_path)
            with tqdm(total=len(images), colour="green") as pbar:
                i = 1
                for index, image in enumerate(images):
                    if image.endswith(".jpg"):

                        """
                        Following are accurate operation on each image, including:
                            1.Changing its name to English if it's not English.
                            2.Whether remove grayscale images depends on the setting.
                        The reason why don't use index but "i" as image's name is because:
                            Some images may be eliminated during the optimization, so the names are not consecutive like
                            this: img_1.jpg, img_3.jpg, img_4.jpg. This makes me feel uncomfortable.
                        """
                        img = cv_imread(source_path + "/" + image)
                        img_channel = len(img.shape)
                        if img_channel == 3:
                            # color image, store
                            name = directory + "_" + str(i) + ".jpg"
                            save_path = os.path.join(target_path, name).replace("\\", "/")
                            cv_imwrite(save_path, img)
                            i += 1
                        else:
                            # grayscale image
                            if params["remove"]:
                                # ignore
                                pass
                            else:
                                # store
                                name = directory + "_" + str(i) + ".jpg"
                                save_path = os.path.join(target_path, name).replace("\\", "/")
                                cv_imwrite(save_path, img)
                                i += 1

                        """
                        Following are just for displaying the progress and does not have any actual functionality.
                        """
                        if index != len(images) - 1:
                            pbar.set_postfix_str("正在处理{}文件夹".format(directory))
                        else:
                            pbar.set_postfix_str("处理完成{}文件夹".format(directory))
                        pbar.update(1)
            # Change the source directory name back if it had been changed. This can avoid some unnecessary conflict.
            os.rename(source_path, temp_source_path)


if __name__ == "__main__":
    main()
