# coding: utf-8

from flask import Flask
from flask import request, jsonify
from flask_cors import CORS, cross_origin
from OthelloLogic import getMoves, execute, getReverseboard
from OthelloAction import getAction
import OthelloActionWeak
import OthelloActionMiddle
from copy import deepcopy

app = Flask(__name__)
CORS(app, support_credentials=True)


def posted_board(num):
    """
    フロントエンドから送られてきた盤面を整形する。

    :param num: 盤面情報の数列
    :type num: str
    :return: 盤面情報を二次元リストに整形したもの
    :rtype: list of list of int
    """
    error_message = "ValidationError"
    ls = []
    str_num = str(num)
    frag = False
    for i in range(len(str_num)):
        if frag:
            ls.append(-1)
            frag = False
            continue
        if str_num[i] == "-":
            frag = True
        else:
            ls.append(int(str_num[i]))
    if len(ls) != 64:
        return error_message
    board = []
    for i in range(8):
        board.append([])
        for j in range(8):
            board[i].append(ls[i * 8 + j])
    return board


@app.route('/')
@cross_origin(support_credentials=True)
def index():
    return 'OthelloArenaAPI'


@app.route('/get', methods=['GET'])
@cross_origin(support_credentials=True)
def get():
    """
    Herokuを起動させるための軽量通信用エンドポイント。
    """
    return "a"


@app.route('/post', methods=['POST'])
@cross_origin(support_credentials=True)
def post():
    """
    現在の盤面を受け取り、対戦相手(Alnya's OthelloAction)の手と、
    打った後の盤面を返すエンドポイント。

    :return: 対戦相手の手と打った後の盤面のjsonデータ
    """
    board = posted_board(request.form['num'])
    if isinstance(board, str):
        return board
    moves = getMoves(board=getReverseboard(deepcopy(board)), player=1, size=8)
    if len(moves) == 0:
        data = {
            'action': [],
            'board': board
        }
        return jsonify(data)
    action = getAction(board=getReverseboard(deepcopy(board)), moves=moves)
    board = execute(board=deepcopy(board), action=action, player=-1, size=8)
    data = {
        'action': action,
        'board': board
    }
    return jsonify(data)


@app.route('/post_weak', methods=['POST'])
@cross_origin(support_credentials=True)
def post():
    """
    現在の盤面を受け取り、対戦相手(Alnya's OthelloActionWeak)の手と、
    打った後の盤面を返すエンドポイント。

    :return: 対戦相手の手と打った後の盤面のjsonデータ
    """
    board = posted_board(request.form['num'])
    if isinstance(board, str):
        return board
    moves = getMoves(board=getReverseboard(deepcopy(board)), player=1, size=8)
    if len(moves) == 0:
        data = {
            'action': [],
            'board': board
        }
        return jsonify(data)
    action = OthelloActionWeak.getAction(board=getReverseboard(deepcopy(board)), moves=moves)
    board = execute(board=deepcopy(board), action=action, player=-1, size=8)
    data = {
        'action': action,
        'board': board
    }
    return jsonify(data)


@app.route('/post_middle', methods=['POST'])
@cross_origin(support_credentials=True)
def post():
    """
    現在の盤面を受け取り、対戦相手(Alnya's OthelloAction)の手と、
    打った後の盤面を返すエンドポイント。

    :return: 対戦相手の手と打った後の盤面のjsonデータ
    """
    board = posted_board(request.form['num'])
    if isinstance(board, str):
        return board
    moves = getMoves(board=getReverseboard(deepcopy(board)), player=1, size=8)
    if len(moves) == 0:
        data = {
            'action': [],
            'board': board
        }
        return jsonify(data)
    action = OthelloActionMiddle.getAction(board=getReverseboard(deepcopy(board)), moves=moves)
    board = execute(board=deepcopy(board), action=action, player=-1, size=8)
    data = {
        'action': action,
        'board': board
    }
    return jsonify(data)


@app.route('/get_moves', methods=['POST'])
@cross_origin(support_credentials=True)
def get_moves():
    """
    現在の盤面を受け取り、プレイヤーの合法手を返すエンドポイント。

    :return: 現在の盤面でのプレイヤーの合法手のjsonデータ
    """
    board = posted_board(request.form['num'])
    if isinstance(board, str):
        return board
    moves = getMoves(board=deepcopy(board), player=1, size=8)
    data = {
        'moves': moves
    }
    return jsonify(data)


@app.route('/player_execute', methods=['POST'])
@cross_origin(support_credentials=True)
def player_execute():
    """
    現在の盤面とプレイヤーの手を受け取り、実行した後の盤面を返すエンドポイント。

    :return: 実行後の盤面のjsonデータ
    """
    board = posted_board(request.form['num'])
    if isinstance(board, str):
        return board
    action = int(request.form['action'])
    action = [action % 8, action // 8]
    board = execute(board=deepcopy(board), action=action, player=1, size=8)
    data = {
        'board': board
    }
    return jsonify(data)


@app.route('/check', methods=['POST'])
@cross_origin(support_credentials=True)
def check():
    """
    デバッグ用エンドポイント。
    """
    board = posted_board(request.form['num'])
    if isinstance(board, str):
        return board
    player_moves = getMoves(board=deepcopy(board), player=1, size=8)
    alnya_moves = getMoves(board=deepcopy(board), player=-1, size=8)
    if len(player_moves) == 0 and len(alnya_moves) == 0:
        return 0
    else:
        return 1


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
    # app.run(debug=True)
