#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import os
from os import listdir
import Tkinter as tk
import cv2

# Einlesen Bilder
images = []
imagesAvgCol = []
scriptPath = os.path.dirname(__file__)
filenames = listdir(os.path.join(scriptPath,'data/Hose'))
print(filenames)
for img in filenames:
    images.append(cv2.imread(os.path.join(scriptPath,'data/Hose',img)))


for img in images:
    # Zählt keine Weißen Pixel (Hintergrund) mit
    totalR = 0
    totalG = 0
    totalB = 0
    totalPixel = 0

    for row in img:
        for pixel in row:
            if pixel[0] > 245 and pixel[1]  > 245 and pixel[2] > 245:
                continue
            else:
                totalR = totalR + pixel[0]
                totalG = totalG + pixel[1]
                totalB = totalB + pixel[2]
                totalPixel = totalPixel +1

    avgPixel = []
    avgPixel.append(totalR / totalPixel)
    avgPixel.append(totalG / totalPixel)
    avgPixel.append(totalB / totalPixel)

    print(avgPixel)
    imagesAvgCol.append(avgPixel)
    
    # Zählt weiße Pixel mit
    average_color_per_row = np.average(img, axis=0)
    average_color = np.average(average_color_per_row, axis=0)
    print(average_color)


print imagesAvgCol