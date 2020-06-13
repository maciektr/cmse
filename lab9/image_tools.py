from PIL import Image
import PIL.ImageOps
import numpy as np


def convert_img(img, invert=True):
    if invert:
        img = PIL.ImageOps.invert(img)
    img = np.asarray(img)
    return img


def read_img(path, invert=True):
    img = Image.open(path).convert('L')
    if invert:
        img = PIL.ImageOps.invert(img)
    read = np.asarray(img)
    return read


if __name__ == '__main__':
    pass
