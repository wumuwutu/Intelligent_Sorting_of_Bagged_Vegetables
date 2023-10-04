# -*- coding: utf-8 -*-
# @Time    : 2023/6/23
# @Author  : wumuwutu
# @Email   : 18392331353@163.com
# @File    : data_get.py
# @Software: Pycharm2022.3.3
# @Function: Crawl images from Bing
"""

    These may are reasons why you don't get the excepted images:
    1.The searching engine doesn't show specific amount of the images with keyword in a page .
    2.The regular expression has bugs.

"""

import math
import requests
import re
import os


def download_image(keyword, link, path, success_num):
    """

    Args:
        keyword: type of the image
        link: hyperlink to the image
        path: where to store the image
        success_num: number of the image that have been downloaded

    Returns:
        None

    """
    image_name = path + "\\" + keyword + "_" + str(success_num) + ".jpg"
    image = requests.get(link)
    with open(image_name, "ab") as f:
        f.write(image.content)


def scrape_images(keyword, page_num):
    """

    Args:
        keyword: is what you want to search for
        page_num: is the number of the page, each page includes about 35 images

    Returns:
        None

    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }
    initial_url = f"https://www.bing.com/images/search?q={keyword}"

    try:
        # count the images
        total_num, success_num, failed_num, repeated_num = 0, 0, 0, 0

        # all downloaded image links
        links = []

        # the path to save: ../download/{keyword}
        if os.path.isdir(os.path.join(os.getcwd(), "download")):
            pass
        else:
            os.mkdir(os.path.join(os.getcwd(), "download"))

        path = os.getcwd() + "\\download\\{}".format(keyword)
        if not os.path.exists(path):
            os.mkdir(path)

        # operate in each page
        for i in range(int(page_num)):
            url = initial_url + "&first={}".format(30*i)  # request to access the page
            response = requests.get(url, headers=headers).content.decode()
            pattern = r"https:\/\/tse\d+-mm.cn.bing.net\/th\?id=OIP\.[\w, -]+&amp;pid=15.1"
            matches = re.findall(pattern, response)

            # download
            for link in matches:
                total_num += 1

                # repeated link
                if link in links:
                    repeated_num += 1

                # new link
                else:
                    try:
                        success_num += 1
                        download_image(keyword, link, path, success_num)
                    except Exception:
                        failed_num += 1
                    finally:
                        links.append(link)
                ratio = round(total_num/(page_num*35)*100, 1)
                print("\r\033[91m|" + "■"*math.ceil(ratio), end="")
                print(" "*(100-math.ceil(ratio)) + "{:5>}%|\033[0m".format(ratio), end="")

    except Exception:
        print("出错了！")
        exit()

    print("\r\033[91m|" + "■"*100 + "100.0%|\033[0m" + "\n" + "下载完毕!")
    print("访问{}个图片链接，重复{}张，下载{}张，失败{}张".format(total_num, repeated_num, success_num, failed_num))


def main():
    """

    Returns:
        None

    """
    try:
        keyword = input("请输入你想要下载的图片类型：")
        page_num = int(input("请输入要下载的图片数量？（1为35张，2为70张）："))
    except ValueError:
        print("输入有误!")
        exit()
    # 调用爬虫函数
    scrape_images(keyword, page_num)


if __name__ == '__main__':
    main()
