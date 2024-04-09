def debug(board):
    for i in range(len(board)):
        for j in range(len((board[0]))):
            print(board[i][j],end=" ")
        print()
    print()

def rotate_maze(tmp, n):
    new = [[tmp[i][j] for i in range(n - 1, -1, -1)] for j in range(n)]
    for i in range(n):
        for j in range(n):
            if new[i][j]:
                new[i][j] -= 1
    return new

def find_to_rotate():
    for n in range(2, 11):
        for c in range(N - n):
            for r in range(N - n):
                if r <= ex < r + n and c <= ey < c + n:
                    for i in range(M + 1):
                        if escape[i]:
                            continue
                        rx, ry = runners[i]
                        if r <= rx < r + n and c <= ry < c + n:
                            return r, c, n
    return False

N, M, K = map(int, input().split())
board = [list(map(int, input().split())) for _ in range(N)] #1~N까지
dx, dy = (-1, 1, 0, 0), (0, 0, -1, 1)
#우회전 공식-> (i, j) -> (j, N -1 - i)
escaped = M
runners = [(-1, -1)]
escape = [False for _ in range(N + 1)]
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
        for i in range(1, M + 1):
            if escape[i]:
                continue
            x, y = runners[i]
            can_move = False
            dist = abs(x - ex) + abs(y - ey)
            for d in range(4):
                nx, ny = dx[d] + x, dy[d] + y
                new_dist = abs(nx - ex) + abs(ny - ey)
                if new_dist < dist:
                    if 0 <= nx < N and 0 <= ny < N and board[nx][ny] == 0:
                        x, y = nx, ny
                        can_move = True
                        break

            if can_move:
                running_dist += 1
            else:
                continue

            if (x, y) != (ex, ey):
                runners[i] = (x, y)
            else:
                escaped -= 1
                escape[i] = True

        if escaped == 0:
            break

        #미로 회전
        r, c, n = find_to_rotate()
        rotated = rotate_maze([[board[i][j] for j in range(c, c + n)] for i in range(r, r + n)], n)

        for i in range(n):
            for j in range(n):
                board[r + i][c + j] = rotated[i][j]

        for i in range(1, M + 1):
            x, y = runners[i]
            if r <= x < r + n and c <= y < c + n: #러너도 같이 회전되면 위치 변환
                x, y = x - r, y - c
                x, y = y, n - 1 - x
                x, y = x + r, y + c

            runners[i] = (x, y)
        ex, ey = ex - r, ey - c
        ex, ey = ey, n - 1 - ex
        ex, ey = ex + r, ey + c

    print(running_dist)
    print(ex + 1, ey + 1)
    #이동거리 합과 출구 좌표

solve()