from spacy.tokenizer import Tokenizer
from spacy.lang.en import English
import multiprocessing
import os


def tokenize_file(path):
    tokenizer = Tokenizer(English().vocab)
    with open(path, 'r') as file:
        text = ''.join(file.readlines())
        tokens = tokenizer(text)
    return list(map(str, tokens))


def get_all_words(folder_path):
    path = os.path.abspath(folder_path)
    with multiprocessing.Pool(processes=8) as pool:
        res = pool.map(tokenize_file, [os.path.join(path, filename) for filename in os.listdir(path)])
    flatten = lambda l: [item for sublist in l for item in sublist]
    return flatten(res)


if __name__ == '__main__':
    folder = 'wiki'
    # folder = 'test_dir'
    res = get_all_words(folder)
    # print(res)
    print(len(res))