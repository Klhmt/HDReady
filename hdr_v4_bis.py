from PIL import Image
from math import exp
import timeit
from statistics import stdev
import pickle
import timeit

# Variable
coeff = None

# Functions
def openImages(path, imageNames):
    """This function open and store the images to merge
    Args:
        path (str): path of the folder that contains the images
        imageNames (tuple): contains the name of files
    Ex:
        path = 'C:/Users/John/myImage/'
        imageNames = ('img1.png', 'img2.png', 'offroad.png')
    """
    images = []
    for name in imageNames:
        images.append(Image.open(path + name))
    return images

def contrast_measure(channels):
    """WIP"""
    pass

def exposition_measure(channels, stdDeviation, multiplier: int=1):
    """This function measures the exposition of a given pixel
    and apply a Gauss curve to it
    Args:
        r (int): red channel
        g (int): green channel
        b (int): blue channel
        stdDeviation (int): standart deviation, parameter of the Gaussian curve
        multiplier (int): multiplier
    Return:
        coeff (int): exposure weight of the pixel"""
    channels = list(channels)
    weight = 1
    for x in range(3):
        weight *= multiplier * coeff[channels[x]]
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
            coefficient = []
            pixels = []
            newPixel = [0, 0, 0]
            # Compute coefficients
            for image in imagesToMerge:
                channels = image.getpixel((x, y))
                pixels.append(channels)
                coefficient.append(exposition_measure(channels, 250, 1))
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

def start(imagesPath: str, finalPath: str, imageNames: tuple, stdDeviation: int, multiplier: int = 1):
    """This function open the appropriate dictionary file
    and proceed to the images fusion
    Args:
        imagesPath : path of the images to merge
        finalPath : complete path of the output merged image (eg: 'C:\\Users\\Tim\\Images\\hdr_bridge.png')
        imagesNames : name of the image files
        stdDeviation : standart deviation of the gaussian curve used a weight generator
        multiplier : multiplier of the weight of each pixel
    """
    global coeff
    try:
        coeff = pickle.load(
            open(r'C:\Users\cjacq\Documents\Clément\Perso\Programmation\HDReady\coeff{}'.format(stdDeviation),'rb')
                )
        images = openImages(imagesPath, imageNames)
        generateNewImage(images, finalPath)
    except FileNotFoundError:
        return None

# Try
#i = openImages('C:/Users/cjacq/Documents/Clément/Perso/Programmation/Photo_samples/', ('img4.jpg', 'img2.jpg','img1.jpg'))
#i = openImages('C:/Users/cjacq/Documents/Clément/Perso/Programmation/Photo_samples/', ('img2.jpg', 'img3.jpg', 'img4.jpg','img5.jpg', 'img6.jpg', 'img7.jpg', 'img1.jpg'))
#i = openImages('C:/Users/cjacq/Documents/Clément/Perso/Programmation/Photo_samples/', ('clavier1_comp.jpg', 'clavier2_comp.jpg'))
#i = openImages('C:/Users/cjacq/Documents/Clément/Perso/Programmation/Photo_samples/', ('1120716.jpg', '1120717.jpg', '1120718.jpg', '1120719.jpg', '1120720.jpg', '1120721.jpg', '1120722.jpg'))
#i = openImages('C:/Users/cjacq/Documents/Clément/Perso/Programmation/Photo_samples/', ('clavier1_comp.jpg', 'clavier2_comp.jpg'))
#i = openImages('C:/Users/cjacq/Documents/Clément/Perso/Programmation/Photo_samples/', ('P1130263.png', 'P1130264.png', 'P1130265.png', 'P1130266.png', 'P1130267.png', 'P1130268.png', 'P1130269.png'))

start(r'C:/Users/cjacq/Documents/Clément/Perso/Programmation/Photo_samples/', r'C:/Users/cjacq/Documents/Clément/Perso/Programmation/Photo_samples/new_function_50.jpg', ('img3.jpg', 'img4.jpg', 'img6.jpg', 'img1.jpg'), 100, 1)

"""
starttime = timeit.default_timer()
for x in range(3):
    generateNewImage(i)
print("The time difference is :", timeit.default_timer() - starttime)"""
