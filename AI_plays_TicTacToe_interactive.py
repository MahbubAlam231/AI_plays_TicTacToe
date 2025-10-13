"""
#!/usr/bin/python3
Author      : Mahbub Alam
File        : AI_plays_TicTacToe_interactive.py
Created     : 2025-09
Description : Interactive TicTacToe game with AI using magic square and minimax algorithm # {{{

This notebook demonstrates how a simple **AI agent** can play TicTacToe against a human using the **minimax algorithm**.

We'll use a *magic square representation* of the 3×3 board to quickly check for winning combinations.

AI will always play "X" and human "O".

# }}}
"""

from itertools import combinations
from IPython.display import display, clear_output
import ipywidgets as widgets
from time import sleep

# ===========[[ Magic Square Representation ]]==========={{{
print(f"")
print(68*"=")
print(f"==={15*'='}[[ Magic Square Representation ]]{15*'='}==\n")
# ==========================================================

"""# {{{

The classic 3×3 magic square:
<table style="border-collapse: collapse; margin: 20px auto; font-size: 18px; text-align: center;">
  <tr>
    <td style="border: 2px solid #333; width: 30px; height: 30px; background-color: #f0f0f0; color: black;"><b>8</b></td>
    <td style="border: 2px solid #333; width: 30px; height: 30px; background-color: #f0f0f0; color: black;"><b>3</b></td>
    <td style="border: 2px solid #333; width: 30px; height: 30px; background-color: #f0f0f0; color: black;"><b>4</b></td>
  </tr>
  <tr>
    <td style="border: 2px solid #333; width: 30px; height: 30px; background-color: #f0f0f0; color: black;"><b>1</b></td>
    <td style="border: 2px solid #333; width: 30px; height: 30px; background-color: #f0f0f0; color: black;"><b>5</b></td>
    <td style="border: 2px solid #333; width: 30px; height: 30px; background-color: #f0f0f0; color: black;"><b>9</b></td>
  </tr>
  <tr>
    <td style="border: 2px solid #333; width: 30px; height: 30px; background-color: #f0f0f0; color: black;"><b>6</b></td>
    <td style="border: 2px solid #333; width: 30px; height: 30px; background-color: #f0f0f0; color: black;"><b>7</b></td>
    <td style="border: 2px solid #333; width: 30px; height: 30px; background-color: #f0f0f0; color: black;"><b>2</b></td>
  </tr>
</table>
ensures that any winning line in TicTacToe (row, column, diagonal) sums to 15.

This allows us to check wins using simple arithmetic instead of explicit board patterns.
Each cell maps to its magic square value, enabling efficient win detection.

Let's start by defining the core constants.

"""# }}}

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

# }}}

# =============[[ Board Display Functions ]]============={{{
print(f"")
print(68*"=")
print(f"==={17*'='}[[ Board Display Functions ]]{17*'='}==\n")
# ==========================================================

"""# {{{

These functions create and update the interactive game board using ipywidgets.
The board uses border styling to create the classic # grid pattern.

"""# }}}

def make_board_display(board, click_handler):
    """Create a 3×3 grid of buttons for an interactive TicTacToe board."""
    buttons = []
    for i in range(9):
        row, col = i // 3, i % 3

        border_top = "3px solid #333" if row > 0 else "0px"
        border_left = "3px solid #333" if col > 0 else "0px"
        margin_top = "-3px" if row > 0 else "0px"
        margin_left = "-3px" if col > 0 else "0px"

        b = widgets.Button(
            description=board[i] if board[i] != "_" else " ",
            layout=widgets.Layout(
                width="72px",
                height="72px",
                border_top=border_top,
                border_left=border_left,
                margin=f"{margin_top} 0px 0px {margin_left}",
                padding="0px"
            ),
            style=widgets.ButtonStyle(button_color="#ffffff"),
            disabled=False,
            tooltip=""
        )
        b.index = i
        b.on_click(click_handler)
        buttons.append(b)
    grid = widgets.GridBox(
        buttons,
        layout=widgets.Layout(
            grid_template_columns="repeat(3, 72px)",
            grid_gap="0px",
            justify_content="center"
        )
    )
    return grid, buttons

def update_(buttons, board):
    """Update button colors and text to reflect current board state."""
    for i, cell in enumerate(board):
        if cell == "X":
            buttons[i].description = "❌"
            buttons[i].style.button_color = "#ffe6e6"
        elif cell == "O":
            buttons[i].description = "⭕"
            buttons[i].style.button_color = "#e6f0ff"
        else:
            buttons[i].description = " "
            buttons[i].style.button_color = "#ffffff"

def disable_all(buttons):
    """Disable all buttons on the board."""
    for b in buttons:
        b.disabled = True

# }}}

# ==============[[ Game Logic Functions ]]==============={{{
print(f"")
print(68*"=")
print(f"==={18*'='}[[ Game Logic Functions ]]{18*'='}===\n")
# ==========================================================

"""# {{{

Core game mechanics including win detection and the **minimax AI algorithm**.

A helper dictionary and a function first.

"""# }}}

# AI will always play "X" and human "O"
score_dict = {
    "X" : 1,
    "O" : -1
}

def avail_moves(board):
    """ This function simply returns all empty positions (marked with '_') on the board.  """

    return [i for i in range(9) if board[i] == "_"]

# ===============[[ Output title like this ]]===============
print(f"")
print(68*"=")
print(f"==={17*'='}[[ Check for Winning Moves ]]{17*'='}==\n")
# ==========================================================

"""# docstring{{{

This function uses the magic square logic.
For each pair of the player's existing moves, check if the magic square
values of those positions and of an available position add up to 15 (winning line).

If a winning move exists, it returns:

- the **index** of the winning square, and
- the **score** of the board position.

Returns None if there's no winning moves.

#### Definition:
**Score** of a board position is defined to be +1 if AI has a winning strategy and -1 if human has a winning strategy.

"""# }}}

def check_player_win(board, player):
    player_moves_ = [i for i in range(9) if board[i] == player]
    avail_magic = [magic[i] for i in avail_moves(board)]

    for tuple_ in combinations(player_moves_, 2):
        surp = 15 - (magic[tuple_[0]] + magic[tuple_[1]])
        if surp in avail_magic:
            return magic_[surp], score_dict[player]

    return None

# ===============[[ Output title like this ]]===============
print(f"")
print(68*"=")
print(f"==={18*'='}[[ The Minimax Algorithm ]]{18*'='}==\n")
# ==========================================================

"""# {{{

Minimax algorithm for optimal AI move selection.

Algorithm:
        Recursively explores all possible game states assuming optimal play.
        - X (AI) maximizes the score (+1 for win)
        - O (human) minimizes the score (-1 for win)
        - Returns (move, score): score of a board position and a move that achieves that score
        - Returns (None, 0) for draw

"""# }}}


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

# }}}

# ==============[[ Interactive TicTacToe ]]=============={{{
print(f"")
print(68*"=")
print(f"==={18*'='}[[ Interactive TicTacToe ]]{18*'='}==\n")
# ==========================================================

"""# {{{

Now play the game! Click cells to make your move as ⭕ while the AI plays as <span style="color: #dc3545; font-size: 25px; font-weight: bold;">❌</span>.

The AI uses the minimax algorithm, so it plays optimally - try to get a draw! 🎮

"""# }}}


def play_interactive():
    """Jupyter version of main() from AI_plays_TicTacToe.py"""
    board = ["_"] * 9

    print("")
    print(68 * "=")
    print(f"==={'='*14}[[ Welcome to AI plays TicTacToe ]]{'='*14}==\n")
    print("AI will play 'X', you play 'O'.\n")
    print(f"Run the above cell(s) to start playing.\n")

    first = input("Do you want to play first? [Y/n] ")
    player, opp = ("O", "X") if first != 'n' else ("X", "O")
    print(f"")

    out = widgets.Output()

    def ai_move():
        nonlocal player, opp
        print("\nThis is AI's turn.\n")
        sleep(0.3)
        res_x = check_player_win(board, "X")
        res_o = check_player_win(board, "O")

        if res_x is not None:
            move_index = res_x[0]
            board[move_index] = "X"
            update_(buttons, board)
            with out:
                clear_output(wait=True)
                print("\nAI wins!")
            disable_all(buttons)
            return True
        elif res_o is not None:
            move_index = res_o[0]
        else:
            move_index, _ = minimax(board, "X", "O")

        board[move_index] = "X"
        update_(buttons, board)

        player, opp = opp, player

        # If your turn is the last turn, already decides if there will be no result
        if len(avail_moves(board)) == 1:
            sleep(0.2)
            board[avail_moves(board)[0]] = player
            update_(buttons, board)
            res = check_player_win(board, player)
            if res is not None:
                p_name = "You"
                print(f"{p_name} win!!")
            else:
                with out:
                    clear_output(wait=True)
                    print(f"\nIt will be a draw!")
            disable_all(buttons)
            return True

        # Ends game when AI takes last empty slot
        if not avail_moves(board):
            with out:
                clear_output(wait=True)
                print("\nIt's a draw!")
            disable_all(buttons)
            return True

        return False

    def handle_click(btn):
        nonlocal player, opp
        if player != "O" or board[btn.index] != "_":
            return

        print("\nThis is your turn.\n")
        board[btn.index] = "O"
        update_(buttons, board)

        player, opp = opp, player

        if not avail_moves(board):
            with out:
                clear_output(wait=True)
                print("\nIt's a draw!")
            disable_all(buttons)
            return

        done = ai_move()
        if done:
            return

    # Build interactive board
    grid, buttons = make_board_display(board, handle_click)

    update_(buttons, board)
    display(grid, out)

    # If AI starts
    if player == "X":
        ai_move()

play_interactive()

# }}}
