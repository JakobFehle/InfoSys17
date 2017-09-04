#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from os import listdir
from PIL import Image
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
from operator import itemgetter

# Einlesen Bilder
scriptPath = os.path.dirname(__file__)
imagesCompiledTrousers = []
imagesCompiledTop = []
imagesCompiledShoes = []
imagesCompiledJacket = []
filenamesTrousers = listdir(os.path.join(scriptPath, 'data/trousers'))
filenamesTop = listdir(os.path.join(scriptPath, 'data/top'))
filenamesShoes = listdir(os.path.join(scriptPath, 'data/shoes'))
filenamesJacket = listdir(os.path.join(scriptPath, 'data/jacket'))
# used for dynamically accessing the four cloth lists
filenames = [filenamesTop, filenamesJacket, filenamesTrousers, filenamesShoes]


def getAvgColor(name, image):
    # Zählt keine Weißen Pixel (Hintergrund) mit
    totalR = 0
    totalG = 0
    totalB = 0
    totalPixel = 0

    for pixel in image:
        if pixel[0] > 245 and pixel[1] > 245 and pixel[2] > 245:
            continue
        else:
            totalR = totalR + pixel[0]
            totalG = totalG + pixel[1]
            totalB = totalB + pixel[2]
            totalPixel = totalPixel + 1

    avgColorRgb = sRGBColor((totalR / totalPixel) / 255., (totalG / totalPixel) / 255., (totalB / totalPixel) / 255.);
    avgColorLab = []

    avgColorLab.append(name)
    avgColorLab.append(convert_color(avgColorRgb, LabColor))

    return avgColorLab


for img in filenamesTrousers:
    image = Image.open(os.path.join(scriptPath, 'data/trousers', img))
    imagesCompiledTrousers.append(getAvgColor(img, list(image.getdata())))

for img in filenamesTop:
    image = Image.open(os.path.join(scriptPath, 'data/top', img))
    imagesCompiledTop.append(getAvgColor(img, list(image.getdata())))

for img in filenamesShoes:
    image = Image.open(os.path.join(scriptPath, 'data/shoes', img))
    imagesCompiledShoes.append(getAvgColor(img, list(image.getdata())))

for img in filenamesJacket:
    image = Image.open(os.path.join(scriptPath, 'data/jacket', img))
    imagesCompiledJacket.append(getAvgColor(img, list(image.getdata())))


def getClosestTrousers(referenceColor):
    deltaEValues = []

    for img in imagesCompiledTrousers:
        image = []
        image.append(img[0])
        image.append(delta_e_cie2000(referenceColor, img[1]))
        deltaEValues.append(image)

    deltaEValues.sort(key=itemgetter(1))

    return deltaEValues[0:3]


def getClosestShoes(referenceColor):
    deltaEValues = []

    for img in imagesCompiledShoes:
        image = []
        image.append(img[0])
        image.append(delta_e_cie2000(referenceColor, img[1]))
        deltaEValues.append(image)

    deltaEValues.sort(key=itemgetter(1))

    return deltaEValues[0:3]


def getClosestJacket(referenceColor):
    deltaEValues = []

    for img in imagesCompiledJacket:
        image = []
        image.append(img[0])
        image.append(delta_e_cie2000(referenceColor, img[1]))
        deltaEValues.append(image)

    deltaEValues.sort(key=itemgetter(1))

    return deltaEValues[0:3]


def getClosestTop(referenceColor):
    deltaEValues = []

    for img in imagesCompiledTop:
        image = []
        image.append(img[0])
        image.append(delta_e_cie2000(referenceColor, img[1]))
        deltaEValues.append(image)

    deltaEValues.sort(key=itemgetter(1))

    return deltaEValues[0:3]


# gets invoked from the UI
def getNextCloth(cloth, imgName, wantedCloth):
    referenceColor = {}
    if (cloth == 'top'):
        for img in imagesCompiledTop:
            if (img[0] == imgName):
                referenceColor = img[1]

    elif (cloth == 'jacket'):
        for img in imagesCompiledJacket:
            if (img[0] == imgName):
                referenceColor = img[1]

    elif (cloth == 'trousers'):
        for img in imagesCompiledTrousers:
            if (img[0] == imgName):
                referenceColor = img[1]

    elif (cloth == 'shoes'):
        for img in imagesCompiledShoes:
            if (img[0] == imgName):
                referenceColor = img[1]

    if (wantedCloth == 'top'):
        return getClosestTop(referenceColor)

    elif (wantedCloth == 'jacket'):
        return getClosestJacket(referenceColor)

    elif (wantedCloth == 'trousers'):
        return getClosestTrousers(referenceColor)

    elif (wantedCloth == 'shoes'):
        return getClosestShoes(referenceColor)

# print(getNextCloth('trousers', 'chino-grau-street-one.jpg', 'shoes'))
# print(getNextCloth('trousers','chino-grau-street-one.jpg','top'))
# print(getNextCloth('trousers','chino-grau-street-one.jpg','jacket'))
