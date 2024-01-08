
# Connect Four AI Game

This project implements the classic game Connect Four with an AI opponent using the Minimax algorithm. The AI's decision-making is enhanced with Alpha-Beta pruning for efficient performance.

## Features

- Two-player game mode: Play against an AI opponent.
- AI uses the Minimax algorithm with Alpha-Beta pruning for optimized decision-making.
- The game board and player moves are managed through a user-friendly console interface.

## Requirements

- Python 3.12.1
- NumPy library for handling the game board as a 2D array.

## Setup

The game is set up using a Conda environment. Ensure you have Conda installed on your system, and then create a new environment:

```bash
conda create --name connect-four python=3.12.1
conda activate connect-four
```

Install the required packages:

```bash
conda install numpy
```

## Running the Game

To run the game, use the following command in your Conda environment:

```bash
python main.py
```

Follow the on-screen instructions to play the game against the AI.

## How to Play

- The game is played on a 7x6 grid.
- Players take turns dropping tokens into one of the seven columns.
- The first player to align four tokens vertically, horizontally, or diagonally wins the game.
- The AI opponent evaluates the board state and makes strategic moves using the Minimax algorithm.

## License

This project is open-source and available under the [MIT License](https://opensource.org/licenses/MIT).
