import matplotlib.pyplot as plt
import networkx as nx


class Circute(nx.Graph):
    def __init__(self, source, target, emf):
        super().__init__()
        self.source = source
        self.target = target
        self.emf = emf

    def plot(self):
        pos = nx.spring_layout(self)
        nc = ['c' for _ in range(self.number_of_nodes())]
        nc[self.source] = 'g'
        nc[self.target] = 'r'

        nx.draw_networkx_nodes(self, pos, node_color=nc, cmap=plt.get_cmap('jet'), node_size=1000)
        ids = dict([])
        for i in self.nodes():
            ids[i] = i
        nx.draw_networkx_labels(self, pos, ids)
        nx.draw_networkx_edges(self, pos, edge_color='c', arrows=True)
        nx.draw_networkx_edge_labels(self, pos, dict(
            map(lambda x: (x[0], str(round(x[1], 2)) + 'Ω'), nx.get_edge_attributes(self, 'resistance').items())))
        plt.show()


class CurrentGraph(nx.DiGraph):
    def __init__(self, circute: Circute):
        super().__init__()
        self.add_nodes_from(circute.nodes())
        nx.set_node_attributes(self, nx.get_node_attributes(circute, 'voltage'), 'voltage')
        print(nx.get_node_attributes(self, 'voltage'))
        self.source = circute.source
        self.target = circute.target
        for i in circute.nodes:
            for k, v in circute[i].items():
                v_curr = (circute.nodes[i]['voltage'] - circute.nodes[k]['voltage']) / v['resistance']
                if v_curr > 0.:
                    self.add_edge(i, k)
                    self[i][k]['current'] = v_curr
                else:
                    self.add_edge(k, i)
                    self[k][i]['current'] = v_curr

    def plot(self):
        pos = nx.spring_layout(self)
        nc = ['c' for _ in range(self.number_of_nodes())]
        nc[self.source] = 'g'
        nc[self.target] = 'r'

        nx.draw_networkx_nodes(self, pos, node_color=nc, cmap=plt.get_cmap('jet'), node_size=1000)
        nx.draw_networkx_labels(self, pos, dict(
            map(lambda x: (x[0], str(round(x[1], 2)) + 'V'), nx.get_node_attributes(self, 'voltage').items())))
        nx.draw_networkx_edges(self, pos, edge_color='c', arrows=True)
        nx.draw_networkx_edge_labels(self, pos, dict(
            map(lambda x: (x[0], str(round(x[1], 2)) + 'A'), nx.get_edge_attributes(self, 'current').items())))
        plt.show()
