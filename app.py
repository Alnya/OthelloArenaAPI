# coding: utf-8
from flask import Flask
from flask import request, jsonify
from flask_cors import CORS, cross_origin
from OthelloLogic import getMoves, execute, getReverseboard
from OthelloAction import getAction
from copy import deepcopy

app = Flask(__name__)
CORS(app, support_credentials=True)


def posted_board(num):
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
    return "a"


@app.route('/post', methods=['POST'])
@cross_origin(support_credentials=True)
def post():
    board = posted_board(request.form['num'])
    if isinstance(board, str):
        return board
    moves = getMoves(board=deepcopy(board), player=-1, size=8)
    if len(moves) == 0:
        data = {
            'action': [],
            'board': board
        }
        return data
    # action = getAction(board=deepcopy(board), moves=moves)
    action = getAction(board=getReverseboard(deepcopy(board)), moves=moves)
    board = execute(board=deepcopy(board), action=action, player=-1, size=8)
    data = {
        'action': action,
        'board': board
    }
    return jsonify(data)


@app.route('/get_moves', methods=['POST'])
@cross_origin(support_credentials=True)
def get_moves():
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
