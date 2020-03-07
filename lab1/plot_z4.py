from matplotlib.animation import FuncAnimation
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

if not args.n:
    fig = plt.figure(figsize=(40,40))
    ax = fig.add_subplot()
    ax.set_ylabel('x_n')
    for i in range(10):
        v = [values[k] for k in range(i,len(values),10)]
        r = [m*(ran/len(v)) for m in range(len(v))]
        ax.plot(r,v)
    ax.set_xlabel('r')
    plt.savefig('plot_z4.png')
else: 
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.set(ylim=(0., 1.))
    ax.set_ylabel('x_n')
    ax.set_xlabel('n')
    r = 1.00
    ax.set_title('r='+str(r)) 

    step = 100
    n = [i for i in range(0,step)]
    line = ax.plot(n,values[0:step])[0]

    def animate(i):
        line.set_ydata(values[i*step:(i+1)*step])
        global r
        r+=1e-2
        ax.set_title('r='+str(format(round(r,2),'.2f')))

    anim = FuncAnimation(fig, animate, interval=100, frames=len(values)//step)
    anim.save("plot_z4.gif", writer='imagemagick')

    # plt.draw()
    # plt.show()

system('rm '+plot_out)
