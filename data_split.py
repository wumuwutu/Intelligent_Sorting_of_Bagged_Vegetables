# -*- coding: utf-8 -*-
# @Time    : 2023/6/29
# @Author  : wumuwutu
# @Email   : 18392331353@163.com
# @File    : get_data.py
# @Software: Pycharm2022.3.3
# @Function: divide the downloaded images into three sets
"""

    You can run this program directly without making any params adjustments, unless you need to customize it.
    You can customize your train、val and test directories.
    Images are split in 6:2:2.

"""

import os
import random
import shutil
from tqdm import tqdm


params = {
    "train": 0,   # 0: default train set("./data/train"), 1: custom path
    "train_path": "D:/VegClassification/data/train",  # custom train path(use absolute address)
    "val": 0,     # 0: default val set("./data/val"),     1: custom path
    "val_path": "D:/VegClassification/data/val",      # custom val path(use absolute address)
    "test": 0,    # 0: default test set("./data/test"),   1: custom path
    "test_path": "D:/VegClassification/data/test",    # custom test path(use absolute address)
    "source": 0,  # 0: default test set("./polish"),      1: custom path
    "source_path": "D:/VegClassification/polished",   # custom source path(use absolute address)

    "mode": 1,  # 1: copy, 0: move

    "train_scale": 0.7,
    "val_scale": 0.2,
    "test_scale": 0.1,
}


def verify_storage_path(train_path, val_path, test_path):
    """

    Args:
        train_path: train
        val_path: val
        test_path: test

    Returns: None

    """
    if os.path.isdir(train_path):
        shutil.rmtree(train_path)
    os.mkdir(train_path)
    if os.path.isdir(val_path):
        shutil.rmtree(val_path)
    os.mkdir(val_path)
    if os.path.isdir(test_path):
        shutil.rmtree(test_path)
    os.mkdir(test_path)


def move_image(source_path, target_path, image, index, directory):
    """

    Args:
        source_path: path where the image locates
        target_path: path where the image move to
        image: image
        index: the number of the image in a directory
        directory: direrctory

    Returns: None

    """

    if params["mode"]:
        shutil.copy(os.path.join(source_path, image), os.path.join(target_path, directory+"_"+str(index)+".jpg"))
    else:
        shutil.move(os.path.join(source_path, image), os.path.join(target_path, directory+"_"+str(index)+".jpg"))


def main():
    """

    Returns:
        None

    """
    # init four path
    initial_path = os.path.join(os.getcwd(), "data")

    # record the father directory
    super_train_path = os.path.join(initial_path, "train")
    super_val_path = os.path.join(initial_path, "val")
    super_test_path = os.path.join(initial_path, "test")
    super_source_path = os.path.join(os.getcwd(), "polished")
    if params["train"]:
        super_train_path = params["train_path"]
    if params["val"]:
        super_val_path = params["val_path"]
    if params["test"]:
        super_test_path = params["test_path"]
    if params["source"]:
        super_source_path = params["source_path"]

    # ensure the target path exists
    if os.path.isdir(initial_path):
        shutil.rmtree(initial_path)
    os.mkdir(initial_path)
    verify_storage_path(super_train_path, super_val_path, super_test_path)  # cannot be omitted

    # the number of images that should be divided in each directory
    # count_train, count_val, count_test = 0, 0, 0

    # operate on each directory
    directories = os.listdir(super_source_path)
    for directory in directories:

        # initial four path
        train_path = os.path.join(super_train_path, directory)
        val_path = os.path.join(super_val_path, directory)
        test_path = os.path.join(super_test_path, directory)
        source_path = os.path.join(super_source_path, directory)

        # list and operate on each specific image in the directory
        images = os.listdir(source_path)
        random.shuffle(images)  # shuffle the image list

        # calculate the number for each directory
        count_train = int(len(images) * float(params["train_scale"]))
        count_test = int(len(images) * float(params["test_scale"]))
        count_val = len(images) - count_train - count_test

        # verify the target path
        verify_storage_path(train_path, val_path, test_path)

        with tqdm(total=len(images), colour="green") as pbar:

            trains, vals, tests = 1, 1, 1  # the new name of each image begins with 1(.jpg)
            for index, image in enumerate(images):  # index begins with 0
                """
                Now count and divide the images into train, val and test set in 6:2:2 proportion.
                """
                if index < count_train:
                    move_image(source_path, train_path, image, trains, directory)
                    trains += 1
                elif index < count_train + count_val:
                    move_image(source_path, val_path, image, vals, directory)
                    vals += 1
                else:
                    move_image(source_path, test_path, image, tests, directory)
                    tests += 1

                """
                Following are just for displaying the progress and does not have any actual functionality.
                """
                if index < len(images) - 1:
                    pbar.set_postfix_str("正在处理{}文件夹".format(directory))
                else:
                    pbar.set_postfix_str("处理完成{}文件夹".format(directory))
                pbar.update(1)


if __name__ == "__main__":
    main()
