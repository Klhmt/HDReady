from PIL import Image
from math import exp
import pickle
from os import listdir
from os.path import isfile, join
import fire

# Variable
coeff = None

# Functions
def openImages(imagesFolderPath):
    """This function open and store the images to merge
    Args:
        imagesFolderPath (str): path of the folder that contains the images to merge
        Ex: imagesFolderPath = 'C:/Users/John/myImage/bracketed_images_bridge/'
    """
    images = []
    imagesPath = [f for f in listdir(imagesFolderPath) if isfile(join(imagesFolderPath, f))]
    for name in imagesPath:
        images.append(Image.open(imagesFolderPath + name))
    return images


def exposition_measure(channels, stdDeviation, multiplier: int=1):
    """This function measures the exposition of a given pixel
    and apply a Gauss curve to it
    Args:
        channels (tuple): tuple that contains red, green and blue channel
        stdDeviation (int): standart deviation, parameter of the Gaussian curve
        multiplier (int): multiplier
    Return:
        coeff (int): exposure weight of the pixel"""
    channels = list(channels)
    weight = 1
    for x in range(3):
        weight *= multiplier * coeff[channels[x]]
    return weight


def generateNewImage(imagesToMerge: list, finalPath: str, multiplier: int=1):
    """This function merges images into a new one
    Arg:
        imagesToMerge (list): list containing the input images
        finalPath (str): path of the final merged image
        multiplier (int): multiplier of the weight of each pixel"""
    height, width = imagesToMerge[0].height, imagesToMerge[0].width
    finalImage = Image.new(mode="RGB", size=(width, height))
    for y in range(height):
        for x in range(width):
            coefficient = []
            pixels = []
            newPixel = [0, 0, 0]
            # Compute coefficients
            for image in imagesToMerge:
                channels = image.getpixel((x, y))
                pixels.append(channels)
                coefficient.append(exposition_measure(channels, 250, multiplier))
            sum_coeff = sum(coefficient)
            # Normalization of coefficient values
            for z in range(len(coefficient)):
                coefficient[z] /= sum_coeff
            # Merging images => WIP 
            for i in range(len(coefficient)):
                for n in range(3):
                    newPixel[n] += pixels[i][n] * coefficient[i]
            # Rounding values
            for a in range(3):
                newPixel[a] = round(newPixel[a])
            # Write new rgb values into the final image
            finalImage.putpixel((x, y), tuple(newPixel))
    finalImage.save(finalPath)


def start(imagesFolderPath: str, finalPath: str, stdDeviation: int = 100, multiplier:int = 1):
    """This function open the appropriate dictionary file
    and proceed to the images fusion
    Args:
        imagesFolderPath : path of the folder that contains the images to merge
        finalPath : complete path of the output merged image (eg: 'C:\\Users\\Tim\\Images\\hdr_bridge.png')
        stdDeviation : standart deviation of the gaussian curve used a weight generator
        multiplier : multiplier of the weight of each pixel
    """
    global coeff
    try:
        coeff = pickle.load(
            open(r'C:\Users\cjacq\Documents\Clément\Perso\Programmation\HDReady\coeff{}'.format(stdDeviation),'rb')
                )
        images = openImages(imagesFolderPath)
        generateNewImage(images, finalPath, multiplier)
        print('HDR merging completed')
    except FileNotFoundError as er:
        print('Error :', er)


fire.Fire(start)
