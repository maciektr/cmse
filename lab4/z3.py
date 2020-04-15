from lab4.sudoku import *
import plot_history
import random
import math


def hist_update(sudoku, step, history):
    if history is not None:
        history['list'].append({
            'id': step,
            'sudoku': sudoku.copy() if history['copy'] else None,
            'loss': sudoku.cost()
        })


def annealing(sudoku, steps, temp, alpha, hist=None):
    cost = sudoku.cost()
    best = {'img': sudoku.copy(), 'cost': cost}

    step_0 = steps
    while steps > 0 and temp > 1e-8:
        new_sudoku, changed = sudoku.next()
        new_cost = new_sudoku.cost(changed, sudoku)
        if best['cost'] > new_cost:
            best['cost'] = new_cost
            best['img'] = new_sudoku.copy()

        diff = cost - new_cost
        if diff > 0 or random.random() <= math.exp(-abs(diff) / temp):
            sudoku = new_sudoku
            cost = new_cost
            hist_update(sudoku, step_0 - steps, hist)
        # hist_update(history, steps_0 - steps, neigh_loss, neigh, True)
        steps -= 1
        temp *= alpha

    return best['img']


if __name__ == '__main__':
    path = 'boards/b1.txt'
    board = Sudoku()
    board.read_from_file(path)

    # board.print()
    # print(board.cost())

    steps = 1e12
    temp = 80
    alpha = 0.9995

    hist = {'list': [], 'copy': None}
    board = annealing(board, steps, temp, alpha, hist)
    plot_history.plot_loss(hist)
    board.print()
