import matplotlib.pyplot as plt
from random import randint
import numpy as np
import imageio
import random
import math


def random_binary(n, density):
    img = np.ones(n ** 2)
    img[:int(n ** 2 * density)] = 0
    np.random.shuffle(img)
    img.shape = (n, n)
    return img.tolist()


def adjacent_filter(ind, n=None):
    if n is not None:
        ind = filter(lambda k: (k[0] < n and k[1] < n), ind)
    return list(filter(lambda k: (k[0] >= 0 and k[1] >= 0), ind))


def adjacent_four(x, y, n=None):
    return adjacent_filter(map(lambda k: (k[0] + x, k[1] + y), zip((-1, 0, 1, 0), (0, -1, 0, 1))), n)


def adjacent_eight(x, y, n=None):
    return adjacent_four(x, y) + adjacent_filter(
        map(lambda k: (k[0] + x, k[1] + y), zip((-1, 1, 1, -1), (-1, -1, 1, 1))), n)


def adjacent_sixteen(x, y, n=None):
    res = []
    for i in range(-2, 2 + 1):
        res.append((-2 + x, i + y))
        res.append((2 + x, i + y))
    for k in range(-1, 1 + 1):
        res.append((k + x, -2 + y))
        res.append((k + x, 2 + y))
    return adjacent_filter(res, n)


def adjacent_sixteen_eight(x, y):
    return adjacent_eight(x, y) + adjacent_sixteen(x, y)


def cost_function(img, adjacency, energy):
    res = 0
    n = len(img)
    for x in range(n - 1):
        for y in range(n - 1):
            for ind in adjacency(x, y, n):
                res += energy(img, x, y, ind[0], ind[1])
    return res


def dist(x, y, k, m):
    return np.sqrt((x - k) ** 2 + (y - m) ** 2)


def energy_simple(img, x, y, k, m):
    d = dist(x, y, k, m)
    if img[x][y] == img[k][m]:
        return 5 / d
    return 0


def choose_img(img):
    # arbitrary swap
    img = list(img)
    n = len(img)
    x, y = randint(0, n - 1), randint(0, n - 1)
    k, m = randint(0, n - 1), randint(0, n - 1)
    img[x][y], img[k][m] = img[k][m], img[x][y]
    return img


def annealing(img, adjacency, energy, steps, temp, alpha):
    cost = cost_function(img, adjacency, energy)
    best = {'img': list(img), 'cost': cost}

    while steps > 0 and temp > 1e-8:
        print('step')
        new_img = choose_img(img)
        new_cost = cost_function(new_img, adjacency, energy)
        if best['cost'] > new_cost:
            best['cost'] = new_cost
            best['img'] = list(new_img)

        diff = cost - new_cost
        if diff > 0 or random.random() <= math.exp(-abs(diff) / temp):
            img = new_img
            cost = new_cost

        #     hist_update(history, steps_0 - steps, neigh_loss, neigh, False)
        # hist_update(history, steps_0 - steps, neigh_loss, neigh, True)
        steps -= 1
        temp *= alpha

    return best['img']


if __name__ == '__main__':
    before_path = 'img1.png'
    after_path = 'img2.png'
    # density = [0.1, 0.3, 0.4]
    img = random_binary(256, 0.1)
    imageio.imsave(before_path, img)
    annealing(img, adjacent_eight, energy_simple, 50, math.sqrt(256), 0.995)
    imageio.imsave(after_path, img)
