from Circute import Circute, CurrentGraph
import networkx as nx
import numpy as np
import dimacs


def read_source(path=None):
    if path is None:
        return map(int, input().split())

    f = open(path, "r")
    r = f.readline().split()
    if r[0] != 'c':
        raise Exception("Illegal argument: cannot find source specification in file under path.")
    return int(r[1]) - 1, int(r[2]) - 1, int(r[3])


def read_graph(path):
    s, t, e = read_source(path)
    G = Circute(s, t, e)
    V, L = dimacs.loadWeightedGraph(path)
    G.add_nodes_from([i for i in range(0, V)])
    G.add_edges_from([(x - 1, y - 1) for (x, y, z) in L])
    i = 0
    for (x, y, z) in L:
        x -= 1
        y -= 1
        # G[x][y]['current'] = 0
        G[x][y]['resistance'] = z
        G[x][y]['id'] = i
        i += 1
    U = {}
    for i in range(0, V):
        U[i] = None
    U[s] = 0
    U[t] = e
    nx.set_node_attributes(G, U, 'voltage')
    return G


def voltages(G):
    n = G.number_of_edges()
    eq = np.zeros(shape=(n, n))
    free = np.zeros(shape=(n, 1))
    for i in G.nodes:
        if G.nodes[i]['voltage'] is not None:
            eq[i][i] = 1.
            free[i] = G.nodes[i]['voltage']
        else:
            for k, v in G[i].items():
                eq[i][i] += 1. / v['resistance']
                eq[i][k] -= 1. / v['resistance']
    U = np.linalg.solve(eq, free)
    for i in G.nodes:
        G.nodes[i]['voltage'] = U[i][0]
    #


def solve(G):
    voltages(G)
    return CurrentGraph(G)

if __name__ == '__main__':
    path = 'graphs/g1'
    G = read_graph(path)
    res = solve(G)
    G.plot()
    res.plot()

