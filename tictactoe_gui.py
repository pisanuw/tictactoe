#!/usr/bin/env python3
"""
Tic-Tac-Toe GUI Game
A graphical tic-tac-toe game with single-player (vs AI) and two-player modes using tkinter.
"""

import tkinter as tk
from tkinter import messagebox, font
import random


class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.root.minsize(600, 600)  # Set minimum window size
        self.root.resizable(True, True)  # Allow resizing

        # Game state
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.game_mode = None  # 'single' or 'two'
        self.difficulty = 'hard'
        self.game_active = False
        self.buttons = []

        # Colors and styling
        self.bg_color = "#2c3e50"
        self.button_bg = "#34495e"
        self.button_hover = "#4a5f7f"
        self.x_color = "#e74c3c"  # Red
        self.o_color = "#3498db"  # Blue
        self.win_color = "#27ae60"  # Green

        # Setup UI
        self.setup_menu_screen()

    def setup_menu_screen(self):
        """Create the main menu screen"""
        self.clear_window()
        self.root.geometry("")  # Reset window size

        # Main frame
        main_frame = tk.Frame(self.root, bg=self.bg_color, padx=60, pady=50)
        main_frame.pack()

        # Title
        title_font = font.Font(family="Arial", size=42, weight="bold")
        title = tk.Label(main_frame, text="Tic-Tac-Toe", font=title_font,
                        bg=self.bg_color, fg="white")
        title.pack(pady=30)

        # Buttons
        button_font = font.Font(family="Arial", size=16)

        single_btn = tk.Button(main_frame, text="Single Player (vs AI)",
                              font=button_font, bg=self.button_bg, fg="white",
                              activebackground=self.button_hover,
                              activeforeground="white",
                              width=25, height=2,
                              command=self.choose_difficulty)
        single_btn.pack(pady=12)

        two_btn = tk.Button(main_frame, text="Two Players",
                           font=button_font, bg=self.button_bg, fg="white",
                           activebackground=self.button_hover,
                           activeforeground="white",
                           width=25, height=2,
                           command=self.start_two_player)
        two_btn.pack(pady=12)

        quit_btn = tk.Button(main_frame, text="Quit",
                            font=button_font, bg="#95a5a6", fg="white",
                            activebackground="#7f8c8d",
                            activeforeground="white",
                            width=25, height=2,
                            command=self.root.quit)
        quit_btn.pack(pady=12)

    def choose_difficulty(self):
        """Screen to choose AI difficulty"""
        self.clear_window()
        self.root.geometry("")  # Reset window size

        main_frame = tk.Frame(self.root, bg=self.bg_color, padx=60, pady=50)
        main_frame.pack()

        title_font = font.Font(family="Arial", size=32, weight="bold")
        title = tk.Label(main_frame, text="Choose Difficulty", font=title_font,
                        bg=self.bg_color, fg="white")
        title.pack(pady=30)

        button_font = font.Font(family="Arial", size=16)

        easy_btn = tk.Button(main_frame, text="Easy",
                            font=button_font, bg="#27ae60", fg="white",
                            activebackground="#229954",
                            activeforeground="white",
                            width=25, height=2,
                            command=lambda: self.start_single_player('easy'))
        easy_btn.pack(pady=12)

        medium_btn = tk.Button(main_frame, text="Medium",
                              font=button_font, bg="#f39c12", fg="white",
                              activebackground="#d68910",
                              activeforeground="white",
                              width=25, height=2,
                              command=lambda: self.start_single_player('medium'))
        medium_btn.pack(pady=12)

        hard_btn = tk.Button(main_frame, text="Hard (Unbeatable)",
                            font=button_font, bg="#e74c3c", fg="white",
                            activebackground="#c0392b",
                            activeforeground="white",
                            width=25, height=2,
                            command=lambda: self.start_single_player('hard'))
        hard_btn.pack(pady=12)

        back_btn = tk.Button(main_frame, text="Back",
                            font=button_font, bg="#95a5a6", fg="white",
                            activebackground="#7f8c8d",
                            activeforeground="white",
                            width=25, height=2,
                            command=self.setup_menu_screen)
        back_btn.pack(pady=12)

    def start_single_player(self, difficulty):
        """Start a single player game"""
        self.game_mode = 'single'
        self.difficulty = difficulty
        self.setup_game_screen()

    def start_two_player(self):
        """Start a two player game"""
        self.game_mode = 'two'
        self.setup_game_screen()

    def setup_game_screen(self):
        """Create the game board screen"""
        self.clear_window()
        self.root.geometry("")  # Reset window size
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.game_active = True
        self.buttons = []

        # Main frame
        main_frame = tk.Frame(self.root, bg=self.bg_color, padx=40, pady=30)
        main_frame.pack(expand=True, fill='both')

        # Status label
        status_font = font.Font(family="Arial", size=20, weight="bold")
        self.status_label = tk.Label(main_frame, text=self.get_status_text(),
                                     font=status_font, bg=self.bg_color, fg="white")
        self.status_label.pack(pady=15)

        # Game board frame
        board_frame = tk.Frame(main_frame, bg=self.bg_color)
        board_frame.pack(pady=15)

        # Create buttons for game board
        button_font = font.Font(family="Arial", size=48, weight="bold")
        for i in range(3):
            row_buttons = []
            for j in range(3):
                btn = tk.Button(board_frame, text="", font=button_font,
                              width=6, height=3,
                              bg=self.button_bg, fg="white",
                              activebackground=self.button_hover,
                              command=lambda row=i, col=j: self.on_cell_click(row, col))
                btn.grid(row=i, column=j, padx=5, pady=5)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)

        # Control buttons frame
        control_frame = tk.Frame(main_frame, bg=self.bg_color)
        control_frame.pack(pady=20)

        control_font = font.Font(family="Arial", size=14)

        new_game_btn = tk.Button(control_frame, text="New Game",
                                font=control_font, bg="#27ae60", fg="white",
                                activebackground="#229954",
                                width=15, height=2,
                                command=self.reset_game)
        new_game_btn.grid(row=0, column=0, padx=8)

        menu_btn = tk.Button(control_frame, text="Main Menu",
                           font=control_font, bg="#95a5a6", fg="white",
                           activebackground="#7f8c8d",
                           width=15, height=2,
                           command=self.setup_menu_screen)
        menu_btn.grid(row=0, column=1, padx=8)

        # Force window to update its size
        self.root.update_idletasks()

    def get_status_text(self):
        """Get the current status text"""
        if self.game_mode == 'single':
            if self.current_player == 'X':
                return "Your turn (X)"
            else:
                return "AI's turn (O)"
        else:
            return f"Player {self.current_player}'s turn"

    def on_cell_click(self, row, col):
        """Handle cell button click"""
        if not self.game_active:
            return

        if self.board[row][col] != ' ':
            return

        # Human player's move
        self.make_move(row, col, self.current_player)

        # Check for game end
        if self.check_game_end():
            return

        # Switch player
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        self.status_label.config(text=self.get_status_text())

        # AI's turn in single player mode
        if self.game_mode == 'single' and self.current_player == 'O' and self.game_active:
            self.root.after(500, self.ai_move)

    def make_move(self, row, col, player):
        """Make a move on the board"""
        self.board[row][col] = player
        color = self.x_color if player == 'X' else self.o_color
        self.buttons[row][col].config(text=player, fg=color, disabledforeground=color)

    def ai_move(self):
        """Make AI move"""
        if not self.game_active:
            return

        move = self.get_ai_move(self.board, 'O', 'X', self.difficulty)
        if move:
            row, col = move
            self.make_move(row, col, 'O')

            # Check for game end
            if self.check_game_end():
                return

            # Switch back to player
            self.current_player = 'X'
            self.status_label.config(text=self.get_status_text())

    def check_game_end(self):
        """Check if game has ended (win or draw)"""
        # Check for winner
        if self.check_winner(self.board, self.current_player):
            self.game_active = False
            self.highlight_winner()

            if self.game_mode == 'single':
                if self.current_player == 'X':
                    message = "Congratulations! You win! 🎉"
                else:
                    message = "AI wins! Better luck next time!"
            else:
                message = f"Player {self.current_player} wins! 🎉"

            self.status_label.config(text=message)
            self.root.after(1500, lambda: messagebox.showinfo("Game Over", message))
            return True

        # Check for draw
        if self.is_board_full(self.board):
            self.game_active = False
            self.status_label.config(text="It's a draw!")
            self.root.after(1500, lambda: messagebox.showinfo("Game Over", "It's a draw!"))
            return True

        return False

    def highlight_winner(self):
        """Highlight the winning combination"""
        player = self.current_player

        # Check rows
        for i in range(3):
            if all(self.board[i][j] == player for j in range(3)):
                for j in range(3):
                    self.buttons[i][j].config(bg=self.win_color)
                return

        # Check columns
        for j in range(3):
            if all(self.board[i][j] == player for i in range(3)):
                for i in range(3):
                    self.buttons[i][j].config(bg=self.win_color)
                return

        # Check diagonals
        if all(self.board[i][i] == player for i in range(3)):
            for i in range(3):
                self.buttons[i][i].config(bg=self.win_color)
            return

        if all(self.board[i][2-i] == player for i in range(3)):
            for i in range(3):
                self.buttons[i][2-i].config(bg=self.win_color)
            return

    def reset_game(self):
        """Reset the current game"""
        self.setup_game_screen()

    def clear_window(self):
        """Clear all widgets from window"""
        for widget in self.root.winfo_children():
            widget.destroy()

    # Game logic methods (from original CLI version)

    def check_winner(self, board, player):
        """Check if the specified player has won"""
        # Check rows
        for row in board:
            if all(cell == player for cell in row):
                return True

        # Check columns
        for col in range(3):
            if all(board[row][col] == player for row in range(3)):
                return True

        # Check diagonals
        if all(board[i][i] == player for i in range(3)):
            return True
        if all(board[i][2-i] == player for i in range(3)):
            return True

        return False

    def is_board_full(self, board):
        """Check if the board is completely filled"""
        return all(cell != ' ' for row in board for cell in row)

    def get_available_moves(self, board):
        """Get list of all available positions on the board"""
        moves = []
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    moves.append((i, j))
        return moves

    def minimax(self, board, depth, is_maximizing, ai_player, human_player):
        """Minimax algorithm for AI decision making"""
        # Base cases
        if self.check_winner(board, ai_player):
            return 10 - depth
        if self.check_winner(board, human_player):
            return depth - 10
        if self.is_board_full(board):
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for row, col in self.get_available_moves(board):
                board[row][col] = ai_player
                score = self.minimax(board, depth + 1, False, ai_player, human_player)
                board[row][col] = ' '
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for row, col in self.get_available_moves(board):
                board[row][col] = human_player
                score = self.minimax(board, depth + 1, True, ai_player, human_player)
                board[row][col] = ' '
                best_score = min(score, best_score)
            return best_score

    def get_ai_move(self, board, ai_player, human_player, difficulty='hard'):
        """Get the AI's move based on difficulty level"""
        available_moves = self.get_available_moves(board)

        if not available_moves:
            return None

        # Easy mode: random move
        if difficulty == 'easy':
            return random.choice(available_moves)

        # Medium mode: mix of optimal and random
        if difficulty == 'medium' and random.random() < 0.5:
            return random.choice(available_moves)

        # Hard mode (or medium 50% of the time): use minimax
        best_score = -float('inf')
        best_move = None

        for row, col in available_moves:
            board[row][col] = ai_player
            score = self.minimax(board, 0, False, ai_player, human_player)
            board[row][col] = ' '

            if score > best_score:
                best_score = score
                best_move = (row, col)

        return best_move if best_move else available_moves[0]


def main():
    """Main function to run the GUI game"""
    root = tk.Tk()
    game = TicTacToeGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
