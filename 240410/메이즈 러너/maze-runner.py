from collections import deque
def debug(board):
    for i in range(len(board)):
        for j in range(len((board[0]))):
            print(board[i][j], end=" ")
        print()
    print()
def rotate_maze(tmp):
    n = len(tmp)
    return [[tmp[i][j] - 1 if tmp[i][j] > 0 else tmp[i][j] for i in range(n - 1, -1, -1)] for j in range(n)]
def find_to_rotate():
    for n in range(2, 11):
        for r in range(N):
            for c in range(N):
                if r <= ex < r + n and c <= ey < c + n:
                    for rx, ry in new_runners:
                        if r <= rx < r + n and c <= ry < c + n:
                            #print("ex, ey", ex, ey, "rx, ry", rx, ry)
                            return r, c, n
    return False

N, M, K = map(int, input().split())
board = [list(map(int, input().split())) for _ in range(N)]  # 1~N까지
dx, dy = (-1, 1, 0, 0), (0, 0, -1, 1)
# 우회전 공식-> (i, j) -> (j, N -1 - i)
escaped = M
runners = deque()
new_runners = deque()
ex, ey = -1, -1


def solve():
    global ex, ey, escaped
    for _ in range(M):
        x, y = map(lambda x: int(x) - 1, input().split())
        runners.append((x, y))
    ex, ey = map(lambda x: int(x) - 1, input().split())

    running_dist = 0
    for k in range(1, K + 1):
        # 참가자 이동
        #print(f"{k} before run {runners}")
        #debug(board)
        #print("ex, ey", ex, ey)
        while runners:
            x, y = runners.popleft()
            dist = abs(x - ex) + abs(y - ey)
            candidates = []
            for d in range(4):
                nx, ny = dx[d] + x, dy[d] + y
                new_dist = abs(nx - ex) + abs(ny - ey)
                if new_dist < dist:
                    if 0 <= nx < N and 0 <= ny < N and board[nx][ny] == 0:
                        candidates.append([nx, ny])
                        break

            if not candidates:
                nx, ny = x, y
            else:
                nx, ny = candidates[0]
                running_dist += 1

            if (nx, ny) != (ex, ey):
                new_runners.append((nx, ny))
            else:
                escaped -= 1

        if escaped == 0:
            break

        # 미로 회전
        #print(f"after run {new_runners}")

        r, c, n = find_to_rotate()
        #print(f"r {r}, c {c}, n {n}")

        to_rotate = [[board[i][j] for j in range(c, c + n)] for i in range(r, r + n)]
        #print("to_rotate")
        #debug(to_rotate)

        #print("rotated")
        rotated = rotate_maze(to_rotate)
        #debug(rotated)

        for i in range(n):
            for j in range(n):
                board[r + i][c + j] = rotated[i][j]

        while new_runners:
            x, y = new_runners.popleft()
            if r <= x < r + n and c <= y < c + n:  # 러너도 같이 회전되면 위치 변환
                x, y = x - r, y - c
                x, y = y, n - 1 - x
                x, y = x + r, y + c
                runners.append((x, y))
            else:
                runners.append((x, y))

        ex, ey = ex - r, ey - c
        ex, ey = ey, n - 1 - ex
        ex, ey = ex + r, ey + c
        '''print("after rotate maze")
        print("ex, ey", ex, ey)
        print("runners", runners)
        debug(board)'''
    print(running_dist)
    print(ex + 1, ey + 1)
    # 이동거리 합과 출구 좌표


solve()
'''
10 9 59
1 7 4 8 3 4 6 5 1 6
0 2 2 6 6 6 9 9 6 7
7 4 4 9 2 2 2 2 6 5
2 8 9 7 0 6 0 5 4 9
1 8 6 9 8 5 4 4 6 6
2 9 5 5 7 9 0 5 0 3
6 9 6 5 5 7 7 5 9 0
9 6 5 6 4 0 8 6 8 0
0 0 9 2 7 7 7 7 5 5
3 9 0 2 2 8 3 0 2 0
7 10
7 10
4 5
10 3
4 5
10 3
10 10
10 10
2 1
6 9
'''