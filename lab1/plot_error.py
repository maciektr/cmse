import matplotlib.pyplot as plt 
from os import system
import numpy as np

plot_out = 'plot.txt'
program = 'z1.o'
steps = 25000

system('./'+program+' > '+plot_out)
errors = list(map(lambda x: float(x[:-1]),open(plot_out,'r').readlines()))
x = [i*steps for i in range(len(errors))]

fig = plt.figure()
ax = fig.add_subplot()
ax.plot(x,errors, marker='o', markevery=int(1e6/steps))

ax.set_xlabel('Number of summations')
ax.set_ylabel('Value of error')

plt.show()