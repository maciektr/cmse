import numpy as np 

def scale(x):
    for i in range(len(x)):
        mx = max(x[i])
        if mx == 0:
            continue
        x[i] = (x[i] / mx)
    return x

def solve(A,B):
    AB = scale(np.hstack((A,B)))

    for i in range(n):
        for k in range(n):
            if i==k:
                continue
            AB[k] = AB[k] * (AB[i][i] / AB[k][i])
            AB[k] -= AB[i]
            AB[k][i] = 0.

    tab = []
    for i in range(n):
        tab.append(AB[i][n] / AB[i][i])
    return np.array(tab)

if __name__ == "__main__":
    n = 500
    val_range = 1*10**6
    A = np.random.uniform(-val_range,val_range,size=(n,n))
    B = np.random.uniform(-val_range,val_range,size=(n,1))
    
    npsol = np.linalg.solve(A,B).reshape((n))
    print("Numpy solution:\n",npsol)
    
    res = solve(A,B)
    
    print("My elimination solution:\n", res)
    print("Results are the same: ",np.all((npsol - res) < 10 ** -7))