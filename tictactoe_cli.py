#!/usr/bin/env python3
"""
Tic-Tac-Toe Game
A tic-tac-toe game with single-player (vs AI) and two-player modes.
"""

import random


def create_board():
    """Create and return an empty 3x3 game board."""
    return [[' ' for _ in range(3)] for _ in range(3)]


def display_board(board):
    """Display the current state of the board."""
    print("\n")
    print("     1   2   3")
    print("   +---+---+---+")
    for i, row in enumerate(board):
        print(f" {i+1} | {row[0]} | {row[1]} | {row[2]} |")
        print("   +---+---+---+")
    print()


def is_valid_move(board, row, col):
    """Check if a move is valid."""
    if row < 0 or row > 2 or col < 0 or col > 2:
        return False
    return board[row][col] == ' '


def make_move(board, row, col, player):
    """Place a player's mark on the board."""
    board[row][col] = player


def check_winner(board, player):
    """Check if the specified player has won."""
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


def is_board_full(board):
    """Check if the board is completely filled."""
    return all(cell != ' ' for row in board for cell in row)


def get_player_move(board, player):
    """Get a valid move from the current player."""
    while True:
        try:
            move = input(f"Player {player}, enter your move (row col): ")
            parts = move.strip().split()

            if len(parts) != 2:
                print("Please enter row and column separated by a space (e.g., '1 2')")
                continue

            row = int(parts[0]) - 1  # Convert to 0-indexed
            col = int(parts[1]) - 1  # Convert to 0-indexed

            if is_valid_move(board, row, col):
                return row, col
            else:
                print("Invalid move! That position is already taken or out of bounds.")
        except ValueError:
            print("Please enter valid numbers for row and column (1-3).")
        except KeyboardInterrupt:
            print("\nGame interrupted. Exiting...")
            exit(0)


def get_available_moves(board):
    """Get list of all available positions on the board."""
    moves = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                moves.append((i, j))
    return moves


def minimax(board, depth, is_maximizing, ai_player, human_player):
    """
    Minimax algorithm for AI decision making.
    Returns the best score for the current board state.
    """
    # Base cases
    if check_winner(board, ai_player):
        return 10 - depth
    if check_winner(board, human_player):
        return depth - 10
    if is_board_full(board):
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for row, col in get_available_moves(board):
            board[row][col] = ai_player
            score = minimax(board, depth + 1, False, ai_player, human_player)
            board[row][col] = ' '
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for row, col in get_available_moves(board):
            board[row][col] = human_player
            score = minimax(board, depth + 1, True, ai_player, human_player)
            board[row][col] = ' '
            best_score = min(score, best_score)
        return best_score


def get_ai_move(board, ai_player, human_player, difficulty='hard'):
    """
    Get the AI's move based on difficulty level.
    - easy: random moves
    - medium: 50% optimal, 50% random
    - hard: always optimal (minimax)
    """
    available_moves = get_available_moves(board)

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
        score = minimax(board, 0, False, ai_player, human_player)
        board[row][col] = ' '

        if score > best_score:
            best_score = score
            best_move = (row, col)

    return best_move if best_move else available_moves[0]


def play_game():
    """Main game loop."""
    print("=" * 40)
    print("Welcome to Tic-Tac-Toe!")
    print("=" * 40)

    # Choose game mode
    while True:
        mode = input("\nChoose game mode:\n1. Single Player (vs AI)\n2. Two Players\nEnter 1 or 2: ").strip()
        if mode in ['1', '2']:
            break
        print("Invalid choice. Please enter 1 or 2.")

    single_player = (mode == '1')
    difficulty = 'hard'

    if single_player:
        print("\nChoose difficulty:")
        print("1. Easy (Random moves)")
        print("2. Medium (Mixed strategy)")
        print("3. Hard (Unbeatable)")
        while True:
            diff_choice = input("Enter 1, 2, or 3: ").strip()
            if diff_choice == '1':
                difficulty = 'easy'
                break
            elif diff_choice == '2':
                difficulty = 'medium'
                break
            elif diff_choice == '3':
                difficulty = 'hard'
                break
            print("Invalid choice. Please enter 1, 2, or 3.")

    print("\nHow to play:")
    print("- Enter row and column numbers (1-3)")
    print("- Example: '1 2' places your mark at row 1, column 2")
    if single_player:
        print("- You are 'X', AI is 'O'")
    else:
        print("- Player 1 is 'X', Player 2 is 'O'")

    board = create_board()
    current_player = 'X'
    move_count = 0

    while True:
        display_board(board)

        # Get and make move
        if single_player and current_player == 'O':
            # AI's turn
            print("AI is thinking...")
            row, col = get_ai_move(board, 'O', 'X', difficulty)
            print(f"AI plays: row {row+1}, column {col+1}")
        else:
            # Human player's turn
            row, col = get_player_move(board, current_player)

        make_move(board, row, col, current_player)
        move_count += 1

        # Check for winner
        if check_winner(board, current_player):
            display_board(board)
            if single_player and current_player == 'O':
                print("AI wins! Better luck next time!")
            elif single_player:
                print("🎉 Congratulations! You win! 🎉")
            else:
                print(f"🎉 Congratulations! Player {current_player} wins! 🎉")
            break

        # Check for draw
        if is_board_full(board):
            display_board(board)
            print("It's a draw! The board is full.")
            break

        # Switch player
        current_player = 'O' if current_player == 'X' else 'X'

    # Ask to play again
    play_again = input("\nWould you like to play again? (y/n): ")
    if play_again.lower() == 'y':
        play_game()
    else:
        print("Thanks for playing! Goodbye!")


if __name__ == "__main__":
    play_game()
