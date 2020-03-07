import matplotlib.pyplot as plt 
from os import system
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-n', action='store_true')
args = parser.parse_args()

plot_out = 'plot_z4.txt'
program = 'z4.o'
ran = 4. - 1. if not args.n else None

system('./'+program+' > '+plot_out)

values = list(map(lambda x: float(x[:-1]),open(plot_out,'r').readlines()))

fig = plt.figure(figsize=(40,40))
ax = fig.add_subplot()
if not args.n:
    for i in range(10):
        v = [values[k] for k in range(i,len(values),10)]
        r = [m*(ran/len(v)) for m in range(len(v))]
        ax.plot(r,v)
    ax.set_xlabel('r')
else: 
    r = [i for i in range(len(values))]
    ax.plot(r,values)
    ax.set_xlabel('n')

ax.set_ylabel('x_n')

plt.savefig('plot_z4.png')

system('rm '+plot_out)
