# coding: utf-8

"""
getActionの引数について

board:現在の盤面の状態
moves:現在の合法手の一覧

"""

# strong

import OthelloLogic as Ol
# オセロのロジックに関するライブラリの読み込み
import copy
import time

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
# 盤面の各角周り3マスを格納した二次元リスト
# 序盤～中盤ではこのマスに置かないようにして進めていく（角を取られてしまうため）

list_first = [
    [0, 0],
    [7, 0],
    [7, 7],
    [0, 7]
]
# 盤面の各角を格納した二次元リスト
# 序盤～中盤ではこのマスが取れるときは積極的に取っていく


def getAction(board, moves):
    """
    メインアプリケーションの関数から呼ばれる関数。
    盤面情報と合法手をそれぞれ二次元リストとして引数に渡すことで、
    最善手を返すアルゴリズム。

    :param board: 現在の盤面の状態
    :type board: list of list of int

    :param moves: 現在の合法手の一覧
    :type moves: list of list of int

    :return: 導き出した最善手
    :rtype: list of int
    """

    start_time = time.time()
    turn = 61
    for i in board:
        turn -= i.count(0)
    # 先手はturn:2n+1 後手はturn:2n+2 (n=0,1,2...)

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
    elif turn < 44:
        return middle_main(board, moves, turn, start_time)
    elif turn < 50:
        move = middle_main(board, moves, turn, start_time)
        if move in dangers:
            return max_move(board, moves)
        return move
    else:
        return complete_main(board, moves, turn, start_time)
    # turnによって使用するアルゴリズムを分ける。
    # 1:特になし。
    # 2:「縦取り」と呼ばれる定石。
    # 3:「兎定石」と呼ばれる定石。
    # 4～14:「開放度」という概念を重視したアルゴリズム。序盤に特に有効。
    # 15～47:辺、角を取りやすいように意識したアルゴリズム。
    # 48～:条件付きで深さ優先探索ベースでminMAX法を応用したアルゴリズム。


def complete_main(board, moves, turn, start_time):
    """
    デバッグ用に、今どのアルゴリズムを使用しているかをコンソールに出力するための関数
    """
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
    """
    デバッグ用に、今どのアルゴリズムを使用しているかをコンソールに出力するための関数
    """
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
    """
    デバッグ用に、今どのアルゴリズムを使用しているかをコンソールに出力するための関数
    """
    move, rate = open_rate(board, moves)
    # if type(rate) == str:
    #     print(f"turn: {turn}\n{rate}")
    # else:
    #     print(f"turn: {turn}\nopen_rate: {rate} points")
    # print(f"time: {time.time() - start_time:.2f} sec.")
    # print(f"move: {move}")
    return move


def complete(board, moves, turn, player):
    """
    深さ優先探索ベースでminMAX法を応用したアルゴリズム。
    考え方は、ゲーム理論を参考にしている。
    早ければ計算量O(n^((60-turn)/2))、
    最悪計算量はO(n^(61-turn)/2)。

    :param board: 現在の盤面の状態
    :type board: list of list of int

    :param moves: 現在の合法手の一覧
    :type moves: list of list of int

    :param turn:　現在のターン数
    :type turn: int

    :param player: 再帰中で今自分のターンなのか相手のターンなのかを管理
                   1なら自分、-1なら相手のターン
    :type player: int

    :return: ans_move: 最善手, rate: 勝率
    :rtype: list of int, int

    """

    tmp_board = copy.deepcopy(board)
    # Pythonでは、関数の引数にリストをそのまま渡しても、オブジェクトIDが同一のため、
    # 参照渡しと同じ扱いになってしまう。そのため、DFSで再帰する当関数ではdeepcopyをして盤面情報を更新する。

    if len(moves) == 0:
        player *= -1
        moves = Ol.getMoves(board, player, 8)
        # 打てる手が無い時はplayerを交代する。
    if len(moves) == 0:
        rate = win_rate(board)
        return None, rate
        # 両者とも打てる手が無い時は探索を終了する。

    ans_move = moves[0]

    if turn == 60:
        next_board = Ol.execute(tmp_board, ans_move, player, 8)
        rate = win_rate(next_board)
        return ans_move, rate
        # 最後のターンまで来たらそのまま最善手と勝率を返す。

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
        # ここでDFS、再帰。

        # 2021/01/09追加、ゲーム理論に準じたアルゴリズム
        if player == 1 and next_rate == 1:
            return move, next_rate
            # 自分のターンで、勝率が1ならその時点で返す。
        elif player == -1 and next_rate == 0:
            return None, next_rate
            # 相手のターンで、勝率が0(相手からすると1)ならその時点で返す。

        if w_rate < next_rate:
            w_rate = next_rate
            ans_move = move
        if l_rate > next_rate:
            l_rate = next_rate
        # 勝率がより高い時に返却値を更新

    if player == 1:
        return ans_move, w_rate
    else:
        return None, l_rate


def win_rate(board):
    """
    現時点で自分が勝っているのか負けているのかを返す関数。

    :param board: 現在の盤面の状態
    :type board: list of list of int

    :return: 自分が勝っているなら1、負けているなら0
    :rtype: int
    """

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
    """
    「開放度」という概念を重視したアルゴリズム。序盤に特に有効。

    :param board: 現在の盤面の状態
    :type board: list of list of int

    :param moves: 現在の合法手の一覧
    :type moves: list of list of int

    :return: 導き出した最善手
    :rtype: list of int
    """

    del_ls = []
    for i in range(4):
        if board[list_first[i][0]][list_first[i][1]] == 1:
            del_ls.append(i)
    for i in del_ls:
        for j in range(i * 3, (i * 3) + 3):
            list_first.append(dangers[j])
    del_ls.sort(reverse=True)
    for i in del_ls:
        del dangers[(i * 3):((i * 3) + 3)]
    # 角周り三つは、各角がそれぞれ自分が取っていたならば、その角周りは安全なので優先的に取っていく。

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
        if move in dangers:
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
        # 全ての合法手が危険な手だった場合、最も危険度が低い手を返すために別の関数へ。
    else:
        return ans_move, ans_rate


def open_rate_exception(board, moves):
    """
    open_rateにおいて、全ての合法手が危険な手だった場合に呼ばれる。
    最も危険度が低い手を返す。
    """

    message = "open_rate_exception: success!"

    danger = [
        [1, 1],
        [1, 6],
        [6, 1],
        [6, 6]
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
    """
    辺、角を取りやすいように意識したアルゴリズム。

    :param board: 現在の盤面の状態
    :type board: list of list of int

    :param moves: 現在の合法手の一覧
    :type moves: list of list of int

    :return: 導き出した最善手
    :rtype: list of int
    """

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
    # 上下左右それぞれの辺のリストと、それらを管理するリスト。

    del_ls = []
    for i in range(4):
        if board[list_first[i][0]][list_first[i][1]] == 1:
            del_ls.append(i)
    for i in del_ls:
        for j in range(i * 3, (i * 3) + 3):
            list_first.append(dangers[j])
    del_ls.sort(reverse=True)
    for i in del_ls:
        del dangers[(i * 3):((i * 3) + 3)]
    # 角周り三つは、各角がそれぞれ自分が取っていたならば、その角周りは安全なので優先的に取っていく。

    for move in moves:
        if move in dangers:
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
    # 良い場所に置けなかった場合、開放度を意識したアルゴリズムへ変更。


def for_middle_check(board, ls):
    """
    middle_checkで盤面の辺の状況を把握するための関数
    """
    ans = 0
    for i in ls:
        ans += board[i[1]][i[0]]
    return ans


def turn2(board):
    """
    2ターン目の時限定で「縦取り」と呼ばれる定石を置く関数。
    """
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
    """
    3ターン目の時限定で「兎定石」と呼ばれる定石を置く関数。
    """
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
    """
    考えられる手の中で一番多くの石が取れる手を返す。
    """
    ans_move = moves[0]
    max_score = get_score(Ol.execute(board=copy.deepcopy(board), action=moves[0], player=1, size=8))
    for move in moves:
        score = get_score(Ol.execute(board=copy.deepcopy(board), action=move, player=1, size=8))
        if max_score < score:
            max_score = score
            ans_move = move
    return ans_move


def get_score(board):
    """
    現在の盤面での自分の石の数を返す。
    """
    score = 0
    for i in board:
        score += i.count(1)
    return score
