# game.py - 游戏核心逻辑：路径检测、失误、胜负
DIRS = {
    0: (-1, 0),
    1: (0, 1),
    2: (1, 0),
    3: (0, -1),
}


class Game:
    def __init__(self, level_data, max_mistakes=3):
        self.grid = [row[:] for row in level_data]
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])
        self.max_mistakes = max_mistakes
        self.mistakes = 0
        self.remaining = sum(1 for r in self.grid for c in r if c is not None)

    def can_fly(self, row, col):
        d = self.grid[row][col]
        if d is None:
            return False
        dr, dc = DIRS[d]
        r, c = row + dr, col + dc
        while 0 <= r < self.rows and 0 <= c < self.cols:
            if self.grid[r][c] is not None:
                return False
            r += dr
            c += dc
        return True

    def click(self, row, col):
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return "empty"
        if self.grid[row][col] is None:
            return "empty"
        if self.can_fly(row, col):
            self.grid[row][col] = None
            self.remaining -= 1
            return "fly"
        else:
            self.mistakes += 1
            return "block"

    def is_win(self):
        return self.remaining == 0

    def is_lose(self):
        return self.mistakes >= self.max_mistakes