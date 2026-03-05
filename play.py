#!/usr/bin/env python3
"""
Tic-Tac-Toe Game Launcher
Choose which version to play
"""

import sys

def main():
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg in ['--pro', '-p', '--professional']:
            from tictactoe_pro import main as pro_main
            pro_main()
        elif arg in ['--ultimate', '-u', '--deluxe']:
            from tictactoe_ultimate import main as ultimate_main
            ultimate_main()
        elif arg in ['--enhanced', '-e', '--premium']:
            from tictactoe_enhanced import main as enhanced_main
            enhanced_main()
        elif arg in ['--gui', '--simple']:
            from tictactoe_gui import main as gui_main
            gui_main()
        elif arg == '--cli':
            from tictactoe_cli import play_game
            play_game()
        elif arg in ['--help', '-h']:
            print("""
🚀 Tic-Tac-Toe Game Launcher - PRO Edition 🚀

Usage:
  python3 play.py                    # PRO version (DEFAULT - BEST!)
  python3 play.py --pro              # PRO version with ALL features
  python3 play.py --ultimate         # Ultimate version (great alternative)
  python3 play.py --enhanced         # Enhanced version
  python3 play.py --gui              # Classic GUI version
  python3 play.py --cli              # Command-line version
  python3 play.py --help             # Show this help message

⭐ PRO VERSION FEATURES (NEW!):
  📹 Game Replays - Watch recordings of past games
  🎯 Challenge Mode - 5 tactical puzzles to solve
  🏆 Tournament Mode - Best-of series competitions
  🔍 AI Analysis - Understand why AI makes each move
  🏅 10 Achievements - Unlock badges and milestones
  💡 Move Hints with Explanations
  👥 2-Player mode with custom names
  🎨 3 Beautiful Themes (Dark, Light, Neon)
  📊 Advanced Statistics with Game History
  ⚙️ AI Speed Control (5 levels)
  ↩️ Undo moves feature
  🔊 Sound effects toggle
  and much more!

All versions include:
  ✅ Unbeatable AI (minimax algorithm)
  ✅ Single player & two player modes
  ✅ Multiple difficulty levels
  ✅ Beautiful UI with themes
            """)
        else:
            print(f"Unknown option: {arg}")
            print("Use --help for usage information")
    else:
        # Default: launch pro version
        from tictactoe_pro import main as pro_main
        pro_main()

if __name__ == "__main__":
    main()
