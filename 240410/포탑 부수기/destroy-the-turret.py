#4시간에 새로운문제 + 풀었던 문제 ㄱㄱ
from collections import deque
# 추적해야 되는 정보, 공격력, 공격시점, 해당 턴에 공격과 관련 있는지(공격자와 피해자가 아닌 것)
N, M, K = map(int, input().split())
board = [list(map(int, input().split())) for _ in range(N)]
attack_time = [[0 for _ in range(M)] for _ in range(N)]
innocent = [[True for _ in range(M)] for _ in range(N)]
ldx, ldy = (0, 1, 0, -1), (1, 0, -1, 0)
bdx, bdy = (-1, -1, -1, 0, 0, 1, 1, 1), (-1, 0, 1, -1, 1, -1, 0, 1)

remain = 0
for i in range(N):
    for j in range(M):
        if board[i][j] > 0:
            remain += 1

def debug(borad):
    for i in range(N):
        for j in range(M):
            print(borad[i][j], end=" ")
        print()
    print()
    print()

def find_attacker():
    ax, ay, min_damage = -1, -1, 1e9
    latest_attack = 0
    for i in range(N):
        for j in range(M):
            if board[i][j] <= 0:
                continue
            if board[i][j] < min_damage:
                min_damage = board[i][j]
                latest_attack = attack_time[i][j]
                ax, ay = i, j

            elif board[i][j] == min_damage:
                if latest_attack < attack_time[i][j]:
                    latest_attack = attack_time[i][j]
                    ax, ay = i, j

                elif latest_attack == attack_time[i][j]:

                    if ax + ay < i + j:
                        ax, ay = i, j

                    elif ax + ay == i + j:
                        if ay < j:
                            ax, ay = i, j

    board[ax][ay] += N + M #포탑 강화
    return ax, ay

def find_victim(ax, ay):
    vx, vy, max_damage = N - 1, M - 1, 0
    oldest_attack = 1e9
    for i in range(N):
        for j in range(M):
            if board[i][j] <= 0 or (i, j) == (ax, ay):
                continue
            if board[i][j] > max_damage:
                max_damage = board[i][j]
                oldest_attack = attack_time[i][j]
                vx, vy = i, j

            elif board[i][j] == max_damage:
                if attack_time[i][j] < oldest_attack: #숫자가 작아야 더 오래된것
                    oldest_attack = attack_time[i][j]
                    vx, vy = i, j

                elif attack_time[i][j] == oldest_attack:
                    if vx + vy > i + j:
                        vx, vy = i, j

                    elif vx + vy == i + j:
                        if vy > j:
                            vx, vy = i, j
    return vx, vy

def attack(ax, ay, vx, vy):
    global remain
    attack_time[ax][ay] = k + 1
    innocent[ax][ay] = False
    innocent[vx][vy] = False
    visited = [[False for _ in range(M)] for _ in range(N)]
    visited[ax][ay] = True
    reached = False
    q = deque()
    q.append((ax, ay, [])) #좌표
    reached_path = []
    while q:
        if reached:
            break
        x, y, path = q.popleft()
        for d in range(4):
            nx, ny = (ldx[d] + x + N) % N, (ldy[d] + y + M) % M
            if not visited[nx][ny] and board[nx][ny] > 0:
                visited[nx][ny] = True
                if (nx, ny) == (vx, vy):
                    reached = True
                    reached_path = path
                    break
                else:
                    q.append((nx, ny, path + [d]))

    if reached: #lazer
        nx, ny = ax, ay
        for d in reached_path:
            nx, ny = (nx + ldx[d] + N) % N, (ny + ldy[d] + M) % M
            innocent[nx][ny] = False
            board[nx][ny] -= board[ax][ay] // 2
            if board[nx][ny] <= 0:
                board[nx][ny] = 0
                remain -= 1

        board[vx][vy] -= board[ax][ay]
        if board[vx][vy] <= 0:
            board[vx][vy] = 0
            remain -= 1
        return

    #if not find bomb
    board[vx][vy] -= board[ax][ay]
    if board[vx][vy] <= 0:
        board[vx][vy] = 0
        remain -= 1

    for d in range(8):
        nx, ny = (vx + bdx[d] + N) % N, (vy + bdy[d] + M) % M
        innocent[nx][ny] = False
        board[nx][ny] -= board[ax][ay] // 2
        if board[nx][ny] <= 0:
            board[nx][ny] = 0
            remain -= 1
    return

def repair():
    for i in range(N):
        for j in range(M):
            if board[i][j] > 0 and innocent[i][j]:
                board[i][j] += 1
    return


for k in range(K):
    innocent = [[True for _ in range(M)] for _ in range(N)]
    ax, ay = find_attacker()
    vx, vy = find_victim(ax, ay) #자기자신 공격 안됨
    attack(ax, ay, vx, vy)
    if remain == 1:
        break
    repair()


ans = 0
for i in range(N):
    for j in range(M):
        ans = max(ans, board[i][j])
print(ans)