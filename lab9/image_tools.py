from PIL import Image
import PIL.ImageOps
import numpy as np


def convert_img(img, invert=True):
    if invert:
        img = PIL.ImageOps.invert(img)
    img = np.asarray(img)
    # gray_img = np.dot(img[..., :3], [0.2989, 0.5870, 0.1140])
    # if invert:
    #     gray_img = np.ones(gray_img.shape) * .255 - gray_img
    # normalised = gray_img * 255 / np.max(gray_img)
    # return normalised
    return img


def read_img(path, invert=True):
    img = Image.open(path)
    # return convert_img(img, invert)
    read = np.asarray(PIL.ImageOps.invert(img.convert('L')))
    return read


if __name__ == '__main__':
    # img = Image.open('alphabet.png').convert('L').save('b.png')
    pass
