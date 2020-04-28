from common import *
import numpy as np
import scipy.linalg
from power_method import power_method


def rayleigh_iteration(matrix, sigma, eps=10 ** -6, steps=10 ** 5):
    vector = np.random.rand(matrix.shape[0])
    k = 0
    while k < steps:
        next_vect = scipy.linalg.inv(matrix - sigma * np.identity(matrix.shape[0])) @ vector
        next_vect = norm(next_vect)
        sigma = (next_vect.T @ matrix @ next_vect) / (next_vect.T @ next_vect)
        if np.linalg.norm(abs(vector - next_vect)) < eps:
            break
        vector = next_vect
        k += 1
    return vector, sigma


if __name__ == '__main__':
    matrix = rand_sym_matrix(4)
    _, sigma = power_method(matrix, steps=10)
    vector, dominant = rayleigh_iteration(matrix, sigma)

    print(vector)
    print(dominant)
    lib_vector, lib_dominant = lib_solution(matrix)
    print(lib_vector)
    print(lib_dominant)

    check_correct(vector, dominant, lib_vector, lib_dominant)
