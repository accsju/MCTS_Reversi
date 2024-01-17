# standerd library
import json
import copy
import math 
import time
import random

# pip library
from tqdm import tqdm 
# originay library
from mcts_reversi_method import Reversi_method

#json_file_name = "mcts_reversi_base.json"
#for_train = 1000 

class MCTS_reversi_train:
    @staticmethod
    def read_json_mcts_reversi_data(json_file_name):
        def init_mcts_json():
            wrap = []
            for i in range(0,60):
                trun = []
                wrap.append(trun)
            data = { "mcts-tree" : wrap,
                     "play-number": 0
            }
            return data
        try:
            with open(json_file_name, 'r') as f:
                mcts_tree = json.load(f)
            return mcts_tree
        except FileNotFoundError:
            mcts_tree = json.dumps(init_mcts_json())
            with open(json_file_name, 'w') as f:
                f.write(mcts_tree)
            print(f"ファイル '{json_file_name}' が見つかりませんでした。新しくjsonファイルを作成します。")
            return init_mcts_json()
        except json.JSONDecodeError as e:
            print(f"JSON デコードエラーが発生しました: {e}")
            return False
        except Exception as e:
            print(f"予期せぬエラーが発生しました: {e}")
            return False
    @staticmethod 
    def save_json_mcts_reversi_data(json_file_name, mcts_tree, play_number):
        if not mcts_tree or not play_number:
            print('更新データがありません。')
            return False
        try:
            with open(json_file_name, 'r') as file:
                json_data = json.load(file)
                json_data['mcts-tree'] = mcts_tree
                log_play_number = json_data['play-number']
                log_play_number += play_number
                json_data['play-number'] = log_play_number
            with open(json_file_name, 'w') as file:
                json.dump(json_data, file)
            print(f"ファイル'{json_file_name}'の更新を完了しました。")
            return True
        except FileExistsError:
            print(f"ファイル'{json_file_name}'が見つかりませんでした。")
            return False
        except json.JSONDecodeError as e:
            print(f"JSON デコードエラーが発生しました: {e}")
            return False
        except Exception as e:
            print(f"予期せぬエラーが発生しました: {e}")
            return False 
    @staticmethod
    def train_setting():
        json_file_name = input("jsonファイルを指定してください: ")
        if not json_file_name.lower().endswith('.json'):
            return print('拡張子が.jsonではありません')
        train_of_number = input("訓練対局数を指定してください: ")
        if not type(int(train_of_number)) is int:
            return print("整数値ではありません。")
        if not int(train_of_number) > 0:
            return print("適切な整数値を入力してください。")
        train_of_number = int(train_of_number)
        return copy.deepcopy({"json-file-name": json_file_name,"train-of-number": train_of_number})
    @staticmethod
    def is_match_board(board_status,record_board_status):
        for i in range(8):
            for j in range(8):
                if board_status[i][j] != record_board_status[i][j]:
                    return False
        return True
    @staticmethod
    def inference(board_setting, mcts_tree):
        records = mcts_tree[board_setting["turn"]-1]
        allowed_moves = Reversi_method.next_moves_search(board_setting)
        optimal_move = MCTS_reversi_train.get_optimal_move(records, allowed_moves, board_setting)
        MCTS_reversi_train.update_phase(optimal_move, board_setting)
    @staticmethod
    def get_optimal_move(records, allowed_moves, board_setting):
        choices = []
        parent_visit = 0
        if board_setting["player"] == 1:
            parent_visit = board_setting["black-parent-node"]
        elif board_setting["player"] == 2:
            parent_visit = board_setting["white-parent-node"] 
        for i in range(len(allowed_moves)):
            for j in range(len(records)):
                if MCTS_reversi_train.is_match_board(allowed_moves[i]["next-board-status"], records[j]["board-status"]) and board_setting["player"] == records[j]["player"]:
                    value = records[j]["win"] / records[j]["visit"] + math.sqrt(2) * math.sqrt(math.log(parent_visit)/records[j]["visit"])
                    choices.append({"value": value, "next-board-status": allowed_moves[i]["next-board-status"], "visit": records[j]["visit"]})
            else:
                choices.append({"value": "infinity", "next-board-status": allowed_moves[i]["next-board-status"], "visit": 0})
        a = -1
        a_log = "a"
        infinity_choice = []
        if len(choices) == 0:
            return 
        for value in choices:
            if value["value"] == "infinity":
                infinity_choice.append(value)
            if not isinstance(value["value"], str):
                if value["value"] > a:
                    a = value["value"]
                    a_log = value
        if len(infinity_choice) != 0:
            return infinity_choice[random.randint(0, len(infinity_choice) - 1)]
        return a_log
    @staticmethod
    def update_phase(optimal_move, board_setting):
        board_setting["board-status"] = optimal_move["next-board-status"]           
        if board_setting["player"] == 1:
            board_setting["player"] = 2
            board_setting["black-parent-node"] = optimal_move["visit"] if optimal_move["visit"] else 1
            board_setting["turn"] += 1
        elif board_setting["player"] == 2:
            board_setting["player"] = 1
            board_setting["white-parent-node"] = optimal_move["visit"] if optimal_move["visit"] else 1
            board_setting["turn"] += 1
        board_setting["log"].append({"board-status": optimal_move["next-board-status"],"player": board_setting["player"]})
    @staticmethod
    def mcts_reversi_back_propagation(winner, board_setting, mcts_tree):
        black_expect = 1 if winner == "black" else 0
        white_expect = 1 if winner == "white" else 0
        if winner == "drow":
            black_expect = 0.5
            white_expect = 0.5 
        for i in range(len(board_setting["log"])):
            for j in range(len(mcts_tree[i])):
                record = mcts_tree[i][j]
                if MCTS_reversi_train.is_match_board(board_setting["log"][i]["board-status"], record["board-status"]) and board_setting["log"][i]["player"] == record["player"]:
                    mcts_tree[i][j]["visit"] += 1
                    if board_setting["log"][i]["player"] == 1:
                        mcts_tree[i][j]["win"] += black_expect
                    elif board_setting["log"][i]["player"] == 2:
                        mcts_tree[i][j]["win"] += white_expect
                    break
            else:
                win = 0
                if board_setting["log"][i]["player"] == 1:
                    win += black_expect
                elif board_setting["log"][i]["player"] == 2:
                    win += white_expect
                mcts_tree[i].append(
                    {
                        "win": win,
                        "visit" : 1,
                        "board-status" : board_setting["log"][i]["board-status"],
                        "player": board_setting["log"][i]["player"]
                    }      
                )
def main():
    setting_data = MCTS_reversi_train.train_setting()
    json_data = MCTS_reversi_train.read_json_mcts_reversi_data(setting_data["json-file-name"])
    mcts_tree = json_data["mcts-tree"] if json_data["mcts-tree"] else print("json data [mcts-tree]の取得に失敗しました。")
    # print(f"モンテカルロツリー: {mcts_tree}")
    # print(f"モンテカルロツリー[0]: {mcts_tree[0]}")
    for play in tqdm(range(setting_data["train-of-number"])):
        board_setting = Reversi_method.initialize_reversi_board()
        while Reversi_method.is_game_end(board_setting):
            MCTS_reversi_train.inference(board_setting, mcts_tree)
        winner = Reversi_method.is_winner(board_setting["board-status"])
        MCTS_reversi_train.mcts_reversi_back_propagation(winner, board_setting, mcts_tree)
    MCTS_reversi_train.save_json_mcts_reversi_data(setting_data["json-file-name"], mcts_tree, setting_data["train-of-number"])
main()

def get_all_record_number(json_file_name): #jsonファイルで各手番、ターンのレコード数を出力する関数を作成せよ。
    try:
        with open(json_file_name, 'r') as f:
            mcts_tree = json.load(f)
    except Exception as e:
        print(f'エラー: {e}')
        return 
    record_number = []
    for i in range(len(mcts_tree["mcts-tree"])):
        record_number.append(len(mcts_tree["mcts-tree"][i]))
    print(f"record_number: {record_number}")
get_all_record_number("test.json")