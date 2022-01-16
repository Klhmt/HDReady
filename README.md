# HDReady
This is a HDR software fully written in Python. This is a project in development, your help will always be appreciated!

## What's the purpose of this project?

A DSLR camera has a limited dynamic range. When there are some dark and very bright areas in the same scene some parts of your image will be over/underexposeded. This programs aims at merging a few **static** bracketed images to have a high dynamic range image.
The fusion algorithm is based on that paper: https://web.stanford.edu/class/cs231m/project-1/exposure-fusion.pdf

## The program

Pillow is used to manipulate images.

If you want to know more about HDR and image merging the following papaer is a gold mine: [NVIDIA_hdr_algorithms](https://research.nvidia.com/sites/default/files/publications/Gallo-Sen_StackBasedHDR_2016.pdf)

## Performance

I'll update the results of my testing as long as the program/algorithm keeps evolving.
As I want to use this program to merge the images I take with my DSLR camera, I will optimize the algorithm as far as possible.
3 x 4592 x 3448 images take ... to compute WIP
