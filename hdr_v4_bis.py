from PIL import Image
from math import exp
import timeit

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
                if 10 <= brightness <= 180:
                    bestPixel[0] += brightness * coefficient * exp(-((brightness-center)**2)/(2*stdDeviation**2))   # brightness value * coefficient
                    bestPixel[1] += coefficient * exp(-((brightness-center)**2)/(2*stdDeviation**2))    # Coefficient
            try:
                bestPixel = round(bestPixel[0] / bestPixel[1])
                delta = round(abs(brightness - bestPixel))
            except ZeroDivisionError:
                delta = 0

            if brightness >= 127:
                pixel = (pixel[0] - delta, pixel[1] - delta, pixel[2] - delta)
            pixel = (pixel[0] + delta, pixel[1] + delta, pixel[2] + delta)
            finalImage.putpixel((x, y), pixel)
    finalImage.save(r"C:\Users\cjacq\Documents\Clément\Perso\Programmation\Photo_samples\hdr_v4bis_bornes_underexposed.png")




# Try
#i = openImages('C:/Users/cjacq/Documents/Clément/Perso/Programmation/Photo_samples/', ('img2.jpg', 'img3.jpg','img5.jpg'))
#i = openImages('C:/Users/cjacq/Documents/Clément/Perso/Programmation/Photo_samples/', ('img2.jpg', 'img3.jpg', 'img4.jpg','img5.jpg', 'img6.jpg', 'img7.jpg', 'img1.jpg'))

#i = openImages('C:/Users/cjacq/Documents/Clément/Perso/Programmation/Photo_samples/', ('1120716.jpg', '1120717.jpg', '1120718.jpg', '1120719.jpg', '1120720.jpg', '1120721.jpg', '1120722.jpg'))
    i = openImages('C:/Users/cjacq/Documents/Clément/Perso/Programmation/Photo_samples/', ('P1130264.png', 'P1130265.png', 'P1130266.png', 'P1130267.png', 'P1130268.png', 'P1130269.png', 'P1130263.png'))
generateNewImage(i, 127, 20)


