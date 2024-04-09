from collections import deque

def debug(board):
    for i in range(len(board)):
        for j in range(len((board[0]))):
            print(board[i][j],end=" ")
        print()
    print()

def rotate_maze(tmp):
    n = len(tmp)
    new = [[tmp[i][j] for i in range(n - 1, -1, -1)] for j in range(n)]
    for i in range(n):
        for j in range(n):
            if new[i][j]:
                new[i][j] -= 1
    return new

def find_to_rotate():
    n = 2
    while True:
        for c in range(N - n):
            for r in range(N - n):
                if r <= ex < r + n and c <= ey < c + n:
                    for rx, ry in new_runners:
                        if r <= rx < r + n and c <= ry < c + n:
                            return r, c, n
        n += 1
    return False

N, M, K = map(int, input().split())
board = [list(map(int, input().split())) for _ in range(N)] #1~N까지
dx, dy = (-1, 1, 0, 0), (0, 0, -1, 1)
#우회전 공식-> (i, j) -> (j, N -1 - i)
escaped = M
runners = deque()
new_runners = deque()
ex, ey = -1 ,-1
def solve():
    global ex, ey, escaped
    for _ in range(M):
        x, y = map(lambda x:int(x) - 1, input().split())
        runners.append((x, y))
    ex, ey = map(lambda x:int(x) - 1, input().split())

    running_dist = 0
    for k in range(1, K + 1):
        #참가자 이동
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

        #미로 회전
        r, c, n = find_to_rotate()
        rotated = rotate_maze([[board[i][j] for j in range(c, c + n)] for i in range(r, r + n)])

        for i in range(n):
            for j in range(n):
                board[r + i][c + j] = rotated[i][j]

        while new_runners:
            x, y = new_runners.popleft()
            if r <= x < r + n and c <= y < c + n: #러너도 같이 회전되면 위치 변환
                x, y = x - r, y - c
                x, y = y, n - 1 - x
                x, y = x + r, y + c
                runners.append((x, y))
            else:
                runners.append((x, y))

        ex, ey = ex - r, ey - c
        ex, ey = ey, n - 1 - ex
        ex, ey = ex + r, ey + c

    print(running_dist)
    print(ex + 1, ey + 1)
    #이동거리 합과 출구 좌표

solve()