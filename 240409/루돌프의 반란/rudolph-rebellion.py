N, M, P, C, D = map(int, input().split()) #게임판 크기, 게임턴, 산타수, 루돌프힘, 산타힘
rr, rc = map(int, input().split())
remain = P
santas = [[False, -1, [-1, -1], 0] for _ in range(P + 1)] #탈락, 기절, 좌표, 점수
santas[0][0] = True
board = [[0 for _ in range(N + 1)] for _ in range(N + 1)]
rdx, rdy = (-1, -1, -1, 0, 0, 1, 1, 1), (-1, 0, 1, -1, 1, -1, 0, 1)
sdx, sdy = (-1, 0, 1, 0), (0, 1, 0, -1)
for _ in range(P):
    num, sx, sy = map(int, input().split())
    santas[num][2] = [sx, sy]
    board[sx][sy] = num

def debug():
    for i in range(1, N + 1):
        for j in range(1, N + 1):
            print(board[i][j], end=" ")
        print()
    print()

def find_dist(r1, c1, r2, c2):
    return (r1 - r2)**2 + (c1 - c2)**2

def r_chain_move(sx, sy, s_num, d):
    global remain
    if 1 <= sx <= N and 1 <= sy <= N:
        if board[sx][sy]: #새로 이동할 위치에 산타가 있다면
            new = board[sx][sy]
            nsx, nsy = sx + rdx[d], sy + rdy[d] #다음 칸 탐색
            r_chain_move(nsx, nsy, new, d)
        board[sx][sy] = s_num
        santas[s_num][2] = [sx, sy]
    else:
        santas[s_num][0] = True
        remain -= 1

    return

def s_chain_move(sx, sy, s_num, d):
    global remain
    # 밀려난 산타
    # 밀려난 산타가 갈 곳
    if 1 <= sx <= N and 1 <= sy <= N:
        if board[sx][sy]:
            new = board[sx][sy]
            nsx, nsy = sx + sdx[d], sy + sdy[d]
            s_chain_move(nsx, nsy, new, d)
        board[sx][sy] = s_num
        santas[s_num][2] = [sx, sy]
    else:
        santas[s_num][0] = True
        remain -= 1
    return
def ru_move():
    global rr, rc, remain
    board[rr][rc] = 0
    min_dist = 1e9
    candidates = []

    for i in range(1, P + 1): #돌진할 산타 선택
        if santas[i][0]: #만약 탈락이면 다음 산타
            continue
        sx, sy = santas[i][2]
        dist = find_dist(rr, rc, sx, sy)
        if dist < min_dist:
            min_dist = dist
            candidates = [[sx, sy]]

        elif dist == min_dist:
            candidates.append([sx, sy])

    candidates.sort(key=lambda x:[-x[0], -x[1]])

    #선택된 산타
    sx, sy = candidates[0]

    min_dist = 1e9
    nd = -1
    for d in range(8):
        nrr, nrc = rdx[d] + rr, rdy[d] + rc
        if 1 <= nrr <= N and 1 <= nrc <= N:
            dist = find_dist(nrr, nrc, sx, sy)
            if dist < min_dist:
                min_dist = dist
                nd = d

    #루돌프 최종 위치
    nrr, nrc = rdx[nd] + rr, rdy[nd] + rc

    if board[nrr][nrc]: #산타가 있다면
        s_num = board[nrr][nrc]
        santas[s_num][1] = m + 1
        santas[s_num][3] += C
        board[nrr][nrc] = 0

        nsx, nsy = rdx[nd]*C + nrr, rdy[nd]*C + nrc #날라간 산타 위치
        if 1 <= nsx <= N and 1 <= nsy <= N:
            if board[nsx][nsy]: #날라갔는데 또 산타가 있다면
                new = board[nsx][nsy] #임시저장
                nnsx, nnsy = nsx + rdx[nd], nsy + rdy[nd]
                r_chain_move(nnsx, nnsy, new, nd)

            santas[s_num][2] = [nsx, nsy]
            board[nsx][nsy] = s_num

        else: #범위 밖이면 탈락
            santas[s_num][0] = True
            remain -= 1

    rr, rc = nrr, nrc
    board[rr][rc] = -1
    return

def santa_move():
    global remain
    for i in range(1, P + 1):
        if santas[i][0] or santas[i][1] >= m: #탈락이거나 기절이라면
            continue

        #산타 돌진 방향 구하기
        sx, sy = santas[i][2]
        candidates = []
        ini_dist = find_dist(rr, rc, sx, sy)
        min_dist = ini_dist
        for d in range(4):
            nsx, nsy = sx + sdx[d], sy + sdy[d]
            if 1 <= nsx <= N and 1 <= nsy <= N and board[nsx][nsy] <= 0:
                dist = find_dist(rr, rc, nsx, nsy)
                if dist < min_dist:
                    min_dist = dist
                    candidates = [(nsx, nsy, d)]
                elif dist == min_dist and dist != ini_dist:
                    candidates.append((nsx, nsy, d))

        if not candidates: #갈곳이 없으면 넘어가기
            continue
        candidates.sort(key=lambda x:[x[2]]) #상우하좌 순 = d가 작은 순
        nsx, nsy, nd = candidates[0] #산타가 이동할 곳

        nd = (nd + 2) % 4
        if board[nsx][nsy] == -1: #루돌프 있다면
            nsx, nsy = nsx + sdx[nd]*D, nsy + sdy[nd]*D
            santas[i][3] += D #점수 획득
            santas[i][1] = m + 1
            santas[i][2] = [nsx, nsy]

            if 1 <= nsx <= N and 1 <= nsy <= N:
                if board[nsx][nsy]:
                    new = board[nsx][nsy]
                    nnsx, nnsy = nsx + sdx[nd], nsy + sdy[nd]
                    s_chain_move(nnsx, nnsy, new, nd)
                board[nsx][nsy] = i

            else: #범위 밖이면 out
                santas[i][0] = True
                remain -= 1

        else:#아무도 없다면
            board[nsx][nsy] = i
            santas[i][2] = [nsx, nsy]
        board[sx][sy] = 0 #기존 자리 제거

    return

for m in range(M):
    ru_move()
    santa_move()
    if remain == 0:
        break

    for i in range(1, P + 1): #탈락 안했다면 점수 추가
        if santas[i][0]:
            continue
        santas[i][3] += 1

for i in range(1, P + 1):
    print(santas[i][3], end=" ")