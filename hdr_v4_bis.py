from PIL import Image
from math import exp
import timeit
from statistics import stdev
import pickle

coeff110 = pickle.load(open(r'C:\Users\cjacq\Documents\Clément\Perso\Programmation\HDReady\coeff110', 'rb'))

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

def saturation_measure(channels):
    """This function measures saturation of a given pixel
    which is the standard deviation within the R, G and B channels
    Args:
        r (int): red channel
        g (int): green channel
        b (int): blue channel
    Return:
        int: standart deviation of r, g, b
    """
    if stdev(channels) == 0:
        return 1
    return stdev(channels)

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
    coeff = 1
    for x in range(3):
        coeff *= multiplier * coeff110[channels[x]]
    return coeff

def gaussian(value, stdDeviation):
    """Function used by dev"""
    return exp(-(((value-127)**2)/(2*(stdDeviation**2))))

def generateNewImage(imagesToMerge: list):
    """This function merges images into a new one
    Arg:
        imagesToMerge (list): list containing the input images"""
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
                coefficient.append(saturation_measure(channels) * exposition_measure(channels, 250, 1))
                #coefficient.append(exposition_measure(r, g, b, 35))
            sum_coeff = sum(coefficient)
            # Normalization of coefficient values
            for z in range(len(coefficient)):
                try:
                    coefficient[z] /= sum_coeff
                except ZeroDivisionError:
                    coefficient[z] = 0
            # Merging images => WIP 
            for i in range(len(coefficient)):
                for n in range(3):
                    newPixel[n] += pixels[i][n] * coefficient[i]
            # Rounding values
            for a in range(3):
                newPixel[a] = round(newPixel[a])
            # Write new rgb values into the final image
            finalImage.putpixel((x, y), tuple(newPixel))
    finalImage.save(r"C:\Users\cjacq\Documents\Clément\Perso\Programmation\Photo_samples\hdr_paper_110_new_merge_dico_list.jpg")


# Try
i = openImages('C:/Users/cjacq/Documents/Clément/Perso/Programmation/Photo_samples/', ('img6.jpg', 'img5.jpg','img3.jpg'))
#i = openImages('C:/Users/cjacq/Documents/Clément/Perso/Programmation/Photo_samples/', ('img2.jpg', 'img3.jpg', 'img4.jpg','img5.jpg', 'img6.jpg', 'img7.jpg', 'img1.jpg'))
#i = openImages('C:/Users/cjacq/Documents/Clément/Perso/Programmation/Photo_samples/', ('clavier1_comp.jpg', 'clavier2_comp.jpg'))
#i = openImages('C:/Users/cjacq/Documents/Clément/Perso/Programmation/Photo_samples/', ('1120716.jpg', '1120717.jpg', '1120718.jpg', '1120719.jpg', '1120720.jpg', '1120721.jpg', '1120722.jpg'))
#i = openImages('C:/Users/cjacq/Documents/Clément/Perso/Programmation/Photo_samples/', ('clavier1_comp.jpg', 'clavier2_comp.jpg'))
generateNewImage(i)