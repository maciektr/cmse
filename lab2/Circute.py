import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


class Circute(nx.Graph):
    def __init__(self, V, L, source, target, emf):
        super().__init__()
        self.add_nodes_from([i for i in range(0, V)])
        self.add_edges_from([(x, y) for (x, y, z) in L])
        for (x, y, z) in L:
            self[x][y]['resistance'] = z
        U = {}
        for i in range(0, V):
            U[i] = None
        U[source] = 0
        U[target] = emf
        nx.set_node_attributes(self, U, 'voltage')
        self.source = source
        self.target = target
        self.emf = emf

    def findVoltages(self):
        n = self.number_of_nodes()
        eq = np.zeros(shape=(n, n))
        free = np.zeros(shape=(n, 1))
        for i in self.nodes:
            if self.nodes[i]['voltage'] is not None:
                eq[i][i] = 1.
                free[i] = self.nodes[i]['voltage']
            else:
                for k, v in self[i].items():
                    eq[i][i] += 1. / v['resistance']
                    eq[i][k] -= 1. / v['resistance']
        U = np.linalg.solve(eq, free)
        for i in self.nodes:
            self.nodes[i]['voltage'] = U[i][0]

    def plot(self):
        pos = nx.spring_layout(self)
        nc = ['c' for _ in range(self.number_of_nodes())]
        nc[self.source] = 'g'
        nc[self.target] = 'r'
        plt.figure("Circute", figsize=(10, 10))
        nx.draw_networkx_nodes(self, pos, node_color=nc, cmap=plt.get_cmap('jet'), node_size=1000)
        ids = dict([])
        for i in self.nodes():
            ids[i] = i
        nx.draw_networkx_labels(self, pos, ids)
        nx.draw_networkx_edges(self, pos, edge_color='c')
        nx.draw_networkx_edge_labels(self, pos, dict(
            map(lambda x: (x[0], str(round(x[1], 2)) + 'Ω'), nx.get_edge_attributes(self, 'resistance').items())))
        plt.draw()


class CurrentGraph(nx.DiGraph):
    def __init__(self, circute: Circute):
        super().__init__(directed=True)
        self.add_nodes_from(circute.nodes())
        nx.set_node_attributes(self, nx.get_node_attributes(circute, 'voltage'), 'voltage')
        self.source = circute.source
        self.target = circute.target
        for i in circute.nodes:
            for k, v in circute[i].items():
                v_curr = (circute.nodes[i]['voltage'] - circute.nodes[k]['voltage']) / v['resistance']
                if v_curr > 0:
                    self.add_edge(i, k)
                    self[i][k]['current'] = abs(v_curr)
                else:
                    self.add_edge(k, i)
                    self[k][i]['current'] = abs(v_curr)

    def plot(self):
        pos = nx.spring_layout(self)
        nc = ['c' for _ in range(self.number_of_nodes())]
        nc[self.source] = 'g'
        nc[self.target] = 'r'
        plt.figure("Solved circute", figsize=(10, 10))
        nx.draw_networkx_nodes(self, pos, node_color=nc, cmap=plt.get_cmap('jet'), node_size=900)
        nx.draw_networkx_labels(self, pos, dict(
            map(lambda x: (x[0], str(round(x[1], 2)) + 'V'), nx.get_node_attributes(self, 'voltage').items())))
        nx.draw_networkx_edges(self, pos, edgelist=self.edges(),
                               edge_color=nx.get_edge_attributes(self, 'current').values(), edge_cmap=plt.cm.Wistia,
                               width=2, arrows=True, arrowstyle='-|>', arrowsize=20, node_size=1000)
        nx.draw_networkx_edge_labels(self, pos, dict(
            map(lambda x: (x[0], str(round(x[1], 2)) + 'A'), nx.get_edge_attributes(self, 'current').items())))
        plt.draw()

    def correct(self, eps=10 ** -7):
        in_curr = {}
        out_curr = {}
        for i in self.nodes():
            for k, v in self[i].items():
                out_curr[k] = out_curr.get(k, 0) + v['current']
                in_curr[i] = in_curr.get(i, 0) + v['current']

        for k, v in in_curr.items():
            if k == self.source or k == self.target:
                continue
            if abs(v - out_curr[k]) > eps:
                return False
        if abs(out_curr[self.source] - in_curr[self.target]) > eps:
            return False
        return True
