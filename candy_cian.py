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
        self.X = len(brd)
        self.Y = len(brd[0])
        self.print_board()
        #self.destroy()

    def swap(self, c1, c2):
        self.b[c1.x][c1.y], self.b[c2.x][c2.y] = self.b[c2.x][c2.y], self.b[c1.x][c1.y]

    def get(self, c):
        return self.b[c.x][c.y]

    def score_for_swap(self, c1, c2):
        self.swap(c1, c2)
        a, _ = self.get_connects(c1)
        b, _ = self.get_connects(c2)
        score = max(a, b)
        self.swap(c1, c2)
        return score

    def on_b(self, c):
        return 0 <= c.x < len(self.b) and 0 <= c.y < len(self.b[0])

    def get_connects(self, c):
        val = self.get(c)
        if val is None:
            return 0, set()
        # Get horizontal score
        horz_visited = set([(c.x, c.y)])
        best_horz_start = c.x
        while best_horz_start > 0:
            if self.get(Cord(best_horz_start - 1, c.y)) != val:
                break
            best_horz_start -= 1
            horz_visited.add((best_horz_start, c.y))
        best_horz_end = c.x
        while best_horz_end < len(self.b) - 1:
            if self.get(Cord(best_horz_end + 1, c.y)) != val:
                break
            best_horz_end += 1
            horz_visited.add((best_horz_end, c.y))

        # Get vertical score
        vert_visited = set([(c.x, c.y)])
        best_vert_start = c.y
        while best_vert_start > 0:
            if self.get(Cord(c.x, best_vert_start - 1)) != val:
                break
            best_vert_start -= 1
            vert_visited.add((c.x, best_vert_start))
        best_vert_end = c.y
        while best_vert_end < len(self.b[0]) - 1:
            if self.get(Cord(c.x, best_vert_end + 1)) != val:
                break
            best_vert_end += 1
            vert_visited.add((c.x, best_vert_end))

        horz_points = 0 if len(horz_visited) < 3 else len(horz_visited)**2
        vert_points = 0 if len(vert_visited) < 3 else len(vert_visited)**2
        print("Start {}".format(c.pair()))
        if horz_points and vert_points:
            print("DOUBLEVE")
            return horz_points + vert_points, horz_visited | vert_visited
        elif horz_points:
            print("Best is horz")
            return horz_points, horz_visited
        else:
            print("Best is verts")
            return vert_points, vert_visited


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

    def print_board(self):
        for y in range(len(self.b[0])):
            print('| ', end='')
            for x in range(len(self.b)):
                print(self.b[x][y], '| ', end='')
            print()
            print('-'*len(self.b)*4)

    def settle(self):
        for x in range(len(self.b)):
            print("Settling column {}".format(x))
            for y in range(len(self.b[0]))[::-1]:
                curr_cord = Cord(x, y)
                if self.get(curr_cord) is not None:
                    print(x, y, "is good")
                    continue
                # Find the next good one
                next_y = y - 1
                while next_y >= 0:
                    if self.get(Cord(x, next_y)) is not None:
                        print("Foind a good one at {}".format(next_y))
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

    def destroy(self):
        something_destroyed = False
        for x in range(len(self.b)):
            for y in range(len(self.b[0])):
                pts, conn = self.get_connects(Cord(x, y))
                if not pts:
                    continue
                # Get best version
                for xy in conn:
                    print("Checking if {} is best".format(str(xy)))
                    new_pts, new_conn = self.get_connects(Cord(*xy))
                    print("It got {} points".format(new_pts))
                    if new_pts > pts:
                        pts = new_pts
                        conn = new_conn
                        x, y = xy
                print("Got points for {},{}".format(x, y))
                print("(It's a {})\n".format(self.get(Cord(x, y))))
                something_destroyed = True
                self.points += pts
                self.zero_places(conn)
        if something_destroyed:
            self.settle()
            self.destroy()



W, H, B, M = map(int, input().split(','))

buf = Buffer(W)

for _ in range(B):
    line = list(map(int, input()))
    buf.push_line(line)

assert('-'*W == input())

b = [[] for _ in range(W)]
for _ in range(H):
    for x, val in enumerate(map(int, input())):
        b[x].append(val)

b = [
    [1, 1, 2],
    [2, 2, 2],
    [1, 2, 1]
]
buf = Buffer(3)

board = Board(b, buf)
best_score = 0
best_pair = None
other = None
for x in range(board.X - 1):
    for y in range(board.Y - 1):
        a, b1 = Cord(x, y), Cord(x + 1, y)
        sc1 = board.score_for_swap(a, b1)
        b2 = Cord(x, y + 1)
        sc2 = board.score_for_swap(a, b2)
        if max(sc1, sc2) > best_score:
            best_pair = a
            other = b1 if sc1 > sc2 else b2
            best_score = max(sc1, sc2)
print(best_pair.pair())
print(other.pair())
print(best_score)

# best_pair = None
# for x in range(W - 1):
#     for y in range(H - 1):


# print(board.points)
# board.print_board()
# print(board.score_for_swap(Cord(0, 0), Cord(0, 1)))
# board.swap(Cord(0,0), Cord(1, 0))
# board.destroy()
# print(board.points)
# board.swap(Cord(1, 0), Cord(2, 0))
# board.destroy()
# print(board.points)
# board.print_board()
