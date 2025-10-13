"""
#!/usr/bin/python3
Author      : Mahbub Alam
File        : AI_plays_TicTacToe.py
Created     : 2025-09
Description : TicTacToe game with AI using magic square and minimax algorithm # {{{

This code demonstrates how a simple **AI agent** can play Tic Tac Toe against a human using the **minimax algorithm**.

We'll use a *magic square representation* of the 3×3 board to quickly check for winning combinations.

Let's start by defining the core constants and helper functions.

# }}}
"""

from itertools import combinations
from time import sleep

magic = [8, 3, 4, 1, 5, 9, 6, 7, 2]
magic_ = {
    8 : 0,
    3 : 1,
    4 : 2,
    1 : 3,
    5 : 4,
    9 : 5,
    6 : 6,
    7 : 7,
    2 : 8
}

score_dict = {
    "X" : 1,
    "O" : -1
}

def print_board(board):
    print("|".join(board[0:3]))
    print("|".join(board[3:6]))
    print("|".join(board[6:9]))

    return None

def check_player_win(board, player):
    player_moves_ = [i for i in range(9) if board[i] == player]
    avail_magic = [magic[i] for i in avail_moves(board)]

    for tuple_ in combinations(player_moves_, 2):
        surp = 15 - (magic[tuple_[0]] + magic[tuple_[1]])
        if surp in avail_magic:
            return magic_[surp], score_dict[player]

    return None

def avail_moves(board):
    return [i for i in range(9) if board[i] == "_"]

def minimax(board, player, opp):
    res = check_player_win(board, player)
    if res is not None:
        return res

    avail_moves_ = avail_moves(board)
    if not avail_moves_:
        return None, 0

    scores = []
    for i in avail_moves_:
        new_board = board.copy()
        new_board[i] = player
        _, score_ = minimax(new_board, opp, player)
        scores.append((i, score_))

    scores.sort(key=lambda x: x[1])
    return scores[-1] if player == "X" else scores[0]

def main():
    board = ["_" for _ in range(9)]

    # ===============[[ Output title like this ]]===============
    print(f"")
    print(68*"=")
    print(f"==={14*'='}[[ Welcome to AI plays TicTacToe ]]{14*'='}==\n")
    # ==========================================================

    print_board(board)
    print(f"")

    print("AI will play 'X', you play 'O'.")
    if input("Do you want to play first? [Y/n] ") == 'n':
        player, opp = "X", "O"
    else:
        player, opp = "O", "X"

    while True:
        if player == "X":
            print("\nThis is AI's turn.\n")
            sleep(0.5)
            res_x = check_player_win(board, "X")
            res_o = check_player_win(board, "O")
            if res_x is not None:
                move_index = res_x[0]
                # print(f"Above board score: {res_x[1]}\n")
                board[move_index] = "X"
                print_board(board)
                print("\nAI wins!")
                break
            elif res_o is not None:
                move_index = res_o[0]
                # print(f"Above board score: {res_o[1]}\n")
            else:
                move_index, score_ = minimax(board, "X", "O")
                # print(f"Above board score: {- score_}\n")

            board[move_index] = "X"
        else:
            print("\nThis is your turn.\n")
            while True:
                input_ = input(f"Make moves as (x, y)-coordinates (0, 1, 2): ")
                x, y = map(int, tuple(input_.replace(' ', '').replace(',', '')))
                move_index = 3*x + y
                if board[move_index] != "_":
                    print("That spot is already taken! Try again.\n")
                else:
                    break

            board[move_index] = "O"
            print(f"")

        print_board(board)
        player, opp = opp, player

        if not avail_moves(board):
            print(f"It's a draw!")
            break

        if len(avail_moves(board)) == 1:
            if player == "O":
                print(f"\nIt will be a draw after your move!\n")
                board[avail_moves(board)[0]] = "O"
                print_board(board)
                break


if __name__ == "__main__":
    main()
