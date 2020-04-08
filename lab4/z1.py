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
    x = randint(0, len(points))
    y = (x + 1) % len(points)
    points[[x, y]] = points[[y, x]]
    return points


def arbitrary_swap(points: np.array):
    x = randint(0, len(points))
    y = randint(0, len(points))
    points[[x, y]] = points[[y, x]]
    return points


if __name__ == '__main__':
    n = 20
    v = 1000
    points = np.random.uniform(-v, v, (n, 2))
    draw_solution(points)
    print(loss(points))
    arbitrary_swap(points)
    draw_solution(points)
    print(loss(points))
