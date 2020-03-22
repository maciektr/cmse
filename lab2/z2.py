import numpy as np 

def scale(x):
    for i in range(len(x)):
        mx = max(x[i])
        if mx == 0:
            continue
        x[i] = (x[i] / mx)
    return x 

if __name__ == "__main__":
    np.set_printoptions(suppress=True)
    val_range = 1*10**6
    n = 500
    A = scale(np.random.uniform(-val_range,val_range,size=(n,n)))
    
    U = np.copy(A)
    L = np.zeros((n,n))

    for i in range(n):
        L[i][i] = 1.
        for k in range(i+1,n):
            l =  U[k][i] / U[i][i]
            U[k] -= U[i] * l
            L[k][i] = l
            U[k][i] = 0.

    X = L @ U 
    print(A)
    print(X)
    print("LU decomposition correct: ",np.all(X - A < 10 ** -7))