from math import exp
import os

import pickle
import fire
import numpy as np
from PIL import Image
from os import listdir
from os.path import isfile, join, dirname

coeff = None


# Functions
def generate_dictionnary(stdDeviation: int)->'coefficient dictionnary':
    """This function generates a dictionnary that associates the weight 
    of a pixel channel and it's weight
    Arg:
        stdDeviation: parameter of the Gaussian function
    Return:
        (dict): dictonnary of weigths"""
    return {value: round((exp(-((value-127)**2)/(2*stdDeviation**2))), 6) 
           for value in range(0, 256)}


def open_images(imagesFolderPath:str)->'list containing array images':
    """This function open and store the images to merge into a list
    Args:
        imagesFolderPath (str): path of the folder containing the images
        e.g. 'C:/Users/John/myImage/bracketed_images_bridge/'
    """
    images = []
    imagesPath = [
        f for f in listdir(imagesFolderPath)
        if isfile(join(imagesFolderPath, f))]
    images = [np.array(Image.open(os.path.join(imagesFolderPath, name))) 
             for name in imagesPath]
    return images


def exposition_measure(channels:tuple)->'weight':
    """This function measures the exposition of a given pixel
    and apply a Gauss curve to compute the weight
    Arg:
        channels (tuple): tuple that contains red, green and blue channel
    Return:
        coeff (int): exposure weight of the pixel"""
    global coeff
    weight = 1
    for x in range(3):
        weight *= coeff[channels[x]]
    return weight


def generate_new_image(imagesToMerge: list, finalPath: str):
    """This function merges the images into a new one and save it
    Arg:
        imagesToMerge (list): list containing the input images
        finalPath (str): path of the final merged image"""
    # Creation of an array with the same dimension as input images
    shape = imagesToMerge[0].shape
    finalImage = np.empty(shape)
    for y in range(shape[0]):
        for x in range(shape[1]):
            newPixel = np.array([0, 0, 0])
            # Compute coefficients
            pixels = [image[x, y] for image in imagesToMerge]
            coefficient = np.array([exposition_measure(rgb) 
                                  for rgb in np.nditer(pixels)])
            sum_coeff = np.sum(coefficient)
            # Normalization of coefficient values
            coefficient = np.array([c / sum_coeff if sum_coeff != 0 
                          else c for c in nditer(coefficient)])
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
    """This function launches the merging process. stdDeviation parameter is
    used to compute the weight of a given pixel. The smaller the value, the
    greater the dynamic range.

    Args:
        imagesFolderPath (str): path of the folder that contains the images
        to merge
        finalPath (str): complete path of the output merged image
            (e.g. 'C:\\Users\\Tim\\Images\\hdr_bridge.png')
        stdDeviation (int): standart deviation of the gaussian curve used
            a weight generator. This parameter can be from 10 to 150
            with a step of 10
    
    Raises:
        FileNotFoundError: if the specified path of the folder is incorrect
        Exception: if there is no image to compute in the folder

    """
    global coeff
    # Check if the folder containing the images exists or not
    if os.path.isdir(imagesFolderPath):
        # Generating the coeff dictionnary and opening the images to merge
        coeff = generate_dictionnary(stdDeviation)
        images = open_images(imagesFolderPath)
    else:
        raise FileNotFoundError
    # Check if the folder contains images:
    if len(os.listdir(imagesFolderPath)) == 0:
        raise Exception("There is no image in the folder!")
    # Check if the final directory exists and create it if it doesn't
    if not os.path.exists(os.path.dirname(finalPath)):
        os.makedirs(os.path.dirname(finalPath))
    generate_new_image(images, finalPath)
    print('HDR merging completed')

print(open_images(r'C:\Users\cjacq\Documents\Clément\Perso\Programmation\Photo_samples\sample5')[0].shape)
print(open_images(r'C:\Users\cjacq\Documents\Clément\Perso\Programmation\Photo_samples\sample5')[0].ndim)
