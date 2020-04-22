from Circuit import Circuit, CurrentGraph
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
    return Circuit(V, L, source, target, emf)


def get_random_circuit(n, type='general', min_r=1, max_r=1000, min_v=1, max_v=1000, density=0.5):
    G = nx.Graph()
    if type == 'erdos':
        G = nx.erdos_renyi_graph(n, density)
        while not nx.is_connected(G):
            G = nx.erdos_renyi_graph(n, density)
    elif type[:7] == 'regular':
        d = int(type[7:])
        G = nx.random_regular_graph(d, n)
    elif type == 'general':
        G = nx.dense_gnm_random_graph(n, n ** 2 - n)
    elif type == 'bridge':
        A = nx.erdos_renyi_graph(n // 2, density)
        while not nx.is_connected(A):
            A = nx.erdos_renyi_graph(n // 2, density)
        B = nx.erdos_renyi_graph(n // 2, density)
        while not nx.is_connected(B):
            B = nx.erdos_renyi_graph(n // 2, density)
        an = A.number_of_nodes()
        A.add_nodes_from([an + i for i in B.nodes()])
        A.add_edges_from([(an + x, an + y) for x, y in B.edges()])
        A.add_edge(1, an + 1)
        G = A
    V = len(G.nodes())
    L = []
    for i in G.nodes():
        for k, v in G[i].items():
            L.append((i, k, randint(min_r, max_r)))
    return Circuit(V, L, 0, V - 1, randint(min_v, max_v))


if __name__ == '__main__':
    path = 'graphs/grid100x100'
    # G = read_from_file(path)
    # G = get_random_circuit(20, 'bridge')
    # G = get_random_circuit(20, 'regular3')
    # G = get_random_circuit(20, 'general')
    G = get_random_circuit(20, 'erdos')
    G.plot()
    res = solve(G)
    print("Solution correct: ", res.correct())
    res.plot()
    plt.show()
