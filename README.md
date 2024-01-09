# Connect Four AI Game

This project implements the classic game Connect Four with two distinct components: a terminal-based game interface and a Flask-based backend for AI opponent logic.

## Features

- Two-player game mode: Play against an AI opponent.
- AI uses the Minimax algorithm with Alpha-Beta pruning for optimized decision-making
- The game board and player moves are managed through a user-friendly terminal interface.
- Real-time interaction with the AI opponent through the Flask server.

## Requirements

- Python 3.12.1
- Conda
- Flask
- NumPy library for handling the game board as a 2D array.

## Conda Environment Setup

To set up the game environment using the provided `environment.yml` file in the repository, follow these steps:

1. **Create the Conda Environment**:
   Use the `environment.yml` file to create a Conda environment. This file contains all the necessary package dependencies for the game.

   ```bash
   conda env create -f environment.yml
   ```

2. **Activate the Environment**:
   Once the environment is created, activate it using:

   ```bash
   conda activate connect-four
   ```

## Running the Flask Server

The Flask server handles the AI logic for the game. To run it, follow these steps:

1. **Set Flask App Environment Variable**:
   In the terminal, navigate to the project directory and set the `FLASK_APP` environment variable to point to your Flask application file.

   On Linux or macOS:

   ```bash
   export FLASK_APP=backend/run.py
   ```

   On Windows (cmd):

   ```cmd
   set FLASK_APP=backend\run.py
   ```

   On Windows (PowerShell):

   ```powershell
   $env:FLASK_APP = "backend\run.py"
   ```

2. **Run the Flask Server**:
   Start the server with the following command:

   ```bash
   flask run
   ```

   This will start the server on `http://127.0.0.1:5000/`.

## Playing the Terminal-Based Game

To play the terminal-based version of Connect Four, run:

```bash
python main.py
```

This will start the game interface in your terminal.

## How to Play

- The game is played on a 7x6 grid.
- Players take turns dropping tokens into one of the seven columns.
- The first player to align four tokens vertically, horizontally, or diagonally wins the game.
- The AI opponent evaluates the board state and makes strategic moves using the Minimax algorithm.

## License

This project is open-source and available under the [MIT License](https://opensource.org/licenses/MIT).
