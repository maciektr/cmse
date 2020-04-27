from common import *
import numpy as np


def norm(vector):
    return vector / abs(np.linalg.norm(vector, axis=0))


def solve(matrix, eps=10 ** -9, steps=10 ** 5):
    vector = np.random.rand(matrix.shape[0])
    k = 0
    dominant_val = 0
    while k < steps:
        next_vec = matrix @ vector
        dominant_val = next_vec[np.argmax(abs(next_vec))]
        next_vec = next_vec / dominant_val
        if np.linalg.norm(abs(next_vec) - abs(vector)) < eps:
            break
        vector = next_vec
        k += 1
    return norm(vector), dominant_val


if __name__ == '__main__':
    matrix = rand_sym_matrix(100)
    vector, dominant = solve(matrix, 10 ** -12, 10 ** 9)
    print(vector)
    print(dominant)
    lib_vector, lib_dominant = lib_solution(matrix)
    check_correct(vector, dominant, lib_vector, lib_dominant)
