import copy
import math
import json
#盤面データを渡すと盤面データから最適な手を出力する関数

def call_goddess_of_justice(justice_power, board_status, player): #call goddess of justice !!
    empty = 0
    for i in range(8):
        for j in range(8):
            if board_status[j][i] == 0:
                empty += 1
    turn = 60 - empty # turn
    def call_akashic_records(turn, justice_power):
        try: 
            with open(justice_power, 'r') as f:
                justice = json.load(f)
            return justice
        except Exception as e:
            print('Summoning failure')
    print(turn, justice_power)
    akashic_records = call_akashic_records(turn, justice_power)['mcts-tree'][turn]

    allowed_moves = []
    for i in range(8):
        for j in range(8):              
            if board_status[i][j] != 0:
                continue
            result = is_flash(j, i, board_status, player)
            if result["inversion-disk-count"]:
                allowed_moves.append(
                    [j, i]
                )
    if len(allowed_moves) == 0:
        print('not place.')
        return 
    choices = []
    for i in range(len(allowed_moves)):
        for j in range(len(akashic_records)):
            if allowed_moves[i][0] == akashic_records[j][0] and allowed_moves[i][1] == akashic_records[j][1]:
                value = akashic_records[j][4] / akashic_records[j][3] 
                choices.append([allowed_moves[i][0], allowed_moves[i][1], value])
        else:
            choices.append([allowed_moves[i][0], allowed_moves[i][1], "infinity"])
    max_value = -1
    max_index = 0
    for i in range(len(choices)):
        if choices[i][2] == "infinity":
            print(f"x座標: {choices[i][0]}, y座標: {choices[i][1]}")
            return
            # return [choices[i][0], choices[i][1]]
        if choices[i][2] > max_value :
            max_value = choices[i][2]
            max_index = i 
    else:
        print(f"x座標: {choices[max_index][0]}, y座標: {choices[max_index][1]}")
        # return best

def is_flash(x, y, board_status, player):
        deep_copy_board_status = copy.deepcopy(board_status)
        trun = 1 if player == 1 else 2
        anti_turn = 2 if player == 1 else 1
        count = 0
        c = 0
        arr = []
        loop = min(x, y)  # top left
        for i in range(loop):
            if board_status[y - i - 1][x - i - 1] == 0:
                break
            if board_status[y - i - 1][x - i - 1] == anti_turn:
                c += 1
            if board_status[y - i - 1][x - i - 1] == trun and c != 0:
                for j in range(c):
                    deep_copy_board_status[y - j - 1][x - j - 1] = trun
                    count += 1
                break
            if board_status[y - i - 1][x - i - 1] == trun and c == 0:
                break
        c = 0
        loop = min(x, 7 - y)  # bottom left
        for i in range(loop):
            if board_status[y + i + 1][x - i - 1] == 0:
                break
            if board_status[y + i + 1][x - i - 1] == anti_turn:
                c += 1
            if board_status[y + i + 1][x - i - 1] == trun and c != 0:
                for j in range(c):
                    deep_copy_board_status[y + j + 1][x - j - 1] = trun
                    count += 1
                break
            if board_status[y + i + 1][x - i - 1] == trun and c == 0:
                break
        c = 0
        loop = min(7 - x, y)  # top right
        for i in range(loop):
            if board_status[y - i - 1][x + i + 1] == 0:
                break
            if board_status[y - i - 1][x + i + 1] == anti_turn:
                c += 1
            if board_status[y - i - 1][x + i + 1] == trun and c != 0:
                for j in range(c):
                    deep_copy_board_status[y - j - 1][x + j + 1] = trun
                    count += 1
                break
            if board_status[y - i - 1][x + i + 1] == trun and c == 0:
                break
        c = 0
        loop = min(7 - x, 7 - y)  # bottom right
        for i in range(loop):
            if board_status[y + i + 1][x + i + 1] == 0:
                break
            if board_status[y + i + 1][x + i + 1] == anti_turn:
                c += 1
            if board_status[y + i + 1][x + i + 1] == trun and c != 0:
                for j in range(c):
                    deep_copy_board_status[y + j + 1][x + j + 1] = trun
                    count += 1
                break
            if board_status[y + i + 1][x + i + 1] == trun and c == 0:
                break
        c = 0
        for i in range(x + 1, 8):  # right
            if board_status[y][i] == 0:
                break
            if board_status[y][i] == anti_turn:
                c += 1
            if board_status[y][i] == trun and c != 0:
                for j in range(x + 1, i):
                    deep_copy_board_status[y][j] = trun
                    count += 1
                break
            if board_status[y][i] == trun and c == 0:
                break
        c = 0
        for i in range(x - 1, -1, -1):  # left
            if board_status[y][i] == 0:
                break
            if board_status[y][i] == anti_turn:
                c += 1
            if board_status[y][i] == trun and c != 0:
                for j in range(i + 1, x):
                    deep_copy_board_status[y][j] = trun
                    count += 1
                break
            if board_status[y][i] == trun and c == 0:
                break
        c = 0
        for i in range(y - 1, -1, -1):  # top
            if board_status[i][x] == 0:
                break
            if board_status[i][x] == anti_turn:
                c += 1
            if board_status[i][x] == trun and c != 0:
                for j in range(i + 1, y):
                    deep_copy_board_status[j][x] = trun
                    count += 1
                break
            if board_status[i][x] == trun and c == 0:
                break
        c = 0
        for i in range(y + 1, 8):  # bottom
            if board_status[i][x] == 0:
                break
            if board_status[i][x] == anti_turn:
                c += 1
            if board_status[i][x] == trun and c != 0:
                for j in range(y + 1, i):
                    deep_copy_board_status[j][x] = trun
                    count += 1
                break
            if board_status[i][x] == trun and c == 0:
                break
        if count:
            deep_copy_board_status[y][x] = trun
        return {
            "inversion-disk-count": count,
            "next-board-status": deep_copy_board_status
        }

player = 1
board_status = [
    [2,2,2,2,2,2,2,2],
    [2,1,1,1,1,2,2,2],
    [2,2,2,2,2,2,2,2],
    [2,1,2,2,2,2,2,2],
    [2,2,1,2,2,2,2,2],
    [2,1,2,2,1,2,2,2],
    [2,2,1,1,1,1,2,2],
    [2,2,1,2,2,2,2,2],
]
call_goddess_of_justice("mcts_reversi_01.json", board_status, player)
