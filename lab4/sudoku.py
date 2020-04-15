from random import randint
import multiset


class Sudoku:
    def __init__(self):
        self.size = 9
        self.board = [[None for _ in range(self.size)] for _ in range(self.size)]
        self.cost_value = None
        self.miss = None

    def read_from_file(self, path):
        with open(path, 'r') as f:
            i = 0
            for line in f.readlines():
                self.board[i] = list(
                    map(lambda x: int(x) if x != 'x' else None, line.split()))
                i += 1

    def print(self):
        for r in self.board:
            print(' '.join(map(lambda x: str(x) if x is not None else 'x', r)))

    @staticmethod
    def block_start(block_id):
        return block_id // 3 * 3, block_id % 3 * 3

    @staticmethod
    def block_id(point):
        return point[0] // 3 * 3 + point[1] // 3

    def get_from_block(self, block_id):
        x, y = self.block_start(block_id)
        res = set()
        conflicts = 0
        for i in range(0, 3):
            for k in range(0, 3):
                el = self.board[x + i][y + k]
                if el in res:
                    conflicts += 1
                res.add(el)
        return res, conflicts

    def col_row_cost(self, x, y):
        res = 0
        seen_col = set()
        seen_row = set()
        for i in range(0, self.size):
            col_el = self.board[x][i]
            row_el = self.board[i][y]
            if col_el in seen_col:
                res += 1
            seen_col.add(col_el)
            for row_el in seen_row:
                res += 1
            seen_row.add(row_el)
        return res

    def cost(self, changed=None, previous=None):
        if self.cost_value is not None:
            return self.cost_value
        res = 0
        if changed is None:
            seen_col = [set() for _ in range(self.size)]
            for i in range(self.size):
                seen_row = set()
                for k in range(self.size):
                    el = self.board[i][k]
                    if el in seen_col[k]:
                        res += 1
                    seen_col[k].add(el)
                    if el in seen_row:
                        res += 1
                    seen_row.add(el)
            for i in range(0, 8 + 1):
                el, con = self.get_from_block(i)
                res += con
        else:
            res = previous.cost()
            x, y = changed
            res -= previous.col_row_cost(x, y)
            res += self.col_row_cost(x, y)
            bid = Sudoku.block_id(changed)
            res -= previous.get_from_block(bid)[1]
            res += self.get_from_block(bid)[1]
        self.cost_value = res
        return res

    def copy(self):
        res = Sudoku()
        res.board = [list(r) for r in self.board]
        res.cost_value = self.cost_value
        return res

    def next(self):
        x, y = randint(0, self.size - 1), randint(0, self.size - 1)
        res = self.copy()
        res.board[x][y] = randint(1, 9)
        res.cost_value = None
        res.miss = None
        return res, (x, y)

    def col_row_missing(self, x, y):
        res = []
        seen_col = set()
        seen_row = set()
        for i in range(0, self.size):
            col_el = self.board[x][i]
            row_el = self.board[i][y]
            seen_col.add(col_el)
            seen_row.add(row_el)
        for num in range(1, 9):
            if (num not in seen_col) or (num not in seen_row):
                res.append(num)
        return res

    def missing(self, changed=None, previous=None):
        if self.miss is not None:
            return self.miss
        self.miss = multiset.Multiset()
        if changed is None:
            seen_col = [set() for _ in range(self.size)]
            for i in range(self.size):
                seen_row = set()
                for k in range(self.size):
                    el = self.board[i][k]
                    seen_col[k].add(el)
                    seen_row.add(el)
                for num in range(1, 9):
                    if num not in seen_row:
                        self.miss.add(num)
            for i in range(self.size):
                for num in range(1, 9):
                    if num not in seen_col[i]:
                        self.miss.add(num)
            for i in range(0, 8 + 1):
                el, con = self.get_from_block(i)
                for num in range(1, 9):
                    if num not in el:
                        self.miss.add(num)
        else:
            self.miss = previous.missing()
            x, y = changed
            self.miss -= previous.col_row_missing(x, y)
            self.miss += self.col_row_missing(x, y)
            bid = Sudoku.block_id(changed)
            prev_block = previous.get_from_block(bid)[0]
            board_block = self.get_from_block(bid)[0]
            for num in range(1, 9):
                if (num not in prev_block) or (num not in board_block):
                    self.miss.add(num)
        return self.miss
