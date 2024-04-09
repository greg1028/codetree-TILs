#연쇄 이동 만약 마지막 기사가 벽에 닿아있으면 모든 기사 못움직임

#명령 받은 기사는 함정 밟아도 피안까이고, 밀린 기사들은 함정 밟으면 피 까임. 피가 0이하로 떨어지면 사라짐

#Q번 끝나고 생존한 기사들이 받은 대미지의 합을 출력하는게 문제임

def debug(board):
    for i in range(L):
        for j in range(L):
            print(board[i][j], end=" ")
        print()
    print()

def push(i, d):
    global possible
    remove_set = set()
    R, C, h, w, k, _ = new_knights[i]
    for r in range(R, R + h):
        for c in range(C, C + w):
            #기존 위치 다 지워
            new_k_board[r][c] = 0
            nr, nc = r + dx[d], c + dy[d]
            if 0 <= nr < L and 0 <= nc < L and board[nr][nc] != 2:
                if board[nr][nc] == 1: #피달고
                    new_knights[i][4] -= 1
                    new_knights[i][5] += 1
                    if new_knights[i][4] <= 0:
                        remove_set.add(i)

                new = new_k_board[nr][nc]#다른기사 있으면 또 옮겨주고
                if not visited[new]:
                    visited[new] = True
                    push(new, d)

            else:
                possible = False
                return



    new_knights[i][0], new_knights[i][1] = R + dx[d], C + dy[d]

    for i in remove_set:
        remove(i)

    R, C, h, w, k, _ = new_knights[i]
    if k > 0:
        for r in range(R, R + h):
            for c in range(C, C + w):
                new_k_board[r][c] = i
    return

def remove(i):
    R, C, h, w, k, _ = new_knights[i]
    for r in range(R, R + h):
        for c in range(C, C + w):
            new_k_board[r][c] = 0
    return

dx, dy = (-1, 0, 1, 0), (0, 1, 0, -1)
L, N, Q = map(int, input().split()) # N마리 기사, Q번 명령
board = [list(map(int, input().split())) for _ in range(L)] #0빈칸, 1함정, 2벽
k_board = [[0 for _ in range(L)] for _ in range(L)] #기사 위치 정보 확인
knights = [[0, 0, 0, 0, 0, 0]] #r, c, h, w, k, dam (받은 데미지)

for i in range(1, N + 1):
    r, c, h, w, k = map(int, input().split()) #좌측 상단 꼭지점이 위치 (r, c). 기사 높이 넓이, k :체력
    r, c = r - 1, c - 1
    knights.append([r, c, h, w, k, 0])
    for rr in range(r, r + h):
        for cc in range(c, c + w):
            k_board[rr][cc] = i


#print("first k_board")
#debug(k_board)
for q in range(Q):#왕의 명령. 사라진 기사에게 명령은 무시
    #print(q + 1)
    i, d = map(int, input().split()) #i번 기사 d로 한칸 이동
    if knights[i][4] <= 0:
        continue

    f_k, f_d = knights[i][4], knights[i][5]
    knights[i][4] = 10000
    possible, new_k_board, new_knights, damage = True, [row[:] for row in k_board], [knight[:] for knight in knights], 0
    visited = [False for _ in range(N + 1)]
    visited[0] = True
    visited[i] = True
    push(i, d)
    if possible:
        #print("moved")
        k_board = new_k_board
        knights = new_knights
    knights[i][4], knights[i][5] = f_k, f_d

    #print("after order")
    #debug(k_board)

#생존한 기사들 대미지의 합 출력
ans = 0
for _, _, _, _, k, dam in knights:
    if k > 0:
        #print("k, dam",k, dam)
        ans += dam
print(ans)