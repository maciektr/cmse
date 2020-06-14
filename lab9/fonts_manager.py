from skimage import measure
import multiprocessing
from PIL import Image
from numpy import fft
import numpy as np
import os

from image_tools import convert_img, read_img


class FontsManager:
    __N_PROCESSES = 8

    def __init__(self, stop=False):
        self.chars_order = [chr(i) for i in range(ord('a'), ord('z') + 1)] \
                           + [chr(i) for i in range(ord('A'), ord('Z') + 1)] \
                           + [chr(i) for i in range(ord('0'), ord('9') + 1)]
        if stop:
            self.chars_order += ['.', ',', '?', '!', ';']

        self.fonts = {}

    def show_read_letter(self, font_name, show_function):
        for img in self.fonts[font_name].values():
            show_function(img)

    def get_chars_order(self):
        return self.chars_order

    def get_chars_img(self, font_name):
        return list(self.fonts[font_name].values())

    def get_font(self, font_name):
        return self.fonts[font_name]

    def get_font_as_list(self, font_name):
        return self.get_font(font_name).items()

    def get_max_char_shape(self, font_name):
        chars = self.get_chars_img(font_name)
        shapes = [c.shape for c in chars]
        x = max(shapes, key=lambda s: s[0])[0]
        y = max(shapes, key=lambda s: s[1])[1]
        return x, y

    @staticmethod
    def cut_char(char, threshold=90, padding=1):
        labeled = measure.label(char > threshold)
        props = measure.regionprops(labeled)
        box = list(props[0].bbox)
        for prop in props:
            for i in range(2):
                box[i] = min(box[i], prop.bbox[i])
            for i in range(2,4):
                box[i] = max(box[i], prop.bbox[i])
        return char[box[0]-padding:box[2]+padding, box[1]-padding:box[3]+padding]

    def load_alphabet(self, alphabet_path, font_name):
        alphabet_size = len(self.chars_order)
        alphabet_img = Image.open(alphabet_path)
        # char_height =alphabet_img.height / alphabet_size
        char_height = 30
        characters_img = [alphabet_img.crop((0, i * char_height, alphabet_img.width, (i+1) * char_height)) for i in
                          range(alphabet_size)]

        font_chars = {}
        for i in range(len(self.chars_order)):
            conv = convert_img(characters_img[i])
            font_chars[self.chars_order[i]] = self.cut_char(conv)
        self.fonts[font_name] = font_chars

    def load_from_folder(self, folder_path):
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                if not file_path.split('/')[-1][:9] == 'alphabet.':
                    continue
                font_name = file_path.split('/')[-2]
                self.load_alphabet(file_path, font_name)
