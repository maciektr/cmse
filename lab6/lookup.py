import multiprocessing
import html2text
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


if __name__ == '__main__':
    # folder = 'wiki'
    folder = 'test_dir'
    res = get_all_words(folder)
    print(res)
    print(len(res))
