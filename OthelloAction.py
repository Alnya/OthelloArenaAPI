"""
引数について

board:現在の盤面の状態
moves:現在の合法手の一覧

詳しい説明はサイトのHomeページをご覧ください。

"""

# strong

import OthelloLogic as Ol
import copy
import time


def getAction(board, moves):
    start_time = time.time()
    turn = 61
    for i in board:
        turn -= i.count(0)
    # 先手turn:1 後手turn:2

    dangers = [
        [1, 0],
        [1, 1],
        [0, 1],

        [1, 7],
        [0, 6],
        [1, 6],

        [7, 6],
        [6, 6],
        [6, 7],

        [6, 0],
        [7, 1],
        [6, 1]
    ]

    # print("--------------------------------------------------")
    # print(f"turn: {turn}")

    if 48 <= turn <= 49:
        if len(moves) < 2:
            return complete_main(board, moves, turn, start_time)
    if turn == 2:
        t2 = turn2(board)
        if t2 is not None and t2 in moves:
            # print(f"縦取り成功!\\(^_^)/")
            return t2
    if turn == 3:
        t3 = turn3(board)
        if t3 is not None and t3 in moves:
            # print(f"兎定石だ!\\('o')/")
            return t3
    if turn < 15:
        return open_rate_main(board, moves, turn, start_time)
    # elif turn < 50:
    #     return middle_main(board, moves, turn, start_time)
    elif 44 <= turn < 50:
        move = middle_main(board, moves, turn, start_time)
        if move in dangers:
            return max_move(board, moves)
        return move
    else:
        return complete_main(board, moves, turn, start_time)


def complete_main(board, moves, turn, start_time):
    move, rate = complete(board, moves, turn, 1)
    if rate == 0:
        # print(f"theory_rate: 0.00 %\nSo, I changed the algorithm.")
        return middle_main(board, moves, turn, start_time)
    else:
        # print(f"turn: {turn}\ntheory_rate: {rate * 100:.2f} %")
        # print(f"time: {time.time() - start_time:.2f} sec.")
        # print(f"move: {move}")
        # print(f"len(moves): {len(moves)}")
        return move


def middle_main(board, moves, turn, start_time):
    move, message = middle_check(board, moves)
    # if message == "middle_check!":
    #     print(f"turn: {turn}\nmiddle_check: {message}")
    # elif type(message) == str:
    #     print(f"turn: {turn}\n{message}")
    # else:
    #     print(f"turn: {turn}\nopen_rate: {message} points")
    # print(f"time: {time.time() - start_time:.2f} sec.")
    # print(f"move: {move}")
    # print(f"len(moves): {len(moves)}")
    return move


def open_rate_main(board, moves, turn, start_time):
    move, rate = open_rate(board, moves)
    # if type(rate) == str:
    #     print(f"turn: {turn}\n{rate}")
    # else:
    #     print(f"turn: {turn}\nopen_rate: {rate} points")
    # print(f"time: {time.time() - start_time:.2f} sec.")
    # print(f"move: {move}")
    return move


def complete(board, moves, turn, player):
    tmp_board = copy.deepcopy(board)
    if len(moves) == 0:
        player *= -1
        moves = Ol.getMoves(board, player, 8)
    if len(moves) == 0:
        rate = win_rate(board)
        return None, rate

    ans_move = moves[0]

    if turn == 60:
        next_board = Ol.execute(tmp_board, ans_move, player, 8)
        rate = win_rate(next_board)
        return ans_move, rate

    w_rate = 0
    l_rate = 1
    for move in moves:
        # tmp_board = copy.deepcopy(board)
        # copy.deepcopyよりforで回した方が早い?
        for h in range(8):
            for w in range(8):
                tmp_board[h][w] = board[h][w]
        next_board = Ol.execute(tmp_board, move, player, 8)
        next_moves = Ol.getMoves(next_board, player * -1, 8)
        next_move, next_rate = complete(next_board, next_moves, turn + 1, player * -1)

        # 2021/01/09追加
        if player == 1 and next_rate == 1:
            return move, next_rate
        elif player == -1 and next_rate == 0:
            return None, next_rate

        if w_rate < next_rate:
            w_rate = next_rate
            ans_move = move
        if l_rate > next_rate:
            l_rate = next_rate

    if player == 1:
        return ans_move, w_rate
    else:
        return None, l_rate


def win_rate(board):
    my_stone = 0
    enemy_stone = 0
    for i in board:
        my_stone += i.count(1)
        enemy_stone += i.count(-1)
    if my_stone > enemy_stone:
        return 1
    else:
        return 0


def open_rate(board, moves):
    danger = [
        [1, 0],
        [1, 1],
        [0, 1],

        [1, 7],
        [0, 6],
        [1, 6],

        [7, 6],
        [6, 6],
        [6, 7],

        [6, 0],
        [7, 1],
        [6, 1]
    ]

    list_first = [
        [0, 0],
        [7, 0],
        [7, 7],
        [0, 7]
    ]

    del_ls = []
    for i in range(4):
        if board[list_first[i][0]][list_first[i][1]] == 1:
            del_ls.append(i)
    for i in del_ls:
        for j in range(i * 3, (i * 3) + 3):
            list_first.append(danger[j])
    del_ls.sort(reverse=True)
    for i in del_ls:
        del danger[(i * 3):((i * 3) + 3)]

    vectors = [
        [-1, -1],
        [0, -1],
        [1, -1],
        [-1, 0],
        [1, 0],
        [-1, 1],
        [0, 1],
        [1, 1]
    ]

    ans_move = moves[0]
    ans_rate = 100

    for move in moves:
        if move in danger:
            continue
        elif move in list_first:
            return move, "great!"
        rate = 0
        zero_board = [[0 for _ in range(8)] for _ in range(8)]
        tmp_board = copy.deepcopy(board)
        next_board = Ol.execute(tmp_board, move, player=1, size=8)
        for h in range(8):
            for w in range(8):
                if board[h][w] == -1 and next_board[h][w] == 1:
                    for vec in vectors:
                        moved_index = [int(h + vec[0]), int(w + vec[1])]
                        if 0 <= moved_index[0] <= 7 and 0 <= moved_index[1] <= 7:
                            zero_board[moved_index[0]][moved_index[1]] = 1
        for h in range(8):
            for w in range(8):
                if board[h][w] == 0 and zero_board[h][w] == 1:
                    rate += 1
        if rate < ans_rate:
            ans_rate = rate
            ans_move = move

    if ans_rate == 100:
        return open_rate_exception(board, moves)
    else:
        return ans_move, ans_rate


def open_rate_exception(board, moves):
    message = "open_rate_exception: success!"

    danger = [
        [1, 1],
        [1, 6],
        [6, 1],
        [6, 6]
    ]

    list_first = [
        [0, 0],
        [7, 0],
        [7, 7],
        [0, 7]
    ]

    ans_move = moves[0]
    success_frag = 0
    for move in moves:
        if move in danger:
            continue
        tmp_board = copy.deepcopy(board)
        next_board = Ol.execute(tmp_board, move, player=1, size=8)
        next_moves = Ol.getMoves(next_board, player=-1, size=8)
        next_frag = 0
        for next_move in next_moves:
            if next_move in list_first:
                next_frag = 1
        if next_frag == 1:
            continue
        ans_move = move
        success_frag = 1
    if success_frag == 0:
        message = "open_rate_exception: failure..."
    return ans_move, message


def middle_check(board, moves):
    left_ls = [
        [0, 0],
        [0, 1],
        [0, 2],
        [0, 3],
        [0, 4],
        [0, 5],
        [0, 6],
        [0, 7],
    ]

    right_ls = [
        [7, 0],
        [7, 1],
        [7, 2],
        [7, 3],
        [7, 4],
        [7, 5],
        [7, 6],
        [7, 7],
    ]

    up_ls = [
        [0, 0],
        [1, 0],
        [2, 0],
        [3, 0],
        [4, 0],
        [5, 0],
        [6, 0],
        [7, 0],
    ]

    down_ls = [
        [0, 7],
        [1, 7],
        [2, 7],
        [3, 7],
        [4, 7],
        [5, 7],
        [6, 7],
        [7, 7],
    ]

    ls_manager = [up_ls, down_ls, left_ls, right_ls]

    danger = [
        [1, 0],
        [1, 1],
        [0, 1],

        [1, 7],
        [0, 6],
        [1, 6],

        [7, 6],
        [6, 6],
        [6, 7],

        [6, 0],
        [7, 1],
        [6, 1]
    ]

    list_first = [
        [0, 0],
        [7, 0],
        [7, 7],
        [0, 7]
    ]

    del_ls = []
    for i in range(4):
        if board[list_first[i][0]][list_first[i][1]] == 1:
            del_ls.append(i)
    for i in del_ls:
        for j in range(i * 3, (i * 3) + 3):
            list_first.append(danger[j])
    del_ls.sort(reverse=True)
    for i in del_ls:
        del danger[(i * 3):((i * 3) + 3)]

    for move in moves:
        if move in danger:
            continue
        elif move in list_first:
            return move, "middle_check!"
        for ls in ls_manager:
            if move in ls:
                tmp_board = copy.deepcopy(board)
                before_execute = for_middle_check(board, ls)
                next_board = Ol.execute(tmp_board, move, player=1, size=8)
                after_execute = for_middle_check(next_board, ls)
                next_moves = Ol.getMoves(next_board, player=-1, size=8)
                if before_execute + 1 < after_execute:
                    frag = 0
                    for next_move in next_moves:
                        if next_move in ls:
                            frag = 1
                    if frag == 1:
                        continue
                    else:
                        return move, "middle_check!"
                elif before_execute + 1 == after_execute:
                    enemy_stone = 0
                    for i in ls:
                        if board[i[1]][i[0]] == -1:
                            enemy_stone += 1
                    if enemy_stone == 0:
                        return move, "middle_check!"

    return open_rate(board, moves)


def for_middle_check(board, ls):
    ans = 0
    for i in ls:
        ans += board[i[1]][i[0]]
    return ans


def turn2(board):
    t2b = [
        [4, 5],
        [5, 4],
        [3, 2],
        [2, 3]
    ]

    t2l = [
        [3, 5],
        [5, 3],
        [4, 2],
        [2, 4]
    ]

    for i in range(len(t2b)):
        if board[t2b[i][0]][t2b[i][1]] != 0:
            return t2l[i]
    return None


def turn3(board):
    t3b = [
        [4, 5],
        [5, 4],
        [3, 2],
        [2, 3]
    ]

    t3l = [
        [2, 4],
        [4, 2],
        [5, 3],
        [3, 5]
    ]

    for i in range(len(t3b)):
        if board[t3b[i][0]][t3b[i][1]] != 0:
            return t3l[i]
    return None


def max_move(board, moves):
    ans_move = moves[0]
    max_score = get_score(Ol.execute(board=copy.deepcopy(board), action=moves[0], player=1, size=8))
    for move in moves:
        score = get_score(Ol.execute(board=copy.deepcopy(board), action=move, player=1, size=8))
        if max_score < score:
            max_score = score
            ans_move = move
    return ans_move


def get_score(board):
    score = 0
    for i in board:
        score += i.count(1)
    return score
