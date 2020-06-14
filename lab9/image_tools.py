from PIL import Image
import PIL.ImageOps
import numpy as np
import cv2


def convert_img(img, invert=True):
    if invert:
        img = PIL.ImageOps.invert(img)
    img = np.asarray(img)
    return img


def read_img(path, invert=True, rotate=True):
    img = Image.open(path).convert('L')
    if rotate:
        angle = detect_angle(path)
        img = img.rotate(angle, fillcolor=255, expand=1)
    if invert:
        img = PIL.ImageOps.invert(img)
    read = np.asarray(img)
    return read


def detect_angle(img_path):
    image = cv2.imread(img_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)
    thresh = cv2.threshold(gray, 0, 255,
                           cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    coords = np.column_stack(np.where(thresh > 0))
    angle = cv2.minAreaRect(coords)[-1]
    angle = -(90 + angle) if angle < -45 else -angle
    angle = round(angle)
    return angle


if __name__ == '__main__':
    pass
    # path = 'fonts/roboto_mono/short.png'
    # img = Image.open(path).convert('L').rotate(10, fillcolor=255, expand=1)
    # img.save('short_rot10.png')
