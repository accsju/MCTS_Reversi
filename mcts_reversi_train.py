import json
import copy
import math

import time
from tqdm import tqdm
#class

from mcts_reversi_method import Reversi_method

json_file_name = "mcts_reversi_01.json"
for_train = 1000

def read_json_mcts_reversi_data(json_file_name):
    def init_mcts_json():
        wrap = []
        for i in range(0,60):
            trun = []
            wrap.append(trun)
        data = { "mcts-tree" : wrap,
                 "number of trainings" : 0 
        }
        return data
    try:
        with open(json_file_name, 'r') as file:
            mcts_tree = json.load(file)
        return mcts_tree
    except FileNotFoundError:
        mcts_tree = json.dumps(init_mcts_json())
        with open(json_file_name, 'w') as file:
            file.write(mcts_tree)
        print(f"ファイル '{json_file_name}' が見つかりませんでした。新しくjsonファイルを作成します。")
        return init_mcts_json()
    except json.JSONDecodeError as e:
        print(f"JSON デコードエラーが発生しました: {e}")
        return False
    except Exception as e:
        print(f"予期せぬエラーが発生しました: {e}")
        return False
def save_json_mcts_reversi_data(json_file_name,mcts_tree,number_of_trainings):
    if not mcts_tree or not number_of_trainings:
        print('更新データがありません。')
        return False
    try:
        with open(json_file_name, 'r') as file:
            json_data = json.load(file)
            json_data['mcts-tree'] = mcts_tree
            json_data['number of trainings'] += number_of_trainings        
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
def mcts_train(for_train, json_file_name):
    #jsonファイルの読み込みとデータの取得
    json_data = read_json_mcts_reversi_data(json_file_name)
    mcts_tree = json_data["mcts-tree"]
    number_of_trainings = json_data["number of trainings"]                           
    if not mcts_tree:
        return print(f"jsonファイル'{json_file_name}'の読込みに失敗しました。プログラムを停止します。")
    for train in tqdm(range(for_train)):
        board_setting = Reversi_method.initialize_reversi_board()
        while Reversi_method.is_game_end(board_setting):#対局が終わるまで モンテカルロアタック!!
            inference(board_setting, mcts_tree)
        result = Reversi_method.is_winner(copy.deepcopy(board_setting["board-status"]))
        back_propagation(board_setting, mcts_tree, result)
        # print(f'対局数:{train+1}')
    
    save_json_mcts_reversi_data(json_file_name, mcts_tree, train+1)
def inference(board_setting, mcts_tree):
    if board_setting["player"] == 1:
        records = mcts_tree[board_setting["trun"]]
        #着手可能な手を探して配列で取得
        allowed_moves = Reversi_method.next_moves_search(board_setting)
        #着手可能な手から推論して最善手を探す
        # print(allowed_moves)
        choice_value = get_choice_values(records, allowed_moves, board_setting["black-parent-node"])
        optimal_move = optimal_move_selection(choice_value)
        # print(optimal_move)
        #最適手を選択した後のログの取得処理 log conf [x,y,trun]
        board_setting["black-log"].append([optimal_move[0], optimal_move[1], board_setting["trun"]])
        #手番などを切り替える
        board_setting["board-status"] = optimal_move[3]
        board_setting["player"] = 2
        board_setting["black-parent-node"] = optimal_move[4]
        board_setting["trun"] += 1
        return 
    if board_setting["player"] == 2:
        records = mcts_tree[board_setting["trun"]]
        #着手可能な手を探して配列で取得
        allowed_moves = Reversi_method.next_moves_search(board_setting)
        #着手可能な手から推論して最善手を探す
        choice_value = get_choice_values(records, allowed_moves, board_setting["white-parent-node"])
        optimal_move = optimal_move_selection(choice_value)
        #最適手を選択した後のログの取得処理       
        board_setting["white-log"].append([optimal_move[0], optimal_move[1], board_setting["trun"]])
        #手番などを切り替える
        board_setting["board-status"] = optimal_move[3]
        board_setting["player"] = 1
        board_setting["white-parent-node"] = optimal_move[4]
        board_setting["trun"] += 1       
    # C = math.sqrt(2)
    # value = expect / visit + math.sqrt(2) * math.sqrt(math.log(parent_visit)/visit)
def get_choice_values(records, allowed_moves, parent_node):
    choices = []
    # choices = [x, y, expect, next-board-status, visit]
    for i in range(len(allowed_moves)):
        for j in range(len(records)):
            if allowed_moves[i][0] == records[j][0] and allowed_moves[i][1] == records[j][1] and allowed_moves[i][3] == records[j][2]:
                value = records[j][4] / records[j][3] + math.sqrt(2) * math.sqrt(math.log(parent_node)/records[j][3])
                choices.append([allowed_moves[i][0], allowed_moves[i][1], value, allowed_moves[i][2], records[j][3]])
                break
        else:
            choices.append([allowed_moves[i][0], allowed_moves[i][1], "infinity", allowed_moves[i][2], 1])
    return choices
def optimal_move_selection(choice_value):
    sticky = -1
    sticky_log = "string obj"
    for value in choice_value:
        if value[2] == "infinity":
            return value
        if value[2] > sticky: 
            sticky_log = value
            sticky = value[2]
    else:
        return sticky_log
def back_propagation(board_setting, mcts_tree, result):
    # [x,y,player,visit,expect ,parent-node] records conf
    black_expect = result[1] if result[0] == "black" else 0
    white_expect = result[1] if result[0] == "white" else 0
    if result[0] == "drow":
        black_expect = 0
        white_expect = 0
    for i in range(len(board_setting["black-log"])):
        for j in range(len(mcts_tree[board_setting["black-log"][i][2]])): 
            record = mcts_tree[board_setting["black-log"][i][2]][j] 
            if record[0] == board_setting["black-log"][i][0] and record[1] == board_setting["black-log"][i][1] and record[2] == 1:
                mcts_tree[board_setting["black-log"][i][2]][j][3] += 1 
                mcts_tree[board_setting["black-log"][i][2]][j][4] += black_expect       
                break
        else:
            mcts_tree[board_setting["black-log"][i][2]].append([ 
                board_setting["black-log"][i][0] ,
                board_setting["black-log"][i][1] ,
                1 ,
                1 ,
                black_expect
            ])
    for i in range(len(board_setting["white-log"])):
        for j in range(len(mcts_tree[board_setting["white-log"][i][2]])): 
            record = mcts_tree[board_setting["white-log"][i][2]][j] 
            if record[0] == board_setting["white-log"][i][0] and record[1] == board_setting["white-log"][i][1] and record[2] == 1:
                mcts_tree[board_setting["white-log"][i][2]][j][3] += 1 
                mcts_tree[board_setting["white-log"][i][2]][j][4] += white_expect       
                break
        else:
            mcts_tree[board_setting["white-log"][i][2]].append([ 
                board_setting["white-log"][i][0] ,
                board_setting["white-log"][i][1] ,
                2 ,
                1 ,
                white_expect
            ])
for i in range(100):
    mcts_train(for_train, json_file_name)
    