#!/usr/bin/env python3
"""
Tic-Tac-Toe PRO - Professional Edition
Epic enhancement with Game Replays, Challenges, Tournament Mode, and AI Analysis!
"""

import tkinter as tk
from tkinter import messagebox, font, scrolledtext
import random
import json
import os
from datetime import datetime
import time


class GameStats:
    """Handle game statistics and persistence with move tracking"""

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
            'elo_rating': 1500,
            'blitz_wins': 0,
            'blitz_losses': 0,
            'blitz_draws': 0,
            'speed_challenge_best': 0,
            'theme': 'dark',
            'sound_enabled': True,
            'board_size': 3,
            'ai_speed': 'normal',
            'show_hints': True,
            'total_time_played': 0,
            'games_history': [],
            'challenges_completed': 0,
            'tournament_wins': 0,
            'daily_challenge_streak': 0,
            'daily_challenge_best_streak': 0,
            'last_daily_completed': None,
            'daily_challenges_total': 0,
            'top_games': [],
            'achievements': {
                'first_win': False,
                'five_wins': False,
                'ten_wins': False,
                'perfect_game': False,
                'beat_hard': False,
                'speed_demon': False,
                'win_streak_5': False,
                'win_streak_10': False,
                'challenge_master': False,
                'tournament_winner': False,
                'perfect_replay': False,
                'daily_devotee': False,
                'week_warrior': False,
                'blitz_master': False,
                'speed_runner': False
            }
        }

    def save_stats(self):
        """Save statistics to file"""
        with open(self.filename, 'w') as f:
            json.dump(self.stats, f, indent=2)

    def record_game_result(self, mode, difficulty, result, duration=0, board_size=3, moves=None, practice=False):
        """Record a game result with full move history"""
        if not practice:
            if mode == 'single':
                key_base = f'single_{difficulty}'
                self.stats[f'{key_base}_{result}'] = self.stats.get(f'{key_base}_{result}', 0) + 1

                if result == 'wins':
                    self.stats['current_streak'] = self.stats.get('current_streak', 0) + 1
                    self.stats['best_streak'] = max(self.stats['best_streak'], self.stats['current_streak'])

                    # Check achievements
                    total_wins = sum(v for k, v in self.stats.items() if 'wins' in k)

                    if total_wins == 1:
                        self.stats['achievements']['first_win'] = True
                    if total_wins == 5:
                        self.stats['achievements']['five_wins'] = True
                    if total_wins == 10:
                        self.stats['achievements']['ten_wins'] = True
                    if difficulty == 'hard':
                        self.stats['achievements']['beat_hard'] = True
                    if self.stats['current_streak'] >= 5:
                        self.stats['achievements']['win_streak_5'] = True
                    if self.stats['current_streak'] >= 10:
                        self.stats['achievements']['win_streak_10'] = True
                    if duration < 30 and board_size == 3:
                        self.stats['achievements']['speed_demon'] = True
                else:
                    self.stats['current_streak'] = 0
            else:
                self.stats['two_player_total'] = self.stats.get('two_player_total', 0) + 1

            self.stats['total_games'] = self.stats.get('total_games', 0) + 1
            self.stats['total_time_played'] = self.stats.get('total_time_played', 0) + duration

        # Track game in history with full move record
        game_record = {
            'timestamp': datetime.now().isoformat(),
            'mode': mode,
            'difficulty': difficulty,
            'result': result,
            'duration': duration,
            'board_size': board_size,
            'moves': moves or [],
            'practice': practice
        }
        if 'games_history' not in self.stats:
            self.stats['games_history'] = []
        self.stats['games_history'].append(game_record)

        # Keep only last 100 games in history
        if len(self.stats['games_history']) > 100:
            self.stats['games_history'] = self.stats['games_history'][-100:]

        self.save_stats()

    def get_stats_display(self):
        """Get formatted statistics for display"""
        easy_wins = self.stats.get('single_easy_wins', 0)
        easy_games = easy_wins + self.stats.get('single_easy_losses', 0) + self.stats.get('single_easy_draws', 0)

        medium_wins = self.stats.get('single_medium_wins', 0)
        medium_games = medium_wins + self.stats.get('single_medium_losses', 0) + self.stats.get('single_medium_draws', 0)

        hard_wins = self.stats.get('single_hard_wins', 0)
        hard_games = hard_wins + self.stats.get('single_hard_losses', 0) + self.stats.get('single_hard_draws', 0)

        total_time_hours = self.stats.get('total_time_played', 0) // 3600
        total_time_mins = (self.stats.get('total_time_played', 0) % 3600) // 60

        return {
            'total_games': self.stats.get('total_games', 0),
            'total_time': f"{total_time_hours}h {total_time_mins}m",
            'easy_games': easy_games,
            'easy_wins': easy_wins,
            'easy_rate': round(100 * easy_wins / max(easy_games, 1)),
            'medium_games': medium_games,
            'medium_wins': medium_wins,
            'medium_rate': round(100 * medium_wins / max(medium_games, 1)),
            'hard_games': hard_games,
            'hard_wins': hard_wins,
            'hard_rate': round(100 * hard_wins / max(hard_games, 1)),
            'current_streak': self.stats.get('current_streak', 0),
            'best_streak': self.stats.get('best_streak', 0),
            'challenges_completed': self.stats.get('challenges_completed', 0),
            'tournament_wins': self.stats.get('tournament_wins', 0)
        }

    def update_elo(self, result, opponent_elo=1500):
        """Update ELO rating based on game result"""
        current_elo = self.stats.get('elo_rating', 1500)
        k_factor = 32  # Standard K-factor

        # Expected score
        expected = 1 / (1 + 10 ** ((opponent_elo - current_elo) / 400))

        # Actual score (1 for win, 0.5 for draw, 0 for loss)
        if result == 'wins':
            actual = 1
        elif result == 'draws':
            actual = 0.5
        else:
            actual = 0

        # New ELO
        new_elo = current_elo + k_factor * (actual - expected)
        self.stats['elo_rating'] = max(800, round(new_elo))
        self.save_stats()
        return self.stats['elo_rating']

    def add_top_game(self, game_data):
        """Add game to top games leaderboard"""
        top_games = self.stats.get('top_games', [])
        top_games.append(game_data)
        # Sort by score (lowest = best play assuming fast wins are better)
        top_games.sort(key=lambda g: g.get('score', float('inf')))
        # Keep only top 10
        self.stats['top_games'] = top_games[:10]
        self.save_stats()

    def get_leaderboard(self):
        """Get formatted leaderboard data"""
        top_games = self.stats.get('top_games', [])
        return {
            'elo_rating': self.stats.get('elo_rating', 1500),
            'blitz_wins': self.stats.get('blitz_wins', 0),
            'blitz_losses': self.stats.get('blitz_losses', 0),
            'blitz_draws': self.stats.get('blitz_draws', 0),
            'speed_best': self.stats.get('speed_challenge_best', 0),
            'top_games': top_games
        }


class TicTacToeProLevel:
    """Challenge level definition"""
    def __init__(self, name, board, player_to_move='X', goal="Win in 3 moves or less"):
        self.name = name
        self.board = [row[:] for row in board]  # Deep copy
        self.player_to_move = player_to_move
        self.goal = goal

    def copy_board(self):
        return [row[:] for row in self.board]


class TicTacToePro:
    """Professional Tic-Tac-Toe with replays, challenges, tournament, and analysis"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tic-Tac-Toe PRO - Professional Edition")
        self.root.configure(bg='#1a1a1a')
        self.root.minsize(800, 750)

        self.stats = GameStats()

        # Themes
        self.themes = {
            'dark': {
                'bg': '#1a1a1a',
                'button': '#2d2d2d',
                'hover': '#404040',
                'text': '#ffffff',
                'x_color': '#ff6b6b',
                'o_color': '#4ecdc4',
                'win_color': '#51cf66',
                'accent': '#ffd93d'
            },
            'light': {
                'bg': '#f5f5f5',
                'button': '#e0e0e0',
                'hover': '#d0d0d0',
                'text': '#333333',
                'x_color': '#e74c3c',
                'o_color': '#3498db',
                'win_color': '#27ae60',
                'accent': '#f39c12'
            },
            'neon': {
                'bg': '#0f0f1e',
                'button': '#1a1a3e',
                'hover': '#2d2d5f',
                'text': '#00ff88',
                'x_color': '#ff006e',
                'o_color': '#00d9ff',
                'win_color': '#00ff88',
                'accent': '#ffbe0b'
            }
        }
        self.current_theme = self.stats.stats.get('theme', 'dark')
        self.theme = self.themes[self.current_theme]

        # AI speed presets
        self.ai_speeds = {
            'instant': 0.1,
            'fast': 0.4,
            'normal': 0.8,
            'slow': 1.5,
            'thinking': 2.5
        }
        self.current_ai_speed = self.stats.stats.get('ai_speed', 'normal')

        # Game state variables
        self.board = None
        self.board_size = 3
        self.game_active = False
        self.current_player = 'X'
        self.game_mode = None
        self.difficulty = None
        self.human_player = 'X'
        self.ai_player = 'O'
        self.move_history = []
        self.undo_history = []
        self.game_start_time = None
        self.practice_mode = False

        # Replay and tournament state
        self.replay_mode = False
        self.current_replay = None
        self.replay_move_index = 0
        self.replay_info_label = None
        self.tournament_series = []
        self.tournament_results = []
        self.tournament_round = 0
        self.tournament_series_length = 0

        # Challenge puzzles
        self.challenge_levels = self.create_challenge_levels()
        self.current_challenge_index = 0

        # Setup UI
        self.setup_menu_screen()

    def create_challenge_levels(self):
        """Create challenge puzzles"""
        return [
            TicTacToeProLevel(
                "Easy Challenge 1: Win Now!",
                [['X', 'O', ' '],
                 ['X', ' ', ' '],
                 [' ', ' ', 'O']],
                'X',
                "Complete in 1 move - X can win immediately!"
            ),
            TicTacToeProLevel(
                "Easy Challenge 2: Block and Win",
                [['O', 'O', ' '],
                 ['X', 'X', ' '],
                 [' ', ' ', ' ']],
                'X',
                "O threatens on top row. Block it and also set up your own win!"
            ),
            TicTacToeProLevel(
                "Medium Challenge 1: Two Threats",
                [['X', ' ', ' '],
                 [' ', 'O', ' '],
                 [' ', ' ', 'X']],
                'X',
                "Create a position where X has TWO ways to win!"
            ),
            TicTacToeProLevel(
                "Medium Challenge 2: Tactical Defense",
                [['O', 'X', 'O'],
                 ['X', ' ', ' '],
                 [' ', ' ', ' ']],
                'X',
                "O is threatening the bottom. Defend AND create an opportunity!"
            ),
            TicTacToeProLevel(
                "Hard Challenge: Master Play",
                [['X', ' ', ' '],
                 ['O', 'X', ' '],
                 [' ', 'O', ' ']],
                'X',
                "Advanced puzzle - Find the winning strategy in 2-3 moves"
            ),
        ]

    def clear_window(self):
        """Clear all widgets from window"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def setup_menu_screen(self):
        """Create main menu"""
        self.clear_window()
        self.root.geometry("")

        main_frame = tk.Frame(self.root, bg=self.theme['bg'], padx=60, pady=40)
        main_frame.pack()

        title_font = font.Font(family="Arial", size=52, weight="bold")
        title = tk.Label(main_frame, text="Tic-Tac-Toe\nPRO", font=title_font,
                        bg=self.theme['bg'], fg=self.theme['accent'], justify='center')
        title.pack(pady=25)

        subtitle_font = font.Font(family="Arial", size=13)
        subtitle = tk.Label(main_frame, text="🚀 Professional Edition - Replays, Challenges & Tournaments",
                           font=subtitle_font, bg=self.theme['bg'], fg=self.theme['text'])
        subtitle.pack(pady=5)

        button_font = font.Font(family="Arial", size=15)

        buttons = [
            ("🎮 Play Game", self.choose_game_mode),
            ("⚡ Blitz Mode", self.setup_blitz_game),
            ("📅 Daily Challenge", self.play_daily_challenge),
            ("🎯 Challenge Mode", self.show_challenges),
            ("🏆 Tournament Mode", self.show_tournament_setup),
            ("📹 Game Replays", self.show_replays),
            ("🏅 Leaderboard", self.show_leaderboard),
            ("📊 Statistics", self.show_statistics),
            ("🏆 Achievements", self.show_achievements),
            ("⚙️ Settings", self.show_settings),
            ("ℹ️ How to Play", self.show_help),
            ("🚪 Quit", self.root.quit)
        ]

        for text, cmd in buttons:
            btn = tk.Button(main_frame, text=text, font=button_font,
                           bg=self.theme['button'], fg=self.theme['text'],
                           activebackground=self.theme['hover'],
                           width=26, height=2, command=cmd)
            btn.pack(pady=8)

    def choose_game_mode(self):
        """Choose between single player and two player"""
        self.clear_window()
        self.root.geometry("")

        main_frame = tk.Frame(self.root, bg=self.theme['bg'], padx=60, pady=40)
        main_frame.pack()

        title_font = font.Font(family="Arial", size=32, weight="bold")
        title = tk.Label(main_frame, text="Choose Game Mode", font=title_font,
                        bg=self.theme['bg'], fg=self.theme['accent'])
        title.pack(pady=25)

        button_font = font.Font(family="Arial", size=15)

        btn1 = tk.Button(main_frame, text="🤖 Single Player (vs AI)",
                        font=button_font, bg=self.theme['button'], fg=self.theme['text'],
                        activebackground=self.theme['hover'],
                        width=26, height=2,
                        command=lambda: (setattr(self, 'game_mode', 'single'), self.choose_difficulty()))
        btn1.pack(pady=10)

        btn2 = tk.Button(main_frame, text="👥 Two Players (Local)",
                        font=button_font, bg=self.theme['button'], fg=self.theme['text'],
                        activebackground=self.theme['hover'],
                        width=26, height=2,
                        command=lambda: (setattr(self, 'game_mode', 'two_player'), self.setup_game_screen()))
        btn2.pack(pady=10)

        back_btn = tk.Button(main_frame, text="← Back",
                            font=button_font, bg=self.theme['button'], fg=self.theme['text'],
                            activebackground=self.theme['hover'],
                            width=26, height=2,
                            command=self.setup_menu_screen)
        back_btn.pack(pady=10)

    def choose_difficulty(self):
        """Choose AI difficulty"""
        self.clear_window()
        self.root.geometry("")

        main_frame = tk.Frame(self.root, bg=self.theme['bg'], padx=60, pady=40)
        main_frame.pack()

        title_font = font.Font(family="Arial", size=32, weight="bold")
        title = tk.Label(main_frame, text="Choose Difficulty", font=title_font,
                        bg=self.theme['bg'], fg=self.theme['accent'])
        title.pack(pady=25)

        button_font = font.Font(family="Arial", size=15)

        difficulties = [
            ("🟢 Easy", "easy"),
            ("🟡 Medium", "medium"),
            ("🔴 Hard", "hard")
        ]

        for text, diff in difficulties:
            btn = tk.Button(main_frame, text=text,
                           font=button_font, bg=self.theme['button'], fg=self.theme['text'],
                           activebackground=self.theme['hover'],
                           width=26, height=2,
                           command=lambda d=diff: (setattr(self, 'difficulty', d), self.setup_game_screen()))
            btn.pack(pady=10)

        back_btn = tk.Button(main_frame, text="← Back",
                            font=button_font, bg=self.theme['button'], fg=self.theme['text'],
                            activebackground=self.theme['hover'],
                            width=26, height=2,
                            command=self.choose_game_mode)
        back_btn.pack(pady=10)

    def setup_game_screen(self):
        """Setup the game board"""
        self.clear_window()
        self.root.geometry("800x750")

        self.board = self.create_board()
        self.move_history = []
        self.undo_history = []
        self.game_active = True
        self.current_player = 'X'
        self.game_start_time = time.time()

        # Top frame for title and info
        top_frame = tk.Frame(self.root, bg=self.theme['bg'])
        top_frame.pack(fill='x', padx=10, pady=10)

        title_font = font.Font(family="Arial", size=20, weight="bold")
        if self.game_mode in ('single', 'blitz', 'daily_challenge'):
            if self.game_mode == 'blitz':
                mode_text = f"⚡ Blitz Mode - {self.difficulty.upper()} AI"
            elif self.game_mode == 'daily_challenge':
                mode_text = "📅 Daily Challenge"
            else:
                mode_text = f"Single Player - {self.difficulty.upper()} AI"
        else:
            mode_text = "Two Players"

        title = tk.Label(top_frame, text=mode_text, font=title_font,
                        bg=self.theme['bg'], fg=self.theme['accent'])
        title.pack()

        # Status label
        self.status_label = tk.Label(top_frame, text="X's Turn",
                                    font=("Arial", 14),
                                    bg=self.theme['bg'], fg=self.theme['text'])
        self.status_label.pack()

        # Board frame
        board_frame = tk.Frame(self.root, bg=self.theme['bg'])
        board_frame.pack(fill='both', expand=True, padx=10, pady=10)

        button_width = 6 if self.board_size == 3 else 4
        button_height = 3 if self.board_size == 3 else 2
        font_size = 48 if self.board_size == 3 else 32

        self.board_buttons = []
        for i in range(self.board_size):
            row_buttons = []
            for j in range(self.board_size):
                btn = tk.Button(board_frame, text='',
                               font=("Arial", font_size, "bold"),
                               bg=self.theme['button'],
                               fg=self.theme['x_color'],
                               activebackground=self.theme['hover'],
                               width=button_width, height=button_height,
                               command=lambda row=i, col=j: self.on_board_click(row, col))
                btn.grid(row=i, column=j, padx=5, pady=5, sticky='nsew')
                row_buttons.append(btn)
            self.board_buttons.append(row_buttons)

        # Control buttons frame
        ctrl_frame = tk.Frame(self.root, bg=self.theme['bg'])
        ctrl_frame.pack(fill='x', padx=10, pady=10)

        btn_font = font.Font(family="Arial", size=12)

        hint_btn = tk.Button(ctrl_frame, text="💡 Hint", font=btn_font,
                            bg=self.theme['button'], fg=self.theme['text'],
                            activebackground=self.theme['hover'],
                            command=self.show_hint)
        hint_btn.pack(side='left', padx=5)

        undo_btn = tk.Button(ctrl_frame, text="↩️ Undo", font=btn_font,
                            bg=self.theme['button'], fg=self.theme['text'],
                            activebackground=self.theme['hover'],
                            command=self.undo_move)
        undo_btn.pack(side='left', padx=5)

        analyze_btn = tk.Button(ctrl_frame, text="🔍 Analyze", font=btn_font,
                               bg=self.theme['button'], fg=self.theme['text'],
                               activebackground=self.theme['hover'],
                               command=self.analyze_position)
        analyze_btn.pack(side='left', padx=5)

        menu_btn = tk.Button(ctrl_frame, text="📋 Menu", font=btn_font,
                            bg=self.theme['button'], fg=self.theme['text'],
                            activebackground=self.theme['hover'],
                            command=self.save_and_return_menu)
        menu_btn.pack(side='right', padx=5)

        self.update_board_display()

        if self.game_mode in ('single', 'blitz', 'daily_challenge') and self.current_player == self.ai_player:
            self.root.after(500, self.make_ai_move)

    def create_board(self):
        """Create empty board"""
        return [[' ' for _ in range(self.board_size)] for _ in range(self.board_size)]

    def get_available_moves(self, board):
        """Get list of available moves"""
        moves = []
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == ' ':
                    moves.append((i, j))
        return moves

    def check_winner(self, board, player):
        """Check if player has won"""
        win_length = self.board_size

        # Check rows
        for row in board:
            for start in range(len(row) - win_length + 1):
                if all(row[start + i] == player for i in range(win_length)):
                    return True

        # Check columns
        for col in range(len(board[0])):
            for start in range(len(board) - win_length + 1):
                if all(board[start + i][col] == player for i in range(win_length)):
                    return True

        # Check diagonals
        for row_start in range(len(board) - win_length + 1):
            for col_start in range(len(board[0]) - win_length + 1):
                if all(board[row_start + i][col_start + i] == player for i in range(win_length)):
                    return True
                if all(board[row_start + i][col_start + win_length - 1 - i] == player for i in range(win_length)):
                    return True

        return False

    def board_full(self, board):
        """Check if board is full"""
        return all(cell != ' ' for row in board for cell in row)

    def minimax(self, board, depth, is_maximizing, alpha=float('-inf'), beta=float('inf')):
        """Minimax algorithm with alpha-beta pruning"""
        if self.check_winner(board, self.ai_player):
            return 10 - depth
        if self.check_winner(board, self.human_player):
            return depth - 10
        if self.board_full(board):
            return 0

        if is_maximizing:
            max_eval = float('-inf')
            for row, col in self.get_available_moves(board):
                board[row][col] = self.ai_player
                eval_score = self.minimax(board, depth + 1, False, alpha, beta)
                board[row][col] = ' '
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for row, col in self.get_available_moves(board):
                board[row][col] = self.human_player
                eval_score = self.minimax(board, depth + 1, True, alpha, beta)
                board[row][col] = ' '
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval

    def get_best_move(self, board):
        """Get best move using minimax"""
        best_score = float('-inf')
        best_moves = []

        for row, col in self.get_available_moves(board):
            board[row][col] = self.ai_player
            score = self.minimax(board, 0, False)
            board[row][col] = ' '

            if score > best_score:
                best_score = score
                best_moves = [(row, col)]
            elif score == best_score:
                best_moves.append((row, col))

        return random.choice(best_moves) if best_moves else None

    def make_ai_move(self):
        """Make AI move"""
        if not self.game_active:
            return

        if self.difficulty == 'easy':
            move = random.choice(self.get_available_moves(self.board))
        elif self.difficulty == 'medium':
            if random.random() < 0.5:
                move = random.choice(self.get_available_moves(self.board))
            else:
                move = self.get_best_move(self.board)
        else:  # hard
            move = self.get_best_move(self.board)

        if move:
            row, col = move
            self.board[row][col] = self.ai_player
            self.move_history.append((row, col, self.ai_player))
            self.update_board_display()

            if self.check_winner(self.board, self.ai_player):
                self.end_game('loss')
            elif self.board_full(self.board):
                self.end_game('draw')
            else:
                self.current_player = self.human_player

    def on_board_click(self, row, col):
        """Handle board click"""
        if not self.game_active or self.board[row][col] != ' ':
            return

        if self.game_mode in ('single', 'blitz', 'daily_challenge') and self.current_player != self.human_player:
            return

        self.board[row][col] = self.current_player
        self.move_history.append((row, col, self.current_player))
        self.update_board_display()

        if self.check_winner(self.board, self.current_player):
            self.end_game('win' if self.current_player == self.human_player else 'loss')
        elif self.board_full(self.board):
            self.end_game('draw')
        else:
            self.current_player = self.ai_player if self.game_mode in ('single', 'blitz', 'daily_challenge') else ('O' if self.current_player == 'X' else 'X')

            if self.game_mode in ('single', 'blitz', 'daily_challenge') and self.current_player == self.ai_player:
                self.root.after(500, self.make_ai_move)

    def update_board_display(self):
        """Update board display"""
        for i in range(self.board_size):
            for j in range(self.board_size):
                cell = self.board[i][j]
                color = self.theme['x_color'] if cell == 'X' else (self.theme['o_color'] if cell == 'O' else self.theme['text'])
                self.board_buttons[i][j].config(text=cell, fg=color)

        # Only update status label if it exists (not in replay mode)
        if hasattr(self, 'status_label') and self.status_label:
            self.status_label.config(text=f"{self.current_player}'s Turn")

    def show_hint(self):
        """Show hint for best move"""
        if self.current_player != self.human_player:
            messagebox.showinfo("Cannot Hint", "Hints only available during your turn!")
            return

        best_move = self.get_best_move(self.board)
        if best_move:
            row, col = best_move
            messagebox.showinfo("💡 Hint",
                              f"Best move: Position ({row+1}, {col+1})\n\nThis move maximizes your winning chances!")

    def undo_move(self):
        """Undo last move"""
        if len(self.move_history) < (2 if self.game_mode in ('single', 'blitz', 'daily_challenge') else 1):
            messagebox.showwarning("Cannot Undo", "No moves to undo!")
            return

        # Undo human move
        self.move_history.pop()
        row, col, _ = self.move_history.pop()
        self.board[row][col] = ' '

        # Undo AI move if playing against AI
        if self.game_mode in ('single', 'blitz', 'daily_challenge') and self.move_history:
            row, col, _ = self.move_history.pop()
            self.board[row][col] = ' '

        self.current_player = 'X'
        self.update_board_display()

    def save_and_return_menu(self):
        """Save game and return to menu"""
        if self.game_active:
            if messagebox.askyesno("Quit Game", "Are you sure? Current game will not be saved."):
                self.setup_menu_screen()
        else:
            self.setup_menu_screen()

    def end_game(self, result):
        """End the game"""
        from datetime import date

        self.game_active = False
        duration = int(time.time() - self.game_start_time)

        if self.game_mode == 'single':
            self.stats.record_game_result('single', self.difficulty, result, duration, self.board_size, self.move_history, self.practice_mode)
        elif self.game_mode == 'blitz':
            # Handle blitz game
            self.stats.record_game_result('single', self.difficulty, result, duration, self.board_size, self.move_history, False)
            # Update blitz stats
            if result == 'wins':
                self.stats.stats['blitz_wins'] = self.stats.stats.get('blitz_wins', 0) + 1
            elif result == 'losses':
                self.stats.stats['blitz_losses'] = self.stats.stats.get('blitz_losses', 0) + 1
            else:
                self.stats.stats['blitz_draws'] = self.stats.stats.get('blitz_draws', 0) + 1

            # Update ELO rating
            new_elo = self.stats.update_elo(result, 1500)

            # Check for blitz achievements
            if self.stats.stats.get('blitz_wins', 0) >= 5:
                self.stats.stats['achievements']['blitz_master'] = True
            if duration <= 15 and result == 'wins':
                self.stats.stats['achievements']['speed_runner'] = True

            # Add to top games if good time
            if duration <= 60:
                self.stats.add_top_game({
                    'duration': duration,
                    'mode': 'blitz',
                    'difficulty': self.difficulty,
                    'result': result,
                    'score': duration
                })

            self.stats.save_stats()
        elif self.game_mode == 'daily_challenge':
            # Handle daily challenge completion
            if result == 'win':
                today = str(date.today())
                last_completed = self.stats.stats.get('last_daily_completed')

                # Increment streak if continuing from yesterday, else reset if there was a gap
                if last_completed:
                    from datetime import datetime, timedelta
                    last_date = datetime.fromisoformat(last_completed).date()
                    today_date = date.today()
                    days_diff = (today_date - last_date).days

                    if days_diff == 1:
                        # Consecutive day, increment streak
                        self.stats.stats['daily_challenge_streak'] = self.stats.stats.get('daily_challenge_streak', 0) + 1
                    elif days_diff > 1:
                        # Streak broken, start new one
                        self.stats.stats['daily_challenge_streak'] = 1
                else:
                    # First daily challenge
                    self.stats.stats['daily_challenge_streak'] = 1

                # Update best streak
                current = self.stats.stats.get('daily_challenge_streak', 1)
                best = self.stats.stats.get('daily_challenge_best_streak', 0)
                self.stats.stats['daily_challenge_best_streak'] = max(current, best)

                # Mark as completed today
                self.stats.stats['last_daily_completed'] = today
                self.stats.stats['daily_challenges_total'] = self.stats.stats.get('daily_challenges_total', 0) + 1

                # Check for achievements
                if current >= 7:
                    self.stats.stats['achievements']['week_warrior'] = True
                if current >= 1:
                    self.stats.stats['achievements']['daily_devotee'] = True

                self.stats.save_stats()
        else:
            self.stats.record_game_result('two_player', 'n/a', result, duration, self.board_size, self.move_history)

        if result == 'win':
            self.status_label.config(text="🎉 YOU WIN!", fg=self.theme['win_color'])
            if self.game_mode == 'blitz':
                elo = self.stats.stats.get('elo_rating', 1500)
                messagebox.showinfo("Blitz Victory! ⚡",
                                  f"🎉 You won!\n\n"
                                  f"Time: {duration}s\n"
                                  f"ELO Rating: {elo}\n\n"
                                  f"Great speed play!")
            elif self.game_mode == 'daily_challenge':
                streak = self.stats.stats.get('daily_challenge_streak', 1)
                best = self.stats.stats.get('daily_challenge_best_streak', 1)
                messagebox.showinfo("Daily Challenge Complete! 📅",
                                  f"🎉 Congratulations!\n\n"
                                  f"Current Streak: {streak} days 🔥\n"
                                  f"Best Streak: {best} days\n\n"
                                  f"Come back tomorrow for your next challenge!")
            else:
                messagebox.showinfo("Victory!", "Congratulations! You won!")
        elif result == 'loss':
            self.status_label.config(text="😔 YOU LOST", fg=self.theme['x_color'])
            if self.game_mode == 'blitz':
                elo = self.stats.stats.get('elo_rating', 1500)
                messagebox.showinfo("Blitz Defeat",
                                  f"❌ AI won!\n\n"
                                  f"Time: {duration}s\n"
                                  f"ELO Rating: {elo}\n\n"
                                  f"Try again for a faster win!")
            elif self.game_mode == 'daily_challenge':
                messagebox.showinfo("Challenge Failed",
                                  "❌ Oops! You lost.\n\n"
                                  "Try again tomorrow with a fresh perspective!")
            else:
                messagebox.showinfo("Defeat", "The AI won. Better luck next time!")
        else:
            self.status_label.config(text="🤝 DRAW", fg=self.theme['accent'])
            messagebox.showinfo("Draw", "It's a tie!")

        self.root.after(1500, self.setup_menu_screen)


    def show_replays(self):
        """Show saved game replays"""
        self.clear_window()
        self.root.geometry("")

        main_frame = tk.Frame(self.root, bg=self.theme['bg'], padx=40, pady=25)
        main_frame.pack(fill='both', expand=True)

        title_font = font.Font(family="Arial", size=28, weight="bold")
        title = tk.Label(main_frame, text="📹 Game Replays", font=title_font,
                        bg=self.theme['bg'], fg=self.theme['accent'])
        title.pack(pady=15)

        games = self.stats.stats.get('games_history', [])
        if not games:
            info = tk.Label(main_frame, text="No game replays available yet.\nPlay some games to see them here!",
                           font=("Arial", 14), bg=self.theme['bg'], fg=self.theme['text'])
            info.pack(pady=30)
        else:
            # Create frame for games list with radio buttons
            list_frame = tk.Frame(main_frame, bg=self.theme['bg'])
            list_frame.pack(pady=15, fill='both', expand=True)

            # Scrollbar
            scrollbar = tk.Scrollbar(list_frame, bg=self.theme['button'])
            scrollbar.pack(side='right', fill='y')

            # Canvas and frame inside for scrolling
            canvas = tk.Canvas(list_frame, bg=self.theme['button'], highlightthickness=0, yscrollcommand=scrollbar.set)
            canvas.pack(side='left', fill='both', expand=True)
            scrollbar.config(command=canvas.yview)

            scrollable_frame = tk.Frame(canvas, bg=self.theme['button'])
            canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')

            self.selected_replay = tk.IntVar()
            game_list = list(reversed(games[-10:]))  # Show last 10 games in reverse order

            for idx, game in enumerate(game_list):
                timestamp = datetime.fromisoformat(game['timestamp']).strftime("%Y-%m-%d %H:%M")
                mode = game['mode']
                result = game['result'].upper()
                duration = game['duration']
                moves_count = len(game.get('moves', []))

                game_text = f"{timestamp} | {mode.title()} | {result} | {duration}s | Moves: {moves_count}"

                radio_btn = tk.Radiobutton(scrollable_frame, text=game_text, variable=self.selected_replay,
                                          value=idx, bg=self.theme['button'], fg=self.theme['text'],
                                          selectcolor=self.theme['accent'], font=("Arial", 11))
                radio_btn.pack(anchor='w', padx=10, pady=5)

            scrollable_frame.update_idletasks()
            canvas.config(scrollregion=canvas.bbox('all'))

            btn_font = font.Font(family="Arial", size=12)
            replay_btn = tk.Button(main_frame, text="▶️ Play Selected Replay", font=btn_font,
                                  bg=self.theme['button'], fg=self.theme['text'],
                                  activebackground=self.theme['hover'],
                                  command=lambda: self.play_replay(game_list))
            replay_btn.pack(pady=10)

        back_btn = tk.Button(main_frame, text="← Back",
                            font=("Arial", 12), bg=self.theme['button'], fg=self.theme['text'],
                            activebackground=self.theme['hover'],
                            width=20, height=2,
                            command=self.setup_menu_screen)
        back_btn.pack(pady=10)

    def play_replay(self, game_list):
        """Play selected game replay"""
        try:
            selected_idx = self.selected_replay.get()
            if selected_idx < 0 or selected_idx >= len(game_list):
                messagebox.showwarning("No Selection", "Please select a game to replay!")
                return

            game = game_list[selected_idx]
            moves = game.get('moves', [])

            if not moves:
                messagebox.showwarning("No Moves", "This game has no moves to replay.")
                return

            # Setup replay state
            self.replay_mode = True
            self.current_replay = game
            self.replay_move_index = 0
            self.board_size = game.get('board_size', 3)
            self.board = self.create_board()
            self.move_history = []
            self.game_active = True
            self.current_player = 'X'
            self.human_player = 'X'
            self.ai_player = 'O'

            # Setup UI
            self.clear_window()
            self.root.geometry("800x750")
            self.setup_replay_screen(moves)
        except Exception as e:
            messagebox.showerror("Replay Error", f"Error playing replay: {str(e)}")

    def setup_replay_screen(self, moves):
        """Setup screen for replay with playback controls"""
        # Top frame for title
        top_frame = tk.Frame(self.root, bg=self.theme['bg'])
        top_frame.pack(fill='x', padx=10, pady=10)

        title_font = font.Font(family="Arial", size=20, weight="bold")
        title = tk.Label(top_frame, text="📹 Game Replay", font=title_font,
                        bg=self.theme['bg'], fg=self.theme['accent'])
        title.pack()

        info_text = f"Replay: {len(moves)} moves | Move: {self.replay_move_index}/{len(moves)}"
        self.replay_info_label = tk.Label(top_frame, text=info_text, font=("Arial", 12),
                                          bg=self.theme['bg'], fg=self.theme['text'])
        self.replay_info_label.pack()

        # Status label to show current state
        self.status_label = tk.Label(top_frame, text="", font=("Arial", 11),
                                    bg=self.theme['bg'], fg=self.theme['accent'])
        self.status_label.pack()

        # Board frame
        board_frame = tk.Frame(self.root, bg=self.theme['bg'])
        board_frame.pack(pady=20)

        self.board_buttons = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]
        btn_size = 8
        btn_font = font.Font(family="Arial", size=16, weight="bold")

        for i in range(self.board_size):
            for j in range(self.board_size):
                btn = tk.Button(board_frame, text=" ", font=btn_font, width=btn_size, height=3,
                               bg=self.theme['button'], fg=self.theme['text'],
                               state='disabled')
                btn.grid(row=i, column=j, padx=5, pady=5)
                self.board_buttons[i][j] = btn

        # Control frame
        ctrl_frame = tk.Frame(self.root, bg=self.theme['bg'])
        ctrl_frame.pack(pady=15)

        btn_font = font.Font(family="Arial", size=11)
        tk.Button(ctrl_frame, text="⏮️ Start", font=btn_font,
                 bg=self.theme['button'], fg=self.theme['text'],
                 activebackground=self.theme['hover'],
                 command=self.replay_start).pack(side='left', padx=5)

        tk.Button(ctrl_frame, text="⏪ Previous", font=btn_font,
                 bg=self.theme['button'], fg=self.theme['text'],
                 activebackground=self.theme['hover'],
                 command=self.replay_previous).pack(side='left', padx=5)

        tk.Button(ctrl_frame, text="▶️ Play All", font=btn_font,
                 bg=self.theme['button'], fg=self.theme['text'],
                 activebackground=self.theme['hover'],
                 command=lambda: self.replay_auto(moves)).pack(side='left', padx=5)

        tk.Button(ctrl_frame, text="⏩ Next", font=btn_font,
                 bg=self.theme['button'], fg=self.theme['text'],
                 activebackground=self.theme['hover'],
                 command=self.replay_next).pack(side='left', padx=5)

        tk.Button(ctrl_frame, text="⏭️ End", font=btn_font,
                 bg=self.theme['button'], fg=self.theme['text'],
                 activebackground=self.theme['hover'],
                 command=lambda: self.replay_end(moves)).pack(side='left', padx=5)

        tk.Button(ctrl_frame, text="← Back", font=btn_font,
                 bg=self.theme['button'], fg=self.theme['text'],
                 activebackground=self.theme['hover'],
                 command=self.show_replays).pack(side='right', padx=5)

        self.update_board_display()

    def replay_start(self):
        """Start replay from beginning"""
        self.replay_move_index = 0
        self.board = self.create_board()
        self.move_history = []
        self.update_board_display()
        self.update_replay_info()

    def replay_previous(self):
        """Go to previous move in replay"""
        if self.replay_move_index > 0:
            self.replay_move_index -= 1
            self.board = self.create_board()
            self.move_history = []
            # Replay moves up to current index
            moves = self.current_replay.get('moves', [])
            for i in range(self.replay_move_index):
                if i < len(moves):
                    row, col, player = moves[i]
                    self.board[row][col] = player
                    self.move_history.append((row, col, player))
            self.update_board_display()
            self.update_replay_info()

    def replay_next(self):
        """Go to next move in replay"""
        moves = self.current_replay.get('moves', [])
        if self.replay_move_index < len(moves):
            row, col, player = moves[self.replay_move_index]
            self.board[row][col] = player
            self.move_history.append((row, col, player))
            self.replay_move_index += 1
            self.update_board_display()
            self.update_replay_info()

    def replay_end(self, moves):
        """Go to end of replay"""
        self.replay_move_index = len(moves)
        self.board = self.create_board()
        self.move_history = []
        # Replay all moves
        for row, col, player in moves:
            self.board[row][col] = player
            self.move_history.append((row, col, player))
        self.update_board_display()
        self.update_replay_info()

    def replay_auto(self, moves):
        """Auto-play all moves in replay"""
        if self.replay_move_index == 0:
            self.board = self.create_board()
            self.move_history = []

        if self.replay_move_index < len(moves):
            row, col, player = moves[self.replay_move_index]
            self.board[row][col] = player
            self.move_history.append((row, col, player))
            self.replay_move_index += 1
            self.update_board_display()
            self.update_replay_info()
            self.root.after(500, lambda: self.replay_auto(moves))

    def update_replay_info(self):
        """Update replay info label"""
        if self.current_replay:
            moves = self.current_replay.get('moves', [])
            info_text = f"Replay: {len(moves)} moves | Move: {self.replay_move_index}/{len(moves)}"
            self.replay_info_label.config(text=info_text)

    def show_challenges(self):
        """Show challenge mode"""
        self.clear_window()
        self.root.geometry("")

        main_frame = tk.Frame(self.root, bg=self.theme['bg'], padx=40, pady=25)
        main_frame.pack(fill='both', expand=True)

        title_font = font.Font(family="Arial", size=28, weight="bold")
        title = tk.Label(main_frame, text="🎯 Challenge Mode", font=title_font,
                        bg=self.theme['bg'], fg=self.theme['accent'])
        title.pack(pady=15)

        info_font = font.Font(family="Arial", size=12)
        info = tk.Label(main_frame, text=f"Completed: {self.stats.stats.get('challenges_completed', 0)}/5",
                       font=info_font, bg=self.theme['bg'], fg=self.theme['text'])
        info.pack(pady=10)

        btn_font = font.Font(family="Arial", size=13)
        for idx, challenge in enumerate(self.challenge_levels):
            status = "✅" if idx < self.stats.stats.get('challenges_completed', 0) else "🔒"
            btn = tk.Button(main_frame, text=f"{status} {challenge.name}",
                           font=btn_font, bg=self.theme['button'], fg=self.theme['text'],
                           activebackground=self.theme['hover'],
                           width=50, height=2,
                           command=lambda i=idx: self.play_challenge(i))
            btn.pack(pady=8)

        back_btn = tk.Button(main_frame, text="← Back",
                            font=btn_font, bg=self.theme['button'], fg=self.theme['text'],
                            activebackground=self.theme['hover'],
                            width=50, height=2,
                            command=self.setup_menu_screen)
        back_btn.pack(pady=15)

    def play_challenge(self, index):
        """Play a specific challenge"""
        self.current_challenge_index = index
        challenge = self.challenge_levels[index]
        self.board = challenge.copy_board()
        self.game_mode = 'challenge'
        self.move_history = []
        self.game_active = True
        self.current_player = challenge.player_to_move
        self.human_player = challenge.player_to_move
        self.ai_player = 'O' if challenge.player_to_move == 'X' else 'X'
        self.game_start_time = time.time()

        self.clear_window()
        self.root.geometry("800x750")

        # Top frame
        top_frame = tk.Frame(self.root, bg=self.theme['bg'])
        top_frame.pack(fill='x', padx=10, pady=10)

        title_font = font.Font(family="Arial", size=18, weight="bold")
        title = tk.Label(top_frame, text=challenge.name, font=title_font,
                        bg=self.theme['bg'], fg=self.theme['accent'])
        title.pack()

        goal_font = font.Font(family="Arial", size=11)
        goal = tk.Label(top_frame, text=challenge.goal, font=goal_font,
                       bg=self.theme['bg'], fg=self.theme['text'])
        goal.pack()

        self.status_label = tk.Label(top_frame, text=f"{self.current_player}'s Turn",
                                    font=("Arial", 14),
                                    bg=self.theme['bg'], fg=self.theme['text'])
        self.status_label.pack()

        # Board
        board_frame = tk.Frame(self.root, bg=self.theme['bg'])
        board_frame.pack(fill='both', expand=True, padx=10, pady=10)

        self.board_buttons = []
        for i in range(3):
            row_buttons = []
            for j in range(3):
                btn = tk.Button(board_frame, text=self.board[i][j] if self.board[i][j] != ' ' else '',
                               font=("Arial", 48, "bold"),
                               bg=self.theme['button'],
                               fg=self.theme['x_color'] if self.board[i][j] == 'X' else (self.theme['o_color'] if self.board[i][j] == 'O' else self.theme['text']),
                               activebackground=self.theme['hover'],
                               width=6, height=3,
                               command=lambda row=i, col=j: self.on_board_click(row, col))
                btn.grid(row=i, column=j, padx=5, pady=5, sticky='nsew')
                row_buttons.append(btn)
            self.board_buttons.append(row_buttons)

    def get_daily_challenge_index(self):
        """Get today's daily challenge index based on date"""
        from datetime import datetime
        day_of_year = datetime.now().timetuple().tm_yday
        return (day_of_year - 1) % len(self.challenge_levels)

    def play_daily_challenge(self):
        """Play today's daily challenge"""
        from datetime import date
        today = str(date.today())
        last_completed = self.stats.stats.get('last_daily_completed')

        # Check if already completed today
        if last_completed == today:
            messagebox.showinfo("Already Completed",
                              f"✅ You've already completed today's challenge!\n\n"
                              f"Current Streak: {self.stats.stats.get('daily_challenge_streak', 0)} days\n\n"
                              f"Come back tomorrow for a new challenge!")
            return

        # Get today's challenge
        index = self.get_daily_challenge_index()
        challenge = self.challenge_levels[index]

        # Show info about the daily challenge
        self.clear_window()
        self.root.geometry("")

        main_frame = tk.Frame(self.root, bg=self.theme['bg'], padx=40, pady=25)
        main_frame.pack(fill='both', expand=True)

        title_font = font.Font(family="Arial", size=28, weight="bold")
        title = tk.Label(main_frame, text="📅 Today's Challenge", font=title_font,
                        bg=self.theme['bg'], fg=self.theme['accent'])
        title.pack(pady=15)

        streak = self.stats.stats.get('daily_challenge_streak', 0)
        best_streak = self.stats.stats.get('daily_challenge_best_streak', 0)

        info_font = font.Font(family="Arial", size=13)
        info_text = f"""
{challenge.name}
{challenge.goal}

Current Streak: {streak} days 🔥
Best Streak: {best_streak} days

Solve this puzzle to continue your streak!
        """
        info = tk.Label(main_frame, text=info_text, font=info_font,
                       bg=self.theme['bg'], fg=self.theme['text'], justify='center')
        info.pack(pady=20, padx=20)

        btn_font = font.Font(family="Arial", size=14)
        play_btn = tk.Button(main_frame, text="▶️ Play Today's Challenge",
                            font=btn_font, bg=self.theme['button'], fg=self.theme['text'],
                            activebackground=self.theme['hover'],
                            width=30, height=2,
                            command=lambda: self.start_daily_challenge(index))
        play_btn.pack(pady=10)

        back_btn = tk.Button(main_frame, text="← Back",
                            font=btn_font, bg=self.theme['button'], fg=self.theme['text'],
                            activebackground=self.theme['hover'],
                            width=30, height=2,
                            command=self.setup_menu_screen)
        back_btn.pack(pady=10)

    def start_daily_challenge(self, index):
        """Start playing today's daily challenge"""
        challenge = self.challenge_levels[index]
        self.board = challenge.copy_board()
        self.game_mode = 'daily_challenge'
        self.move_history = []
        self.game_active = True
        self.current_player = challenge.player_to_move
        self.human_player = challenge.player_to_move
        self.ai_player = 'O' if challenge.player_to_move == 'X' else 'X'
        self.game_start_time = time.time()

        self.clear_window()
        self.root.geometry("800x750")

        # Top frame
        top_frame = tk.Frame(self.root, bg=self.theme['bg'])
        top_frame.pack(fill='x', padx=10, pady=10)

        title_font = font.Font(family="Arial", size=18, weight="bold")
        title = tk.Label(top_frame, text="📅 " + challenge.name, font=title_font,
                        bg=self.theme['bg'], fg=self.theme['accent'])
        title.pack()

        goal_font = font.Font(family="Arial", size=11)
        goal = tk.Label(top_frame, text=challenge.goal, font=goal_font,
                       bg=self.theme['bg'], fg=self.theme['text'])
        goal.pack()

        self.status_label = tk.Label(top_frame, text=f"{self.current_player}'s Turn",
                                    font=("Arial", 14),
                                    bg=self.theme['bg'], fg=self.theme['text'])
        self.status_label.pack()

        # Board
        board_frame = tk.Frame(self.root, bg=self.theme['bg'])
        board_frame.pack(fill='both', expand=True, padx=10, pady=10)

        self.board_buttons = []
        for i in range(3):
            row_buttons = []
            for j in range(3):
                btn = tk.Button(board_frame, text=self.board[i][j] if self.board[i][j] != ' ' else '',
                               font=("Arial", 48, "bold"),
                               bg=self.theme['button'],
                               fg=self.theme['x_color'] if self.board[i][j] == 'X' else (self.theme['o_color'] if self.board[i][j] == 'O' else self.theme['text']),
                               activebackground=self.theme['hover'],
                               width=6, height=3,
                               command=lambda row=i, col=j: self.on_board_click(row, col))
                btn.grid(row=i, column=j, padx=5, pady=5, sticky='nsew')
                row_buttons.append(btn)
            self.board_buttons.append(row_buttons)

    def show_tournament_setup(self):
        """Setup tournament mode"""
        self.clear_window()
        self.root.geometry("")

        main_frame = tk.Frame(self.root, bg=self.theme['bg'], padx=60, pady=40)
        main_frame.pack()

        title_font = font.Font(family="Arial", size=32, weight="bold")
        title = tk.Label(main_frame, text="🏆 Tournament Mode", font=title_font,
                        bg=self.theme['bg'], fg=self.theme['accent'])
        title.pack(pady=25)

        button_font = font.Font(family="Arial", size=15)

        tournaments = [
            ("Best of 1", 1),
            ("Best of 3", 3),
            ("Best of 5", 5),
            ("Best of 7", 7)
        ]

        for text, series_len in tournaments:
            btn = tk.Button(main_frame, text=text,
                           font=button_font, bg=self.theme['button'], fg=self.theme['text'],
                           activebackground=self.theme['hover'],
                           width=26, height=2,
                           command=lambda s=series_len: self.start_tournament(s))
            btn.pack(pady=10)

        back_btn = tk.Button(main_frame, text="← Back",
                            font=button_font, bg=self.theme['button'], fg=self.theme['text'],
                            activebackground=self.theme['hover'],
                            width=26, height=2,
                            command=self.setup_menu_screen)
        back_btn.pack(pady=10)

    def start_tournament(self, series_length):
        """Start a tournament series"""
        self.tournament_series_length = series_length
        self.tournament_results = []
        self.tournament_round = 0
        self.play_tournament_game()

    def play_tournament_game(self):
        """Play a tournament game"""
        self.tournament_round += 1
        self.game_mode = 'tournament'
        self.difficulty = 'hard'
        self.move_history = []
        self.game_active = True
        self.current_player = 'X'
        self.human_player = 'X'
        self.ai_player = 'O'
        self.board = self.create_board()
        self.game_start_time = time.time()

        self.setup_game_screen()

    def setup_blitz_game(self):
        """Setup blitz mode (fast game on 3x3 board)"""
        self.clear_window()
        self.root.geometry("")

        main_frame = tk.Frame(self.root, bg=self.theme['bg'], padx=60, pady=40)
        main_frame.pack()

        title_font = font.Font(family="Arial", size=32, weight="bold")
        title = tk.Label(main_frame, text="⚡ Blitz Mode", font=title_font,
                        bg=self.theme['bg'], fg=self.theme['accent'])
        title.pack(pady=25)

        info_font = font.Font(family="Arial", size=13)
        info = tk.Label(main_frame, text="Fast-paced games on 3×3 board\nAI plays at maximum speed\nBuild your ELO rating!",
                       font=info_font, bg=self.theme['bg'], fg=self.theme['text'])
        info.pack(pady=15)

        button_font = font.Font(family="Arial", size=15)

        difficulties = [
            ("🟢 Easy Blitz", "easy"),
            ("🟡 Medium Blitz", "medium"),
            ("🔴 Hard Blitz", "hard")
        ]

        for text, diff in difficulties:
            btn = tk.Button(main_frame, text=text,
                           font=button_font, bg=self.theme['button'], fg=self.theme['text'],
                           activebackground=self.theme['hover'],
                           width=26, height=2,
                           command=lambda d=diff: self.start_blitz_game(d))
            btn.pack(pady=10)

        back_btn = tk.Button(main_frame, text="← Back",
                            font=button_font, bg=self.theme['button'], fg=self.theme['text'],
                            activebackground=self.theme['hover'],
                            width=26, height=2,
                            command=self.setup_menu_screen)
        back_btn.pack(pady=15)

    def start_blitz_game(self, difficulty):
        """Start a blitz game"""
        self.game_mode = 'blitz'
        self.difficulty = difficulty
        self.board_size = 3
        self.current_ai_speed = 'instant'
        self.move_history = []
        self.game_active = True
        self.current_player = 'X'
        self.human_player = 'X'
        self.ai_player = 'O'
        self.board = self.create_board()
        self.game_start_time = time.time()
        self.setup_game_screen()

    def show_leaderboard(self):
        """Show leaderboard with ELO rating and top games"""
        self.clear_window()
        self.root.geometry("")

        main_frame = tk.Frame(self.root, bg=self.theme['bg'], padx=40, pady=25)
        main_frame.pack(fill='both', expand=True)

        title_font = font.Font(family="Arial", size=28, weight="bold")
        title = tk.Label(main_frame, text="🏅 Leaderboard", font=title_font,
                        bg=self.theme['bg'], fg=self.theme['accent'])
        title.pack(pady=15)

        leaderboard = self.stats.get_leaderboard()

        info_font = font.Font(family="Arial", size=12)
        header_text = f"""
YOUR RATING & STATS

ELO Rating: {leaderboard['elo_rating']}
Blitz Record: {leaderboard['blitz_wins']}W - {leaderboard['blitz_losses']}L - {leaderboard['blitz_draws']}D
Blitz Win Rate: {round(100 * leaderboard['blitz_wins'] / max(leaderboard['blitz_wins'] + leaderboard['blitz_losses'], 1))}%
Best Speed Challenge: {leaderboard['speed_best']}s

TOP GAMES (Speed Rankings):
        """

        header_label = tk.Label(main_frame, text=header_text, font=info_font,
                               bg=self.theme['bg'], fg=self.theme['text'], justify='left')
        header_label.pack(pady=10, padx=20)

        # Games list
        if leaderboard['top_games']:
            games_text = ""
            for idx, game in enumerate(leaderboard['top_games'], 1):
                games_text += f"{idx}. Time: {game.get('duration', 0)}s | {game.get('mode', 'N/A').title()}\n"
        else:
            games_text = "Play games to populate the leaderboard!"

        games_label = tk.Label(main_frame, text=games_text, font=info_font,
                              bg=self.theme['bg'], fg=self.theme['accent'], justify='left')
        games_label.pack(pady=10, padx=20)

        back_btn = tk.Button(main_frame, text="← Back",
                            font=info_font, bg=self.theme['button'], fg=self.theme['text'],
                            activebackground=self.theme['hover'],
                            width=20, height=2,
                            command=self.setup_menu_screen)
        back_btn.pack(pady=15)

    def show_statistics(self):
        """Display detailed statistics"""
        stats_display = self.stats.get_stats_display()

        self.clear_window()
        self.root.geometry("")

        main_frame = tk.Frame(self.root, bg=self.theme['bg'], padx=40, pady=25)
        main_frame.pack()

        title_font = font.Font(family="Arial", size=28, weight="bold")
        title = tk.Label(main_frame, text="📊 Statistics", font=title_font,
                        bg=self.theme['bg'], fg=self.theme['accent'])
        title.pack(pady=15)

        stats_font = font.Font(family="Arial", size=13)

        # Calculate blitz win rate
        blitz_total = self.stats.stats.get('blitz_wins', 0) + self.stats.stats.get('blitz_losses', 0) + self.stats.stats.get('blitz_draws', 0)
        blitz_rate = round(100 * self.stats.stats.get('blitz_wins', 0) / max(blitz_total, 1))

        stats_text = f"""
Total Games: {stats_display['total_games']}
Total Time: {stats_display['total_time']}

STANDARD MODES
EASY MODE
  Wins: {stats_display['easy_wins']}/{stats_display['easy_games']}
  Win Rate: {stats_display['easy_rate']}%

MEDIUM MODE
  Wins: {stats_display['medium_wins']}/{stats_display['medium_games']}
  Win Rate: {stats_display['medium_rate']}%

HARD MODE
  Wins: {stats_display['hard_wins']}/{stats_display['hard_games']}
  Win Rate: {stats_display['hard_rate']}%

BLITZ MODE ⚡
  Record: {self.stats.stats.get('blitz_wins', 0)}W - {self.stats.stats.get('blitz_losses', 0)}L - {self.stats.stats.get('blitz_draws', 0)}D
  Win Rate: {blitz_rate}%
  ELO Rating: {self.stats.stats.get('elo_rating', 1500)}

Streaks
  Current: {stats_display['current_streak']}
  Best: {stats_display['best_streak']}

Challenges Completed: {stats_display['challenges_completed']}/5
Tournament Wins: {stats_display['tournament_wins']}
Daily Challenges: {self.stats.stats.get('daily_challenges_total', 0)}
        """

        stats_label = tk.Label(main_frame, text=stats_text, font=stats_font,
                              bg=self.theme['bg'], fg=self.theme['text'], justify='left')
        stats_label.pack(pady=10, padx=10)

        back_btn = tk.Button(main_frame, text="← Back",
                            font=stats_font, bg=self.theme['button'], fg=self.theme['text'],
                            activebackground=self.theme['hover'],
                            width=20, height=2,
                            command=self.setup_menu_screen)
        back_btn.pack(pady=15)

    def show_achievements(self):
        """Display achievements"""
        self.clear_window()
        self.root.geometry("")

        main_frame = tk.Frame(self.root, bg=self.theme['bg'], padx=40, pady=25)
        main_frame.pack(fill='both', expand=True)

        title_font = font.Font(family="Arial", size=28, weight="bold")
        title = tk.Label(main_frame, text="🏅 Achievements", font=title_font,
                        bg=self.theme['bg'], fg=self.theme['accent'])
        title.pack(pady=15)

        achievements_list = [
            ('first_win', '🥇 First Victory', 'Win your first game'),
            ('five_wins', '🥈 Five Timer', 'Win 5 games total'),
            ('ten_wins', '🥉 Ten Striker', 'Win 10 games total'),
            ('beat_hard', '⚔️ Hard Master', 'Beat the Hard AI'),
            ('win_streak_5', '🔥 Hot Streak', 'Win 5 games in a row'),
            ('win_streak_10', '🌪️ Unstoppable', 'Win 10 games in a row'),
            ('speed_demon', '⚡ Speed Demon', 'Win a 3×3 in under 30 seconds'),
            ('challenge_master', '🎯 Challenge Master', 'Complete all challenges'),
            ('tournament_winner', '🏆 Tournament Victor', 'Win a tournament'),
            ('perfect_replay', '📹 Perfect Script', 'Win a complex game'),
            ('blitz_master', '⚡ Blitz Master', 'Win 5 blitz games'),
            ('speed_runner', '🏃 Speed Runner', 'Win a blitz in under 15 seconds'),
            ('daily_devotee', '📅 Daily Devotee', 'Complete a daily challenge'),
            ('week_warrior', '🔥 Week Warrior', '7-day daily challenge streak'),
        ]

        scrolled = scrolledtext.ScrolledText(main_frame, height=18, width=65,
                                            bg=self.theme['button'],
                                            fg=self.theme['text'],
                                            font=("Arial", 11))
        scrolled.pack(pady=10, fill='both', expand=True)

        for key, name, desc in achievements_list:
            unlocked = self.stats.stats.get('achievements', {}).get(key, False)
            status = "✅" if unlocked else "🔒"
            text = f"{status} {name}\n   {desc}\n\n"
            scrolled.insert(tk.END, text)

        scrolled.config(state='disabled')

        back_btn = tk.Button(main_frame, text="← Back",
                            font=("Arial", 12), bg=self.theme['button'], fg=self.theme['text'],
                            activebackground=self.theme['hover'],
                            width=20, height=2,
                            command=self.setup_menu_screen)
        back_btn.pack(pady=10)

    def show_settings(self):
        """Show settings menu"""
        self.clear_window()
        self.root.geometry("")

        main_frame = tk.Frame(self.root, bg=self.theme['bg'], padx=40, pady=25)
        main_frame.pack()

        title_font = font.Font(family="Arial", size=28, weight="bold")
        title = tk.Label(main_frame, text="⚙️ Settings", font=title_font,
                        bg=self.theme['bg'], fg=self.theme['accent'])
        title.pack(pady=15)

        btn_font = font.Font(family="Arial", size=13)

        # Theme selection
        theme_label = tk.Label(main_frame, text="Theme:", font=btn_font,
                              bg=self.theme['bg'], fg=self.theme['text'])
        theme_label.pack(pady=10)

        for theme_name in ['dark', 'light', 'neon']:
            btn = tk.Button(main_frame, text=f"{'✓ ' if theme_name == self.current_theme else ''}{theme_name.title()}",
                           font=btn_font, bg=self.theme['button'], fg=self.theme['text'],
                           activebackground=self.theme['hover'],
                           width=26, height=2,
                           command=lambda t=theme_name: self.change_theme(t))
            btn.pack(pady=5)

        back_btn = tk.Button(main_frame, text="← Back",
                            font=btn_font, bg=self.theme['button'], fg=self.theme['text'],
                            activebackground=self.theme['hover'],
                            width=26, height=2,
                            command=self.setup_menu_screen)
        back_btn.pack(pady=15)

    def change_theme(self, theme_name):
        """Change theme"""
        self.current_theme = theme_name
        self.stats.stats['theme'] = theme_name
        self.stats.save_stats()
        self.theme = self.themes[theme_name]
        self.show_settings()

    def show_help(self):
        """Show help/tutorial"""
        self.clear_window()
        self.root.geometry("")

        main_frame = tk.Frame(self.root, bg=self.theme['bg'], padx=40, pady=20)
        main_frame.pack(fill='both', expand=True)

        title_font = font.Font(family="Arial", size=24, weight="bold")
        title = tk.Label(main_frame, text="ℹ️ How to Play", font=title_font,
                        bg=self.theme['bg'], fg=self.theme['accent'])
        title.pack(pady=15)

        help_text = """
🎮 GAME MODES
• Play Game - Challenge AI or play with another player
• Challenge Mode - Solve tactical puzzles (5 levels)
• Tournament Mode - Best-of series against Hard AI
• Game Replays - Watch recordings of past games
• AI Analysis - See why AI makes each move

🎯 BASIC RULES
Get 3 (or 4/5 on larger boards) marks in a row to win!
Line can be horizontal, vertical, or diagonal.

🤖 AI DIFFICULTY
• Easy - Random moves
• Medium - 50% smart, 50% random
• Hard - Perfect play (nearly unbeatable)

💡 FEATURES
✓ Move Hints
✓ Undo moves
✓ Position Analysis
✓ Game History with Replays
✓ Challenge Puzzles
✓ Tournament Series
✓ Statistics Tracking
✓ Multiple Themes

⌨️ CONTROLS
• Mouse: Click to play
• Keyboard: 1-9 (numpad layout)

🏆 ACHIEVEMENTS
Unlock 10 different badges by completing various goals!
        """

        help_label = tk.Label(main_frame, text=help_text, font=("Arial", 11),
                             bg=self.theme['bg'], fg=self.theme['text'], justify='left')
        help_label.pack(pady=10, padx=10, fill='both', expand=True)

        back_btn = tk.Button(main_frame, text="← Back",
                            font=("Arial", 12), bg=self.theme['button'], fg=self.theme['text'],
                            activebackground=self.theme['hover'],
                            width=20, height=2,
                            command=self.setup_menu_screen)
        back_btn.pack(pady=10)

    def analyze_position(self):
        """Analyze current position with detailed move analysis"""
        if not self.game_active:
            return

        analysis_text = "🔍 CURRENT POSITION ANALYSIS\n\n"

        # Evaluate available moves
        available_moves = self.get_available_moves(self.board)
        move_scores = []

        for row, col in available_moves:
            # Test this move
            self.board[row][col] = self.current_player
            score = self.minimax(self.board, 0, self.current_player != self.ai_player)
            self.board[row][col] = ' '
            move_scores.append(((row, col), score))

        # Sort by score (descending for AI, ascending for human in minimax context)
        move_scores.sort(key=lambda x: x[1], reverse=True)

        analysis_text += f"Current Player: {self.current_player}\n"
        analysis_text += f"Available Moves: {len(available_moves)}\n\n"
        analysis_text += "TOP 3 MOVES (by evaluation):\n"

        for idx, ((row, col), score) in enumerate(move_scores[:3], 1):
            eval_type = "Winning" if score > 5 else ("Blocking" if score > 0 else "Neutral")
            analysis_text += f"{idx}. Position ({row+1},{col+1}) - {eval_type}\n"

        analysis_text += "\n💡 Use the HINT button to get the best move!\n"

        messagebox.showinfo("🔍 Position Analysis", analysis_text)

    def run(self):
        """Run the game"""
        self.root.mainloop()


def main():
    game = TicTacToePro()
    game.run()


if __name__ == "__main__":
    main()
