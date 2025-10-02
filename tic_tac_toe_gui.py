import tkinter as tk
from tkinter import messagebox, font
import time

# Constants for the game
CELL_SIZE = 120
GRID_SIZE = 3
WINDOW_WIDTH = CELL_SIZE * GRID_SIZE
WINDOW_HEIGHT = WINDOW_WIDTH + 100  # Extra space for title and score
PLAYER = 'X'
AI = 'O'

class TicTacToeGUI:
    """
    A GUI for a Tic-Tac-Toe game with an unbeatable AI opponent.
    The GUI is built using tkinter, and the AI uses the minimax algorithm.
    """
    def __init__(self, master):
        self.master = master
        self.master.title("Fancy Tic-Tac-Toe")
        self.master.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.master.resizable(False, False)

        # Game state variables
        self.board = [['' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.scores = {PLAYER: 0, AI: 0}
        self.game_over = False

        self.create_widgets()
        self.reset_game()

    def create_widgets(self):
        """Creates and places all the GUI widgets."""
        # Custom fonts
        self.title_font = font.Font(family="Helvetica", size=24, weight="bold")
        self.score_font = font.Font(family="Helvetica", size=16)
        self.cell_font = font.Font(family="Helvetica", size=48, weight="bold")

        # Title Label
        title_label = tk.Label(self.master, text="AI Tic-Tac-Toe", font=self.title_font, pady=10)
        title_label.pack()

        # Score Frame
        score_frame = tk.Frame(self.master)
        score_frame.pack(pady=5)
        
        self.player_score_var = tk.StringVar(value=f"Player (X): {self.scores[PLAYER]}")
        player_score_label = tk.Label(score_frame, textvariable=self.player_score_var, font=self.score_font, padx=20)
        player_score_label.grid(row=0, column=0)
        
        self.ai_score_var = tk.StringVar(value=f"AI (O): {self.scores[AI]}")
        ai_score_label = tk.Label(score_frame, textvariable=self.ai_score_var, font=self.score_font, padx=20)
        ai_score_label.grid(row=0, column=1)

        # Game Canvas
        self.canvas = tk.Canvas(self.master, width=WINDOW_WIDTH, height=WINDOW_WIDTH, bg='white')
        self.canvas.pack(pady=10)

        # Bind click event to the canvas
        self.canvas.bind("<Button-1>", self.handle_player_click)

    def reset_game(self):
        """Resets the board and game state for a new round."""
        self.game_over = False
        self.board = [['' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.canvas.delete("all")  # Clear canvas of marks and lines
        self.draw_grid()

    def draw_grid(self):
        """Draws the 3x3 grid lines on the canvas."""
        for i in range(1, GRID_SIZE):
            # Vertical lines
            self.canvas.create_line(i * CELL_SIZE, 0, i * CELL_SIZE, WINDOW_WIDTH, width=4)
            # Horizontal lines
            self.canvas.create_line(0, i * CELL_SIZE, WINDOW_WIDTH, i * CELL_SIZE, width=4)

    def handle_player_click(self, event):
        """Handles a click event from the human player."""
        if self.game_over:
            return

        col = event.x // CELL_SIZE
        row = event.y // CELL_SIZE

        if self.board[row][col] == '':
            self.make_move(row, col, PLAYER)
            
            # Check for game over after player's move
            winner = self.check_winner()
            if winner:
                self.end_game(winner)
            elif not self.is_board_full():
                self.master.after(500, self.ai_move) # Add a small delay for AI move

    def make_move(self, row, col, player):
        """Places a player's mark on the board and updates the GUI."""
        self.board[row][col] = player
        x = col * CELL_SIZE + CELL_SIZE / 2
        y = row * CELL_SIZE + CELL_SIZE / 2
        
        color = "blue" if player == PLAYER else "red"
        self.canvas.create_text(x, y, text=player, font=self.cell_font, fill=color)

    def ai_move(self):
        """Calculates and performs the AI's move using minimax."""
        if self.game_over:
            return
            
        best_score = -float('inf')
        best_move = None

        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if self.board[r][c] == '':
                    self.board[r][c] = AI
                    score = self.minimax(self.board, 0, False)
                    self.board[r][c] = '' # Backtrack
                    if score > best_score:
                        best_score = score
                        best_move = (r, c)
        
        if best_move:
            self.make_move(best_move[0], best_move[1], AI)
            winner = self.check_winner()
            if winner:
                self.end_game(winner)

    def minimax(self, board, depth, is_maximizing):
        """
        Minimax algorithm implementation. Recursively explores game states
        to find the optimal move for the AI.
        - is_maximizing: True for AI (O), False for Player (X)
        """
        winner = self.check_winner(board_state=board)
        if winner == AI:
            return 10 - depth
        if winner == PLAYER:
            return depth - 10
        if self.is_board_full(board_state=board):
            return 0

        if is_maximizing: # AI's turn (wants to maximize score)
            best_score = -float('inf')
            for r in range(GRID_SIZE):
                for c in range(GRID_SIZE):
                    if board[r][c] == '':
                        board[r][c] = AI
                        score = self.minimax(board, depth + 1, False)
                        board[r][c] = ''
                        best_score = max(score, best_score)
            return best_score
        else: # Player's turn (wants to minimize score)
            best_score = float('inf')
            for r in range(GRID_SIZE):
                for c in range(GRID_SIZE):
                    if board[r][c] == '':
                        board[r][c] = PLAYER
                        score = self.minimax(board, depth + 1, True)
                        board[r][c] = ''
                        best_score = min(score, best_score)
            return best_score

    def check_winner(self, board_state=None):
        """
        Checks for a win or a tie on the board.
        Returns the winner ('X' or 'O'), 'Tie', or None.
        """
        b = board_state if board_state else self.board

        # Check rows, columns, and diagonals
        lines = []
        lines.extend(b)  # Rows
        lines.extend([list(x) for x in zip(*b)]) # Columns
        lines.append([b[i][i] for i in range(GRID_SIZE)]) # Main diagonal
        lines.append([b[i][GRID_SIZE - 1 - i] for i in range(GRID_SIZE)]) # Anti-diagonal

        for line in lines:
            if len(set(line)) == 1 and line[0] != '':
                return line[0]

        if self.is_board_full(board_state=b):
            return 'Tie'
        
        return None

    def is_board_full(self, board_state=None):
        """Checks if the board is full."""
        b = board_state if board_state else self.board
        return all(cell != '' for row in b for cell in row)
        
    def end_game(self, winner):
        """Handles the end of the game state."""
        self.game_over = True
        
        # Draw winning line animation
        win_info = self.get_winning_line_info()
        if win_info:
            self.draw_winning_line(win_info)

        if winner == 'Tie':
            message = "It's a tie!"
        else:
            message = f"{winner} wins!"
            self.scores[winner] += 1
            self.player_score_var.set(f"Player (X): {self.scores[PLAYER]}")
            self.ai_score_var.set(f"AI (O): {self.scores[AI]}")

        # Ask to play again
        if messagebox.askyesno("Game Over", message + "\nDo you want to play again?"):
            self.reset_game()
        else:
            self.master.quit()

    def get_winning_line_info(self):
        """Finds the coordinates for the winning line."""
        b = self.board
        # Check rows
        for r in range(GRID_SIZE):
            if len(set(b[r])) == 1 and b[r][0] != '':
                return ('row', r)
        # Check columns
        for c in range(GRID_SIZE):
            if len(set([b[r][c] for r in range(GRID_SIZE)])) == 1 and b[0][c] != '':
                return ('col', c)
        # Check diagonals
        if len(set([b[i][i] for i in range(GRID_SIZE)])) == 1 and b[0][0] != '':
            return ('diag', 0)
        if len(set([b[i][GRID_SIZE - 1 - i] for i in range(GRID_SIZE)])) == 1 and b[0][GRID_SIZE-1] != '':
            return ('diag', 1)
        return None

    def draw_winning_line(self, win_info):
        """Draws a red line through the winning cells."""
        line_type, index = win_info
        half = CELL_SIZE / 2

        if line_type == 'row':
            y = index * CELL_SIZE + half
            self.canvas.create_line(half, y, WINDOW_WIDTH - half, y, width=5, fill='green', capstyle=tk.ROUND)
        elif line_type == 'col':
            x = index * CELL_SIZE + half
            self.canvas.create_line(x, half, x, WINDOW_WIDTH - half, width=5, fill='green', capstyle=tk.ROUND)
        elif line_type == 'diag':
            if index == 0: # Main diagonal
                self.canvas.create_line(half, half, WINDOW_WIDTH - half, WINDOW_WIDTH - half, width=5, fill='green', capstyle=tk.ROUND)
            else: # Anti-diagonal
                self.canvas.create_line(WINDOW_WIDTH - half, half, half, WINDOW_WIDTH - half, width=5, fill='green', capstyle=tk.ROUND)

# Main execution block
if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToeGUI(root)
    root.mainloop()