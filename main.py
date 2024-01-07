import numpy as np
import random
import math

# Constants
PLAYER_PIECE = 1
AI_PIECE = 2
ROW_COUNT = 6
COLUMN_COUNT = 7

class ConnectFour:
    def __init__(self):
        self.board = np.zeros((ROW_COUNT, COLUMN_COUNT), dtype=int)
        self.game_over = False
        self.turn = 0  # 0 for player, 1 for AI

    def drop_piece(self, board, row, col, piece):
        board[row][col] = piece

    def is_valid_location(self, col):
        return self.board[ROW_COUNT-1][col] == 0
    
    def is_terminal_node(self, board):
        return self.is_winning_move(board, PLAYER_PIECE) or self.is_winning_move(board, AI_PIECE) or len(self.get_valid_locations()) == 0

    def is_winning_move(self, board, piece):
        # Check horizontal locations for win
        for c in range(COLUMN_COUNT - 3):
            for r in range(ROW_COUNT):
                if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                    return True

        # Check vertical locations for win
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT - 3):
                if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                    return True

        # Check positively sloped diagonals
        for c in range(COLUMN_COUNT - 3):
            for r in range(ROW_COUNT - 3):
                if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                    return True

        # Check negatively sloped diagonals
        for c in range(3, COLUMN_COUNT):
            for r in range(ROW_COUNT - 3):
                if board[r][c] == piece and board[r - 1][c - 1] == piece and board[r - 2][c - 2] == piece and board[r - 3][c - 3] == piece:
                    return True

        return False

    def get_next_open_row(self, col):
        for r in range(ROW_COUNT):
            if self.board[r][col] == 0:
                return r

    def print_board(self):
        for row in np.flip(self.board, 0):
            print('|', end='')
            for cell in row:
                if cell == PLAYER_PIECE:
                    print('X', end='|')
                elif cell == AI_PIECE:
                    print('O', end='|')
                else:
                    print(' ', end='|')
            print()
        print(f"{'-' * (2 * COLUMN_COUNT + 1)}")
        print(' 0 1 2 3 4 5 6')  # Column numbers for reference

    def find_winning_columns(self, board, piece):
        winning_columns = []

        # Check horizontal locations for potential win
        for c in range(COLUMN_COUNT - 3):
            for r in range(ROW_COUNT):
                for i in range(4):
                    if board[r][c + i] == 0 and (r == ROW_COUNT - 1 or board[r + 1][c + i] != 0):
                        temp_board = board.copy()
                        temp_board[r][c + i] = piece
                        if self.is_winning_move(temp_board, piece):
                            winning_columns.append(c + i)

        # Check vertical locations for potential win
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT - 3):
                if board[r][c] == 0:
                    temp_board = board.copy()
                    temp_board[r][c] = piece
                    if self.is_winning_move(temp_board, piece):
                        winning_columns.append(c)

        # Check positively sloped diagonals for potential win
        for c in range(COLUMN_COUNT - 3):
            for r in range(ROW_COUNT - 3):
                for i in range(4):
                    if board[r + i][c + i] == 0 and (r + i == ROW_COUNT - 1 or board[r + i + 1][c + i] != 0):
                        temp_board = board.copy()
                        temp_board[r + i][c + i] = piece
                        if self.is_winning_move(temp_board, piece):
                            winning_columns.append(c + i)

        # Check negatively sloped diagonals for potential win
        for c in range(3, COLUMN_COUNT):
            for r in range(3, ROW_COUNT):
                for i in range(4):
                    if board[r - i][c - i] == 0 and (r - i == ROW_COUNT - 1 or board[r - i + 1][c - i] != 0):
                        temp_board = board.copy()
                        temp_board[r - i][c - i] = piece
                        if self.is_winning_move(temp_board, piece):
                            winning_columns.append(c - i)

        return list(set(winning_columns))  # Return unique columns

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        valid_locations = self.get_valid_locations()
        is_terminal = self.is_terminal_node(board)
        
        if depth == 0 or is_terminal:
            if is_terminal:
                if self.is_winning_move(board, AI_PIECE):
                    winning_columns = self.find_winning_columns(board, AI_PIECE)
                    best_column = self.choose_best_column(winning_columns, board, AI_PIECE)  # Choose the best column from the list
                    print(f"Best column AI: {best_column}")
                    return (best_column, 100000000000000)
                elif self.is_winning_move(board, PLAYER_PIECE):
                    winning_columns = self.find_winning_columns(board, PLAYER_PIECE)
                    best_column = self.choose_best_column(winning_columns, board, PLAYER_PIECE)
                    print(f"Best column PL: {best_column}")
                    return (best_column, -10000000000000)
                else:
                    return (None, 0)  # Game is over, no more valid moves
            else:
                return (None, self.score_position(board, AI_PIECE))

        if maximizing_player:
            value = -math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = self.get_next_open_row(col)
                b_copy = board.copy()
                self.drop_piece(b_copy, row, col, AI_PIECE)
                new_score = self.minimax(b_copy, depth-1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value

        else: # Minimizing player
            value = math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = self.get_next_open_row(col)
                b_copy = board.copy()
                self.drop_piece(b_copy, row, col, PLAYER_PIECE)
                new_score = self.minimax(b_copy, depth-1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value

    def score_position(self, board, piece):
        score = 0

        # Score center column
        center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
        center_count = center_array.count(piece)
        score += center_count * 3  # Center column is usually more valuable

        # Score Horizontal
        for r in range(ROW_COUNT):
            row_array = [int(i) for i in list(board[r, :])]
            for c in range(COLUMN_COUNT - 3):
                window = row_array[c:c + 4]
                score += self.evaluate_window(window, piece)

        # Score Vertical
        for c in range(COLUMN_COUNT):
            col_array = [int(i) for i in list(board[:, c])]
            for r in range(ROW_COUNT - 3):
                window = col_array[r:r + 4]
                score += self.evaluate_window(window, piece)

        # Score positive sloped diagonals
        for r in range(ROW_COUNT - 3):
            for c in range(COLUMN_COUNT - 3):
                window = [board[r + i][c + i] for i in range(4)]
                score += self.evaluate_window(window, piece)

        # Score negative sloped diagonals
        for r in range(3, ROW_COUNT):
            for c in range(COLUMN_COUNT - 3):
                window = [board[r - i][c + i] for i in range(4)]
                score += self.evaluate_window(window, piece)

        return score

    def evaluate_window(self, window, piece):
        score = 0
        opp_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE

        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(0) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(0) == 2:
            score += 2

        if window.count(opp_piece) == 3 and window.count(0) == 1:
            score -= 80
        
        if window.count(opp_piece) == 2 and window.count(0) == 1:
            score -= 30

        return score

    def choose_best_column(self, winning_columns, board, piece):
        best_score = -math.inf
        best_column = random.choice(winning_columns)

        for col in winning_columns:
            row = self.get_next_open_row(col)
            temp_board = board.copy()
            self.drop_piece(temp_board, row, col, piece)
            score = self.evaluate_board_for_future_opportunities(temp_board, piece)

            if score > best_score:
                best_score = score
                best_column = col

        return best_column

    def evaluate_board_for_future_opportunities(self, board, piece):
        score = 0

        # Evaluate the board for future opportunities after making a move
        # This can include checking for potential two-way wins, blocking opponent moves, etc.

        # Example: Add points if the move sets up a two-way win
        # This is a placeholder logic, replace with your own strategy
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                if board[r][c] == 0:
                    # Check if placing a piece here sets up a two-way win
                    board[r][c] = piece
                    if self.is_winning_move(board, piece):
                        # Additional checks to see if this creates a two-way win
                        score += 10  # Assign a score based on strategic advantage
                    board[r][c] = 0  # Reset the board

        return score

    def get_valid_locations(self):
        valid_locations = []
        for col in range(COLUMN_COUNT):
            if self.is_valid_location(col):
                valid_locations.append(col)
        return valid_locations

    def pick_best_move(self, piece):
        best_score = -math.inf
        best_col = random.choice(self.get_valid_locations())
        other_col = best_col
        for col in self.get_valid_locations():
            row = self.get_next_open_row(col)
            temp_board = np.copy(self.board)
            self.drop_piece(temp_board,row, col, piece)
            (new_col,score) = self.minimax(temp_board, 4, -math.inf, math.inf, True)  # Depth set to 4
            if score > best_score:
                best_score = score
                best_col = new_col
                other_col = new_col
        print(f"Score: {best_score} at {best_col}. Alternative: {other_col}")
        return best_col

    def player_move(self):
        valid_move = False
        while not valid_move:
            col = int(input("Player 1 (X) Make your Selection (0-6): "))
            if self.is_valid_location(col):
                row = self.get_next_open_row(col)
                self.drop_piece(self.board, row, col, PLAYER_PIECE)
                if self.is_winning_move(self.board, PLAYER_PIECE):
                    self.game_over = True
                valid_move = True
                self.turn += 1
                self.turn = self.turn % 2

    def ai_move(self):
        col = self.pick_best_move(AI_PIECE)
        if self.is_valid_location(col):
            row = self.get_next_open_row(col)
            self.drop_piece(self.board, row, col, AI_PIECE)
            if self.is_winning_move(self.board, AI_PIECE):
                self.game_over = True
            self.turn += 1
            self.turn = self.turn % 2

    def play_game(self):
        while not self.game_over:
            self.print_board()
            if self.turn == 0:
                self.player_move()
            else:
                self.ai_move()
        self.print_board()
        print(f"You {'won' if self.turn else 'lost'}!")

# Create a new game and start playing
game = ConnectFour()
game.play_game()
