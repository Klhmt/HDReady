from PIL import Image
from math import exp
import timeit
from statistics import stdev

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
    """
    channels = (r, g, b)
    return stdev(channels)

def exposition_measure(r, g, b, stdDeviation):
    """This function measures the exposition of a given pixel
    and apply a Gauss curve to it"""
    channels = [r, g, b]
    for x in channels:
        x *= exp(-((x-127)**2)/(2*(stdDeviation**2)))
    return r*g*b

def generateNewImage(imagesToMerge: list, center:int, stdDeviation: int, coefficient:int = 1):
    """This function merge together each pixel of the different images
    The coefficient or weight is gaussian function:
    a * exp(-((pixel[i]-center)**2)/(2*stdDeviation**2)) TEST2"""
    height, width = imagesToMerge[0].height, imagesToMerge[0].width
    finalImage = Image.new(mode="RGB", size=(width, height))
    for y in range(height):
        for x in range(width):
            bestPixel = [0, 0]   #  [sum of brightness, sum of coefficient] 
            for image in imagesToMerge:
                pixel = image.getpixel((x, y))
                brightness = 0.299 * pixel[0] + 0.587 * pixel[1] + 0.114 * pixel[2]     # Transformation of rbg to brightness value
                coeff = coefficient * exp(-((brightness-center)**2)/(2*stdDeviation**2))  # Coefficient
                bestPixel[0] += brightness * coeff   # brightness value * coefficient
                bestPixel[1] += coeff
            deltas = [pixel[1]-pixel[0], pixel[2]-pixel[0], pixel[2]-pixel[1]]
            bestPixel = round(bestPixel[0] / bestPixel[1])
            r = round(bestPixel / (0.229 + 0.587 * (pixel[1]-pixel[0]) + 0.114 * (pixel[2]-pixel[0])))
            v = round((bestPixel - 0.299*r) / (0.587 + 0.114 * (pixel[2]-pixel[1])))
            b = round((bestPixel - (0.299*r + 0.587*v)) / 0.114)
            finalImage.putpixel((x, y), (r, v, b))
    finalImage.save(r"C:\Users\cjacq\Documents\Clément\Perso\Programmation\Photo_samples\hdr_new_deltas_100.png")

print(saturation_measure(10, 14, 50))


# Try
#i = openImages('C:/Users/cjacq/Documents/Clément/Perso/Programmation/Photo_samples/', ('img2.jpg', 'img3.jpg','img5.jpg'))
#i = openImages('C:/Users/cjacq/Documents/Clément/Perso/Programmation/Photo_samples/', ('img2.jpg', 'img3.jpg', 'img4.jpg','img5.jpg', 'img6.jpg', 'img7.jpg', 'img1.jpg'))

#i = openImages('C:/Users/cjacq/Documents/Clément/Perso/Programmation/Photo_samples/', ('1120716.jpg', '1120717.jpg', '1120718.jpg', '1120719.jpg', '1120720.jpg', '1120721.jpg', '1120722.jpg'))
#i = openImages('C:/Users/cjacq/Documents/Clément/Perso/Programmation/Photo_samples/', ('P1130264.png', 'P1130265.png', 'P1130266.png', 'P1130267.png', 'P1130268.png', 'P1130269.png', 'P1130263.png'))
#generateNewImage(i, 127, 100)


