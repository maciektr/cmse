class Sudoku:
    def __init__(self):
        self.size = 9
        self.board = [[None for _ in range(self.size)] for _ in range(self.size)]

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
        return res
