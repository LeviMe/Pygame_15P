#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  1 03:13:00 2021

@author: levi
"""

import cv2
import os
import numpy as np
import random as rd
from PIL import ImageFont, ImageDraw, Image


LENGTH = 360
FONTPATH = "./Assets/fonts/cookie.ttf"
FONT = ImageFont.truetype(FONTPATH, int(8 / 10 * LENGTH))


def generate_bg_image():
    path = os.path.join("Assets", "pictures", "bg3.jpg")
    image = cv2.imread(path)
    image_h, image_w, _ = image.shape
    x0, y0 = rd.randint(0, image_w - LENGTH - 1), rd.randint(0, image_h - LENGTH - 1)
    image = image[y0 : y0 + LENGTH, x0 : x0 + LENGTH, :]

    image = cv2.addWeighted(image, 0.75, image, 0, 0.2)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2RGBA)
    # passage en RGBA pour pixels tranparents sur les bords.
    return image


def set_rounded_corners(img, ratio):
    ALPHA = (255, 255, 255, 0)
    n, p, _ = img.shape
    assert n == p
    l = int(n * ratio)
    for x in range(0, l):
        for y in range(0, l):
            if ((l - x) ** 2 + (l - y) ** 2) > l ** 2:
                img[x, y, :] = ALPHA
                img[n - x - 1, y, :] = ALPHA
                img[x, n - y - 1, :] = ALPHA
                img[n - x - 1, n - y - 1, :] = ALPHA


def set_number(number, bg_image):
    color = (255, 255, 255, 255)
    img_digit = np.zeros((LENGTH, LENGTH, 3), dtype=np.uint8)
    img_digit = Image.fromarray(img_digit)
    label = str(number)
    draw = ImageDraw.Draw(img_digit)
    draw.text((0, 0), label, font=FONT, fill=color)

    img_digit = np.array(img_digit)
    s_lines = np.sum(np.sum(img_digit, axis=1), axis=1)
    s_col = np.sum(np.sum(img_digit, axis=0), axis=1)

    x_min, x_max, y_min, y_max = 0, LENGTH - 1, 0, LENGTH - 1
    while s_lines[x_min] == 0:
        x_min += 1
    while s_lines[x_max] == 0:
        x_max -= 1
    while s_col[y_min] == 0:
        y_min += 1
    while s_col[y_max] == 0:
        y_max -= 1

    img_digit = img_digit[x_min:x_max, y_min:y_max, :]

    width, height = x_max - x_min, y_max - y_min
    x0, y0 = (LENGTH - width + 1) // 2, (LENGTH - height + 1) // 2
    img_centered = np.zeros((LENGTH, LENGTH, 3), dtype=np.uint8)
    img_centered[x0 : x0 + width, y0 : y0 + height, :] = img_digit[:width, :height, :]

    img_bgra = cv2.cvtColor(img_centered, cv2.COLOR_BGR2BGRA)
    alpha = img_bgra[:, :, 3]
    alpha[np.all(img_bgra[:, :, 0:3] == (0, 0, 0), 2)] = 0
    img_result = cv2.addWeighted(bg_image, 1, img_bgra, 1, 0.2)
    return img_result


def main(n=25):

    for i in range(1, n):
        tile = generate_bg_image()
        tile = set_number(i, tile)
        set_rounded_corners(tile, 0.2)

        path = os.path.join("Assets", "pictures", "Tile_" + str(i) + "_.png")
        print("generating Tile_" + str(i) + "_.png")
        cv2.imwrite(path, tile)

    # cv2.imshow("nom fenetre", tile)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
