from common import *
from scipy.linalg import lu_factor, lu_solve
import numpy as np
from power_method import power_method


def inv_pow_method(matrix, sigma,  eps=10 ** -12, steps=10 ** 9):
    vector = np.random.rand(matrix.shape[0])
    k = 0
    dominant_val = None
    A = (matrix - sigma @ np.identity(matrix.shape[0]))
    lu_piv = lu_factor(A)
    while k < steps:
        next_vect = lu_solve(lu_piv, vector)
        dominant_val = next_vect[np.argmax(abs(next_vect))]
        next_vect = next_vect / dominant_val
        if np.linalg.norm(abs(next_vect) - abs(vector)) < eps:
            break
        vector = next_vect
        k += 1
    return norm(vector), dominant_val


if __name__ == '__main__':
    matrix = rand_sym_matrix(100)
    sigma, _ = power_method(matrix, steps=10)
    vector, dominant = inv_pow_method(matrix, sigma)
    print(vector)
    print(dominant)
    lib_vector, lib_dominant = lib_solution(matrix)
    print(lib_vector)
    check_correct(vector, dominant, lib_vector, lib_dominant)
