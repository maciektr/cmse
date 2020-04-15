from random import randint


class Sudoku:
    def __init__(self):
        self.size = 9
        self.board = [[None for _ in range(self.size)] for _ in range(self.size)]
        self.cost_value = None
        self.mutable = []

    def initialize(self):
        self.mutable = []
        for i in range(self.size):
            for k in range(self.size):
                if self.board[i][k] is None:
                    self.mutable.append((i, k))
        missing = list(self.missing())
        for x, y in self.mutable:
            self.board[x][y] = missing.pop()

    def read_from_file(self, path):
        with open(path, 'r') as f:
            i = 0
            for line in f.readlines():
                self.board[i] = list(
                    map(lambda x: int(x) if x != 'x' else None, line.split()))
                i += 1
        # self.initialize()

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

    def cost(self):
        if self.cost_value is not None:
            return self.cost_value
        res = 0
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
        self.cost_value = res
        return res

    def copy(self):
        res = Sudoku()
        res.board = [list(r) for r in self.board]
        res.cost_value = self.cost_value
        return res

    # def next_random(self):
    #     x, y = self.mutable[randint(0, len(self.mutable) - 1)]
    #     res = self.copy()
    #     res.board[x][y] = randint(1, 9)
    #     res.cost_value = None
    #     res.mutable = self.mutable
    #     return res, (x, y)

    def missing(self):
        miss = []
        for i in range(0, 8 + 1):
            el, con = self.get_from_block(i)
            for num in range(1, 9+1):
                if num not in el:
                    miss.append(num)
        return miss

    def random_mutable(self):
        return self.mutable[randint(0, len(self.mutable) - 1)]

    def next(self):
        x, y = self.random_mutable()
        k, m = self.random_mutable()
        res = self.copy()
        res.board[x][y], res.board[k][m] = res.board[k][m], res.board[x][y]
        res.cost_value = None
        res.mutable = self.mutable
        return res, [(x, y), (k, m)]
