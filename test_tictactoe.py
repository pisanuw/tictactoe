#!/usr/bin/env python3
"""
Test script for tic-tac-toe game
Tests core game logic functions
"""

import sys
sys.path.insert(0, '/home/cssuwbstudent/pisan/Downloads/tictactoe')

from tictactoe_cli import (
    create_board, is_valid_move, make_move,
    check_winner, is_board_full, get_available_moves
)


def test_board_creation():
    """Test that board is created correctly"""
    board = create_board()
    assert len(board) == 3, "Board should have 3 rows"
    assert all(len(row) == 3 for row in board), "Each row should have 3 columns"
    assert all(cell == ' ' for row in board for cell in row), "All cells should be empty"
    print("✓ Board creation test passed")


def test_valid_moves():
    """Test move validation"""
    board = create_board()
    assert is_valid_move(board, 0, 0) == True, "Empty cell should be valid"
    assert is_valid_move(board, -1, 0) == False, "Negative row should be invalid"
    assert is_valid_move(board, 0, 5) == False, "Out of bounds column should be invalid"

    make_move(board, 1, 1, 'X')
    assert is_valid_move(board, 1, 1) == False, "Occupied cell should be invalid"
    print("✓ Move validation test passed")


def test_winner_detection():
    """Test win condition checking"""
    # Test horizontal win
    board = create_board()
    make_move(board, 0, 0, 'X')
    make_move(board, 0, 1, 'X')
    make_move(board, 0, 2, 'X')
    assert check_winner(board, 'X') == True, "Should detect horizontal win"
    print("✓ Horizontal win detection passed")

    # Test vertical win
    board = create_board()
    make_move(board, 0, 0, 'O')
    make_move(board, 1, 0, 'O')
    make_move(board, 2, 0, 'O')
    assert check_winner(board, 'O') == True, "Should detect vertical win"
    print("✓ Vertical win detection passed")

    # Test diagonal win
    board = create_board()
    make_move(board, 0, 0, 'X')
    make_move(board, 1, 1, 'X')
    make_move(board, 2, 2, 'X')
    assert check_winner(board, 'X') == True, "Should detect diagonal win"
    print("✓ Diagonal win detection passed")

    # Test anti-diagonal win
    board = create_board()
    make_move(board, 0, 2, 'O')
    make_move(board, 1, 1, 'O')
    make_move(board, 2, 0, 'O')
    assert check_winner(board, 'O') == True, "Should detect anti-diagonal win"
    print("✓ Anti-diagonal win detection passed")


def test_draw_detection():
    """Test draw condition"""
    board = create_board()
    # Fill board with no winner
    moves = [
        (0, 0, 'X'), (0, 1, 'O'), (0, 2, 'X'),
        (1, 0, 'O'), (1, 1, 'X'), (1, 2, 'O'),
        (2, 0, 'O'), (2, 1, 'X'), (2, 2, 'O')
    ]
    for row, col, player in moves:
        make_move(board, row, col, player)

    assert is_board_full(board) == True, "Board should be full"
    assert check_winner(board, 'X') == False, "X should not have won"
    assert check_winner(board, 'O') == False, "O should not have won"
    print("✓ Draw detection test passed")


def test_available_moves():
    """Test getting available moves"""
    board = create_board()
    moves = get_available_moves(board)
    assert len(moves) == 9, "Empty board should have 9 available moves"

    make_move(board, 1, 1, 'X')
    moves = get_available_moves(board)
    assert len(moves) == 8, "Board with 1 move should have 8 available moves"
    assert (1, 1) not in moves, "Occupied position should not be available"
    print("✓ Available moves test passed")


def run_all_tests():
    """Run all tests"""
    print("Running Tic-Tac-Toe tests...\n")

    try:
        test_board_creation()
        test_valid_moves()
        test_winner_detection()
        test_draw_detection()
        test_available_moves()

        print("\n" + "=" * 40)
        print("All tests passed! ✓")
        print("=" * 40)
        return True

    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return False
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
