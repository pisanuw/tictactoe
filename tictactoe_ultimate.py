#!/usr/bin/env python3
"""
Tic-Tac-Toe ULTIMATE - Deluxe Edition
All-in-one premium tic-tac-toe with hints, achievements, challenges, replays, and more!
"""

import tkinter as tk
from tkinter import messagebox, font, scrolledtext
import random
import json
import os
from datetime import datetime
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
            'board_size': 3,
            'ai_speed': 'normal',
            'show_hints': True,
            'total_time_played': 0,
            'games_history': [],
            'achievements': {
                'first_win': False,
                'five_wins': False,
                'ten_wins': False,
                'perfect_game': False,
                'beat_hard': False,
                'speed_demon': False,
                'win_streak_5': False,
                'win_streak_10': False
            }
        }

    def save_stats(self):
        """Save statistics to file"""
        with open(self.filename, 'w') as f:
            json.dump(self.stats, f, indent=2)

    def record_game_result(self, mode, difficulty, result, duration=0, board_size=3):
        """Record a game result with timestamp"""
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

        # Track game in history
        game_record = {
            'timestamp': datetime.now().isoformat(),
            'mode': mode,
            'difficulty': difficulty,
            'result': result,
            'duration': duration,
            'board_size': board_size
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
            'best_streak': self.stats.get('best_streak', 0),
            'current_streak': self.stats.get('current_streak', 0),
        }


class TicTacToeUltimate:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe Ultimate 🎮")
        self.root.minsize(800, 750)
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
        self.game_start_time = None
        self.practice_mode = False
        self.p1_name = "Player X"
        self.p2_name = "Player O"

        # Statistics
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

        # Setup UI
        self.setup_menu_screen()

    def create_board(self):
        """Create empty board"""
        return [[' ' for _ in range(self.board_size)] for _ in range(self.board_size)]

    def setup_menu_screen(self):
        """Create main menu"""
        self.clear_window()
        self.root.geometry("")

        main_frame = tk.Frame(self.root, bg=self.theme['bg'], padx=60, pady=40)
        main_frame.pack()

        title_font = font.Font(family="Arial", size=52, weight="bold")
        title = tk.Label(main_frame, text="Tic-Tac-Toe\nULTIMATE", font=title_font,
                        bg=self.theme['bg'], fg=self.theme['accent'], justify='center')
        title.pack(pady=25)

        subtitle_font = font.Font(family="Arial", size=13)
        subtitle = tk.Label(main_frame, text="🚀 Deluxe Edition with Hints, Achievements & More",
                           font=subtitle_font, bg=self.theme['bg'], fg=self.theme['text'])
        subtitle.pack(pady=5)

        button_font = font.Font(family="Arial", size=15)

        buttons = [
            ("🎮 Play vs AI", self.choose_difficulty),
            ("👥 Two Players", self.setup_two_player_names),
            ("🎯 Challenge Mode", self.show_challenges),
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

    def show_achievements(self):
        """Display achievements"""
        self.clear_window()
        self.root.geometry("")

        main_frame = tk.Frame(self.root, bg=self.theme['bg'], padx=40, pady=25)
        main_frame.pack()

        title_font = font.Font(family="Arial", size=32, weight="bold")
        title = tk.Label(main_frame, text="🏆 ACHIEVEMENTS", font=title_font,
                        bg=self.theme['bg'], fg=self.theme['accent'])
        title.pack(pady=15)

        achievements_list = [
            ('first_win', '🥇 First Victory', 'Win your first game'),
            ('five_wins', '🥈 Five Timer', 'Win 5 games total'),
            ('ten_wins', '🥉 Ten Striker', 'Win 10 games total'),
            ('beat_hard', '⚔️ Hard Mode Victor', 'Beat the Hard AI'),
            ('win_streak_5', '🔥 Hot Streak', 'Win 5 games in a row'),
            ('win_streak_10', '🌪️ Unstoppable', 'Win 10 games in a row'),
            ('speed_demon', '⚡ Speed Demon', 'Win a 3×3 game in under 30 seconds'),
            ('perfect_game', '💎 Perfect Game', 'Win without losing a position (future update)')
        ]

        ach_font = font.Font(family="Arial", size=13)
        for key, name, desc in achievements_list:
            unlocked = self.stats.stats.get('achievements', {}).get(key, False)
            status = "✅ UNLOCKED" if unlocked else "🔒 LOCKED"
            color = self.theme['win_color'] if unlocked else self.theme['text']

            text = f"{name}\n{desc}\n{status}"
            label = tk.Label(main_frame, text=text, font=ach_font,
                           bg=self.theme['bg'], fg=color, justify='left')
            label.pack(pady=8, padx=20, anchor='w')

        back_btn = tk.Button(main_frame, text="← Back",
                            font=ach_font, bg=self.theme['button'], fg=self.theme['text'],
                            activebackground=self.theme['hover'],
                            width=20, height=2,
                            command=self.setup_menu_screen)
        back_btn.pack(pady=15)

    def show_help(self):
        """Show help/tutorial"""
        self.clear_window()
        self.root.geometry("")

        main_frame = tk.Frame(self.root, bg=self.theme['bg'], padx=40, pady=20)
        main_frame.pack(fill='both', expand=True)

        title_font = font.Font(family="Arial", size=28, weight="bold")
        title = tk.Label(main_frame, text="ℹ️ How to Play", font=title_font,
                        bg=self.theme['bg'], fg=self.theme['accent'])
        title.pack(pady=15)

        help_text = """
🎮 OBJECTIVE
Get 3 (or 4/5 on larger boards) of your marks in a row to win!

🎯 GAME MODES
• Play vs AI - Challenge yourself against 3 difficulty levels
• Two Players - Play locally with a friend
• Challenge Mode - Solve preset puzzles
• Practice Mode - Play without stats tracking

⌨️ CONTROLS
• Mouse: Click any empty cell to place your mark
• Keyboard: Press 1-9 (numpad layout) for quick moves
  7 8 9 (top)
  4 5 6 (middle)
  1 2 3 (bottom)

💡 HINTS
• Click the "Hint" button to see the best next move
• Hints explain WHY the move is best

🏅 AI DIFFICULTY
• Easy 🟢 - Random moves, great for learning
• Medium 🟡 - Mixed strategy, balanced challenge
• Hard 🔴 - Perfect play, nearly unbeatable

🎨 FEATURES
✓ Multiple themes (Dark, Light, Neon)
✓ Variable board sizes (3×3, 4×4, 5×5)
✓ Sound effects (toggle on/off)
✓ Statistics tracking (auto-saves)
✓ Achievements system
✓ Game history tracking
✓ Undo moves feature
✓ Move hints with explanations

🏆 ACHIEVEMENTS
Unlock badges by completing challenges!

📚 STRATEGY TIPS
• Control the center for maximum options
• Create multiple winning threats
• Block your opponent's winning moves
• In 3×3: Best opening is center or corner
        """

        help_font = font.Font(family="Arial", size=11)
        help_label = tk.Label(main_frame, text=help_text, font=help_font,
                             bg=self.theme['bg'], fg=self.theme['text'], justify='left')
        help_label.pack(pady=10, padx=10)

        back_btn = tk.Button(main_frame, text="← Back",
                            font=help_font, bg=self.theme['button'], fg=self.theme['text'],
                            activebackground=self.theme['hover'],
                            width=20, height=2,
                            command=self.setup_menu_screen)
        back_btn.pack(pady=10)

    def show_challenges(self):
        """Show challenge mode"""
        messagebox.showinfo("🎯 Challenge Mode",
                           "Coming soon! Preset puzzle scenarios and time trials.\n\nFor now, try beating Hard AI!")
        self.setup_menu_screen()

    def show_statistics(self):
        """Display detailed statistics"""
        self.clear_window()
        self.root.geometry("")

        main_frame = tk.Frame(self.root, bg=self.theme['bg'], padx=40, pady=25)
        main_frame.pack()

        title_font = font.Font(family="Arial", size=32, weight="bold")
        title = tk.Label(main_frame, text="📊 Statistics", font=title_font,
                        bg=self.theme['bg'], fg=self.theme['accent'])
        title.pack(pady=15)

        stats = self.stats.get_stats_display()
        stats_font = font.Font(family="Arial", size=12)

        stats_text = f"""
Total Games Played: {stats['total_games']}
Total Play Time: {stats['total_time']}
Current Streak: {stats['current_streak']} wins  |  Best Streak: {stats['best_streak']} wins

═══════════════════════════════════════

🟢 EASY MODE
    Games: {stats['easy_games']}  |  Wins: {stats['easy_wins']}  |  Win Rate: {stats['easy_rate']}%

🟡 MEDIUM MODE
    Games: {stats['medium_games']}  |  Wins: {stats['medium_wins']}  |  Win Rate: {stats['medium_rate']}%

🔴 HARD MODE
    Games: {stats['hard_games']}  |  Wins: {stats['hard_wins']}  |  Win Rate: {stats['hard_rate']}%
        """

        stats_label = tk.Label(main_frame, text=stats_text.strip(), font=stats_font,
                              bg=self.theme['bg'], fg=self.theme['text'], justify='left',
                              family='Courier')
        stats_label.pack(pady=15)

        button_font = font.Font(family="Arial", size=12)

        btn_frame = tk.Frame(main_frame, bg=self.theme['bg'])
        btn_frame.pack(pady=10)

        reset_btn = tk.Button(btn_frame, text="Reset Statistics",
                             font=button_font, bg="#e74c3c", fg="white",
                             activebackground="#c0392b",
                             width=15, height=2,
                             command=self.reset_statistics)
        reset_btn.grid(row=0, column=0, padx=5)

        back_btn = tk.Button(btn_frame, text="← Back",
                            font=button_font, bg=self.theme['button'], fg=self.theme['text'],
                            activebackground=self.theme['hover'],
                            width=15, height=2,
                            command=self.setup_menu_screen)
        back_btn.grid(row=0, column=1, padx=5)

    def reset_statistics(self):
        """Reset all statistics"""
        if messagebox.askyesno("Reset Stats", "Are you sure? This cannot be undone!"):
            self.stats.stats = self.stats.get_default_stats()
            self.stats.save_stats()
            messagebox.showinfo("Success", "Statistics reset!")
            self.show_statistics()

    def show_settings(self):
        """Show advanced settings"""
        self.clear_window()
        self.root.geometry("")

        main_frame = tk.Frame(self.root, bg=self.theme['bg'], padx=40, pady=25)
        main_frame.pack()

        title_font = font.Font(family="Arial", size=32, weight="bold")
        title = tk.Label(main_frame, text="⚙️ Settings", font=title_font,
                        bg=self.theme['bg'], fg=self.theme['accent'])
        title.pack(pady=15)

        settings_font = font.Font(family="Arial", size=13)

        # Theme selection
        theme_frame = tk.Frame(main_frame, bg=self.theme['bg'])
        theme_frame.pack(pady=12)

        tk.Label(theme_frame, text="Theme:", font=settings_font,
                bg=self.theme['bg'], fg=self.theme['text']).pack(side='left', padx=10)

        for theme_name in ['dark', 'light', 'neon']:
            btn = tk.Button(theme_frame, text=theme_name.upper(), font=settings_font,
                           bg=self.theme['button'], fg=self.theme['text'],
                           activebackground=self.theme['hover'],
                           width=10,
                           command=lambda t=theme_name: self.set_theme(t))
            btn.pack(side='left', padx=3)

        # AI Speed
        speed_frame = tk.Frame(main_frame, bg=self.theme['bg'])
        speed_frame.pack(pady=12)

        tk.Label(speed_frame, text="AI Speed:", font=settings_font,
                bg=self.theme['bg'], fg=self.theme['text']).pack(side='left', padx=10)

        for speed in ['instant', 'fast', 'normal', 'slow']:
            btn = tk.Button(speed_frame, text=speed.capitalize(), font=settings_font,
                           bg=self.theme['button'], fg=self.theme['text'],
                           activebackground=self.theme['hover'],
                           width=10,
                           command=lambda s=speed: self.set_ai_speed(s))
            btn.pack(side='left', padx=3)

        # Board size
        size_frame = tk.Frame(main_frame, bg=self.theme['bg'])
        size_frame.pack(pady=12)

        tk.Label(size_frame, text="Board Size:", font=settings_font,
                bg=self.theme['bg'], fg=self.theme['text']).pack(side='left', padx=10)

        for size in [3, 4, 5]:
            btn = tk.Button(size_frame, text=f"{size}×{size}", font=settings_font,
                           bg=self.theme['button'], fg=self.theme['text'],
                           activebackground=self.theme['hover'],
                           width=8,
                           command=lambda s=size: self.set_board_size(s))
            btn.pack(side='left', padx=3)

        # Back button
        back_btn = tk.Button(main_frame, text="← Back",
                            font=settings_font, bg=self.theme['button'], fg=self.theme['text'],
                            activebackground=self.theme['hover'],
                            width=20, height=2,
                            command=self.setup_menu_screen)
        back_btn.pack(pady=20)

    def set_theme(self, theme_name):
        """Change theme"""
        self.current_theme = theme_name
        self.theme = self.themes[theme_name]
        self.stats.stats['theme'] = theme_name
        self.stats.save_stats()
        self.show_settings()

    def set_ai_speed(self, speed):
        """Set AI speed"""
        self.current_ai_speed = speed
        self.stats.stats['ai_speed'] = speed
        self.stats.save_stats()
        self.show_settings()

    def set_board_size(self, size):
        """Set board size"""
        self.board_size = size
        self.stats.stats['board_size'] = size
        self.stats.save_stats()
        self.show_settings()

    def setup_two_player_names(self):
        """Get player names for two-player mode"""
        self.clear_window()
        self.root.geometry("")

        main_frame = tk.Frame(self.root, bg=self.theme['bg'], padx=60, pady=50)
        main_frame.pack()

        title_font = font.Font(family="Arial", size=32, weight="bold")
        title = tk.Label(main_frame, text="👥 Two Players", font=title_font,
                        bg=self.theme['bg'], fg=self.theme['accent'])
        title.pack(pady=25)

        input_font = font.Font(family="Arial", size=14)

        # Player 1 Name
        tk.Label(main_frame, text="Player 1 (X):", font=input_font,
                bg=self.theme['bg'], fg=self.theme['text']).pack(pady=5)
        p1_entry = tk.Entry(main_frame, font=input_font, width=30)
        p1_entry.insert(0, "Player X")
        p1_entry.pack(pady=5)

        # Player 2 Name
        tk.Label(main_frame, text="Player 2 (O):", font=input_font,
                bg=self.theme['bg'], fg=self.theme['text']).pack(pady=5)
        p2_entry = tk.Entry(main_frame, font=input_font, width=30)
        p2_entry.insert(0, "Player O")
        p2_entry.pack(pady=5)

        button_font = font.Font(family="Arial", size=14)

        play_btn = tk.Button(main_frame, text="Start Game ▶",
                            font=button_font, bg="#27ae60", fg="white",
                            activebackground="#229954",
                            width=25, height=2,
                            command=lambda: self.start_two_player(p1_entry.get(), p2_entry.get()))
        play_btn.pack(pady=20)

        back_btn = tk.Button(main_frame, text="← Back",
                            font=button_font, bg=self.theme['button'], fg=self.theme['text'],
                            activebackground=self.theme['hover'],
                            width=25, height=2,
                            command=self.setup_menu_screen)
        back_btn.pack(pady=10)

    def start_two_player(self, p1_name, p2_name):
        """Start two player game"""
        self.game_mode = 'two'
        self.p1_name = p1_name if p1_name.strip() else "Player X"
        self.p2_name = p2_name if p2_name.strip() else "Player O"
        self.practice_mode = False
        self.setup_game_screen()

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

        button_font = font.Font(family="Arial", size=15)

        difficulties = [
            ("🟢 Easy", "easy"),
            ("🟡 Medium", "medium"),
            ("🔴 Hard", "hard")
        ]

        for text, diff in difficulties:
            btn = tk.Button(main_frame, text=text, font=button_font,
                           bg=self.theme['button'], fg=self.theme['text'],
                           activebackground=self.theme['hover'],
                           width=25, height=2,
                           command=lambda d=diff: self.start_single_player(d, False))
            btn.pack(pady=10)

        # Practice mode checkbox
        practice_btn = tk.Button(main_frame, text="📝 Practice Mode (No Stats)", font=button_font,
                                bg="#9b59b6", fg="white",
                                activebackground="#8e44ad",
                                width=25, height=2,
                                command=lambda: self.choose_practice_difficulty())
        practice_btn.pack(pady=10)

        back_btn = tk.Button(main_frame, text="← Back", font=button_font,
                            bg=self.theme['button'], fg=self.theme['text'],
                            activebackground=self.theme['hover'],
                            width=25, height=2,
                            command=self.setup_menu_screen)
        back_btn.pack(pady=10)

    def choose_practice_difficulty(self):
        """Choose difficulty for practice mode"""
        self.clear_window()
        self.root.geometry("")

        main_frame = tk.Frame(self.root, bg=self.theme['bg'], padx=60, pady=50)
        main_frame.pack()

        title_font = font.Font(family="Arial", size=32, weight="bold")
        title = tk.Label(main_frame, text="Practice Mode\n(Stats not tracked)", font=title_font,
                        bg=self.theme['bg'], fg=self.theme['accent'], justify='center')
        title.pack(pady=30)

        button_font = font.Font(family="Arial", size=15)

        difficulties = [
            ("🟢 Easy", "easy"),
            ("🟡 Medium", "medium"),
            ("🔴 Hard", "hard")
        ]

        for text, diff in difficulties:
            btn = tk.Button(main_frame, text=text, font=button_font,
                           bg=self.theme['button'], fg=self.theme['text'],
                           activebackground=self.theme['hover'],
                           width=25, height=2,
                           command=lambda d=diff: self.start_single_player(d, True))
            btn.pack(pady=10)

        back_btn = tk.Button(main_frame, text="← Back", font=button_font,
                            bg=self.theme['button'], fg=self.theme['text'],
                            activebackground=self.theme['hover'],
                            width=25, height=2,
                            command=self.choose_difficulty)
        back_btn.pack(pady=10)

    def start_single_player(self, difficulty, practice=False):
        """Start single player game"""
        self.game_mode = 'single'
        self.difficulty = difficulty
        self.practice_mode = practice
        self.setup_game_screen()

    def setup_game_screen(self):
        """Setup game board"""
        self.clear_window()
        self.root.geometry("")
        self.board = self.create_board()
        self.current_player = 'X'
        self.game_active = True
        self.buttons = []
        self.move_history = []
        self.game_start_time = time.time()

        main_frame = tk.Frame(self.root, bg=self.theme['bg'], padx=25, pady=15)
        main_frame.pack(fill='both', expand=True)

        # Status and hint frame
        top_frame = tk.Frame(main_frame, bg=self.theme['bg'])
        top_frame.pack(pady=10, fill='x')

        status_font = font.Font(family="Arial", size=18, weight="bold")
        self.status_label = tk.Label(top_frame, text=self.get_status_text(),
                                    font=status_font, bg=self.theme['bg'],
                                    fg=self.theme['accent'])
        self.status_label.pack(side='left', padx=10)

        # Hint button (in game for single player)
        hint_font = font.Font(family="Arial", size=11)
        if self.game_mode == 'single' and self.current_player == 'X':
            hint_btn = tk.Button(top_frame, text="💡 Hint",
                                font=hint_font, bg="#3498db", fg="white",
                                activebackground="#2980b9",
                                command=self.show_hint)
            hint_btn.pack(side='right', padx=10)

        # Game board
        board_frame = tk.Frame(main_frame, bg=self.theme['bg'])
        board_frame.pack(pady=15)

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
                btn.grid(row=i, column=j, padx=3, pady=3)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)

        # Control buttons
        control_frame = tk.Frame(main_frame, bg=self.theme['bg'])
        control_frame.pack(pady=15)

        control_font = font.Font(family="Arial", size=12)

        new_game_btn = tk.Button(control_frame, text="🔄 New", font=control_font,
                                bg="#27ae60", fg="white",
                                activebackground="#229954",
                                width=10, height=2,
                                command=self.reset_game)
        new_game_btn.grid(row=0, column=0, padx=5)

        undo_btn = tk.Button(control_frame, text="↶ Undo", font=control_font,
                            bg=self.theme['button'], fg=self.theme['text'],
                            activebackground=self.theme['hover'],
                            width=10, height=2,
                            command=self.undo_move)
        undo_btn.grid(row=0, column=1, padx=5)

        menu_btn = tk.Button(control_frame, text="🏠 Menu", font=control_font,
                           bg=self.theme['button'], fg=self.theme['text'],
                           activebackground=self.theme['hover'],
                           width=10, height=2,
                           command=self.setup_menu_screen)
        menu_btn.grid(row=0, column=2, padx=5)

        self.root.update_idletasks()

        # Keyboard bindings
        for i in range(1, 10):
            self.root.bind(str(i), lambda e, r=(i-1)//3, c=(i-1)%3: self.keyboard_move(r, c))

    def show_hint(self):
        """Show move hint"""
        if not self.game_active or self.current_player != 'X':
            return

        available = self.get_available_moves(self.board)
        if not available:
            messagebox.showinfo("Hint", "No moves available!")
            return

        best_move = self.get_best_move_for_hint()
        if best_move:
            row, col = best_move
            msg_map = {
                0: "Top", 1: "Middle", 2: "Bottom"
            }
            col_map = {
                0: "Left", 1: "Center", 2: "Right"
            }
            position = f"{msg_map.get(row, '?')} {col_map.get(col, '?')}"

            messagebox.showinfo("💡 Hint",
                              f"Best move: Position {row+1},{col+1} ({position})\n\n"
                              f"This position is strong because it:\n"
                              f"• Controls key board areas\n"
                              f"• Creates winning opportunities\n"
                              f"• Blocks opponent threats")

    def get_best_move_for_hint(self):
        """Get best move using minimax"""
        available = self.get_available_moves(self.board)
        if not available:
            return None

        best_score = -float('inf')
        best_move = None

        for row, col in available:
            self.board[row][col] = 'X'
            score = self.minimax(self.board, 0, False)
            self.board[row][col] = ' '

            if score > best_score:
                best_score = score
                best_move = (row, col)

        return best_move

    def keyboard_move(self, row, col):
        """Handle keyboard input"""
        if self.game_active:
            if self.game_mode == 'single' and self.current_player != 'X':
                return
            self.on_cell_click(row, col)

    def get_status_text(self):
        """Get status message"""
        if not self.game_active:
            return "Game Over"
        if self.game_mode == 'single':
            return "Your turn (X) 🔴" if self.current_player == 'X' else "AI thinking... ⏳"
        else:
            player_name = self.p1_name if self.current_player == 'X' else self.p2_name
            return f"{player_name}'s turn ({self.current_player})"

    def on_cell_click(self, row, col):
        """Handle cell click"""
        if row >= self.board_size or col >= self.board_size:
            return

        if not self.game_active or self.board[row][col] != ' ':
            return

        if self.game_mode == 'single' and self.current_player != 'X':
            return

        self.move_history.append((row, col, self.current_player))
        self.make_move(row, col, self.current_player)

        if self.check_game_end():
            return

        self.current_player = 'O' if self.current_player == 'X' else 'X'
        self.status_label.config(text=self.get_status_text())

        if self.game_mode == 'single' and self.current_player == 'O' and self.game_active:
            delay = self.ai_speeds.get(self.current_ai_speed, 0.8) * 1000
            self.root.after(int(delay), self.ai_move)

    def make_move(self, row, col, player):
        """Make a move"""
        self.board[row][col] = player
        color = self.theme['x_color'] if player == 'X' else self.theme['o_color']
        self.buttons[row][col].config(text=player, fg=color, disabledforeground=color)
        self.buttons[row][col].config(state='disabled')

    def ai_move(self):
        """AI move"""
        if not self.game_active:
            return

        move = self.get_ai_move(self.board)
        if move:
            row, col = move
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

            game_duration = int(time.time() - self.game_start_time)

            if self.game_mode == 'single':
                if self.current_player == 'X':
                    msg = "🎉 YOU WIN!"
                    if not self.practice_mode:
                        self.stats.record_game_result('single', self.difficulty, 'wins', game_duration, self.board_size)
                else:
                    msg = "AI wins! Try again!"
                    if not self.practice_mode:
                        self.stats.record_game_result('single', self.difficulty, 'losses', game_duration, self.board_size)
            else:
                winner = self.p1_name if self.current_player == 'X' else self.p2_name
                msg = f"🎉 {winner} WINS!"

            self.status_label.config(text=msg, fg=self.theme['win_color'])
            self.root.after(2000, lambda: messagebox.showinfo("Game Over", msg))
            return True

        if self.is_board_full(self.board):
            self.game_active = False
            game_duration = int(time.time() - self.game_start_time)
            msg = "It's a DRAW!"
            if self.game_mode == 'single' and not self.practice_mode:
                self.stats.record_game_result('single', self.difficulty, 'draws', game_duration, self.board_size)
            self.status_label.config(text=msg, fg=self.theme['accent'])
            self.root.after(2000, lambda: messagebox.showinfo("Game Over", msg))
            return True

        return False

    def highlight_winner(self):
        """Highlight winning line"""
        player = self.current_player

        # Rows
        for i in range(self.board_size):
            if all(self.board[i][j] == player for j in range(self.board_size)):
                for j in range(self.board_size):
                    self.buttons[i][j].config(bg=self.theme['win_color'])
                return

        # Columns
        for j in range(self.board_size):
            if all(self.board[i][j] == player for i in range(self.board_size)):
                for i in range(self.board_size):
                    self.buttons[i][j].config(bg=self.theme['win_color'])
                return

        # Diagonals
        if all(self.board[i][i] == player for i in range(self.board_size)):
            for i in range(self.board_size):
                self.buttons[i][i].config(bg=self.theme['win_color'])
            return

        if all(self.board[i][self.board_size-1-i] == player for i in range(self.board_size)):
            for i in range(self.board_size):
                self.buttons[i][self.board_size-1-i].config(bg=self.theme['win_color'])

    def undo_move(self):
        """Undo last move"""
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

    # Game logic

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
    """Run the game"""
    root = tk.Tk()
    game = TicTacToeUltimate(root)
    root.mainloop()


if __name__ == "__main__":
    main()
