def move_runners():
    new = [[[] for _ in range(N)] for _ in range(N)]
    for i in range(1, M + 1):
        live, x, y, d = runners[i]
        if not live: #죽으면 넘어가
            continue

        if abs(x - cx) + abs(y - cy) > 3: #술래와 거리가 4이상이면 안도망.
            new[x][y].append(i)
            continue

        nx, ny = dx[d] + x, dy[d] + y
        if 0 <= nx < N and 0 <= ny < N: #움직였는데 격자 안.
            if (nx, ny) != (cx, cy): #술래가 없으면 움직
                runners[i][1], runners[i][2] = nx, ny
            else:
                nx, ny = x, y #있으면 재자리

        else: #격자 벗어나면
            nd = (d + 2) % 4
            runners[i][3] = nd #일단 방향바꿈
            nx, ny = dx[nd] + x, dy[nd] + y
            if (nx, ny) != (cx, cy): #이동시 술래 없으면 이동
                runners[i][1], runners[i][2] = nx, ny

            else:
                nx, ny = x, y #술래 있으면 재자리

        new[nx][ny].append(i) #도망자의 최종 이동.

    return new

def mk_chase():
    sx = sy = (N - 1) // 2
    cx, cy = sx, sy
    cd = 0

    dist = 1
    moves = []
    make_right, make_reverse = False, False
    while not make_right:
        for _ in range(2): # 두번마다 거리 늘어남.
            for _ in range(dist): #거리 다 가면 방향 바꿈
                cx, cy = dx[cd] + cx, dy[cd] + cy
                moves.append([cx, cy, cd])
                if (cx, cy) == (0, 0):
                    cd = 2
                    moves[-1][2] = cd
                    make_right = True
                    break

            if make_right:
                break
            #거리 다 이동했으면 보는 방향 보정해줌.
            cd = (cd + 1) % 4
            moves[-1][2] = cd
        dist += 1

    dist -= 2
    for _ in range(dist):  # 거리 다 가면 방향 바꿈
        cx, cy = dx[cd] + cx, dy[cd] + cy
        moves.append([cx, cy, cd])
    moves[-1][2] = 1
    cd = 1

    while not make_reverse:
        for _ in range(2): # 두번마다 거리 줄어듬.
            for _ in range(dist): #거리 다 가면 방향 바꿈
                cx, cy = dx[cd] + cx, dy[cd] + cy
                moves.append([cx, cy, cd])
                if (cx, cy) == (sx, sy):
                    cd = 0
                    moves[-1][2] = cd
                    make_reverse = True
                    break

            if make_reverse:
                break
            #거리 다 이동했으면 보는 방향 보정해줌.
            cd = (cd + 3) % 4
            moves[-1][2] = cd
        dist -= 1

    return moves

N, M, H, K = map(int, input().split())
runners = [[False, 1e9, 1e9, 1e9]] #runner 0은 더미데이터. #live, x, y, d
dx, dy = (-1, 0, 1, 0), (0, 1, 0, -1) # 상 우 하 좌
trees = [[False for _ in range(N)] for _ in range(N)]
board = [[[] for _ in range(N)] for _ in range(N)] #도망자 정보. 여러명이 같은 자리에 있을 수 도 있다는 점.
for m in range(1, M + 1): #도망자 입력. 좌우로는 항상 오른쪽 보고 시작, 상하로는 항상 아래쪽 보고 시작.
    x, y, d = map(int, input().split()) # d가 1이면 우, d가 2면 하
    x, y = x - 1, y - 1
    runners.append([True, x, y, d])
    board[x][y].append(m)

for _ in range(H): #나무 입력
    x, y = map(int, input().split())
    x, y = x - 1, y - 1
    trees[x][y] = True

#술래 이동부터 구현.
c_move = mk_chase() #술래의 좌표, 보는 방향이 담겨있음.
len_c_move = N*N*2 - 2 #모든 좌표개수 *2 - (0, 0), (sx, sy) 만약 N >= 5 일때
score = 0
cx, cy = N // 2, N // 2

for k in range(K):
    board = move_runners()
    #2. 술래 움직임. 이동 직후 시야 내에 있는 도망자 잡음.
    # 술래 시야는 바라보고 있는 시야 기준 본인 위치 포함 항상 3칸임
    cx, cy, cd = c_move[k % len_c_move]
    cat_this_turn = 0#이번턴에 잡은 도둑 수.
    for length in range(3): #범위 3 만큼 잡아버려
        cat_x, cat_y = dx[cd]*length + cx, dy[cd]*length + cy
        if 0 <= cat_x < N and 0 <= cat_y < N and not trees[cat_x][cat_y]:
            for catched in board[cat_x][cat_y]:
                runners[catched][0] = False
                cat_this_turn += 1

    score += cat_this_turn * (k + 1)
print(score)

#테케를 다 맞춰도 항상 틀릴 수 있다는 것을 명심해.
#코드 작성 후 문제 한번 더 읽기. -> 빠진 기능이나 놓친 조건 확인. 한번에 모든것을 실수없이 구현할 수 없음
#함수 단위, 기능 단위 로 잘 동작하는지 확인, 테스트 케이스 확인.

# 확인해야될 함수 및 기능 목록.
#mk_chase() 통과 완료, move_runners(), 도둑 잡기.