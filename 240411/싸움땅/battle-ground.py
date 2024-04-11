#플레이어 이동.
'''
이동 방향에 벽 있으면 반대로 한칸
'''
'''
    1. 이동 방향에 플레이어 없는 경우
        총이 있으면 획득.
        내가 총이 있으면 공격력이 더 쌘 총 획득 후 내 총을 내려놓음
'''

'''
    2. 이동 방향에 플레이어 있는 경우
        결투 : 초기능력치 + 총의 공격력이 큰 놈이 이김.
                합 같으면 초기 능력치가 높은 놈이 이김.
        
        승자 : 승자의 전투력 (초기 능력치 + 총 공격력) - (패자의 전투력)을 포인트로 얻음
            해당칸에 있는 총과 내 총중 공격력이 높은 총을 획득 후 나머지 총을 내려놓음
        
        패자 : 본인이 가지고 있는 총을 격자에 내려놓고 원래 방향으로 이동. 
                이동 후 총이 있으면 공격력이 높은 총을 획득 후 나머지 총들은 해당 격자에 내려놓음.
                
            이동칸에 다른 플레이어 있거나 범위 밖이면 90도씩 우회전 후 빈칸으로 이동.
                          
'''
#각 총의 정보들 : n*n 격자에 heap을 넣어서 구현 부호 신경 잘 쓰기.
# 사람의 정보. : 새로운 사람 위치 격자와, 사람의 위치와 점수를 기록하는 점수를 가진 리스트 작성.
#좌표 입력 신경 잘 쓰기
import heapq

def move(i):
    [x, y], d, s_ability, g_ability = players[i]
    board[x][y] = 0 #이 좌표에 나밖에 없다는 것이 확실해야 됨.
    # 처음 플레이어가 갈 좌표
    nx, ny = dx[d] + x, dy[d] + y
    if not (0 <= nx < N and 0 <= ny < N): #범위 밖이면 방향 반대로
        nd = (d + 2) % 4
        players[i][1] = nd
        nx, ny = dx[nd] + x, dy[nd] + y

    #있든 없든 좌표 업데이트 함. board에서는 아직 안나타남.
    players[i][0] = [nx, ny]

    #플레이어가 없을 경우
    if board[nx][ny] == 0:
        board[nx][ny] = i #이동
        #총 있는지 확인.
        if guns[nx][ny]: #총이 바닥에 있다면
            max_gun = -heapq.heappop(guns[nx][ny]) #부호확인

            if max_gun > g_ability: #player 가 주우면
                players[i][3] = max_gun #양수

                if g_ability > 0: #player 손에 총이 있다면
                    heapq.heappush(guns[nx][ny], -g_ability)

            else: #플레이어가 줍지 않으면
                heapq.heappush(guns[nx][ny], -max_gun) #다시 집어넣기

    #플레이어가 있을 경우 결투
    else:
        wait_player = board[nx][ny]
        board[nx][ny] = 0 #해당 자리 비워 놓기
        [_, _], _, w_sa, w_ga = players[wait_player]
        if w_sa + w_ga > s_ability + g_ability: #
            winner = wait_player
            losser = i

        elif w_sa + w_ga < s_ability + g_ability:
            winner = i
            losser = wait_player

        else:
            if w_sa > s_ability:
                winner = wait_player
                losser = i
            else:
                winner = i
                losser = wait_player

        #승자는 전투력 차이만큼 점수 획득
        scores[winner] += (players[winner][2] + players[winner][3]) - (players[losser][2] + players[losser][3])
        wx, wy = players[winner][0]
        board[wx][wy] = winner #승자위치

        #패자는 본인 총 내려놓고 원래 방향대로 이동.
        [lx, ly], ld, ls, lg = players[losser]
        if lg > 0:
            heapq.heappush(guns[lx][ly], -lg)
        players[losser][3] = 0

        #이때 이동하려는 칸에 다른 사람있거나 범위 밖이면 오른쪽으로 90도씩 회전하면서 이동.
        for add_d in range(4):
            nlx, nly = dx[(ld + add_d) % 4] + lx, dy[(ld + add_d) % 4] + ly
            if 0 <= nlx < N and 0 <= nly < N and board[nlx][nly] == 0:
                board[nlx][nly] = losser #패자 위치
                players[losser][0] = [nlx, nly]
                players[losser][1] = (ld + add_d) % 4
                break

        #해당칸에 총이 있다면 공격력 가장 강한 총 획득 후, 나머지 내려놓음.
        if guns[nlx][nly]:
            max_gun = -heapq.heappop(guns[nlx][nly])
            players[losser][3] = max_gun

        #승자는 총 고르기
        if guns[wx][wy]:
            max_gun = -heapq.heappop(guns[wx][wy])
            if max_gun > players[winner][3]:
                if players[winner][3] > 0:
                    heapq.heappush(guns[wx][wy], -players[winner][3])
                players[winner][3] = max_gun

#초기 설정 및 입력 부분
dx, dy = (-1, 0, 1, 0), (0, 1, 0, -1)
N, M, K = map(int, input().split()) #크기, 플레이어 수, 라운드
board = [list(map(int, input().split())) for _ in range(N)]
guns = [[[] for _ in range(N)] for _ in range(N)] #heap임
for i in range(N):
    for j in range(N):
        if board[i][j]:
            guns[i][j].append(-board[i][j])

board = [[0 for _ in range(N)] for _ in range(N)] #사람 위치
players = [[[1e9, 1e9], 1e9, 1e9, 1e9]] #0번은 없고, 순서대로 [좌표], 방향, 캐릭능력치, 총 능력치
scores = [0 for _ in range(M + 1)]
for i in range(1, M + 1):
    x, y, d, s = map(int, input().split())
    x, y = x - 1, y - 1
    board[x][y] = i
    players.append([[x, y], d, s, 0])

#실제로 동작
for k in range(K):
    for i in range(1, M + 1):
        move(i) #한명씩 순차적으로 이동.

#정답 출력
ans = ""
for i in range(1, M + 1):
    ans += str(scores[i]) + " "
print(ans[:-1])