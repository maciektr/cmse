from Circute import Circute, CurrentGraph


def solve(G):
    G.findVoltages()
    return CurrentGraph(G)


if __name__ == '__main__':
    path = 'graphs/g1'
    G = Circute(path)
    res = solve(G)
    # G.plot()
    res.plot()
