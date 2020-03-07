import matplotlib.pyplot as plt 
from os import system

plot_out = 'plot_z4.txt'
program = 'z4.o'
ran = 4. - 1.

system('./'+program+' > '+plot_out)

values = list(map(lambda x: float(x[:-1]),open(plot_out,'r').readlines()))

fig = plt.figure(figsize=(40,40))
ax = fig.add_subplot()
for i in range(10):
    v = [values[k] for k in range(i,len(values),10)]
    r = [m*(ran/len(v)) for m in range(len(v))]
    ax.plot(r,v)

ax.set_xlabel('n')
ax.set_ylabel('x_n')

plt.savefig('plot_z4.png')

system('rm '+plot_out)
