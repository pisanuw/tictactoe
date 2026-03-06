#!/usr/bin/env python3
"""
Cloud Run web entrypoint for Tic-Tac-Toe.

This wraps existing game logic from tictactoe_cli.py into a simple
browser-playable web app and JSON API suitable for deployment.
"""

import os
from typing import List

from flask import Flask, jsonify, render_template_string, request

from tictactoe_cli import check_winner, get_ai_move, is_board_full


app = Flask(__name__)


PAGE_HTML = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Tic-Tac-Toe Cloud</title>
  <style>
    body { font-family: Arial, sans-serif; max-width: 560px; margin: 24px auto; padding: 0 12px; }
    h1 { margin-bottom: 8px; }
    .controls { margin: 12px 0 18px; display: flex; gap: 12px; align-items: center; }
    .board { display: grid; grid-template-columns: repeat(3, 96px); gap: 8px; }
    button.cell { height: 96px; font-size: 40px; cursor: pointer; }
    .status { margin: 14px 0; font-weight: bold; min-height: 24px; }
    .actions { margin-top: 12px; }
    button { padding: 8px 12px; }
    select { padding: 6px; }
  </style>
</head>
<body>
  <h1>Tic-Tac-Toe Cloud</h1>
  <p>Play in your browser. You are X, AI is O.</p>

  <div class="controls">
    <label for="difficulty">Difficulty:</label>
    <select id="difficulty">
      <option value="easy">Easy</option>
      <option value="medium">Medium</option>
      <option value="hard" selected>Hard</option>
    </select>
    <button id="newGame">New Game</button>
  </div>

  <div class="status" id="status">Your turn</div>
  <div class="board" id="board"></div>

  <script>
    let board = [
      [' ', ' ', ' '],
      [' ', ' ', ' '],
      [' ', ' ', ' ']
    ];
    let gameOver = false;
    let isProcessing = false;

    function renderBoard() {
      const boardEl = document.getElementById('board');
      boardEl.innerHTML = '';
      for (let r = 0; r < 3; r++) {
        for (let c = 0; c < 3; c++) {
          const cell = document.createElement('button');
          cell.className = 'cell';
          cell.textContent = board[r][c] === ' ' ? '' : board[r][c];
          cell.disabled = gameOver || board[r][c] !== ' ' || isProcessing;
          cell.addEventListener('click', () => playerMove(r, c));
          boardEl.appendChild(cell);
        }
      }
    }

    function setStatus(text) {
      document.getElementById('status').textContent = text;
    }

    function resetGame() {
      board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']];
      gameOver = false;
      isProcessing = false;
      setStatus('Your turn');
      renderBoard();
    }

    async function playerMove(row, col) {
      if (gameOver || board[row][col] !== ' ' || isProcessing) return;

      isProcessing = true;
      board[row][col] = 'X';
      renderBoard();

      const difficulty = document.getElementById('difficulty').value;
      setStatus('AI is thinking...');

      const response = await fetch('/api/ai-move', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ board, difficulty })
      });

      if (!response.ok) {
        setStatus('Error contacting server');
        isProcessing = false;
        renderBoard();
        return;
      }

      const result = await response.json();
      board = result.board;

      if (result.status === 'x_won') {
        gameOver = true;
        setStatus('You win!');
      } else if (result.status === 'o_won') {
        gameOver = true;
        setStatus('AI wins!');
      } else if (result.status === 'draw') {
        gameOver = true;
        setStatus('Draw game');
      } else {
        setStatus('Your turn');
      }

      isProcessing = false;
      renderBoard();
    }

    document.getElementById('newGame').addEventListener('click', resetGame);
    resetGame();
  </script>
</body>
</html>
"""


def _validate_board(board: List[List[str]]) -> bool:
    if not isinstance(board, list) or len(board) != 3:
        return False
    valid = {"X", "O", " "}
    for row in board:
        if not isinstance(row, list) or len(row) != 3:
            return False
        for cell in row:
            if cell not in valid:
                return False
    return True


def _status(board: List[List[str]]) -> str:
    if check_winner(board, "X"):
        return "x_won"
    if check_winner(board, "O"):
        return "o_won"
    if is_board_full(board):
        return "draw"
    return "in_progress"


@app.get("/")
def index():
    return render_template_string(PAGE_HTML)


@app.get("/healthz")
def healthz():
    return jsonify({"status": "ok"}), 200


@app.post("/api/ai-move")
def ai_move():
    payload = request.get_json(silent=True) or {}
    board = payload.get("board")
    difficulty = payload.get("difficulty", "hard")

    if difficulty not in {"easy", "medium", "hard"}:
        difficulty = "hard"

    if not _validate_board(board):
        return jsonify({"error": "Invalid board format"}), 400

    current_status = _status(board)
    if current_status != "in_progress":
        return jsonify({"board": board, "status": current_status}), 200

    ai_play = get_ai_move(board, "O", "X", difficulty)
    if ai_play is not None:
        row, col = ai_play
        board[row][col] = "O"

    return jsonify({"board": board, "status": _status(board)})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)
