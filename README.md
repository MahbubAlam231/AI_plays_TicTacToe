# AI Plays TicTacToe

## Overview

This project demonstrates an AI agent playing TicTacToe against a human player using a magic square representation and the minimax algorithm. The AI plays optimally, making it impossible to beat—your best outcome is a draw!

---

## Jupyter Notebook

For a full walkthrough with code and interactive play, see the
Jupyter Notebook [AI_plays_TicTacToe_interactive.ipynb](AI_plays_TicTacToe_interactive.ipynb)

---

## Features

- **Interactive GUI**: Click-based gameplay using ipywidgets with a visual grid
- **Magic Square Logic**: Uses a 3×3 magic square for efficient win detection (any winning line sums to 15)
- **Minimax Algorithm**: AI makes optimal moves by exploring all possible game states
- **Visual Feedback**: Color-coded moves (red for AI's ❌, blue for player's ⭕)
- **Flexible Start**: Choose whether you or the AI goes first

## Requirements

```python
ipywidgets
IPython
```

## How to Play

1. Run all cells in the notebook
2. Choose whether to play first (Y/n)
3. Click on empty cells to place your ⭕
4. The AI will respond with its ❌ move
5. Try to achieve a draw—the AI won't let you win!

## Technical Details

### Magic Square Representation
```
8 | 3 | 4
---------
1 | 5 | 9
---------
6 | 7 | 2
```

Each position maps to a magic square value, enabling quick win detection by checking if any three positions sum to 15.

### Game Logic

- **AI (X)**: Maximizes score (+1 for win)
- **Human (O)**: Minimizes score (-1 for win)
- **Draw**: Score of 0

The minimax algorithm recursively evaluates all possible game states to select the optimal move.

## File Structure

- Magic square setup and mapping
- Board display functions with ipywidgets
- Game logic:
    - Win detection, available moves
    - Minimax algorithm implementation
- Interactive gameplay function

## Challenge

Since the AI plays perfectly using minimax, can you force a draw? Good luck! 🎮
