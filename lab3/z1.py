from test_functions import *

def bisection(f,a,b,epsilon):
    iterations = 0
    while abs(a-b) > epsilon:
        iterations += 1
        s = (a+b)/2
        if f(s) <= epsilon:
            break
        if f(a) * f(b) < 0:
            b = s
        else:
            a = s
    return {'solution':(a+b)/2, 'iterations':iterations}

def test(epsilon):
    print('eps: ', epsilon)
    print('f1: ',bisection(f1, f1_a, f1_b, epsilon))
    print('f2: ',bisection(f2, f2_a, f2_b, epsilon))
    print('f3: ',bisection(f3, f3_a, f3_b, epsilon))

if __name__=='__main__':
    test(10 ** -7)
    test(10 ** -15)
    test(10 ** -33)
