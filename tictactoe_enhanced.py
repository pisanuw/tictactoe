#!/usr/bin/env python3
"""
Tic-Tac-Toe Enhanced - Premium Edition
A feature-rich graphical tic-tac-toe game with AI, statistics, themes, animations, and more!
"""

import tkinter as tk
from tkinter import messagebox, font
import random
import json
import os
from pathlib import Path
import time


class GameStats:
    """Handle game statistics and persistence"""

    def __init__(self, filename='tictactoe_stats.json'):
        self.filename = filename
        self.stats = self.load_stats()

    def load_stats(self):
        """Load statistics from file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    return json.load(f)
            except:
                return self.get_default_stats()
        return self.get_default_stats()

    def get_default_stats(self):
        """Get default stats structure"""
        return {
            'single_easy_wins': 0,
            'single_easy_losses': 0,
            'single_easy_draws': 0,
            'single_medium_wins': 0,
            'single_medium_losses': 0,
            'single_medium_draws': 0,
            'single_hard_wins': 0,
            'single_hard_losses': 0,
            'single_hard_draws': 0,
            'two_player_total': 0,
            'total_games': 0,
            'current_streak': 0,
            'best_streak': 0,
            'theme': 'dark',
            'sound_enabled': True,
            'board_size': 3
        }

    def save_stats(self):
        """Save statistics to file"""
        with open(self.filename, 'w') as f:
            json.dump(self.stats, f, indent=2)

    def record_game_result(self, mode, difficulty, result):
        """Record a game result"""
        if mode == 'single':
            key_base = f'single_{difficulty}'
            self.stats[f'{key_base}_{result}'] = self.stats.get(f'{key_base}_{result}', 0) + 1

            if result == 'wins':
                self.stats['current_streak'] = self.stats.get('current_streak', 0) + 1
                self.stats['best_streak'] = max(self.stats['best_streak'], self.stats['current_streak'])
            else:
                self.stats['current_streak'] = 0
        else:
            self.stats['two_player_total'] = self.stats.get('two_player_total', 0) + 1

        self.stats['total_games'] = self.stats.get('total_games', 0) + 1
        self.save_stats()

    def get_stats_display(self):
        """Get formatted statistics for display"""
        easy_games = self.stats.get('single_easy_wins', 0) + self.stats.get('single_easy_losses', 0) + self.stats.get('single_easy_draws', 0)
        medium_games = self.stats.get('single_medium_wins', 0) + self.stats.get('single_medium_losses', 0) + self.stats.get('single_medium_draws', 0)
        hard_games = self.stats.get('single_hard_wins', 0) + self.stats.get('single_hard_losses', 0) + self.stats.get('single_hard_draws', 0)

        return {
            'total_games': self.stats.get('total_games', 0),
            'easy_games': easy_games,
            'easy_wins': self.stats.get('single_easy_wins', 0),
            'medium_games': medium_games,
            'medium_wins': self.stats.get('single_medium_wins', 0),
            'hard_games': hard_games,
            'hard_wins': self.stats.get('single_hard_wins', 0),
            'best_streak': self.stats.get('best_streak', 0),
            'current_streak': self.stats.get('current_streak', 0),
        }


class TicTacToeEnhanced:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe Enhanced")
        self.root.minsize(700, 700)
        self.root.resizable(True, True)

        # Game state
        self.board = None
        self.current_player = 'X'
        self.game_mode = None
        self.difficulty = 'hard'
        self.game_active = False
        self.buttons = []
        self.board_size = 3
        self.move_history = []

        # Statistics
        self.stats = GameStats()

        # Themes
        self.themes = {
            'dark': {
                'bg': '#2c3e50',
                'button': '#34495e',
                'hover': '#4a5f7f',
                'text': 'white',
                'x_color': '#e74c3c',
                'o_color': '#3498db',
                'win_color': '#27ae60',
                'accent': '#f39c12'
            },
            'light': {
                'bg': '#ecf0f1',
                'button': '#d5dbdb',
                'hover': '#bdc3c7',
                'text': '#2c3e50',
                'x_color': '#e74c3c',
                'o_color': '#3498db',
                'win_color': '#27ae60',
                'accent': '#f39c12'
            }
        }
        self.current_theme = self.stats.stats.get('theme', 'dark')
        self.theme = self.themes[self.current_theme]

        # Setup UI
        self.setup_menu_screen()

    def create_board(self):
        """Create empty board"""
        return [[' ' for _ in range(self.board_size)] for _ in range(self.board_size)]

    def setup_menu_screen(self):
        """Create the main menu"""
        self.clear_window()
        self.root.geometry("")

        main_frame = tk.Frame(self.root, bg=self.theme['bg'], padx=60, pady=50)
        main_frame.pack()

        title_font = font.Font(family="Arial", size=48, weight="bold")
        title = tk.Label(main_frame, text="Tic-Tac-Toe\nEnhanced", font=title_font,
                        bg=self.theme['bg'], fg=self.theme['accent'], justify='center')
        title.pack(pady=30)

        subtitle_font = font.Font(family="Arial", size=12)
        subtitle = tk.Label(main_frame, text="Premium Edition", font=subtitle_font,
                           bg=self.theme['bg'], fg=self.theme['text'])
        subtitle.pack(pady=5)

        button_font = font.Font(family="Arial", size=16)

        buttons = [
            ("Single Player (vs AI)", self.choose_difficulty),
            ("Two Players", self.start_two_player),
            ("Statistics", self.show_statistics),
            ("Settings", self.show_settings),
            ("Quit", self.root.quit)
        ]

        for text, cmd in buttons:
            btn = tk.Button(main_frame, text=text, font=button_font,
                           bg=self.theme['button'], fg=self.theme['text'],
                           activebackground=self.theme['hover'],
                           width=25, height=2, command=cmd)
            btn.pack(pady=12)

    def show_statistics(self):
        """Display game statistics"""
        self.clear_window()
        self.root.geometry("")

        main_frame = tk.Frame(self.root, bg=self.theme['bg'], padx=40, pady=30)
        main_frame.pack()

        title_font = font.Font(family="Arial", size=32, weight="bold")
        title = tk.Label(main_frame, text="📊 Statistics", font=title_font,
                        bg=self.theme['bg'], fg=self.theme['accent'])
        title.pack(pady=20)

        stats = self.stats.get_stats_display()
        stats_font = font.Font(family="Arial", size=14)

        stats_text = f"""
Total Games Played: {stats['total_games']}
Current Streak: {stats['current_streak']} wins
Best Streak: {stats['best_streak']} wins

Easy Mode:
  Games: {stats['easy_games']} | Wins: {stats['easy_wins']}
  Win Rate: {round(100 * stats['easy_wins'] / max(stats['easy_games'], 1))}%

Medium Mode:
  Games: {stats['medium_games']} | Wins: {stats['medium_wins']}
  Win Rate: {round(100 * stats['medium_wins'] / max(stats['medium_games'], 1))}%

Hard Mode:
  Games: {stats['hard_games']} | Wins: {stats['hard_wins']}
  Win Rate: {round(100 * stats['hard_wins'] / max(stats['hard_games'], 1))}%
        """

        stats_label = tk.Label(main_frame, text=stats_text.strip(), font=stats_font,
                              bg=self.theme['bg'], fg=self.theme['text'], justify='left')
        stats_label.pack(pady=20)

        button_font = font.Font(family="Arial", size=14)

        reset_btn = tk.Button(main_frame, text="Reset Statistics",
                             font=button_font, bg="#e74c3c", fg="white",
                             activebackground="#c0392b",
                             width=20, height=2,
                             command=self.reset_statistics)
        reset_btn.pack(pady=10)

        back_btn = tk.Button(main_frame, text="Back to Menu",
                            font=button_font, bg=self.theme['button'], fg=self.theme['text'],
                            activebackground=self.theme['hover'],
                            width=20, height=2,
                            command=self.setup_menu_screen)
        back_btn.pack(pady=10)

    def reset_statistics(self):
        """Reset all statistics"""
        if messagebox.askyesno("Reset Stats", "Are you sure you want to reset all statistics?"):
            self.stats.stats = self.stats.get_default_stats()
            self.stats.save_stats()
            self.show_statistics()

    def show_settings(self):
        """Show settings menu"""
        self.clear_window()
        self.root.geometry("")

        main_frame = tk.Frame(self.root, bg=self.theme['bg'], padx=40, pady=30)
        main_frame.pack()

        title_font = font.Font(family="Arial", size=32, weight="bold")
        title = tk.Label(main_frame, text="⚙️ Settings", font=title_font,
                        bg=self.theme['bg'], fg=self.theme['accent'])
        title.pack(pady=20)

        settings_font = font.Font(family="Arial", size=14)

        # Theme selection
        theme_frame = tk.Frame(main_frame, bg=self.theme['bg'])
        theme_frame.pack(pady=20)

        theme_label = tk.Label(theme_frame, text="Theme:", font=settings_font,
                              bg=self.theme['bg'], fg=self.theme['text'])
        theme_label.pack(side='left', padx=10)

        dark_btn = tk.Button(theme_frame, text="🌙 Dark", font=settings_font,
                            bg=self.theme['button'], fg=self.theme['text'],
                            activebackground=self.theme['hover'],
                            width=12,
                            command=lambda: self.set_theme('dark'))
        dark_btn.pack(side='left', padx=5)

        light_btn = tk.Button(theme_frame, text="☀️ Light", font=settings_font,
                             bg=self.theme['button'], fg=self.theme['text'],
                             activebackground=self.theme['hover'],
                             width=12,
                             command=lambda: self.set_theme('light'))
        light_btn.pack(side='left', padx=5)

        # Board size selection
        size_frame = tk.Frame(main_frame, bg=self.theme['bg'])
        size_frame.pack(pady=20)

        size_label = tk.Label(size_frame, text="Board Size:", font=settings_font,
                             bg=self.theme['bg'], fg=self.theme['text'])
        size_label.pack(side='left', padx=10)

        for size in [3, 4, 5]:
            btn = tk.Button(size_frame, text=f"{size}×{size}", font=settings_font,
                           bg=self.theme['button'], fg=self.theme['text'],
                           activebackground=self.theme['hover'],
                           width=8,
                           command=lambda s=size: self.set_board_size(s))
            btn.pack(side='left', padx=5)

        # Sound toggle
        sound_frame = tk.Frame(main_frame, bg=self.theme['bg'])
        sound_frame.pack(pady=20)

        sound_label = tk.Label(sound_frame, text="Sound Effects:", font=settings_font,
                              bg=self.theme['bg'], fg=self.theme['text'])
        sound_label.pack(side='left', padx=10)

        sound_enabled = self.stats.stats.get('sound_enabled', True)
        sound_status = "✓ On" if sound_enabled else "✗ Off"

        sound_btn = tk.Button(sound_frame, text=sound_status, font=settings_font,
                             bg=self.theme['button'], fg=self.theme['text'],
                             activebackground=self.theme['hover'],
                             width=8,
                             command=self.toggle_sound)
        sound_btn.pack(side='left', padx=5)

        back_btn = tk.Button(main_frame, text="Back", font=settings_font,
                            bg=self.theme['button'], fg=self.theme['text'],
                            activebackground=self.theme['hover'],
                            width=20, height=2,
                            command=self.setup_menu_screen)
        back_btn.pack(pady=30)

    def set_theme(self, theme_name):
        """Change theme"""
        self.current_theme = theme_name
        self.theme = self.themes[theme_name]
        self.stats.stats['theme'] = theme_name
        self.stats.save_stats()
        self.show_settings()

    def set_board_size(self, size):
        """Set board size"""
        if size != 3:
            messagebox.showinfo("Board Size",
                              f"Playing on {size}×{size} board!\nWin with {size} in a row.")
        self.board_size = size
        self.stats.stats['board_size'] = size
        self.stats.save_stats()
        self.show_settings()

    def toggle_sound(self):
        """Toggle sound effects"""
        self.stats.stats['sound_enabled'] = not self.stats.stats.get('sound_enabled', True)
        self.stats.save_stats()
        self.show_settings()

    def play_sound(self):
        """Play a beep sound if enabled"""
        if self.stats.stats.get('sound_enabled', True):
            try:
                import winsound
                winsound.Beep(1000, 100)
            except:
                try:
                    os.system('beep')
                except:
                    pass

    def choose_difficulty(self):
        """Choose AI difficulty"""
        self.clear_window()
        self.root.geometry("")

        main_frame = tk.Frame(self.root, bg=self.theme['bg'], padx=60, pady=50)
        main_frame.pack()

        title_font = font.Font(family="Arial", size=32, weight="bold")
        title = tk.Label(main_frame, text="Choose Difficulty", font=title_font,
                        bg=self.theme['bg'], fg=self.theme['accent'])
        title.pack(pady=30)

        button_font = font.Font(family="Arial", size=16)

        difficulties = [
            ("🟢 Easy - Random moves", "easy"),
            ("🟡 Medium - Mixed strategy", "medium"),
            ("🔴 Hard - Unbeatable AI", "hard")
        ]

        for text, diff in difficulties:
            btn = tk.Button(main_frame, text=text, font=button_font,
                           bg=self.theme['button'], fg=self.theme['text'],
                           activebackground=self.theme['hover'],
                           width=25, height=2,
                           command=lambda d=diff: self.start_single_player(d))
            btn.pack(pady=12)

        back_btn = tk.Button(main_frame, text="Back", font=button_font,
                            bg=self.theme['button'], fg=self.theme['text'],
                            activebackground=self.theme['hover'],
                            width=25, height=2,
                            command=self.setup_menu_screen)
        back_btn.pack(pady=12)

    def start_single_player(self, difficulty):
        """Start single player game"""
        self.game_mode = 'single'
        self.difficulty = difficulty
        self.setup_game_screen()

    def start_two_player(self):
        """Start two player game"""
        self.game_mode = 'two'
        self.setup_game_screen()

    def setup_game_screen(self):
        """Setup the game board"""
        self.clear_window()
        self.root.geometry("")
        self.board = self.create_board()
        self.current_player = 'X'
        self.game_active = True
        self.buttons = []
        self.move_history = []

        main_frame = tk.Frame(self.root, bg=self.theme['bg'], padx=30, pady=20)
        main_frame.pack(fill='both', expand=True)

        # Status label
        status_font = font.Font(family="Arial", size=20, weight="bold")
        self.status_label = tk.Label(main_frame, text=self.get_status_text(),
                                     font=status_font, bg=self.theme['bg'],
                                     fg=self.theme['accent'])
        self.status_label.pack(pady=15)

        # Game board
        board_frame = tk.Frame(main_frame, bg=self.theme['bg'])
        board_frame.pack(pady=15)

        # Calculate button size based on board size
        button_width = 6 if self.board_size == 3 else 4
        button_height = 3 if self.board_size == 3 else 2
        font_size = 48 if self.board_size == 3 else 32

        button_font = font.Font(family="Arial", size=font_size, weight="bold")

        for i in range(self.board_size):
            row_buttons = []
            for j in range(self.board_size):
                btn = tk.Button(board_frame, text="", font=button_font,
                              width=button_width, height=button_height,
                              bg=self.theme['button'], fg=self.theme['text'],
                              activebackground=self.theme['hover'],
                              command=lambda row=i, col=j: self.on_cell_click(row, col))
                btn.grid(row=i, column=j, padx=4, pady=4)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)

        # Control buttons
        control_frame = tk.Frame(main_frame, bg=self.theme['bg'])
        control_frame.pack(pady=20)

        control_font = font.Font(family="Arial", size=13)

        new_game_btn = tk.Button(control_frame, text="New Game",
                                font=control_font, bg="#27ae60", fg="white",
                                activebackground="#229954",
                                width=12, height=2,
                                command=self.reset_game)
        new_game_btn.grid(row=0, column=0, padx=8)

        undo_btn = tk.Button(control_frame, text="Undo",
                            font=control_font, bg=self.theme['button'],
                            fg=self.theme['text'],
                            activebackground=self.theme['hover'],
                            width=12, height=2,
                            command=self.undo_move)
        undo_btn.grid(row=0, column=1, padx=8)

        menu_btn = tk.Button(control_frame, text="Main Menu",
                           font=control_font, bg=self.theme['button'],
                           fg=self.theme['text'],
                           activebackground=self.theme['hover'],
                           width=12, height=2,
                           command=self.setup_menu_screen)
        menu_btn.grid(row=0, column=2, padx=8)

        self.root.update_idletasks()

        # Bind keyboard controls (numpad 1-9 and number keys)
        self.root.bind('1', lambda e: self.keyboard_move(0, 0))
        self.root.bind('2', lambda e: self.keyboard_move(0, 1))
        self.root.bind('3', lambda e: self.keyboard_move(0, 2))
        self.root.bind('4', lambda e: self.keyboard_move(1, 0))
        self.root.bind('5', lambda e: self.keyboard_move(1, 1))
        self.root.bind('6', lambda e: self.keyboard_move(1, 2))
        self.root.bind('7', lambda e: self.keyboard_move(2, 0))
        self.root.bind('8', lambda e: self.keyboard_move(2, 1))
        self.root.bind('9', lambda e: self.keyboard_move(2, 2))

    def keyboard_move(self, row, col):
        """Handle keyboard moves"""
        if self.game_active and self.game_mode == 'single' and self.current_player == 'X':
            self.on_cell_click(row, col)
        elif self.game_active and self.game_mode == 'two':
            self.on_cell_click(row, col)

    def get_status_text(self):
        """Get status message"""
        if not self.game_active:
            return "Game Over"
        if self.game_mode == 'single':
            return "Your turn (X)" if self.current_player == 'X' else "AI's turn (O)"
        else:
            return f"Player {self.current_player}'s turn"

    def on_cell_click(self, row, col):
        """Handle cell click"""
        if not self.game_active or self.board[row][col] != ' ':
            return

        if self.game_mode == 'single' and self.current_player != 'X':
            return

        self.play_sound()
        self.move_history.append((row, col, self.current_player))
        self.make_move(row, col, self.current_player)

        if self.check_game_end():
            return

        self.current_player = 'O' if self.current_player == 'X' else 'X'
        self.status_label.config(text=self.get_status_text())

        if self.game_mode == 'single' and self.current_player == 'O' and self.game_active:
            self.root.after(800, self.ai_move)

    def make_move(self, row, col, player):
        """Make a move"""
        self.board[row][col] = player
        color = self.theme['x_color'] if player == 'X' else self.theme['o_color']
        self.buttons[row][col].config(text=player, fg=color, disabledforeground=color)
        self.buttons[row][col].config(state='disabled')

    def ai_move(self):
        """AI makes a move"""
        if not self.game_active:
            return

        move = self.get_ai_move(self.board)
        if move:
            row, col = move
            self.play_sound()
            self.move_history.append((row, col, 'O'))
            self.make_move(row, col, 'O')

            if self.check_game_end():
                return

            self.current_player = 'X'
            self.status_label.config(text=self.get_status_text())

    def check_game_end(self):
        """Check if game ended"""
        if self.check_winner(self.board, self.current_player):
            self.game_active = False
            self.highlight_winner()

            if self.game_mode == 'single':
                if self.current_player == 'X':
                    msg = "🎉 You win! Congratulations!"
                    self.stats.record_game_result('single', self.difficulty, 'wins')
                else:
                    msg = "AI wins! Try again!"
                    self.stats.record_game_result('single', self.difficulty, 'losses')
            else:
                msg = f"🎉 Player {self.current_player} wins!"

            self.status_label.config(text=msg, fg=self.theme['win_color'])
            self.root.after(1500, lambda: messagebox.showinfo("Game Over", msg))
            return True

        if self.is_board_full(self.board):
            self.game_active = False
            msg = "It's a draw!"
            if self.game_mode == 'single':
                self.stats.record_game_result('single', self.difficulty, 'draws')
            self.status_label.config(text=msg, fg=self.theme['accent'])
            self.root.after(1500, lambda: messagebox.showinfo("Game Over", msg))
            return True

        return False

    def highlight_winner(self):
        """Highlight winning line"""
        player = self.current_player

        # Check rows
        for i in range(self.board_size):
            if all(self.board[i][j] == player for j in range(self.board_size)):
                for j in range(self.board_size):
                    self.buttons[i][j].config(bg=self.theme['win_color'])
                return

        # Check columns
        for j in range(self.board_size):
            if all(self.board[i][j] == player for i in range(self.board_size)):
                for i in range(self.board_size):
                    self.buttons[i][j].config(bg=self.theme['win_color'])
                return

        # Check diagonals
        if all(self.board[i][i] == player for i in range(self.board_size)):
            for i in range(self.board_size):
                self.buttons[i][i].config(bg=self.theme['win_color'])
            return

        if all(self.board[i][self.board_size-1-i] == player for i in range(self.board_size)):
            for i in range(self.board_size):
                self.buttons[i][self.board_size-1-i].config(bg=self.theme['win_color'])

    def undo_move(self):
        """Undo the last move"""
        if not self.move_history or not self.game_active:
            return

        row, col, player = self.move_history.pop()
        self.board[row][col] = ' '
        self.buttons[row][col].config(text='', bg=self.theme['button'], state='normal')

        if self.move_history:
            row, col, player = self.move_history[-1]
            self.current_player = 'O' if player == 'X' else 'X'
        else:
            self.current_player = 'X'

        self.status_label.config(text=self.get_status_text())

    def reset_game(self):
        """Reset current game"""
        self.setup_game_screen()

    def clear_window(self):
        """Clear all widgets"""
        for widget in self.root.winfo_children():
            widget.destroy()

    # Game logic methods

    def check_winner(self, board, player):
        """Check if player won"""
        # Rows
        for i in range(self.board_size):
            if all(board[i][j] == player for j in range(self.board_size)):
                return True

        # Columns
        for j in range(self.board_size):
            if all(board[i][j] == player for i in range(self.board_size)):
                return True

        # Diagonals
        if all(board[i][i] == player for i in range(self.board_size)):
            return True

        if all(board[i][self.board_size-1-i] == player for i in range(self.board_size)):
            return True

        return False

    def is_board_full(self, board):
        """Check if board is full"""
        return all(cell != ' ' for row in board for cell in row)

    def get_available_moves(self, board):
        """Get available moves"""
        moves = []
        for i in range(self.board_size):
            for j in range(self.board_size):
                if board[i][j] == ' ':
                    moves.append((i, j))
        return moves

    def minimax(self, board, depth, is_maximizing):
        """Minimax algorithm"""
        if self.check_winner(board, 'O'):
            return 10 - depth
        if self.check_winner(board, 'X'):
            return depth - 10
        if self.is_board_full(board):
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for row, col in self.get_available_moves(board):
                board[row][col] = 'O'
                score = self.minimax(board, depth + 1, False)
                board[row][col] = ' '
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for row, col in self.get_available_moves(board):
                board[row][col] = 'X'
                score = self.minimax(board, depth + 1, True)
                board[row][col] = ' '
                best_score = min(score, best_score)
            return best_score

    def get_ai_move(self, board):
        """Get AI move"""
        available = self.get_available_moves(board)

        if not available:
            return None

        # Easy: random
        if self.difficulty == 'easy':
            return random.choice(available)

        # Medium: 50% random
        if self.difficulty == 'medium' and random.random() < 0.5:
            return random.choice(available)

        # Hard: minimax
        best_score = -float('inf')
        best_move = None

        for row, col in available:
            board[row][col] = 'O'
            score = self.minimax(board, 0, False)
            board[row][col] = ' '

            if score > best_score:
                best_score = score
                best_move = (row, col)

        return best_move if best_move else available[0]


def main():
    """Run the enhanced game"""
    root = tk.Tk()
    game = TicTacToeEnhanced(root)
    root.mainloop()


if __name__ == "__main__":
    main()
