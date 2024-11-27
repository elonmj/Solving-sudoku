# Sudoku

[![python version](https://img.shields.io/badge/python-3.12-blue)](https://www.python.org/)

[![license](https://img.shields.io/badge/license-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A simple [Sudoku](https://en.wikipedia.org/wiki/Sudoku) game written in Python using the [`pygame`](https://www.pygame.org) library.


# Features
- Randomly generated Sudoku boards
- Randomly pruned cells
- Check for valid moves
- Check for game completion
- Timer
- Reset the board
- Solve the board using Constraint Satisfaction Problem (CSP) with OR-TOOLS
- Highlight the selected cell
- Highlight the same numbers in the same row, column, and box

## Installation
1. Install the required dependencies:  
`pip install -r requirements.txt`
2. Run the game:  
`python main.py`

## Settings

You can change the number of randomly-pruned cells in the Sudoku board in the [`prune`](sudoku/logic/board.py) method in `board.py`.
