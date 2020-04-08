import numpy as np
# Since scipy.imread is deprecated
import imageio


def low_rank_approx(img, k):
    res = [None for _ in range(img.shape[2])]
    for m in range(img.shape[2]):
        u, s, vh = np.linalg.svd(img[:, :, m])
        comp = (u @ vh) * s[0]
        for i in range(1, k):
            comp += (u @ vh) * s[i]
        res[m] = comp

    res = np.array(res)
    res = np.moveaxis(res, 0, -1)

    print(img[0][0])
    print(res[0][0])
    print(res.shape)
    return res


if __name__ == '__main__':
    path = 'Lenna.png'
    comp_path = 'LennaCompressed.jpg'
    img = imageio.imread(path)
    imageio.imsave(comp_path, low_rank_approx(img, 512))
    # low_rank_approx(img, 100)
