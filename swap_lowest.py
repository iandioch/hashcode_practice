import sys
w, h, buffers, moves = [int(x) for x in sys.stdin.readline().strip().split(',')]

buff = []

board = []
for i in range(buffers):
    buff.append([int(c) for c in sys.stdin.readline().strip()])

sys.stdin.readline()
for i in range(h):
    board.append([int(c) for c in sys.stdin.readline().strip()])

for i in range(moves):
    print ("0, 0, 1, 0")
