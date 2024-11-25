# Sudoku

[![python version](https://img.shields.io/badge/python-3.12-blue)](https://www.python.org/)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![license](https://img.shields.io/badge/license-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A simple [Sudoku](https://en.wikipedia.org/wiki/Sudoku) game written in Python using the [`pygame`](https://www.pygame.org) library.

<img src="https://raw.githubusercontent.com/alxdrcirilo/sudoku-python/main/assets/images/sudoku.png" alt="sudoku" width="480">

> [!NOTE]
> If you have `uv` installed, you can just run `uv run main.py` at the root of the project.

## Installation

### Setup Instructions

1. Clone the repository:  
`git clone https://github.com/alxdrcirilo/sudoku-python.git`
2. Create a virtual environment:  
`virtualenv .venv`
3. Activate the virtual environment:  
`source .venv/bin/activate`
4. Install the required dependencies:  
`pip install -r requirements.txt`
5. Run the game:  
`python main.py`

## Settings

You can change the number of randomly-pruned cells in the Sudoku board in the [`prune`](sudoku/logic/board.py) method in `board.py`.

## Credits

### Assets

"Hearts and health bar" [Game asset]. (n.d.). itch.io. Retrieved Nov 26, 2024, from <https://fliflifly.itch.io/hearts-and-health-bar>

### Fonts

This project uses the [Open Sans](https://fonts.google.com/specimen/Open+Sans) font.
