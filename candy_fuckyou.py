import copy
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
            #print("At pair {}, {}".format(*cor.pair()))
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
            for y in range(len(self.b[0]))[::-1]:
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

    def straightlines(self):
        repls = set()
        score = 0
        w = len(self.b)
        h = len(self.b[0])
        #print(','.join([y for y in '\n'.join(str(x) for x in self.b)]))
        for y in range(h-1, -1, -1):
            x = 0 
            while x < w-2:
                #print('try ', x, y)
                if self.b[x][y] == self.b[x+1][y]:
                    n = 2
                    for i in range(x+2, w):
                        if self.b[i][y] != self.b[x][y]:
                            break
                        n += 1
                    if n > 2: 
                        x += n 
                        score += n**2
                        #print('hi')
                        repls |= set(Cord(i,y) for i in range(x-n, x))
                x += 1
        for x in range(0, w):
            y = h-1
            while y > 1:
                if self.b[x][y] == self.b[x][y-1]:
                    n = 2
                    for i in range(y-2, -1, -1):
                        if self.b[x][i] != self.b[x][y]:
                            break
                        n += 1
                    if n > 2: 
                        #print('ho')
                        repls |= set(Cord(x,i) for i in range(y-n+1, y+1))
                        y -= n 
                        score += n**2
                y -= 1
        return repls, score

    def destroy(self):
        something_destroyed = False
        repls, score = self.straightlines()
        for c in repls:
            #print(c.x, c.y)
            self.b[c.x][c.y] = None
        self.points += score
        #print('score = ', score)
        if score == 0:
            return
        self.settle()
        self.destroy()


W, H, B, M = map(int, input().split(','))

buf = Buffer(W)

for _ in range(B):
    line = list(map(int, input().strip()))
    buf.push_line(line)

assert('-'*W == input().strip())

q = []
b = [[0 for i in range(H)] for j in range(W)]
for _ in range(H):
    line = list(map(int, input().strip()))
    q.append(line)

for y in range(H):
    for x in range(W):
        b[x][y] = q[y][x]


board = Board(b, buf)
board.destroy()
#print(b)

#print(board.score_for_swap(Cord(0, 0), Cord(0 ,1)))

for movelol in range(1):
    bestscore = 0
    bestquad = [0,0,0,0]
    for x in range(W-1):
        for y in range(H-1, -1, -1):
            newbuf = copy.deepcopy(buf) 
            newb = copy.deepcopy(b)
            newboard = Board(newb, newbuf)
            newboard.swap(Cord(x, y), Cord(x+1, y))
            newboard.destroy()
            #print(newboard.points)
            if newboard.points > bestscore:
                bestscore = newboard.points
                bestquad = [y, x, y, x+1]
    for x in range(W):
        for y in range(H-1, 0, -1):
            newbuf = copy.deepcopy(buf) 
            newb = copy.deepcopy(b)
            newboard = Board(newb, newbuf)
            newboard.swap(Cord(x, y), Cord(x, y-1))
            newboard.destroy()
            #print(newboard.points)
            if newboard.points > bestscore:
                bestscore = newboard.points
                bestquad = [y,x,y-1,x]
    if bestscore == 0:
        break
    print (','.join([str(q) for q in bestquad]))
    board.swap(Cord(bestquad[1], bestquad[0]), Cord(bestquad[3], bestquad[2]))
    board.destroy()
