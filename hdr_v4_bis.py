from PIL import Image
from math import exp
import timeit
from statistics import stdev
from matplotlib.pyplot import plot, show, legend

def openImages(path, imageNames):
    """This function open and store the images to merge
    Args:
        path (str): path of the folder that contains the images
        imageNames (tuple): contains the name of files
    Ex:
        path = 'C:/Users/John/Python/'
        imageNames = ('img1.png', 'img2.png', 'offroad.png')
    """
    images = []
    for name in imageNames:
        images.append(Image.open(path + name))
    return images

def saturation_measure(r, g, b):
    """This function measures saturation of a given pixel
    which is the standard deviation within the R, G and B channels
    Args:
        r (int): red channel
        g (int): green channel
        b (int): blue channel
    Return:
        int: standart deviation of r, g, b
    """
    channels = (r, g, b)
    if stdev(channels) == 0:
        return 1
    return stdev(channels)

def contrast_measure(r, g, b):
    """WIP"""
    pass

def exposition_measure(r, g, b, stdDeviation, multiplier: int=1):
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
    channels = [r, g, b]
    coeff = 1
    for x in range(3):
        coeff *= multiplier * exp(-(((channels[x]-127)**2)/(2*(stdDeviation**2))))
    return coeff

def gaussian(value, stdDeviation):
    """Function used by dev"""
    return exp(-(((value-127)**2)/(2*(stdDeviation**2))))

def generateNewImage(imagesToMerge: list):
    """This function merges images into a new one. WIP"""
    height, width = imagesToMerge[0].height, imagesToMerge[0].width
    finalImage = Image.new(mode="RGB", size=(width, height))
    for y in range(height):
        for x in range(width):
            coefficient = []
            # Compute coefficients
            for image in imagesToMerge:
                r, g, b = image.getpixel((x, y))
                #coefficient.append(saturation_measure(r, g, b) * exposition_measure(r, g, b, 5, 100))
                coefficient.append(exposition_measure(r, g, b, 100))
            sum_coeff = sum(coefficient)
            # Normalization of coefficient values
            for z in range(len(coefficient)):
                try:
                    coefficient[z] /= sum_coeff
                except ZeroDivisionError:
                    coefficient[z] = 0
            # Merging images => WIP 
            newPixel = [0, 0, 0]
            for coeff in coefficient:
                newPixel[0] += r * coeff
                newPixel[1] += g * coeff
                newPixel[2] += b * coeff
            # Rounding values
            for a in range(3):
                newPixel[a] = round(newPixel[a])
            newPixel = tuple(newPixel)
            # Write new rgb values into the final image
            finalImage.putpixel((x, y), newPixel)
    finalImage.save(r"C:\Users\cjacq\Documents\Clément\Perso\Programmation\Photo_samples\hdr_paper_100_7img_no_saturation.png")


# Try
#i = openImages('C:/Users/cjacq/Documents/Clément/Perso/Programmation/Photo_samples/', ('img6.jpg', 'img5.jpg','img3.jpg'))
i = openImages('C:/Users/cjacq/Documents/Clément/Perso/Programmation/Photo_samples/', ('img2.jpg', 'img3.jpg', 'img4.jpg','img5.jpg', 'img6.jpg', 'img7.jpg', 'img1.jpg'))

#i = openImages('C:/Users/cjacq/Documents/Clément/Perso/Programmation/Photo_samples/', ('1120716.jpg', '1120717.jpg', '1120718.jpg', '1120719.jpg', '1120720.jpg', '1120721.jpg', '1120722.jpg'))
#i = openImages('C:/Users/cjacq/Documents/Clément/Perso/Programmation/Photo_samples/', ('P1130264.png', 'P1130265.png', 'P1130266.png', 'P1130267.png', 'P1130268.png', 'P1130269.png', 'P1130263.png'))
generateNewImage(i)

"""
x = [i for i in range(256)]
y = [2*gaussian(x, 20) for x in range(256)]
z = [2*gaussian(x, 20) for x in range(256)]
k = [2*gaussian(x, 50) for x in range(256)]
l = [2*gaussian(x, 20) for x in range(256)]

plot(x, z, color='orange', label='2-35')

plot(x, l, color='red')
legend()
show()"""