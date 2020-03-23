import matplotlib.pyplot as plt 
import numpy as np 
import time

def scale(x):
    return (x.T / np.max(x, axis=1)).T

def partial_pivoting(X):
    for i in range(len(X)):
        mx = X[i][i]
        mi = i
        for k in range(i+1,len(X)):
            if X[i][k] > mx:
                mx = X[i][k]
                mi = k
        X[[i, k]] = X[[k, i]]

    return X 

def solve(A,B):
    n = A.shape[0]
    AB = scale(np.hstack((A,B)))
    AB = partial_pivoting(AB)

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

def main(n = 500):
    val_range = 1*10**6
    A = np.random.uniform(-val_range,val_range,size=(n,n))
    B = np.random.uniform(-val_range,val_range,size=(n,1))
    
    start = time.time()
    npsol = np.linalg.solve(A,B).reshape((n))
    np_time = round(time.time() - start,4)
    print("Numpy solution:\n",npsol)
    
    start = time.time()
    res = solve(A,B)
    my_time = round(time.time() - start,4)
    print("My elimination solution:\n", res)

    print("Results are the same: ",np.all((npsol - res) < 10 ** -7))
    print("Numpy solution took:", np_time, "seconds")
    print("My solution took:", my_time, "seconds")

def timethat():
    ns = [n for n in range(500,2000,100)]
    np_time = []
    my_time = []

    for n in ns:
        print("Testing for n = ",n)
        val_range = 1*10**6
        A = np.random.uniform(-val_range,val_range,size=(n,n))
        B = np.random.uniform(-val_range,val_range,size=(n,1))

        start = time.time()
        runs = 40
        for i in range(runs):
            np.linalg.solve(A,B)
        
        p = (time.time() - start) / runs
        start = time.time()
        solve(A,B)
        m = time.time() - start

        np_time.append(p)
        my_time.append(m)

    mx = max(np_time)
    np_time = [x / mx for x in np_time]
    mx = max(my_time)
    my_time = [x / mx for x in my_time]

    fig = plt.figure()#figsize=(40,40))
    ax = fig.add_subplot()
    # ax.set(ylim=(0., 1.))
    ax.set_ylabel('t(s)')
    ax.set_xlabel('n')

    ax.plot(ns,np_time)
    ax.plot(ns,my_time)
    plt.show()

        


if __name__ == "__main__":
    main(500)
    # timethat()

