import matplotlib.pyplot as plt
from random import randint
import plot_history
import numpy as np


def draw_solution(points):
    fig = plt.figure("TSP", figsize=(10, 10))
    ax = plt.axes()
    p = np.concatenate((points, np.array([points[0]])))
    ax.plot(*p.T, marker='o')
    plt.show()


def dist(x, y):
    return np.sqrt(np.sum((x - y) ** 2))


def loss(points):
    res = 0
    n = len(points)
    for i in range(n + 1):
        res += (dist(points[i % n], points[(i + 1) % n]))
    return res


def consecutive_swap(points):
    x = randint(0, len(points) - 1)
    y = (x + 1) % len(points)
    points[[x, y]] = points[[y, x]]
    return points


def flip_swap(points):
    x = randint(0, len(points) - 1)
    y = randint(0, len(points) - 1)
    points[x:y] = np.flip(points[x:y])
    return points


def arbitrary_swap(points):
    x = randint(0, len(points) - 1)
    y = randint(0, len(points) - 1)
    points[[x, y]] = points[[y, x]]
    return points


# def greedy_init(points):


def sannealing(points, choose, steps, temp, alpha, history=None):
    n = steps
    while steps > 0 and temp > 0:
        neigh = choose(points.copy())
        d = loss(points) - loss(neigh)
        if d > 0 or np.random.rand(1) <= np.exp(d / temp):
            points = neigh
            if history is not None and history['all'] == False:
                history['list'].append({'id': n - steps,
                                        'loss': round(loss(points), 2),
                                        'points': None if not history['copy'] else np.concatenate(
                                            (points, np.array([points[0]])))
                                        })
        if history is not None and history['all'] == True:
            history['list'].append({'id': n - steps,
                                    'loss': round(loss(neigh), 2),
                                    'points': None if not history['copy'] else np.concatenate(
                                        (neigh, np.array([neigh[0]])))
                                    })
        steps -= 1
        temp *= alpha
    return points


def get_points(n=20, v=1000, type='uniform'):
    if type == 'normal':
        return np.random.normal((0, 0), (v, v), (n, 2))
    if type == 'groups':
        k = v // 3
        res = np.empty(shape=(0, 2))
        y = -2 * k
        for _ in range(3):
            x = -2 * k
            for _ in range(3):
                r = np.random.uniform(-k, k, (n // 9, 2)) + np.array([x, y])
                res = np.concatenate((res, r))
                x += 2 * k
            y += 2 * k
        return res

    return np.random.uniform(-v, v, (n, 2))


if __name__ == '__main__':
    n = 500
    v = 10000
    points = get_points(n, v, 'groups')
    draw_solution(points)
    hist = {'list': [], 'copy': False, 'all': True}
    # hist = None
    # print(loss(points))
    points = sannealing(points, consecutive_swap, 4000, 200, 0.9994, hist)
    # print(loss(points))
    draw_solution(points)
    # plot_history.plot_anim(hist)
    plot_history.plot_loss(hist)
