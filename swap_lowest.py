import sys

w, h, buffers, moves = [int(x) for x in sys.stdin.readline().strip().split(',')]

def copy2d(old):
    new1 = [[x for x in y] for y in old]
    return new1

def swap(newboard, x1, y1, x2, y2):
    newboard[y1][x1], newboard[y2][x2] = newboard[y2][x2], newboard[y1][x1]
    return newboard

def calc_score_of_swap(board):
    score = 0
    for y in range(h-1, -1, -1):
        x = 0
        while x < w-2:
            #print(board[y][x], board[y][x+1], board[y][x+2])
            if board[y][x] == board[y][x+1]:
                n = 2
                for i in range(x+2, w):
                    if board[y][i] != board[y][x]:
                        break
                    n += 1
                if n > 2:
                    x += n
                    score += n**2
            x += 1
    for x in range(0, w):
        y = h-1
        while y > 1:
            #print('checking vert ', y, x)
            if board[y][x] == board[y-1][x]:
                n = 2
                for i in range(y-2, -1, -1):
                    if board[i][x] != board[y][x]:
                        break
                    n += 1
                if n > 2:
                    y -= n
                    score += n**2
            y -= 1
    return score

buff = []
board = []

for i in range(buffers):
    buff.append([(c) for c in sys.stdin.readline().strip()])

sys.stdin.readline()
for i in range(h):
    board.append([(c) for c in sys.stdin.readline().strip()])

for i in board:
    pass#print (i)
calc_score_of_swap(board)

for i in range(1):
    #print(i)
    bestscore = 0
    bestquad = [0,0,0,0]
    for x in range(w-1):
        for y in range(h-2, -1, -1):
            newboard = copy2d(board)
            x1 = x
            y1 = y
            x2 = x
            y2 = y+1
            newboard[y1][x1], newboard[y2][x2] = newboard[y2][x2], newboard[y1][x1]
            if board[y][x] == newboard[y][x]:
                # no change
                continue
            #print ('\n'.join([''.join([str(c) for c in j]) for j in newboard]))
            score = calc_score_of_swap(newboard)
            if score > bestscore:
                bestscore = score
                bestquad = [y1, x1, y2, x2]
    print (','.join([str(t) for t in bestquad]))
