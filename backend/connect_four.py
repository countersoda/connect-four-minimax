import numpy as np
import random
import math

# Constants
PLAYER_TOKEN = 1
AI_TOKEN = 2
ROW_COUNT = 6
COLUMN_COUNT = 7
DEPTH = 5

class ConnectFour:
    def __init__(self, depth=5):
        self.board = np.zeros((ROW_COUNT, COLUMN_COUNT), dtype=int)
        self.game_over = False
        self.turn = 0  # 0 for player, 1 for AI
        self.winner = -1
        self.depth = depth

    def drop_token(self, board, row, col, token):
        board[row][col] = token

    def is_valid_location(self, board, col):
        return board[ROW_COUNT-1][col] == 0
    
    def is_terminal_node(self, board):
        return self.is_winning_move(board, PLAYER_TOKEN) or self.is_winning_move(board, AI_TOKEN) or len(self.get_valid_locations(board)) == 0

    def is_winning_move(self, board, token):
        # Check horizontal locations for win
        for c in range(COLUMN_COUNT - 3):
            for r in range(ROW_COUNT):
                if board[r][c] == token and board[r][c + 1] == token and board[r][c + 2] == token and board[r][c + 3] == token:
                    return True

        # Check vertical locations for win
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT - 3):
                if board[r][c] == token and board[r + 1][c] == token and board[r + 2][c] == token and board[r + 3][c] == token:
                    return True

        # Check positively sloped diagonals
        for c in range(COLUMN_COUNT - 3):
            for r in range(ROW_COUNT - 3):
                if board[r][c] == token and board[r + 1][c + 1] == token and board[r + 2][c + 2] == token and board[r + 3][c + 3] == token:
                    return True

       # Check negatively sloped diagonals
        for c in range(COLUMN_COUNT - 3):
            for r in range(3, ROW_COUNT):
                if board[r][c] == token and board[r - 1][c + 1] == token and board[r - 2][c + 2] == token and board[r - 3][c + 3] == token:
                    return True

        return False

    def get_next_open_row(self, board, col):
        for r in range(ROW_COUNT):
            if board[r][col] == 0:
                return r

    def print_board(self, board):
        for row in np.flip(board, 0):
            print('|', end='')
            for cell in row:
                if cell == PLAYER_TOKEN:
                    print('X', end='|')
                elif cell == AI_TOKEN:
                    print('O', end='|')
                else:
                    print(' ', end='|')
            print()
        print(f"{'-' * (2 * COLUMN_COUNT + 1)}")
        print(' 0 1 2 3 4 5 6')  # Column numbers for reference

    def find_winning_columns(self, board, token):
        winning_columns = []

        # Check horizontal locations for potential win
        for c in range(COLUMN_COUNT - 3):
            for r in range(ROW_COUNT):
                for i in range(4):
                    if board[r][c + i] == 0 and (r == ROW_COUNT - 1 or board[r + 1][c + i] != 0):
                        temp_board = np.copy(board)
                        temp_board[r][c + i] = token
                        if self.is_winning_move(temp_board, token):
                            winning_columns.append(c + i)

        # Check vertical locations for potential win
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT - 3):
                if board[r][c] == 0:
                    temp_board = np.copy(board)
                    temp_board[r][c] = token
                    if self.is_winning_move(temp_board, token):
                        winning_columns.append(c)

        # Check positively sloped diagonals for potential win
        for c in range(COLUMN_COUNT - 3):
            for r in range(ROW_COUNT - 3):
                for i in range(4):
                    if board[r + i][c + i] == 0 and (r + i == ROW_COUNT - 1 or board[r + i + 1][c + i] != 0):
                        temp_board = np.copy(board)
                        temp_board[r + i][c + i] = token
                        if self.is_winning_move(temp_board, token):
                            winning_columns.append(c + i)

        # Check negatively sloped diagonals for potential win
        for c in range(COLUMN_COUNT - 3):
            for r in range(3, ROW_COUNT):
                for i in range(4):
                    if board[r - i][c - i] == 0 and (r - i == ROW_COUNT - 1 or board[r - i + 1][c - i] != 0):
                        temp_board = np.copy(board)
                        temp_board[r - i][c - i] = token
                        if self.is_winning_move(temp_board, token):
                            winning_columns.append(c - i)

        return list(set(winning_columns))  # Return unique columns

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        valid_locations = self.get_valid_locations(board)
        is_terminal = self.is_terminal_node(board)
        
        if depth == 0 or is_terminal:
            if is_terminal:
                if self.is_winning_move(board, AI_TOKEN):
                    return (None, 10000 * depth)  # None for column as it's a terminal state
                elif self.is_winning_move(board, PLAYER_TOKEN):
                    return (None, -10000 * depth)
                else:
                    return (None, 0)  # Game is over, no more valid moves
            else:
                return (None, self.score_position(board, AI_TOKEN))  # Non-terminal, depth reached

        if maximizing_player:
            value = -math.inf
            best_column = None
            for col in valid_locations:
                row = self.get_next_open_row(board, col)
                b_copy = np.copy(board)
                self.drop_token(b_copy, row, col, AI_TOKEN)
                _, new_score = self.minimax(b_copy, depth-1, alpha, beta, False)
                if new_score > value:
                    value = new_score
                    best_column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return (best_column, value)

        else:  # Minimizing player
            value = math.inf
            best_column = None
            for col in valid_locations:
                row = self.get_next_open_row(board, col)
                b_copy = np.copy(board)
                self.drop_token(b_copy, row, col, PLAYER_TOKEN)
                _, new_score = self.minimax(b_copy, depth-1, alpha, beta, True)
                if new_score < value:
                    value = new_score
                    best_column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return (best_column, value)

    def score_position(self, board, token):
        score = 0

        # Score center column
        center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
        center_count = center_array.count(token)
        score += center_count * 2  # Center column is usually more valuable

        # Score Horizontal
        for r in range(ROW_COUNT):
            row_array = [int(i) for i in list(board[r, :])]
            for c in range(COLUMN_COUNT - 3):
                window = row_array[c:c + 4]
                score += self.evaluate_window(window, token)

        # Score Vertical
        for c in range(COLUMN_COUNT):
            col_array = [int(i) for i in list(board[:, c])]
            for r in range(ROW_COUNT - 3):
                window = col_array[r:r + 4]
                score += self.evaluate_window(window, token)

        # Score positive sloped diagonals
        for c in range(COLUMN_COUNT - 3):
            for r in range(ROW_COUNT - 3):
                window = [board[r + i][c + i] for i in range(4)]
                score += self.evaluate_window(window, token)

        # Score negative sloped diagonals
        for c in range(COLUMN_COUNT - 3):
            for r in range(3, ROW_COUNT):
                window = [board[r - i][c + i] for i in range(4)]
                score += self.evaluate_window(window, token)

        return score

    def evaluate_window(self, window, token):
        score = 0
        opp_token = PLAYER_TOKEN if token == AI_TOKEN else AI_TOKEN

        if window.count(token) == 4:
            score += 100
        elif window.count(token) == 3 and window.count(0) == 1:
            score += 5
        elif window.count(token) == 2 and window.count(0) == 2:
            score += 2

        if window.count(opp_token) == 3 and window.count(0) == 1:
            score -= 4

        return score

    def get_valid_locations(self, board):
        valid_locations = []
        for col in range(COLUMN_COUNT):
            if self.is_valid_location(board, col):
                valid_locations.append(col)
        return valid_locations

    def pick_best_move(self, token):
        depth = self.depth     # You can adjust the depth based on how deep you want the search to be
        best_col, _ = self.minimax(self.board, depth, -math.inf, math.inf, token == AI_TOKEN)
        return best_col

    def player_move(self):
        valid_move = False
        while not valid_move:
            try:
                col = int(input("Player 1 (X) Make your Selection (0-6): "))
                if self.is_valid_location(self.board, col):
                    row = self.get_next_open_row(self.board, col)
                    self.drop_token(self.board, row, col, PLAYER_TOKEN)
                    if self.is_winning_move(self.board, PLAYER_TOKEN):
                        self.game_over = True
                    valid_move = True
                    self.turn += 1
                    self.turn = self.turn % 2
            except Exception as e:
                print(e)

    def make_move(self,col):
        if self.is_valid_location(self.board, col) and self.turn == 0:
            row = self.get_next_open_row(self.board, col)
            self.drop_token(self.board, row, col, PLAYER_TOKEN)
            if self.is_winning_move(self.board, PLAYER_TOKEN):
                self.game_over = True
                self.winner = PLAYER_TOKEN
            self.turn += 1
            self.turn = self.turn % 2
            return True
        else:
            return False
            
    def ai_move(self):
        col = self.pick_best_move(AI_TOKEN)
        if col is not None and self.is_valid_location(self.board, col):
            row = self.get_next_open_row(self.board, col)
            self.drop_token(self.board, row, col, AI_TOKEN)
            if self.is_winning_move(self.board, AI_TOKEN):
                self.game_over = True
                self.winner = AI_TOKEN
            self.turn += 1
            self.turn = self.turn % 2
        return col

    def play_game(self):
        while not self.game_over:
            self.print_board(self.board)
            if self.turn == 0:
                self.player_move()
            else:
                self.ai_move()
        self.print_board(self.board)
        print(f"You {'won' if self.turn else 'lost'}!")