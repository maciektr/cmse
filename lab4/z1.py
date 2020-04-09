import matplotlib.pyplot as plt
from random import randint
import numpy as np


def draw_solution(points: np.array):
    fig = plt.figure("TSP", figsize=(10, 10))
    ax = plt.axes()
    p = np.concatenate((points, np.array([points[0]])))
    ax.plot(*p.T, marker='o')
    plt.show()


def dist(x, y):
    return np.sqrt(np.sum((x - y) ** 2))


def loss(points: np.array):
    res = 0
    n = len(points)
    for i in range(n + 1):
        res += (dist(points[i % n], points[(i + 1) % n]))
    return res


def consecutive_swap(points: np.array):
    x = randint(0, len(points)-1)
    y = (x + 1) % len(points)
    points[[x, y]] = points[[y, x]]
    return points


def arbitrary_swap(points: np.array):
    x = randint(0, len(points)-1)
    y = randint(0, len(points)-1)
    points[[x, y]] = points[[y, x]]
    return points


def sannealing(points, choose, temp, steps, alpha):
    while steps > 0 and temp > 0:
        neigh = choose(points.copy())
        d = loss(points) - loss(neigh)
        if d > 0 or np.random.rand(1) <= np.exp(d/temp):
            points = neigh
        steps -= 1
        temp *= alpha
    return points


if __name__ == '__main__':
    n = 20
    v = 1000
    points = np.random.uniform(-v, v, (n, 2))
    draw_solution(points)
    points = sannealing(points, arbitrary_swap, 100, 5000, 0.9994)
    draw_solution(points)
