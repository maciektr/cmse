from spacy.tokenizer import Tokenizer
from spacy.lang.en import English
import os


def tokenize_file(path):
    tokenizer = Tokenizer(English().vocab)
    with open(path, 'r') as file:
        text = ''.join(file.readlines())
        tokens = tokenizer(text)
    return list(map(str, tokens))


def get_all_words(folder_path, verbose=False):
    res = []
    path = os.path.abspath(folder_path)
    for filename in os.listdir(path):
        if verbose:
            print("Tokenizing file", filename)
        res += tokenize_file(os.path.join(path, filename))
    return res


if __name__ == '__main__':
    folder = 'wiki'
    print(get_all_words(folder))
