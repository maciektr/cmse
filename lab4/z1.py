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
    if y < x:
        x, y = y, x
    points[x:y] = np.flip(points[x:y], axis=0)
    return points


def arbitrary_swap(points):
    x = randint(0, len(points) - 1)
    y = randint(0, len(points) - 1)
    points[[x, y]] = points[[y, x]]
    return points


def greedy_init(points):
    for i in range(1, len(points) - 1):
        for k in range(i + 1, len(points)):
            if dist(points[i - 1], points[k]) < dist(points[i - 1], points[i]):
                points[[i, k]] = points[[k, i]]
    return points


def sannealing(points, choose, steps, temp, alpha, history=None):
    best = {'points':[],'loss':np.inf}
    n = steps
    t0 = temp
    while steps > 0 and temp > 1e-8:
        neigh = choose(points.copy())
        n_los = loss(neigh)
        d = loss(points) - n_los
        if n_los < best['loss']:
            best['loss'] = n_los
            best['points'] = neigh.copy()
        if d > 0 or np.random.rand(1) <= np.exp(-abs(d) / temp):
            points = neigh
            if history is not None and history['all'] is False:
                history['list'].append({'id': n - steps,
                                        'loss': round(loss(points), 2),
                                        'points': None if not history['copy'] else np.concatenate(
                                            (points, np.array([points[0]])))
                                        })
        if history is not None and history['all'] is True:
            history['list'].append({'id': n - steps,
                                    'loss': round(loss(neigh), 2),
                                    'points': None if not history['copy'] else np.concatenate(
                                        (neigh, np.array([neigh[0]])))
                                    })
        steps -= 1
        temp *= alpha
    return best['points']


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
    n = 100
    v = 10000
    points = get_points(n, v, 'uniform')
    draw_solution(points)
    hist = {'list': [], 'copy': False, 'all': True}
    # hist = None
    points = greedy_init(points)
    los = loss(points)
    draw_solution(points)
    points = sannealing(points, flip_swap, 100000, 22, 0.995, hist)
    draw_solution(points)
    # plot_history.plot_anim(hist)
    plot_history.plot_loss(hist)
    print("Obtained ", str(round(100 * (los - loss(points)) / los, 2)), "% improvement over greedy.")
