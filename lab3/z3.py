from test_functions import * 

def diff(f, x, h=10**-7):
    return (f(x+h) - f(x-h))/(2*h)

def secants(f, a, b, iter, eps):
    x = [a,b,None]
    i = 0
    while i < iter and abs(f(x[(i+1)%3])) > eps:
        x_1 = x[i%3]
        x_2 = x[(i+1)%3]
        x[(i+2)%3] = x_1 - f(x_1)*(x_1 - x_2)/(f(x_1) - f(x_2))
        i = i+1

    return {'solution':x[(i+1)%3], 'iterations':i}

def test(eps):
    print('eps: ', eps)
    print('f1: ',secants(f1, f1_a, f1_b, 7, eps))
    print('f2: ',secants(f2, f2_a, f2_b, 40, eps))
    print('f3: ',secants(f3, f3_a, f3_b, 30, eps))

if __name__ == '__main__':
    test(10 ** -7)
    test(10 ** -15)
    test(10 ** -33)