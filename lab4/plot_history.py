from matplotlib.animation import FuncAnimation
from matplotlib import pyplot as plt


def plot_anim(history, out_path='history.gif'):
    fig = plt.figure()
    ax = fig.add_subplot()
    # ax.set(ylim=(0., 1.))
    ax.set_ylabel('y')
    ax.set_xlabel('x')

    ax.set_title('step=' + str(history['list'][0]['id']) + ' loss=' + str(history['list'][0]['loss']))
    line = ax.plot(*zip(*history['list'][0]['points']), marker='o')[0]

    def animate(i):
        line.set_data(*zip(*history['list'][i]['points']))
        ax.set_title('step=' + str(history['list'][i]['id']) + ' loss=' + str(history['list'][i]['loss']))

    anim = FuncAnimation(fig, animate, interval=100, frames=len(history['list']))
    anim.save(out_path, writer='imagemagick')


def plot_loss(history):
    fig = plt.figure("Loss change", figsize=(10, 10))
    ax = plt.axes()
    steps = list(map(lambda x: x.get('id'), history['list']))
    loss = list(map(lambda x: x.get('loss'), history['list']))
    ax.plot(steps, loss)
    plt.show()
