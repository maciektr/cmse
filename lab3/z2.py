from test_functions import * 

def diff(f, x, h=10**-7):
    return (f(x+h) - f(x-h))/(2*h)

def newton(f, a, b, iter, eps):
    x = a
    i = 0
    while i < iter and abs(f(x)) > eps:
        x = x - f(x)/diff(f,x)
        i = i+1

    return {'solution':x, 'iterations':i}

def test(eps):
    print('eps: ', eps)
    print('f1: ',newton(f1, f1_a, f1_b, 30, eps))
    print('f2: ',newton(f2, f2_a, f2_b, 60, eps))
    print('f3: ',newton(f3, f3_a, f3_b, 60, eps))

if __name__ == '__main__':
    test(10 ** -7)
    test(10 ** -15)
    test(10 ** -33)