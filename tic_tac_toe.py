"""
@file tic_tac_toe.py
@brief Tic Tac Toe game with multiple game modes.

This module implements a command-line Tic Tac Toe game that supports:
- Single player vs computer (Easy mode - beatable AI)
- Single player vs computer (Hard mode - unbeatable AI using minimax)
- Two player mode (local multiplayer)

@author User
@date 2024
"""

import random
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class GameMode(Enum):
    """
    @brief Enumeration of available game modes.
    """
    EASY = 1
    HARD = 2
    TWO_PLAYER = 3


class Difficulty(Enum):
    """
    @brief Enumeration of AI difficulty levels.
    """
    EASY = 1
    HARD = 2


class GameResult(Enum):
    """
    @brief Enumeration of possible game outcomes.
    """
    PLAYER1_WIN = 1  # Human wins in vs computer, Player 1 wins in two player
    PLAYER2_WIN = 2  # Computer wins in vs computer, Player 2 wins in two player
    DRAW = 3


@dataclass
class Scoreboard:
    """
    @brief Tracks scores between players across a gaming session.

    Maintains win counts for both players and draws. Provides methods
    to record game results and display the current score.
    """
    player1_name: str = "Player 1"
    player2_name: str = "Player 2"
    player1_wins: int = 0
    player2_wins: int = 0
    draws: int = 0
    games_played: int = 0

    def record_result(self, result: GameResult) -> None:
        """
        @brief Record the result of a game.

        @param result The outcome of the game.
        """
        self.games_played += 1
        if result == GameResult.PLAYER1_WIN:
            self.player1_wins += 1
        elif result == GameResult.PLAYER2_WIN:
            self.player2_wins += 1
        else:
            self.draws += 1

    def display(self) -> None:
        """
        @brief Display the current scoreboard to the console.
        """
        print("\n" + "=" * 40)
        print("            SCOREBOARD")
        print("=" * 40)
        print(f"  {self.player1_name}: {self.player1_wins}")
        print(f"  {self.player2_name}: {self.player2_wins}")
        print(f"  Draws: {self.draws}")
        print(f"  Games Played: {self.games_played}")
        print("=" * 40)

    def reset(self) -> None:
        """
        @brief Reset all scores to zero.
        """
        self.player1_wins = 0
        self.player2_wins = 0
        self.draws = 0
        self.games_played = 0


# Type alias for the game board
Board = list[list[str]]


def create_board() -> Board:
    """
    @brief Create an empty 3x3 game board.

    @return A 3x3 list of lists initialized with empty spaces.
    """
    return [[" " for _ in range(3)] for _ in range(3)]


def copy_board(board: Board) -> Board:
    """
    @brief Create a deep copy of the game board.

    @param board The board to copy.
    @return A new board with the same state.
    """
    return [row[:] for row in board]


def display_board(board: Board) -> None:
    """
    @brief Display the current board state to the console.

    Renders the board in a human-readable format with grid lines.

    @param board The current game board to display.
    """
    print("\n")
    for i, row in enumerate(board):
        print(f" {row[0]} | {row[1]} | {row[2]} ")
        if i < 2:
            print("-----------")
    print("\n")


def display_positions() -> None:
    """
    @brief Display position numbers for player reference.

    Shows a diagram of the board with position numbers 1-9
    so players know which number corresponds to which cell.
    """
    print("\nPosition numbers:")
    print(" 1 | 2 | 3 ")
    print("-----------")
    print(" 4 | 5 | 6 ")
    print("-----------")
    print(" 7 | 8 | 9 ")
    print()


def get_position(num: int) -> tuple[int, int]:
    """
    @brief Convert a position number (1-9) to board coordinates.

    @param num The position number from 1 to 9.
    @return A tuple of (row, column) indices for the board.

    @note Position mapping:
          1 -> (0,0), 2 -> (0,1), 3 -> (0,2)
          4 -> (1,0), 5 -> (1,1), 6 -> (1,2)
          7 -> (2,0), 8 -> (2,1), 9 -> (2,2)
    """
    num -= 1
    return num // 3, num % 3


def position_to_num(row: int, col: int) -> int:
    """
    @brief Convert board coordinates to a position number.

    @param row The row index (0-2).
    @param col The column index (0-2).
    @return The position number from 1 to 9.
    """
    return row * 3 + col + 1


def is_valid_move(board: Board, position: int) -> bool:
    """
    @brief Check if a move is valid.

    A move is valid if the position is between 1-9 and the cell is empty.

    @param board The current game board.
    @param position The position number to check (1-9).
    @return True if the move is valid, False otherwise.
    """
    if position < 1 or position > 9:
        return False
    row, col = get_position(position)
    return board[row][col] == " "


def make_move(board: Board, position: int, player: str) -> None:
    """
    @brief Place a player's mark on the board.

    @param board The current game board (modified in place).
    @param position The position number where to place the mark (1-9).
    @param player The player's mark ('X' or 'O').

    @pre is_valid_move(board, position) must be True.
    """
    row, col = get_position(position)
    board[row][col] = player


def check_winner(board: Board, player: str) -> bool:
    """
    @brief Check if the specified player has won the game.

    Checks all possible winning conditions:
    - Three in a row (horizontal)
    - Three in a column (vertical)
    - Three in a diagonal

    @param board The current game board.
    @param player The player's mark to check ('X' or 'O').
    @return True if the player has won, False otherwise.
    """
    # Check rows
    for row in board:
        if all(cell == player for cell in row):
            return True

    # Check columns
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True

    # Check main diagonal (top-left to bottom-right)
    if all(board[i][i] == player for i in range(3)):
        return True

    # Check anti-diagonal (top-right to bottom-left)
    if all(board[i][2 - i] == player for i in range(3)):
        return True

    return False


def is_board_full(board: Board) -> bool:
    """
    @brief Check if the board is completely filled.

    @param board The current game board.
    @return True if no empty cells remain, False otherwise.
    """
    return all(cell != " " for row in board for cell in row)


def get_available_moves(board: Board) -> list[int]:
    """
    @brief Get a list of all available (empty) positions.

    @param board The current game board.
    @return A list of position numbers (1-9) that are still available.
    """
    moves = []
    for i in range(1, 10):
        if is_valid_move(board, i):
            moves.append(i)
    return moves


def find_winning_move(board: Board, player: str) -> Optional[int]:
    """
    @brief Find a move that would win the game for the specified player.

    @param board The current game board.
    @param player The player's mark ('X' or 'O').
    @return The winning position number, or None if no winning move exists.
    """
    for move in get_available_moves(board):
        test_board = copy_board(board)
        make_move(test_board, move, player)
        if check_winner(test_board, player):
            return move
    return None


def minimax(board: Board, is_maximizing: bool, player: str, opponent: str) -> float:
    """
    @brief Minimax algorithm for optimal move calculation.

    Recursively evaluates all possible game states to find the optimal move.
    Uses a simple scoring system: +10 for win, -10 for loss, 0 for draw.

    @param board The current game board.
    @param is_maximizing True if maximizing player's turn, False otherwise.
    @param player The AI player's mark.
    @param opponent The opponent's mark.
    @return The score of the best possible outcome from this state.
    """
    # Terminal states
    if check_winner(board, opponent):
        return -10.0
    if check_winner(board, player):
        return 10.0
    if is_board_full(board):
        return 0.0

    available = get_available_moves(board)

    if is_maximizing:
        best_score: float = float("-inf")
        for move in available:
            make_move(board, move, player)
            score = minimax(board, False, player, opponent)
            row, col = get_position(move)
            board[row][col] = " "  # Undo move
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for move in available:
            make_move(board, move, opponent)
            score = minimax(board, True, player, opponent)
            row, col = get_position(move)
            board[row][col] = " "  # Undo move
            best_score = min(score, best_score)
        return best_score


def computer_move_hard(board: Board, computer: str, human: str) -> int:
    """
    @brief Determine the optimal move for the computer using minimax.

    This AI is unbeatable - it will always win or draw.

    @param board The current game board.
    @param computer The computer's mark ('X' or 'O').
    @param human The human player's mark.
    @return The position number of the best move (1-9).
    """
    available = get_available_moves(board)

    # First move optimization: pick a corner or center
    if len(available) == 9:
        return random.choice([1, 3, 5, 7, 9])

    best_score: float = float("-inf")
    best_move = available[0]

    for move in available:
        make_move(board, move, computer)
        score = minimax(board, False, computer, human)
        row, col = get_position(move)
        board[row][col] = " "  # Undo move

        if score > best_score:
            best_score = score
            best_move = move

    return best_move


def computer_move_easy(board: Board, computer: str, human: str) -> int:
    """
    @brief Determine a move for the computer in easy mode.

    Easy mode AI behavior:
    - 30% chance to make a smart move (block or win)
    - 70% chance to make a random move

    This makes the AI beatable while still providing some challenge.

    @param board The current game board.
    @param computer The computer's mark ('X' or 'O').
    @param human The human player's mark.
    @return The position number of the chosen move (1-9).
    """
    available = get_available_moves(board)

    # 30% chance to play smart
    if random.random() < 0.3:
        # Check if computer can win
        winning_move = find_winning_move(board, computer)
        if winning_move is not None:
            return winning_move

        # Check if need to block human
        blocking_move = find_winning_move(board, human)
        if blocking_move is not None:
            return blocking_move

    # Otherwise, make a random move
    return random.choice(available)


def get_computer_move(
    board: Board, computer: str, human: str, difficulty: Difficulty
) -> int:
    """
    @brief Get the computer's move based on difficulty setting.

    @param board The current game board.
    @param computer The computer's mark ('X' or 'O').
    @param human The human player's mark.
    @param difficulty The AI difficulty level.
    @return The position number of the computer's move (1-9).
    """
    if difficulty == Difficulty.EASY:
        return computer_move_easy(board, computer, human)
    else:
        return computer_move_hard(board, computer, human)


def get_player_move(board: Board, player_name: str = "Player") -> int:
    """
    @brief Get a valid move from a human player via console input.

    Continues prompting until a valid move is entered.

    @param board The current game board.
    @param player_name The name to display in the prompt.
    @return The position number of the player's move (1-9).
    """
    while True:
        try:
            move = input(f"{player_name}, enter your move (1-9): ").strip()
            move = int(move)
            if is_valid_move(board, move):
                return move
            else:
                print("Invalid move. Position is either taken or out of range.")
        except ValueError:
            print("Please enter a number between 1 and 9.")


def select_game_mode() -> GameMode:
    """
    @brief Display menu and get the user's game mode selection.

    @return The selected GameMode enum value.
    """
    print("\n=== SELECT GAME MODE ===")
    print("1. Easy Mode (vs Computer - beatable)")
    print("2. Hard Mode (vs Computer - unbeatable)")
    print("3. Two Player Mode")

    while True:
        try:
            choice = int(input("\nEnter your choice (1-3): ").strip())
            if choice == 1:
                return GameMode.EASY
            elif choice == 2:
                return GameMode.HARD
            elif choice == 3:
                return GameMode.TWO_PLAYER
            else:
                print("Please enter 1, 2, or 3.")
        except ValueError:
            print("Please enter a valid number.")


def play_vs_computer(difficulty: Difficulty) -> GameResult:
    """
    @brief Play a game against the computer.

    @param difficulty The AI difficulty level (EASY or HARD).
    @return The result of the game (PLAYER1_WIN for human, PLAYER2_WIN for computer).
    """
    mode_name = "Easy" if difficulty == Difficulty.EASY else "Hard"
    print(f"\n=== TIC TAC TOE ({mode_name} Mode) ===")
    print("You are X, Computer is O")
    display_positions()

    board = create_board()
    human = "X"
    computer = "O"
    current_player = human  # Human goes first

    while True:
        display_board(board)

        if current_player == human:
            print("Your turn!")
            move = get_player_move(board, "You")
            make_move(board, move, human)

            if check_winner(board, human):
                display_board(board)
                print("Congratulations! You win!")
                return GameResult.PLAYER1_WIN
        else:
            print("Computer is thinking...")
            move = get_computer_move(board, computer, human, difficulty)
            make_move(board, move, computer)
            print(f"Computer plays position {move}")

            if check_winner(board, computer):
                display_board(board)
                print("Computer wins! Better luck next time.")
                return GameResult.PLAYER2_WIN

        if is_board_full(board):
            display_board(board)
            print("It's a draw!")
            return GameResult.DRAW

        # Switch players
        current_player = computer if current_player == human else human


def play_two_player() -> GameResult:
    """
    @brief Play a two-player game (local multiplayer).

    Player 1 is X, Player 2 is O. Players alternate turns.

    @return The result of the game.
    """
    print("\n=== TIC TAC TOE (Two Player Mode) ===")
    print("Player 1 is X, Player 2 is O")
    display_positions()

    board = create_board()
    player1 = "X"
    player2 = "O"
    current_player = player1

    while True:
        display_board(board)

        player_name = "Player 1 (X)" if current_player == player1 else "Player 2 (O)"
        print(f"{player_name}'s turn!")
        move = get_player_move(board, player_name)
        make_move(board, move, current_player)

        if check_winner(board, current_player):
            display_board(board)
            print(f"{player_name} wins!")
            if current_player == player1:
                return GameResult.PLAYER1_WIN
            else:
                return GameResult.PLAYER2_WIN

        if is_board_full(board):
            display_board(board)
            print("It's a draw!")
            return GameResult.DRAW

        # Switch players
        current_player = player2 if current_player == player1 else player1


def play_game(scoreboard: Scoreboard) -> GameMode:
    """
    @brief Main game orchestration function.

    Handles game mode selection and dispatches to the appropriate
    game function based on user choice. Records the result to the scoreboard.

    @param scoreboard The scoreboard to record the game result.
    @return The game mode that was played.
    """
    game_mode = select_game_mode()

    # Set appropriate player names based on game mode
    if game_mode == GameMode.TWO_PLAYER:
        scoreboard.player1_name = "Player 1"
        scoreboard.player2_name = "Player 2"
    else:
        scoreboard.player1_name = "You"
        scoreboard.player2_name = "Computer"

    if game_mode == GameMode.EASY:
        result = play_vs_computer(Difficulty.EASY)
    elif game_mode == GameMode.HARD:
        result = play_vs_computer(Difficulty.HARD)
    else:
        result = play_two_player()

    scoreboard.record_result(result)
    scoreboard.display()

    return game_mode


def main() -> None:
    """
    @brief Main entry point for the Tic Tac Toe game.

    Runs the game loop, allowing players to play multiple games
    until they choose to quit. Tracks scores across the session.
    """
    print("\n" + "=" * 40)
    print("       WELCOME TO TIC TAC TOE")
    print("=" * 40)

    scoreboard = Scoreboard()
    last_game_mode: Optional[GameMode] = None

    while True:
        current_mode = play_game(scoreboard)

        # Check if game mode changed and offer to reset scores
        if last_game_mode is not None and current_mode != last_game_mode:
            if scoreboard.games_played > 1:
                reset = input("\nGame mode changed. Reset scores? (y/n): ").strip().lower()
                if reset == "y":
                    scoreboard.reset()
                    print("Scores have been reset!")

        last_game_mode = current_mode

        print("\nWhat would you like to do?")
        print("1. Play again (same mode)")
        print("2. Change game mode")
        print("3. Reset scores")
        print("4. Quit")

        while True:
            try:
                choice = input("\nEnter your choice (1-4): ").strip()
                if choice == "1":
                    # Play again with same mode
                    if current_mode == GameMode.TWO_PLAYER:
                        result = play_two_player()
                    elif current_mode == GameMode.EASY:
                        result = play_vs_computer(Difficulty.EASY)
                    else:
                        result = play_vs_computer(Difficulty.HARD)
                    scoreboard.record_result(result)
                    scoreboard.display()
                    break
                elif choice == "2":
                    # Will select new mode at top of loop
                    break
                elif choice == "3":
                    scoreboard.reset()
                    print("Scores have been reset!")
                    scoreboard.display()
                elif choice == "4":
                    print("\n" + "=" * 40)
                    print("        FINAL SCORES")
                    scoreboard.display()
                    print("\nThanks for playing!")
                    return
                else:
                    print("Please enter 1, 2, 3, or 4.")
            except ValueError:
                print("Please enter a valid number.")

        # If choice was "1", we already played, so continue to menu
        # If choice was "2", continue to top of loop for new mode selection
        if choice == "1":
            continue


if __name__ == "__main__":
    main()
