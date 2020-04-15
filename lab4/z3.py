from lab4.sudoku import *

if __name__ == '__main__':
    path = 'boards/b1.txt'
    board = Sudoku()
    board.read_from_file(path)
    board.print()
    print(board.cost())
