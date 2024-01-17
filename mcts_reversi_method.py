import copy
class Reversi_method:
    @staticmethod
    def initialize_reversi_board():
        board_status = [
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,2,1,0,0,0],
            [0,0,0,1,2,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
        ]
        board_setting = {
            "player": 1, 
            "log": [],
            "turn": 0,
            "board-status": board_status,
            "black-parent-node": 1,
            "white-parent-node": 1
        }
        return copy.deepcopy(board_setting)
    @staticmethod
    def is_winner(board_status): 
        black = 0
        white = 0
        for i in range(8):
            for j in range(8):
                if board_status[i][j] == 1:
                    black += 1
                    continue
                if board_status[i][j] == 2:
                    white += 1
        if black == white:
            return "drow"
        if black > white:
            return "black"
        if black < white:
            return "white" 
    @staticmethod
    def is_available_place(x, y, board_setting):
        board_status = board_setting["board-status"] 
        deep_copy_board_status = copy.deepcopy(board_setting["board-status"])
        trun = 1 if board_setting["player"] == 1 else 2
        anti_turn = 2 if board_setting["player"] == 1 else 1
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
    @staticmethod
    def is_move(board_setting):
        board_status = board_setting["board-status"]
        allowed_moves = []
        for i in range(8): 
            for j in range(8):
                if board_status[i][j] != 0:
                    continue
                result = Reversi_method.is_available_place(j, i, board_setting)
                if result["inversion-disk-count"]:
                    allowed_moves.append(1)
        if len(allowed_moves) == 0:
            return  False 
        return True 
    @staticmethod 
    def is_game_end(board_setting):
        board_status = board_setting["board-status"]      
        black = 0
        white = 0
        for i in range(8):
            for j in range(8):
                if board_status[i][j] == 1:
                    black += 1
                if board_status[i][j] == 2:
                    white += 1
        # print(f"black: {black} | white: {white}")
        if black == 0 or white == 0:
           return False
        if Reversi_method.is_move(board_setting):
            return True
        if board_setting["player"] == 1:
            board_setting["player"] = 2
        elif board_setting["player"] == 2:
            board_setting["player"] = 1 
        if Reversi_method.is_move(board_setting):
            return True
        return False
    @staticmethod
    def next_moves_search(board_setting):
        board_status = board_setting["board-status"] 
        allowed_moves = []
        for i in range(8):
            for j in range(8):              
                if board_status[i][j] != 0:
                    continue
                result = Reversi_method.is_available_place(j, i, board_setting)
                if result["inversion-disk-count"]:
                    allowed_moves.append(
                        {"next-board-status": result["next-board-status"]}
                    )
        return allowed_moves
