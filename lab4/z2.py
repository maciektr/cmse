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


def adjacent_filter(ind, n):
    if n is not None:
        ind = filter(lambda k: (k[0] < n and k[1] < n), ind)
    res = list(filter(lambda k: (k[0] >= 0 and k[1] >= 0), ind))
    return res


def adjacent_four(x, y, n):
    return adjacent_filter(map(lambda k: (k[0] + x, k[1] + y), zip((-1, 0, 1, 0), (0, -1, 0, 1))), n)


def adjacent_eight(x, y, n):
    return adjacent_four(x, y, n) + adjacent_filter(
        map(lambda k: (k[0] + x, k[1] + y), zip((-1, 1, 1, -1), (-1, -1, 1, 1))), n)


def adjacent_sixteen(x, y, n):
    res = []
    for i in range(-2, 2 + 1):
        res.append((-2 + x, i + y))
        res.append((2 + x, i + y))
    for k in range(-1, 1 + 1):
        res.append((k + x, -2 + y))
        res.append((k + x, 2 + y))
    return adjacent_filter(res, n)


def adjacent_sixteen_eight(x, y, n):
    return adjacent_eight(x, y, n) + adjacent_sixteen(x, y, n)


def cost_function(img, adjacency, energy, changed=None, prev_img=None, prev_cost=None):
    res = 0
    n = len(img)
    if changed is None:
        for x in range(n - 1):
            for y in range(n - 1):
                for ind in adjacency(x, y, n):
                    res += energy(img, x, y, ind[0], ind[1])
    else:
        res = prev_cost
        for pos in changed:
            adj = adjacency(pos[0], pos[1], 20)
            for ind in adj:
                res -= energy(prev_img, pos[0], pos[1], ind[0], ind[1])
                res += energy(img, pos[0], pos[1], ind[0], ind[1])

    return res


def dist(x, y, k, m):
    return np.sqrt((x - k) ** 2 + (y - m) ** 2)


def energy_simple(img, x, y, k, m):
    d = dist(x, y, k, m)
    if img[x][y] == img[k][m] == 1:
        return -5 / d
    return 0


def choose_img(img):
    # arbitrary swap
    img = list(img)
    n = len(img)
    x, y = randint(0, n - 1), randint(0, n - 1)
    k, m = randint(0, n - 1), randint(0, n - 1)
    img[x][y], img[k][m] = img[k][m], img[x][y]
    return img, [(x, y), (k, m)]


def hist_update(img, cost, history):
    if history is not None:
        history['list'].append({'id': id,
                                'loss': round(neigh_loss, 2),
                                'points': None if not history['copy'] else list(neigh) + [neigh[0]]
                                })


def annealing(img, adjacency, energy, steps, temp, alpha, hist=None):
    cost = cost_function(img, adjacency, energy)
    best = {'img': list(img), 'cost': cost}

    while steps > 0 and temp > 1e-8:
        new_img, changed = choose_img(img)
        new_cost = cost_function(new_img, adjacency, energy, changed, img, cost)
        if best['cost'] > new_cost:
            best['cost'] = new_cost
            best['img'] = list(new_img)

        diff = cost - new_cost
        if diff > 0 or random.random() <= math.exp(-abs(diff) / temp):
            img = new_img
            cost = new_cost

            # hist_update(history, steps_0 - steps, neigh_loss, neigh, False)
        # hist_update(history, steps_0 - steps, neigh_loss, neigh, True)
        steps -= 1
        temp *= alpha

    return best['img']


if __name__ == '__main__':
    before_path = 'img1.png'
    after_path = 'img2.png'
    # density = [0.1, 0.3, 0.4]

    n = 32
    density = 0.4
    steps = 2500
    temp = 80
    alpha = 0.9995

    img = random_binary(n, density)
    imageio.imsave(before_path, img)

    hist = {'list':[]}
    annealing(img, adjacent_eight, energy_simple, steps, temp, alpha, hist)

    imageio.imsave(after_path, img)
