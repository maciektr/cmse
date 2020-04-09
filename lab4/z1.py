import matplotlib.pyplot as plt
from random import randint
import plot_history
import random
import math


def draw_solution(points):
    fig = plt.figure("TSP", figsize=(10, 10))
    ax = plt.axes()
    p = list(points) + [points[0]]
    ax.plot(*zip(*p), marker='o')
    plt.show()


def dist(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def loss(points):
    res = 0
    n = len(points)
    for i in range(n):
        res += (dist(points[i % n], points[(i + 1) % n]))
    return res


def consecutive_swap(points):
    points = list(points)
    x = randint(0, len(points) - 1)
    y = (x + 1) % len(points)
    points[x], points[y] = points[y], points[x]
    return points


def arbitrary_swap(points):
    points = list(points)
    x = randint(0, len(points) - 1)
    y = randint(0, len(points) - 1)
    points[x], points[y] = points[y], points[x]
    return points


def reverse_swap(points):
    points = list(points)
    x = randint(0, len(points) - 1)
    y = randint(0, len(points) - 1)
    if y < x:
        x, y = y, x
    points[x:y] = reversed(points[x:y])
    return points


def greedy_init(points):
    points = list(points)
    for i in range(1, len(points) - 1):
        for k in range(i + 1, len(points)):
            if dist(points[i - 1], points[k]) < dist(points[i - 1], points[i]):
                points[i], points[k] = points[k], points[i]
    return points


def hist_update(history, id, neigh_loss, neigh, all):
    if history is not None and history['all'] == all:
        history['list'].append({'id': id,
                                'loss': round(neigh_loss, 2),
                                'points': None if not history['copy'] else list(neigh) + [neigh[0]]
                                })


def sannealing(points, choose, steps, temp, alpha, history=None):
    points_loss = loss(points)
    best = {'points': points, 'loss': points_loss}
    steps_0 = steps
    temp_0 = temp

    while steps > 0 and temp > 1e-8:
        neigh = choose(points)
        neigh_loss = loss(neigh)
        if best['loss'] > neigh_loss:
            best['loss'] = neigh_loss
            best['points'] = list(neigh)

        diff = points_loss - neigh_loss
        if diff > 0 or random.random() <= math.exp(-abs(diff) / temp):
            points = list(neigh)
            points_loss = neigh_loss

            hist_update(history, steps_0 - steps, neigh_loss, neigh, False)
        hist_update(history, steps_0 - steps, neigh_loss, neigh, True)
        steps -= 1
        temp *= alpha
    return best['points']


def get_points(n=20, v=1000, type='uniform'):
    if type == 'normal':
        return [[random.gauss(0, v), random.gauss(0, v)] for _ in range(n)]
    if type == 'groups':
        k = v // 3
        res = []
        y = -2 * k
        for _ in range(3):
            x = -2 * k
            for _ in range(3):
                r = [[random.uniform(-k, k) + x, random.uniform(-k, k) + y] for _ in range(n // 2)]
                res = res + r
                x += 2 * k
            y += 2 * k
        return res
    return [[random.uniform(-v, v), random.uniform(-v, v)] for _ in range(n)]


if __name__ == '__main__':
    n = 500
    v = 1000
    # points = get_points(n, v, 'groups')
    points = [[random.uniform(-1000, 1000), random.uniform(-1000, 1000)] for i in range(100)]
    # draw_solution(points)

    points = greedy_init(points)
    draw_solution(points)

    init_loss = loss(points)
    hist = {'list': [], 'copy': False, 'all': False}

    points = sannealing(points, arbitrary_swap, 5000, math.sqrt(n), 0.995, hist)
    draw_solution(points)

    # plot_history.plot_anim(hist)
    plot_history.plot_loss(hist)
    print("Obtained ", str(round(100 * (init_loss - loss(points)) / init_loss, 2)), "% improvement over initial state.")

    ########## Test swap functions ##########
    # ns = [100,500,1000]
    # typs = ['uniform', 'normal', 'groups']
    # for n in ns:
    #     for t in typs:
    #         print("N: ", n, " Type: ", t)
    #         points = get_points(n, v, t)
    #         init_loss = loss(points)
    #         p = list(points)
    #         p = sannealing(p, arbitrary_swap, 100000, 31, 0.995, None)
    #         arb_per = str(round(100 * (init_loss - loss(p)) / init_loss, 2))
    #
    #         p = list(points)
    #         p = sannealing(p, consecutive_swap, 100000, 31, 0.995, None)
    #         con_per = str(round(100 * (init_loss - loss(p)) / init_loss, 2))
    #
    #         p = list(points)
    #         p = sannealing(p, reverse_swap, 100000, 31, 0.995, None)
    #         rev_per = str(round(100 * (init_loss - loss(p)) / init_loss, 2))
    #         print("Arbitrary: ", arb_per, "% Consec: ", con_per, "% Rev: ", rev_per, "%")
