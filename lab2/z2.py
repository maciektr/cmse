import numpy as np 
from z1 import scale

def get_random_array(n):
    val_range = 10**6
    return np.random.uniform(-val_range,val_range,size=(n,n))

def decomposition(A):
    n = A.shape[0]
    U = np.copy(A)
    L = np.zeros((n,n))

    for i in range(n):
        L[i][i] = 1.
        for k in range(i+1,n):
            l =  U[k][i] / U[i][i]
            U[k] -= U[i] * l
            L[k][i] = l
            U[k][i] = 0.
    return L,U

if __name__ == "__main__":
    np.set_printoptions(suppress=True)
    A = scale(get_random_array(4))
    
    L, U = decomposition(A)

    X = L @ U 
    print(A)
    print(X)
    print("LU decomposition correct: ",np.all(X - A < 10 ** -7))