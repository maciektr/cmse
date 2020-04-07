from Circute import Circute, CurrentGraph
import matplotlib.pyplot as plt
from random import randint
import networkx as nx
import dimacs


def solve(G):
    G.findVoltages()
    return CurrentGraph(G)


def read_from_file(pathToFile):
    source, target, emf = dimacs.read_source(pathToFile)
    V, L = dimacs.loadWeightedGraph(pathToFile)
    L = list(map(lambda x: (x[0] - 1, x[1] - 1, x[2]), L))
    return Circute(V, L, source, target, emf)


def get_random_circute(n, min_r=1, max_r=1000, min_v=1, max_v=1000, density=0.5):
    G = nx.erdos_renyi_graph(n, density)
    while not nx.is_connected(G):
        G = nx.erdos_renyi_graph(n, density)
    V = len(G.nodes())
    L = []
    for i in G.nodes():
        for k, v in G[i].items():
            L.append((i, k, randint(min_r, max_r)))
    return Circute(V, L, 0, V - 1, randint(min_v, max_v))


if __name__ == '__main__':
    path = 'graphs/clique20'
    G = read_from_file(path)
    # G = get_random_circute(100)
    G.plot()
    res = solve(G)
    res.plot()
    plt.show()
