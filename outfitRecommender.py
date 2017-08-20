#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import os
from os import listdir
import Tkinter as tk
import cv2

# Einlesen Bilder
scriptPath = os.path.dirname(__file__)
imagesCompiledTrousers = []
imagesCompiledTop = []
imagesCompiledShoes = []
imagesCompiledJacket = []
filenamesTrousers = listdir(os.path.join(scriptPath,'data/trousers'))
filenamesTop = listdir(os.path.join(scriptPath,'data/top'))
filenamesShoes = listdir(os.path.join(scriptPath,'data/shoes'))
filenamesJacket = listdir(os.path.join(scriptPath,'data/jacket'))

def getAvgColor(name,image):
    # Zählt keine Weißen Pixel (Hintergrund) mit
    totalR = 0
    totalG = 0
    totalB = 0
    totalPixel = 0

    for row in image:
        for pixel in row:
            if pixel[0] > 245 and pixel[1]  > 245 and pixel[2] > 245:
                continue
            else:
                totalR = totalR + pixel[2]
                totalG = totalG + pixel[1]
                totalB = totalB + pixel[0]
                totalPixel = totalPixel +1

    avgPixel = []
    avgPixel.append(name)
    avgPixel.append(totalR / totalPixel)
    avgPixel.append(totalG / totalPixel)
    avgPixel.append(totalB / totalPixel)

    return avgPixel
    
for img in filenamesTrousers:
    image = cv2.imread(os.path.join(scriptPath,'data/trousers',img))
    imagesCompiledTrousers.append(getAvgColor(img, image))
    
for img in filenamesTop:
    image = cv2.imread(os.path.join(scriptPath,'data/top',img))
    imagesCompiledTop.append(getAvgColor(img, image))
    
for img in filenamesShoes:
    image = cv2.imread(os.path.join(scriptPath,'data/shoes',img))
    imagesCompiledShoes.append(getAvgColor(img, image))
    
for img in filenamesJacket:
    image = cv2.imread(os.path.join(scriptPath,'data/jacket',img))
    imagesCompiledJacket.append(getAvgColor(img, image))

print(imagesCompiledJacket)
print(imagesCompiledTop)
print(imagesCompiledShoes)
print(imagesCompiledJacket)

# Convert Average Colors from RGB into Lab Color Space for better 
# similarity measure (delta e distance measure between colors in 3D space)
#
#newCol = cv2.cvtColor(np.array([160,160,160]), cv2.COLOR_BGR2LAB)
