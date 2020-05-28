from nltk.corpus import stopwords
from string import punctuation
import multiprocessing
import html2text
import nltk
import os


def tokenize_file(path):
    h = html2text.HTML2Text()
    h.ignore_links = True
    h.ignore_images = True
    h.ignore_tables = True
    h.ignore_emphasis = True
    with open(path, 'r') as file:
        return set(h.handle(file.read()).split())


def get_all_words(folder_path):
    path = os.path.abspath(folder_path)
    with multiprocessing.Pool(processes=8) as pool:
        res = pool.map(tokenize_file, [os.path.join(path, filename) for filename in os.listdir(path)])
    result = set()
    for r in res:
        result = result | r
    return list(result)


def process_words(words):
    nltk.download('stopwords')
    words = list(map(lambda w: w.lower(), words))
    stop_words = list(stopwords.words('english'))
    stop_words += ['.html', 'http://']
    for stop in stop_words:
        words = filter(lambda w: stop not in w, words)

    chars = list(punctuation)
    chars = chars + ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    for char in chars:
        words = list(map(lambda w: w.replace(char, ''), words))
    words = list(filter(lambda w: w != 'aa', words))
    words = list(filter(lambda w: w != 'aaa', words))
    words = list(filter(lambda w: len(w) > 1, words))
    return list(words)


if __name__ == '__main__':
    # folder = 'wiki'
    folder = 'test_dir'
    res = get_all_words(folder)
    # print("R",res)
    words = sorted(process_words(res))
    # words = list(sorted(words))[:10]
    # words = res
    # print(words)
    print("---------")
    print(len(res))
    print(len(words))
    print(words[:200])
