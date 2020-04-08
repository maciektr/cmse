import numpy as np
# Since scipy.imread is deprecated
import imageio
from skimage import img_as_ubyte

def low_rank_approx(img, k):
    res = np.empty(shape=img.shape)
    for m in range(img.shape[2]):
        u, s, vh = np.linalg.svd(img[:, :, m])
        comp = np.zeros(shape=img.shape[:2])
        for i in range(k):
            x = np.zeros(shape=img.shape[:2])
            x[i][i] = s[i]
            comp += u @ x @ vh
        res[:, :, m] = comp
    return res


if __name__ == '__main__':
    path = 'Lenna.png'
    comp_path = 'LennaCompressed.png'
    rank = 60

    img = imageio.imread(path)
    imageio.imsave(comp_path, low_rank_approx(img, rank))
