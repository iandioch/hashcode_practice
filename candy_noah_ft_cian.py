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

    def settle(self, xs):
        for x in xs:
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
                if next_y >= 0:
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
        self.settle(set([c.x for c in repls]))
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

bestmoves = [
[28,10,28,11],
[26,25,26,26],
[27,16,26,16],
[27,15,26,15],
[26,3,26,4],
[25,3,24,3],
[18,0,18,1],
[28,4,27,4],
[21,2,21,3],
[24,16,24,17],
[24,23,23,23],
[25,23,25,24],
[14,22,13,22],
[21,5,21,6],
[22,13,22,14],
[24,13,24,14],
[17,19,17,20],
[18,13,18,14],
[21,10,21,11],
[25,13,25,14],
[28,15,28,16],
[23,14,23,15],
[25,23,25,24],
[17,20,16,20],
[25,6,25,7],
[29,11,28,11],
[23,0,22,0],
[22,23,21,23],
[21,23,21,24],
[27,26,26,26],
[25,5,25,6],
[21,5,20,5],
[28,19,28,20],
[29,19,29,20],
[23,23,22,23],
[26,22,25,22],
[29,20,28,20],
[23,20,23,21],
[26,22,25,22],
[21,22,20,22],
[21,24,21,25],
[25,26,25,27],
[24,27,24,28],
[21,25,21,26],
[29,29,28,29],
[23,28,22,28],
[22,28,22,29],
[28,10,27,10],
[25,7,25,8],
[22,9,22,10],
[21,9,21,10],
[25,10,24,10],
[25,8,25,9],
[22,7,22,8],
[21,6,21,7],
[26,5,25,5],
[26,8,25,8],
[21,6,20,6],
[27,8,26,8],
[29,8,28,8],
[27,8,27,9],
[25,10,25,11],
[24,10,24,11],
[23,10,23,11],
[29,10,28,10],
[29,9,29,10],
[28,8,27,8],
[21,11,20,11],
[25,4,24,4],
[27,7,27,8],
[25,2,24,2],
[24,1,23,1],
[25,0,25,1],
[25,1,25,2],
[26,2,25,2],
[22,1,21,1],
[26,3,26,4],
[26,6,25,6],
[27,1,27,2],
[25,1,25,2],
[25,6,24,6],
[22,6,22,7],
[25,7,24,7],
[28,10,27,10],
[25,6,25,7],
[25,4,24,4],
[27,2,26,2],
[26,7,25,7],
[24,7,23,7],
[18,5,18,6],
[16,7,16,8],
[19,2,18,2],
[4,10,3,10],
[17,8,17,9],
[18,14,18,15],
[20,15,19,15],
[24,14,23,14],
[19,25,19,26],
[13,26,13,27],
[20,26,19,26],
]

# bestmoves = [
# [28,10,28,11],
# [26,25,26,26],
# [27,16,26,16],
# [27,15,26,15],
# [26,3,26,4],
# [25,3,24,3],
# [18,0,18,1],
# [28,4,27,4],
# [21,2,21,3],
# [24,16,24,17],
# [24,23,23,23],
# [25,23,25,24],
# [14,22,13,22],
# [21,5,21,6],
# [22,13,22,14],
# [24,13,24,14],
# [17,19,17,20],
# [18,13,18,14],
# [21,10,21,11],
# [25,13,25,14],
# [28,15,28,16],
# [23,14,23,15],
# [25,23,25,24],
# [17,20,16,20],
# [12,20,12,21],
# [12,19,12,20],
# [5,23,5,24],
# [25,6,25,7],
# [19,10,18,10],
# [20,6,19,6],
# [17,3,17,4],
# [19,4,19,5],
# [3,3,3,4],
# [8,3,8,4],
# [7,11,7,12],
# [27,11,27,12],
# [24,11,24,12],
# [20,10,20,11],
# [15,9,15,10],
# [23,8,23,9],
# [19,14,18,14],
# [3,11,3,12],
# [16,14,16,15],
# [25,7,25,8],
# [27,10,26,10],
# [14,8,13,8],
# [18,7,18,8],
# [23,5,23,6],
# [8,10,7,10],
# [24,4,24,5],
# [14,9,13,9],
# [19,7,18,7],
# [9,3,9,4],
# [4,2,3,2],
# [25,5,25,6],
# ]


for move in bestmoves:
    old_pts = board.points
    board.swap(Cord(move[1], move[0]), Cord(move[3], move[2]))
    board.destroy()
    #print ('{:>2}, {:>2}, {:>2}, {:>2}'.format(*[str(x) for x in move]), end='')
    #print('    {} (+{})'.format(board.points, board.points - old_pts))
    print(board.points - old_pts)

sys.exit()
#print(b)

#print(board.score_for_swap(Cord(0, 0), Cord(0 ,1)))

for movelol in range(M-len(bestmoves)):
    bestscore = 0
    bestquad = [0,0,0,0]
    for x in range(W-1):
        for y in range(H-1, 1, -1):
            newbuf = copy.deepcopy(buf) 
            newb = copy.deepcopy(b)
            if newb[x][y] == newb[x+1][y]:
                continue
            newboard = Board(newb, newbuf)
            newboard.swap(Cord(x, y), Cord(x+1, y))
            newboard.destroy()
            #print(newboard.points)
            if newboard.points > bestscore:
                bestscore = newboard.points
                bestquad = [y, x, y, x+1]
    for x in range(W):
        for y in range(H-1, 1, -1):
            newbuf = copy.deepcopy(buf) 
            newb = copy.deepcopy(b)
            if newb[x][y] == newb[x][y-1]:
                continue
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
