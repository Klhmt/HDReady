# HDReady
HDReady is an image merging software fully written in Python. This is a project in development so that your help will always be appreciated!

## What's the purpose of this project?

A DSLR camera has a limited dynamic range. When there are some dark and very bright areas in the same scene some parts of your image will be over/underexposeded. This programs aims at merging a few **static** bracketed images to have a high dynamic range image.

## The program

Pillow is used to manipulate images.
To merge the images, we find a weight for each channel of each pixel of each image according to its well-exposedness. We use a Gaussian curve centered in 127 to find the weight.
In order not to compute same weights many times - a same input gives a same output - the weight are already computed and stored into a file that is loaded on the program. The fusion algorithm is based on this paper: https://web.stanford.edu/class/cs231m/project-1/exposure-fusion.pdf \
The contrast and saturation measures are not yet implemented because of performance reasons. Exposure measure only already gives good results.

If you want to know more about HDR and image merging in general the following paper is a gold mine: [NVIDIA_hdr_algorithms](https://research.nvidia.com/sites/default/files/publications/Gallo-Sen_StackBasedHDR_2016.pdf)

## How to use

Get code files.\
Open a terminal from the same folder as the python script.\
Then type: ```python hdready.py [path of the folder that contains the images to merge] [path of the future output image] [standartDeviation]```\
Example: ```python hdready.py C:\Tim\Images\ToMerge\bridge\ C:\Tim\Images\bridge_merged.jpg 100```\
Standart deviation parameter must be an integer between 10 and 150 with a step of 10 (10 or 20 or 30 ... 140 or 150). This parameter directly impact the results of the merging algorithm. **The smaller the value, the greater the dynamic range**. However, if the value is too small there will be artifacts. You have to choose the right value for a balanced result.

## Execution time

I'll update the results of my testing as long as the program/algorithm keeps evolving.
As I want to use this program to merge the images I take with my DSLR camera, I will optimize the algorithm as far as possible.\
7 x 4600 x 3456 images take around 5 minutes to compute.\
3 x 4600 x 3456 images take around 3 minutes to compute.\
The previous results have been obtained with a Ryzen 5 2600X.

## RAM Consumption

The python script was started from command line (not with an IDE).\
With 3 x 60 Mo loaded images the merging algorithm represents 260 Mo.\
With 7 x 70 Mo loaded images the merging algorithm represents 500 Mo.

## CPU Performance

The Python script was started from command line (not with an IDE).\
The merging algorithm in full load consumes 8 to 10% of my Ryzen 5 2600X CPU.

## Future fonctionnality

The next step is to implement an algorithm that aligns the input images if they are shaky.
