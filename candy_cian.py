import sys
from queue import Queue

class Cord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def pair(self):
        return self.x, self.y

class Buffer:
    def __init__(self, width):
        self.cols = [[] for _ in range(width)]

    def push_line(self, line):
        for i, val in enumerate(line):
            self.cols[i].append(val)

    def pop_col(self, col_i):
        return self.cols[col_i].pop() if self.cols[col_i] else None

class Board:
    def __init__(self, brd, buff):
        self.b = brd
        self.buff = buff
        self.points = 0

    def swap(self, c1, c2):
        self.b[c1.x][c1.y], self.b[c2.x][c2.y] = self.b[c2.x][c2.y], self.b[c1.x][c1.y]

    def get(self, c):
        return self.b[c.x][c.y]

    def score_for_swap(self, c1, c2):
        self.swap(c1, c2)
        score = max(len(self.bfs(c1)), len(self.bfs(c2)))
        self.swap(c1, c2)
        return score**2 if score >= 3 else 0

    def on_b(self, c):
        return 0 <= c.x < len(self.b) and 0 <= c.y < len(self.b[0])

    def bfs(self, c):
        q = Queue()
        q.put(c)
        visited = set()
        val = self.get(c)
        if val is None:
            return visited
        muts = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        while not q.empty():
            cor = q.get()
            print("At pair {}, {}".format(*cor.pair()))
            for x_mut, y_mut in muts:
                nxt_cor = Cord(cor.x + x_mut, cor.y + y_mut)
                if not self.on_b(nxt_cor):
                    continue
                if nxt_cor.pair() not in visited and self.get(nxt_cor) == val:
                    q.put(nxt_cor)
            visited.add(cor.pair())
        return visited

    def zero_places(self, it):
        for x, y in it:
            self.b[x][y] = None

    def settle(self):
        for x in range(len(self.b)):
            for y in range(len(self.b))[::-1]:
                curr_cord = Cord(x, y)
                if self.get(curr_cord) is not None:
                    continue
                # Find the next good one
                next_y = y - 1
                while next_y >= 0:
                    if self.get(Cord(x, next_y)) is not None:
                        break
                    next_y -= 1
                if next_y > 0:
                    # Good one found
                    self.swap(curr_cord, Cord(x, next_y))
                else:
                    # Buffer time!
                    self.b[x][y] = self.buff.pop_col(x)
                if self.get(curr_cord) is None:
                    # Buffer empty
                    break

    def destroy(self):
        something_destroyed = False
        for x in range(len(self.b)):
            for y in range(len(self.b[0])):
                conn = self.bfs(Cord(x, y))
                if len(conn) < 3:
                    continue
                something_destroyed = True
                self.points += len(conn)**2
                self.zero_places(conn)
        if not something_destroyed:
            return
        self.settle()
        self.destroy()


W, H, B, M = map(int, input().split(','))

buf = Buffer(W)

for _ in range(B):
    line = list(map(int, input()))
    buf.push_line(line)

assert('-'*W == input())

b = []
for _ in range(H):
    line = list(map(int, input()))
    b.append(line)

board = Board(b, buf)

print(board.score_for_swap(Cord(0, 0), Cord(0 ,1)))

