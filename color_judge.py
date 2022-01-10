# from scraping import SapporoSubwayScraper
import os
import csv
import glob
import numpy as np
import subprocess
# import urllib.request
# from PIL import Image
from pdf2image import convert_from_path, convert_from_bytes
from pathlib import Path

def rgb_to_type(rgb_list)->int:
    #色差の閾値
    threshold = 50
    color_array = np.asarray(rgb_list)
    for i in range(len(CROWD_RGBs)):
        crowd_rgb_array = np.asarray(CROWD_RGBs[i])
        color_dist = abs(color_array - crowd_rgb_array)
        sum_dist = color_dist.sum()
        if sum_dist < threshold:
            return i #0 - 1 混み具合

def judge_none(array):
    # 配列が正しいかの判定（Noneがある，最初が0でない，最後が1でない，1のあとに0があるとアウト）
    if array[0] == 1:
        return False
    if array[len(array)-1] == 0:
        return False
    for elem in array:
        if elem is None:
            return False
    for i in range(1,len(array)-1):
        if array[i-1] == 1 and array[i] == 0:
            return False
    return True # いずれもあてはまらなければTrue

# 第1引数は元のPDFファイルのフルパス，第2引数は保存先のPDFファイルのフルパス

CROWD_RGBs = [
    [255, 255, 255],
    [118, 113, 113]
]

pdf_filepath = Path("./for_test.pdf")
pdf_images = convert_from_path(pdf_filepath)
judged_color = []
# iページずつ特定のセルの色を判定する
for page in pdf_images:
    img_array = np.asarray(page)
    # print(img_array[10][750])
    judged_color.append(rgb_to_type(img_array[10][750])) # 判定配列の完成

# 配列が不正ならストップしてlogに書く？
print(judge_none(judged_color))
que_end_page = 0 #解説ページが始まるページ
for i in range(len(judged_color)):
    if judged_color[i] == 1:
        que_end_page = i
        break

cmd = f"pdftk {pdf_filepath} cat 1-{que_end_page} output output.pdf"
print(cmd)
os.system(cmd)
