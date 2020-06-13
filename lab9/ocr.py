from numpy import fft, linalg
import numpy as np
import multiprocessing

from image_tools import read_img, convert_img
from fonts_manager import FontsManager


class Ocr:
    __N_PROCESSES = 8

    def __init__(self, fonts_folder='fonts'):
        self.fonts_manager = FontsManager(stop=False)
        self.fonts_manager.load_from_folder(fonts_folder)

    def read_text(self, file_path, font_name, overlap_threshold=0.5):
        text_img = read_img(file_path)
        text_img = self.denoise(text_img)
        chars_freq = self.characters_freq(font_name, text_img.shape)
        max_char_shape = self.fonts_manager.get_max_char_shape(font_name)

        with multiprocessing.Pool(processes=Ocr.__N_PROCESSES) as pool:
            res = pool.map(Ocr.img_to_positions, [(char, char_freq, text_img) for char, char_freq in chars_freq])
        found_chars_with_corr = Ocr.flatten(res)

        found_chars_with_corr = self.remove_duplicates(found_chars_with_corr, max_char_shape, overlap_threshold)
        found_chars = [(pos, char) for pos, char, _ in found_chars_with_corr]
        text = self.pos_to_text(found_chars, max_char_shape)
        return text

    # def correct_rotation(self, text_img):
    #     pass

    @staticmethod
    def fft_single_char(args):
        char, char_img, shape = args
        return char, fft.fft2(np.rot90(char_img, 2), s=shape)

    def characters_freq(self, font_name, shape):
        with multiprocessing.Pool(processes=Ocr.__N_PROCESSES) as pool:
            res = pool.map(Ocr.fft_single_char, [(char, char_img, shape) for char, char_img in
                                                 self.fonts_manager.get_font_as_list(font_name)])
            return res

    @staticmethod
    def correlation(img, char_freq):
        img_freq = fft.fft2(img)
        corr = np.abs(np.real(fft.ifft2(np.multiply(img_freq, char_freq))))
        return corr

    @staticmethod
    def get_positions(correlation, threshold=0.94):
        max_corr = np.max(correlation)
        positions = np.nonzero(correlation >= max_corr * threshold)
        positions = zip(positions[0], positions[1])
        res = [(pos, correlation[pos[0], pos[1]]) for pos in positions]
        return res

    @staticmethod
    def flatten(array):
        return [val for sublist in array for val in sublist]

    @staticmethod
    def img_to_positions(args):
        char, char_freq, img = args
        corr = Ocr.correlation(img, char_freq)
        pos_corr = Ocr.get_positions(corr)
        res = [(p, char, c) for p, c in pos_corr]
        return res

    @staticmethod
    def overlapping(pos_x, pox_y, shape, threshold=0.5):
        return abs(pos_x[0] - pox_y[0]) < shape[0] * threshold \
               and abs(pos_x[1] - pox_y[1]) < shape[1] * threshold

    def remove_duplicates(self, chars_with_corr, max_char_shape, threshold=0.5):
        chars_with_corr = sorted(chars_with_corr, key=lambda x: -x[2])
        res = []
        for pos, char, corr in chars_with_corr:
            place = True
            for res_pos, _, _ in res:
                if self.overlapping(res_pos, pos, max_char_shape, threshold):
                    place = False
                    break
            if place:
                res.append((pos, char, corr))
        return res

    @staticmethod
    def denoise(img, rank=None):
        if rank is None:
            rank = min(img.shape[0], img.shape[1]) // 3
        s, v, d = linalg.svd(img, full_matrices=False)
        v = np.diag(v)
        v[rank:, rank:] = 0
        return s @ v @ d

    @staticmethod
    def pos_to_text(found_chars, max_char_shape, space_threshold=1.1):
        char_width, char_height = max_char_shape
        found_chars = sorted(found_chars)

        lines = []
        last = 0
        temp = []
        for i in range(len(found_chars)):
            pos, char = found_chars[i]
            if abs(found_chars[last][0][0] - pos[0]) > char_height:
                lines.append(temp)
                last = i
                temp = []
            temp.append((pos[1], char))
        lines.append(temp)

        temp = []
        lines_res = []
        for line in lines:
            line = sorted(line)
            for k in range(len(line)):
                pos, char = line[k]
                if k > 0 and abs(pos - line[k - 1][0]) > space_threshold * char_width:
                    temp.append(' ')
                temp.append(char)
            lines_res.append(temp)
            temp = []
        res = [''.join(line) for line in lines_res]
        return '\n'.join(res)
