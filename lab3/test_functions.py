from math import cos, cosh, tan, pi, exp

def f1(x):
    return cos(x) * cosh(x) -1

def f2(x):
    return (1/x) - tan(x)

def f3(x):
    return (2 ** (-x)) + exp(x) + 2*cos(x) - 6

f1_a = 3/2*pi
f1_b = 2*pi
f2_a = 10 ** -5
f2_b = pi/2
f3_a = 1
f3_b = 3