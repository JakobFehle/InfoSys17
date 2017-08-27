#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import os
from os import listdir
import Tkinter as tk
import cv2
from colormath.color_objects import sRGBColor, AdobeRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
from operator import itemgetter


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


    avGColorRgb = sRGBColor((totalR / totalPixel) / 255., (totalG / totalPixel) / 255., (totalB / totalPixel) / 255.);

    avgColorLab = []
  
    avgColorLab.append(name)
    avgColorLab.append(convert_color(avGColorRgb, LabColor))
    
    
    return avgColorLab

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


def getClosestTrousers(imgName):
    referenceColor = {}
    deltaEValues = []
    
    for img in imagesCompiledTrousers:
        if(img[0] == imgName):
            referenceColor = img[1]

    for img in imagesCompiledTrousers:
        image = []
        image.append(img[0])
        image.append(delta_e_cie2000(referenceColor, img[1]))
        deltaEValues.append(image)
        
    deltaEValues.sort(key=itemgetter(1))   

    return deltaEValues[1:4]
        
def getClosestShoes(imgName):
    referenceColor = {}
    deltaEValues = []
    
    for img in imagesCompiledShoes:
        if(img[0] == imgName):
            referenceColor = img[1]

    for img in imagesCompiledShoes:
        image = []
        image.append(img[0])
        image.append(delta_e_cie2000(referenceColor, img[1]))
        deltaEValues.append(image)
        
    deltaEValues.sort(key=itemgetter(1))   

    return deltaEValues[1:4]

def getClosestJacket(imgName):
    referenceColor = {}
    deltaEValues = []
    
    for img in imagesCompiledJacket:
        if(img[0] == imgName):
            referenceColor = img[1]

    for img in imagesCompiledJacket:
        image = []
        image.append(img[0])
        image.append(delta_e_cie2000(referenceColor, img[1]))
        deltaEValues.append(image)
        
    deltaEValues.sort(key=itemgetter(1))   

    return deltaEValues[1:4]

def getClosestTop(imgName):
    referenceColor = {}
    deltaEValues = []
    
    for img in imagesCompiledTop:
        if(img[0] == imgName):
            referenceColor = img[1]

    for img in imagesCompiledTop:
        image = []
        image.append(img[0])
        image.append(delta_e_cie2000(referenceColor, img[1]))
        deltaEValues.append(image)
        
    deltaEValues.sort(key=itemgetter(1))   

    return deltaEValues[1:4]

print(getClosestTrousers('chino-grau-street-one.jpg'))
print(getClosestShoes('ballerinas-in-metallicoptik-silber-buffalo_list.jpg'))
print(getClosestJacket('blazer-mit-kurzform-grau-b-c-best-connections-by-heine.jpg'))
print(getClosestTop('bluse-mit-muster-weiss-orsay.jpg'))
