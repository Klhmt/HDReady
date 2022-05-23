from math import exp, floor
import os

import fire
from PIL import Image
from os import listdir
from os.path import isfile, join, dirname
from multiprocessing import Pool

class Images_stack():
    """WIP"""
    
    def __init__(self, img_list, stdDeviation, processes):
        self.stack = img_list
        self.stdDeviation = stdDeviation
        self.height = self.stack[0].height
        self.width = self.stack[0].width
        self.processes = processes
        self.coefficients = {value: round((exp( - ((value - 127) ** 2) / (2 * self.stdDeviation ** 2))), 6) 
            for value in range(0, 256)}
        self.parts = [(x * floor(self.width / self.processes), 0, (x + 1) * floor(self.width / self.processes), self.height) for x in range(self.processes - 1)] + [((self.processes - 1) * floor(self.width / self.processes), 0, self.width, self.height)]


    def images_crop(self):
        """This function cuts the images stack into processes ones 
        CAS OU PROCESSE = 1 cf hdr ready

        Args:
            processes (int): number of cores used by the fusion process and number
                of parts of the images.

        Return:
            (list): list containing Images_stack objects 

        """
        if self.processes == 1:
            return self
        return [Divided_images_stack([img.crop(self.parts[x]) for img in self.stack], self.stdDeviation, self.parts, self.width, self.height) for x in range(self.processes)]


class Divided_images_stack():
    """WIP"""

    def __init__(self, img_list, stdDeviation, parts, final_width, final_height):
        self.stack = img_list
        self.stdDeviation = stdDeviation
        self.parts = parts
        self.width = self.stack[0].width
        self.height = self.stack[0].height
        self.final_width = final_width
        self.final_height = final_height
        self.coefficients = {value: round((exp( - ((value - 127) ** 2) / (2 * self.stdDeviation ** 2))), 6) 
            for value in range(0, 256)}
    
    
    def exposition_measure(self, channels:tuple)->'weight':
        """This function measures the exposition of a given pixel
        and apply a Gauss curve to compute the weight

        Arg:
            channels (tuple): tuple that contains red, green and blue channel

        Return:
            coeff (int): exposure weight of the pixel
            
        """
        weight = 1
        for x in range(3):
            weight *= self.coefficients[channels[x]]
        return weight


    def generate_new_image(self)->'hdr piece of image':
        """This function merges the images into a new one

        Arg:
            imagesToMerge (list): list containing the input images

        Return:
            finalImage (image object): a part of the final image

        """
        finalImage = Image.new(mode="RGB", size=(self.final_width, self.final_height))

        for y in range(self.height):
            for x in range(self.width):
                newPixel = [0, 0, 0]
                # Compute coefficients
                pixels = [image.getpixel((x, y)) for image in self.stack]
                coefficient = [self.exposition_measure(rgb) for rgb in pixels]
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
        
        return finalImage


    def reassemble(self)->'final image':
        """This function reassembles the parts of the final image
        
        Return:
            (Image object): final image

        """
        finalImage = Image.new(mode="RGB", size=(self.final_width, self.final_height))
        for x in range(len(self.stack)):
            finalImage.paste(self.stack[x], self.parts[x][:2])
        return finalImage
    

def open_images(imagesFolderPath:str)->'list containing images':
    """This function open and store the images to merge into a list
    
    Args:
        imagesFolderPath (str): path of the folder containing the images
        e.g. 'C:/Users/John/myImage/bracketed_images_bridge/'
    
    """
    images = []
    imagesPath = [
        f for f in listdir(imagesFolderPath)
        if isfile(join(imagesFolderPath, f))]
    images = [Image.open(os.path.join(imagesFolderPath, name)) 
             for name in imagesPath]
    return images


def hdr(imagesToMerge):
    return imagesToMerge.generate_new_image()


def start(imgFolderPath, finalPath, stdDeviation, processes):
    """main function that launche the HDR process"""
    if __name__ == '__main__':
        # Check if the folder containing the images exists or not
        if os.path.isdir(imgFolderPath):
            # Opening of the images to merge
            images = open_images(imgFolderPath)
        else:
            raise FileNotFoundError
        # Check if the folder contains images:
        if len(os.listdir(imgFolderPath)) == 0:
            raise Exception("There is no image in the folder")
        # Check if the final directory exists and create it if it doesn't
        if not os.path.exists(os.path.dirname(finalPath)):
            os.makedirs(os.path.dirname(finalPath))
        # Creating the images stack
        stack = Images_stack(images, stdDeviation, processes)
        # Dividing the images stack into processes ones
        divided_stack = stack.images_crop()
        # HDR merging
        with Pool(processes) as p:
            results = Divided_images_stack(p.map(hdr, divided_stack), stack.stdDeviation, stack.parts, stack.width, stack.height)
        # Reassembling the pieces of the final image
        final_image = results.reassemble()
        final_image.save(finalPath)  
        print('HDR merging process completed') 

# Setting up the CLI application
fire.Fire(start)