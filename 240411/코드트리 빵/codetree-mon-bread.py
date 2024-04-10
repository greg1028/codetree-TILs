from collections import deque
N, M = map(int, input().split())
root = [[True for _ in range(N)] for _ in range(N)] #True 면 이동 가능
board = [list(map(int, input().split())) for _ in range(N)] #베이스 캠프 1
con = tuple(tuple(map(lambda x:int(x) - 1, input().split())) for _ in range(M))
people_loc = [(False, -1, -1) for _ in range(M)] #is_in, 좌표
dx, dy = (-1, 0, 0, 1), (0, -1, 1, 0)

def debug(board):
    for i in range(N):
        for j in range(N):
            print(board[i][j], end=" ")
        print()
    print()

def find_base_camp(i):
    x, y = con[i]
    q = deque()
    q.append((x, y, 0))
    visited = [[False for _ in range(N)] for _ in range(N)]
    visited[x][y] = True
    min_dist = 1e9
    candidates = []
    while q:
        x, y, dist = q.popleft()
        for d in range(4):
            nx, ny = dx[d] + x, dy[d] + y
            if 0 <= nx < N and 0 <= ny < N and not visited[nx][ny]:
                visited[nx][ny] = True
                if root[nx][ny]:
                    if board[nx][ny] == 1: #베이스캠프라면
                        if min_dist > dist + 1:
                            min_dist = dist + 1
                            candidates = [(nx, ny)]

                        elif min_dist == dist + 1:
                            candidates.append((nx, ny))

                    if min_dist > dist + 1:
                        q.append((nx, ny, dist + 1))
    candidates.sort(key=lambda x:[x[0], x[1]])
    x, y = candidates[0]
    board[x][y] = 0
    root[x][y] = False
    people_loc[i] = (True, x, y)
    return
def move(i):
    visited = [[False for _ in range(N)] for _ in range(N)]
    _, sx, sy = people_loc[i]
    q = deque()
    q.append((sx, sy, []))
    cx, cy = con[i]
    find_way = False
    while q:
        x, y, path = q.popleft()
        for d in range(4):
            nx, ny = dx[d] + x, dy[d] + y
            if 0 <= nx < N and 0 <= ny < N and root[nx][ny] and not visited[nx][ny]:
                visited[nx][ny] = True
                new = path + [d]
                q.append((nx, ny, new))
                if (nx, ny) == (cx, cy):
                    find_way = True
                    nd = new[0]
                    mx, my = sx + dx[nd], sy + dy[nd]
                    people_loc[i] = [True, mx, my]

                    if (mx, my) == (cx, cy):
                        people_loc[i][0] = False
                        return True

                if find_way:
                    return False

    return False

remain = M #주의
time = 0
while remain > 0:

    convi_reach_people = []
    for i in range(M):
        is_in, x, y = people_loc[i]
        if not is_in: #나갔거나 아직 들어오지 않았다면
            continue
        reached = move(i)
        if reached:
            convi_reach_people.append(i)

    #2. 편의점에 도착한 사람들 처리 ()
    for i in convi_reach_people:
        _, x, y = people_loc[i]
        root[x][y] = False
        remain -= 1

    if remain == 0:
        break

    #3. t분의 사람 편의점과 가장 가까운 베이스 캠프에 들어감
    if time < M:
        find_base_camp(time)

    time += 1

print(time + 1)