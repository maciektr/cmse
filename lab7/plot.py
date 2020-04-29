import matplotlib.pyplot as plt
import time

from common import rand_sym_matrix
from power_method import power_method
from inv_pow_method import inv_pow_method
from rayleigh import rayleigh_method


def timeit(function, runs=10, mn_min=50, mn_max=1500, title='', eps=10 ** -6, steps=10 ** 5):
    ns = [n for n in range(mn_min, mn_max, 50)]
    my_time = []

    for n in ns:
        print("Testing for n = ", n)
        matrix = rand_sym_matrix(n)

        start = time.time()
        for i in range(runs):
            _, __ = function(matrix, eps=eps, steps=steps)

        my_time.append((time.time() - start) / runs)

    fig = plt.figure()  # figsize=(40,40))
    ax = fig.add_subplot()
    # ax.set(ylim=(0., 1.))
    ax.set_ylabel('t(s)')
    ax.set_xlabel('n')

    ax.plot(ns, my_time)
    plt.title(title)
    plt.show()

    def timeit(function, runs=10, mn_min=50, mn_max=1500, title='', eps=10 ** -6, steps=10 ** 5):
        ns = [n for n in range(mn_min, mn_max, 50)]
        my_time = []

        for n in ns:
            print("Testing for n = ", n)
            matrix = rand_sym_matrix(n)

            start = time.time()
            for i in range(runs):
                _, __ = function(matrix, eps=eps, steps=steps)

            my_time.append((time.time() - start) / runs)

        fig = plt.figure()  # figsize=(40,40))
        ax = fig.add_subplot()
        # ax.set(ylim=(0., 1.))
        ax.set_ylabel('t(s)')
        ax.set_xlabel('n')

        ax.plot(ns, my_time)
        plt.title(title)
        plt.show()


def compare(func1, func2, runs=3, mn_min=100, mn_max=1000, step=100, f1_label='', f2_label='', eps=10 ** -6, steps=10 ** 5):
    ns = [n for n in range(mn_min, mn_max+1, step)]
    func1_time = []
    func2_time = []

    for n in ns:
        print("Testing for n = ", n)
        matrix = rand_sym_matrix(n)

        start = time.time()
        for i in range(runs):
            _, __ = func1(matrix, eps=eps, steps=steps)
        func1_time.append((time.time() - start) / runs)

        start = time.time()
        for i in range(runs):
            _, __ = func2(matrix, eps=eps, steps=steps)
        func2_time.append((time.time() - start) / runs)

    fig = plt.figure()  # figsize=(40,40))
    ax = fig.add_subplot()
    # ax.set(ylim=(0., 1.))
    ax.set_ylabel('t(s)')
    ax.set_xlabel('n')

    ax.plot(ns, func1_time, label=f1_label)
    ax.plot(ns, func2_time, label=f2_label)
    ax.legend(loc='upper left')
    plt.show()


if __name__ == '__main__':
    # timeit(inv_pow_method, title='Inveresed power method', runs=3, mn_max=1250)
    compare(power_method, rayleigh_method, f1_label='Power method', f2_label='Rayleigh method', runs=4)
