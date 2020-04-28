from common import *
from scipy.linalg import lu_factor, lu_solve
import numpy as np
from power_method import power_method


def inv_pow_method(matrix, sigma,  eps=10 ** -9, steps=10 ** 9):
    vector = np.random.rand(matrix.shape[0])
    vector = norm(vector)
    k = 0
    A = (matrix - sigma * np.identity(matrix.shape[0]))
    lu_piv = lu_factor(A)
    while k < steps:
        next_vect = lu_solve(lu_piv, vector)
        next_vect = norm(next_vect)
        if np.linalg.norm(abs(next_vect) - abs(vector)) < eps:
            break
        vector = next_vect
        k += 1
        sigma = vector.T @ matrix @ vector
    return norm(vector), sigma


if __name__ == '__main__':
    matrix = rand_sym_matrix(100)
    _, sigma = power_method(matrix, steps=10)

    vector, dominant = inv_pow_method(matrix, sigma)
    print(vector)
    print(dominant)
    lib_vector, lib_dominant = lib_solution(matrix)
    check_correct(vector, dominant, lib_vector, lib_dominant)