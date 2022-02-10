from math import exp
import os

import pickle
import fire
from PIL import Image
from os import listdir
from os.path import isfile, join, dirname

coeff = None


# Functions
def openImages(imagesFolderPath):
    """This function open and store the images to merge
    Args:
        imagesFolderPath (str): path of the folder containing the images
        Ex: 'C:/Users/John/myImage/bracketed_images_bridge/'
    """
    images = []
    imagesPath = [
        f for f in listdir(imagesFolderPath)
        if isfile(join(imagesFolderPath, f))]
    images = [Image.open(os.path.join(imagesFolderPath, name)) 
             for name in imagesPath]
    return images


def exposition_measure(channels):
    """This function measures the exposition of a given pixel
    and apply a Gauss curve to it
    Arg:
        channels (tuple): tuple that contains red, green and blue channel
    Return:
        coeff (int): exposure weight of the pixel"""
    global coeff
    weight = 1
    for x in range(3):
        weight *= coeff[channels[x]]
    return weight


def generateNewImage(imagesToMerge: list, finalPath: str):
    """This function merges images into a new one
    Arg:
        imagesToMerge (list): list containing the input images
        finalPath (str): path of the final merged image"""
    height, width = imagesToMerge[0].height, imagesToMerge[0].width
    finalImage = Image.new(mode="RGB", size=(width, height))
    for y in range(height):
        for x in range(width):
            newPixel = [0, 0, 0]
            # Compute coefficients
            pixels = [image.getpixel((x, y)) for image in imagesToMerge]
            coefficient = [exposition_measure(rgb) for rgb in pixels]
            sum_coeff = sum(coefficient)
            # Normalization of coefficient values
            coefficient = [c / sum_coeff if sum_coeff != 0 
                          else c for c in coefficient]
            # Merging
            for i in range(len(coefficient)):
                for n in range(3):
                    newPixel[n] += pixels[i][n] * coefficient[i]
            # Rounding values
            newPixel = tuple([round(a) for a in newPixel])
            # Write new rgb values into the final image
            finalImage.putpixel((x, y), newPixel)
    finalImage.save(finalPath)


def start(imagesFolderPath: str, finalPath: str,
          stdDeviation: int = 100):
    """This function launches the merging process
    Args:
        imagesFolderPath (str): path of the folder that contains the images
        to merge
        finalPath (str): complete path of the output merged image
            (eg: 'C:\\Users\\Tim\\Images\\hdr_bridge.png')
        stdDeviation (int): standart deviation of the gaussian curve used
            a weight generator. This parameter can be from 10 to 150
            with a step of 10"""
    global coeff
    # Check if the folder containing the images exists or not
    if os.path.isdir(imagesFolderPath):
        # Opening of the coeffxx file
        path = os.path.join(
            os.path.dirname(__file__), "coeff{}".format(stdDeviation))
        with open(path, 'rb') as f:
            coeff = pickle.load(f)
        images = openImages(imagesFolderPath)
    else:
        raise FileNotFoundError
    # Check if the folder contains images:
    if len(os.listdir(imagesFolderPath)) == 0:
        raise Exception("There is no image in the folder!")
    # Check if the final directory exists and create it if it doesn't
    if not os.path.exists(os.path.dirname(finalPath)):
        os.makedirs(os.path.dirname(finalPath))
    generateNewImage(images, finalPath)
    print('HDR merging completed')


fire.Fire(start)
