# coding: utf-8
from flask import Flask
from flask import request, jsonify
from OthelloLogic import getMoves, getReverseboard, execute
from OthelloAction import getAction
from copy import deepcopy

app = Flask(__name__)


@app.route('/')
def index():
    return 'OthelloArenaAPI'


@app.route('/get', methods=['GET'])
def get():
    return "a"


@app.route('/post', methods=['POST'])
def post():
    error_message = "ValidationError"
    # name = request.form['name']
    num = request.form['num']
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

    # ls = list(str(num))
    # ls = [int(i) for i in ls]
    # ans = []
    # for i in range(2):
    #     ans.append([])
    #     for j in range(2):
    #         ans[i].append(ls[2 * i + j])

    if len(ls) != 64:
        return error_message

    board = []
    for i in range(8):
        board.append([])
        for j in range(8):
            board[i].append(ls[i * 8 + j])
    # board[3][3] = -1
    # board[3][4] = 1
    # board[4][3] = 1
    # board[4][4] = -1
    moves = getMoves(board=deepcopy(board), player=-1, size=8)
    action = getAction(board=deepcopy(board), moves=moves)
    board = execute(board=deepcopy(board), action=action, player=-1, size=8)
    data = {
        # 'name': name,
        # 'num': num,
        # 'ls': ls,
        'action': action,
        'board': board
    }
    return jsonify(data)


@app.route('/get_moves', methods=['POST'])
def get_moves():
    error_message = "ValidationError"
    num = request.form['num']
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
    moves = getMoves(board=deepcopy(board), player=1, size=8)
    data = {
        'moves': moves
    }
    return jsonify(data)


if __name__ == '__main__':
    app.run()
