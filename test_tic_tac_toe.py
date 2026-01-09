"""
@file test_tic_tac_toe.py
@brief Unit tests for the Tic Tac Toe game module.

This module contains comprehensive unit tests for all game functions
including board operations, move validation, win detection, and AI logic.

@author User
@date 2024
"""

import unittest
from unittest.mock import patch

from tic_tac_toe import (
    Difficulty,
    GameResult,
    Scoreboard,
    check_winner,
    computer_move_easy,
    computer_move_hard,
    copy_board,
    create_board,
    find_winning_move,
    get_available_moves,
    get_position,
    is_board_full,
    is_valid_move,
    make_move,
    position_to_num,
)


class TestBoardCreation(unittest.TestCase):
    """
    @brief Test cases for board creation and copying functions.
    """

    def test_create_board_returns_3x3_grid(self) -> None:
        """
        @brief Verify create_board returns a 3x3 grid.
        """
        board = create_board()
        self.assertEqual(len(board), 3)
        for row in board:
            self.assertEqual(len(row), 3)

    def test_create_board_all_empty(self) -> None:
        """
        @brief Verify all cells in new board are empty spaces.
        """
        board = create_board()
        for row in board:
            for cell in row:
                self.assertEqual(cell, " ")

    def test_copy_board_creates_independent_copy(self) -> None:
        """
        @brief Verify copy_board creates a deep copy.
        """
        original = create_board()
        original[0][0] = "X"
        copied = copy_board(original)

        # Modify copy and verify original is unchanged
        copied[0][0] = "O"
        self.assertEqual(original[0][0], "X")
        self.assertEqual(copied[0][0], "O")

    def test_copy_board_preserves_state(self) -> None:
        """
        @brief Verify copy_board preserves all cell values.
        """
        original = create_board()
        original[0][0] = "X"
        original[1][1] = "O"
        original[2][2] = "X"

        copied = copy_board(original)
        self.assertEqual(copied[0][0], "X")
        self.assertEqual(copied[1][1], "O")
        self.assertEqual(copied[2][2], "X")


class TestPositionConversion(unittest.TestCase):
    """
    @brief Test cases for position conversion functions.
    """

    def test_get_position_corners(self) -> None:
        """
        @brief Verify corner positions convert correctly.
        """
        self.assertEqual(get_position(1), (0, 0))  # Top-left
        self.assertEqual(get_position(3), (0, 2))  # Top-right
        self.assertEqual(get_position(7), (2, 0))  # Bottom-left
        self.assertEqual(get_position(9), (2, 2))  # Bottom-right

    def test_get_position_center(self) -> None:
        """
        @brief Verify center position converts correctly.
        """
        self.assertEqual(get_position(5), (1, 1))

    def test_get_position_edges(self) -> None:
        """
        @brief Verify edge positions convert correctly.
        """
        self.assertEqual(get_position(2), (0, 1))  # Top
        self.assertEqual(get_position(4), (1, 0))  # Left
        self.assertEqual(get_position(6), (1, 2))  # Right
        self.assertEqual(get_position(8), (2, 1))  # Bottom

    def test_position_to_num_inverse(self) -> None:
        """
        @brief Verify position_to_num is inverse of get_position.
        """
        for pos in range(1, 10):
            row, col = get_position(pos)
            self.assertEqual(position_to_num(row, col), pos)


class TestMoveValidation(unittest.TestCase):
    """
    @brief Test cases for move validation.
    """

    def test_is_valid_move_empty_board(self) -> None:
        """
        @brief Verify all positions are valid on empty board.
        """
        board = create_board()
        for pos in range(1, 10):
            self.assertTrue(is_valid_move(board, pos))

    def test_is_valid_move_occupied_cell(self) -> None:
        """
        @brief Verify occupied cells are invalid moves.
        """
        board = create_board()
        make_move(board, 5, "X")
        self.assertFalse(is_valid_move(board, 5))

    def test_is_valid_move_out_of_range(self) -> None:
        """
        @brief Verify out-of-range positions are invalid.
        """
        board = create_board()
        self.assertFalse(is_valid_move(board, 0))
        self.assertFalse(is_valid_move(board, 10))
        self.assertFalse(is_valid_move(board, -1))


class TestMakeMove(unittest.TestCase):
    """
    @brief Test cases for making moves on the board.
    """

    def test_make_move_places_marker(self) -> None:
        """
        @brief Verify make_move places the correct marker.
        """
        board = create_board()
        make_move(board, 1, "X")
        self.assertEqual(board[0][0], "X")

    def test_make_move_different_positions(self) -> None:
        """
        @brief Verify moves work for all positions.
        """
        board = create_board()
        make_move(board, 5, "O")
        self.assertEqual(board[1][1], "O")

        make_move(board, 9, "X")
        self.assertEqual(board[2][2], "X")


class TestWinDetection(unittest.TestCase):
    """
    @brief Test cases for win condition detection.
    """

    def test_check_winner_row_win(self) -> None:
        """
        @brief Verify horizontal win detection.
        """
        board = create_board()
        # Top row win
        board[0] = ["X", "X", "X"]
        self.assertTrue(check_winner(board, "X"))
        self.assertFalse(check_winner(board, "O"))

    def test_check_winner_column_win(self) -> None:
        """
        @brief Verify vertical win detection.
        """
        board = create_board()
        # Left column win
        board[0][0] = "O"
        board[1][0] = "O"
        board[2][0] = "O"
        self.assertTrue(check_winner(board, "O"))
        self.assertFalse(check_winner(board, "X"))

    def test_check_winner_diagonal_win(self) -> None:
        """
        @brief Verify main diagonal win detection.
        """
        board = create_board()
        board[0][0] = "X"
        board[1][1] = "X"
        board[2][2] = "X"
        self.assertTrue(check_winner(board, "X"))

    def test_check_winner_anti_diagonal_win(self) -> None:
        """
        @brief Verify anti-diagonal win detection.
        """
        board = create_board()
        board[0][2] = "O"
        board[1][1] = "O"
        board[2][0] = "O"
        self.assertTrue(check_winner(board, "O"))

    def test_check_winner_no_winner(self) -> None:
        """
        @brief Verify no false positives when no winner.
        """
        board = create_board()
        board[0][0] = "X"
        board[0][1] = "O"
        board[0][2] = "X"
        self.assertFalse(check_winner(board, "X"))
        self.assertFalse(check_winner(board, "O"))

    def test_check_winner_all_rows(self) -> None:
        """
        @brief Verify win detection for all three rows.
        """
        for row_idx in range(3):
            board = create_board()
            board[row_idx] = ["X", "X", "X"]
            self.assertTrue(check_winner(board, "X"))

    def test_check_winner_all_columns(self) -> None:
        """
        @brief Verify win detection for all three columns.
        """
        for col_idx in range(3):
            board = create_board()
            for row_idx in range(3):
                board[row_idx][col_idx] = "O"
            self.assertTrue(check_winner(board, "O"))


class TestBoardFull(unittest.TestCase):
    """
    @brief Test cases for board full detection.
    """

    def test_is_board_full_empty(self) -> None:
        """
        @brief Verify empty board is not full.
        """
        board = create_board()
        self.assertFalse(is_board_full(board))

    def test_is_board_full_partial(self) -> None:
        """
        @brief Verify partially filled board is not full.
        """
        board = create_board()
        make_move(board, 1, "X")
        make_move(board, 2, "O")
        self.assertFalse(is_board_full(board))

    def test_is_board_full_complete(self) -> None:
        """
        @brief Verify completely filled board is detected as full.
        """
        board = [
            ["X", "O", "X"],
            ["O", "X", "O"],
            ["O", "X", "O"],
        ]
        self.assertTrue(is_board_full(board))


class TestAvailableMoves(unittest.TestCase):
    """
    @brief Test cases for available moves detection.
    """

    def test_get_available_moves_empty_board(self) -> None:
        """
        @brief Verify all 9 positions available on empty board.
        """
        board = create_board()
        moves = get_available_moves(board)
        self.assertEqual(moves, [1, 2, 3, 4, 5, 6, 7, 8, 9])

    def test_get_available_moves_partial(self) -> None:
        """
        @brief Verify correct moves on partially filled board.
        """
        board = create_board()
        make_move(board, 1, "X")
        make_move(board, 5, "O")
        moves = get_available_moves(board)
        self.assertEqual(moves, [2, 3, 4, 6, 7, 8, 9])

    def test_get_available_moves_full_board(self) -> None:
        """
        @brief Verify no moves available on full board.
        """
        board = [
            ["X", "O", "X"],
            ["O", "X", "O"],
            ["O", "X", "O"],
        ]
        moves = get_available_moves(board)
        self.assertEqual(moves, [])


class TestFindWinningMove(unittest.TestCase):
    """
    @brief Test cases for finding winning moves.
    """

    def test_find_winning_move_exists(self) -> None:
        """
        @brief Verify winning move is found when it exists.
        """
        board = create_board()
        board[0][0] = "X"
        board[0][1] = "X"
        # Position 3 (0,2) should win
        winning = find_winning_move(board, "X")
        self.assertEqual(winning, 3)

    def test_find_winning_move_none(self) -> None:
        """
        @brief Verify None returned when no winning move.
        """
        board = create_board()
        board[0][0] = "X"
        winning = find_winning_move(board, "X")
        self.assertIsNone(winning)

    def test_find_winning_move_column(self) -> None:
        """
        @brief Verify winning move found in column.
        """
        board = create_board()
        board[0][0] = "O"
        board[1][0] = "O"
        # Position 7 (2,0) should win
        winning = find_winning_move(board, "O")
        self.assertEqual(winning, 7)

    def test_find_winning_move_diagonal(self) -> None:
        """
        @brief Verify winning move found in diagonal.
        """
        board = create_board()
        board[0][0] = "X"
        board[1][1] = "X"
        # Position 9 (2,2) should win
        winning = find_winning_move(board, "X")
        self.assertEqual(winning, 9)


class TestComputerMoveHard(unittest.TestCase):
    """
    @brief Test cases for hard mode AI (minimax).
    """

    def test_computer_takes_winning_move(self) -> None:
        """
        @brief Verify AI takes winning move when available.
        """
        board = create_board()
        board[0][0] = "O"
        board[0][1] = "O"
        # Computer should take position 3 to win
        move = computer_move_hard(board, "O", "X")
        self.assertEqual(move, 3)

    def test_computer_blocks_opponent(self) -> None:
        """
        @brief Verify AI blocks opponent's winning move.
        """
        board = create_board()
        board[0][0] = "X"
        board[0][1] = "X"
        # Computer should block at position 3
        move = computer_move_hard(board, "O", "X")
        self.assertEqual(move, 3)

    def test_computer_prefers_win_over_block(self) -> None:
        """
        @brief Verify AI prefers winning over blocking.
        """
        board = create_board()
        # X can win at position 3
        board[0][0] = "X"
        board[0][1] = "X"
        # O can win at position 6
        board[1][0] = "O"
        board[1][1] = "O"
        # Computer (O) should take position 6 to win
        move = computer_move_hard(board, "O", "X")
        self.assertEqual(move, 6)


class TestComputerMoveEasy(unittest.TestCase):
    """
    @brief Test cases for easy mode AI.
    """

    def test_computer_move_easy_returns_valid_move(self) -> None:
        """
        @brief Verify easy AI returns a valid move.
        """
        board = create_board()
        move = computer_move_easy(board, "O", "X")
        self.assertIn(move, range(1, 10))

    def test_computer_move_easy_respects_available(self) -> None:
        """
        @brief Verify easy AI only picks available positions.
        """
        board = create_board()
        # Fill most of the board
        make_move(board, 1, "X")
        make_move(board, 2, "O")
        make_move(board, 3, "X")
        make_move(board, 4, "O")
        make_move(board, 5, "X")
        make_move(board, 6, "O")
        make_move(board, 7, "X")
        # Only 8, 9 available
        move = computer_move_easy(board, "O", "X")
        self.assertIn(move, [8, 9])

    @patch("tic_tac_toe.random.random")
    def test_computer_move_easy_smart_mode_wins(
        self, mock_random: unittest.mock.MagicMock
    ) -> None:
        """
        @brief Verify easy AI takes winning move in smart mode.
        """
        mock_random.return_value = 0.1  # Trigger smart mode (< 0.3)

        board = create_board()
        board[0][0] = "O"
        board[0][1] = "O"
        # Should take position 3 to win
        move = computer_move_easy(board, "O", "X")
        self.assertEqual(move, 3)

    @patch("tic_tac_toe.random.random")
    def test_computer_move_easy_smart_mode_blocks(
        self, mock_random: unittest.mock.MagicMock
    ) -> None:
        """
        @brief Verify easy AI blocks in smart mode when can't win.
        """
        mock_random.return_value = 0.1  # Trigger smart mode (< 0.3)

        board = create_board()
        board[0][0] = "X"
        board[0][1] = "X"
        # Should block at position 3
        move = computer_move_easy(board, "O", "X")
        self.assertEqual(move, 3)


class TestGameScenarios(unittest.TestCase):
    """
    @brief Integration tests for complete game scenarios.
    """

    def test_draw_scenario(self) -> None:
        """
        @brief Verify draw detection in a complete game.
        """
        board = [
            ["X", "O", "X"],
            ["X", "X", "O"],
            ["O", "X", "O"],
        ]
        self.assertTrue(is_board_full(board))
        self.assertFalse(check_winner(board, "X"))
        self.assertFalse(check_winner(board, "O"))

    def test_x_wins_scenario(self) -> None:
        """
        @brief Verify X win detection in a complete game.
        """
        board = [
            ["X", "X", "X"],
            ["O", "O", " "],
            [" ", " ", " "],
        ]
        self.assertTrue(check_winner(board, "X"))
        self.assertFalse(is_board_full(board))

    def test_o_wins_scenario(self) -> None:
        """
        @brief Verify O win detection in a complete game.
        """
        board = [
            ["X", "X", "O"],
            ["X", "O", " "],
            ["O", " ", " "],
        ]
        self.assertTrue(check_winner(board, "O"))


class TestScoreboard(unittest.TestCase):
    """
    @brief Test cases for the Scoreboard class.
    """

    def test_scoreboard_initial_state(self) -> None:
        """
        @brief Verify scoreboard starts with zero scores.
        """
        scoreboard = Scoreboard()
        self.assertEqual(scoreboard.player1_wins, 0)
        self.assertEqual(scoreboard.player2_wins, 0)
        self.assertEqual(scoreboard.draws, 0)
        self.assertEqual(scoreboard.games_played, 0)

    def test_scoreboard_custom_names(self) -> None:
        """
        @brief Verify scoreboard accepts custom player names.
        """
        scoreboard = Scoreboard(player1_name="Alice", player2_name="Bob")
        self.assertEqual(scoreboard.player1_name, "Alice")
        self.assertEqual(scoreboard.player2_name, "Bob")

    def test_record_player1_win(self) -> None:
        """
        @brief Verify recording a player 1 win.
        """
        scoreboard = Scoreboard()
        scoreboard.record_result(GameResult.PLAYER1_WIN)
        self.assertEqual(scoreboard.player1_wins, 1)
        self.assertEqual(scoreboard.player2_wins, 0)
        self.assertEqual(scoreboard.draws, 0)
        self.assertEqual(scoreboard.games_played, 1)

    def test_record_player2_win(self) -> None:
        """
        @brief Verify recording a player 2 win.
        """
        scoreboard = Scoreboard()
        scoreboard.record_result(GameResult.PLAYER2_WIN)
        self.assertEqual(scoreboard.player1_wins, 0)
        self.assertEqual(scoreboard.player2_wins, 1)
        self.assertEqual(scoreboard.draws, 0)
        self.assertEqual(scoreboard.games_played, 1)

    def test_record_draw(self) -> None:
        """
        @brief Verify recording a draw.
        """
        scoreboard = Scoreboard()
        scoreboard.record_result(GameResult.DRAW)
        self.assertEqual(scoreboard.player1_wins, 0)
        self.assertEqual(scoreboard.player2_wins, 0)
        self.assertEqual(scoreboard.draws, 1)
        self.assertEqual(scoreboard.games_played, 1)

    def test_record_multiple_games(self) -> None:
        """
        @brief Verify recording multiple game results.
        """
        scoreboard = Scoreboard()
        scoreboard.record_result(GameResult.PLAYER1_WIN)
        scoreboard.record_result(GameResult.PLAYER2_WIN)
        scoreboard.record_result(GameResult.PLAYER1_WIN)
        scoreboard.record_result(GameResult.DRAW)
        scoreboard.record_result(GameResult.PLAYER1_WIN)

        self.assertEqual(scoreboard.player1_wins, 3)
        self.assertEqual(scoreboard.player2_wins, 1)
        self.assertEqual(scoreboard.draws, 1)
        self.assertEqual(scoreboard.games_played, 5)

    def test_reset_scoreboard(self) -> None:
        """
        @brief Verify reset clears all scores.
        """
        scoreboard = Scoreboard()
        scoreboard.record_result(GameResult.PLAYER1_WIN)
        scoreboard.record_result(GameResult.PLAYER2_WIN)
        scoreboard.record_result(GameResult.DRAW)

        scoreboard.reset()

        self.assertEqual(scoreboard.player1_wins, 0)
        self.assertEqual(scoreboard.player2_wins, 0)
        self.assertEqual(scoreboard.draws, 0)
        self.assertEqual(scoreboard.games_played, 0)

    def test_reset_preserves_names(self) -> None:
        """
        @brief Verify reset preserves player names.
        """
        scoreboard = Scoreboard(player1_name="Alice", player2_name="Bob")
        scoreboard.record_result(GameResult.PLAYER1_WIN)
        scoreboard.reset()

        self.assertEqual(scoreboard.player1_name, "Alice")
        self.assertEqual(scoreboard.player2_name, "Bob")


class TestGameResult(unittest.TestCase):
    """
    @brief Test cases for the GameResult enum.
    """

    def test_game_result_values(self) -> None:
        """
        @brief Verify GameResult enum values.
        """
        self.assertEqual(GameResult.PLAYER1_WIN.value, 1)
        self.assertEqual(GameResult.PLAYER2_WIN.value, 2)
        self.assertEqual(GameResult.DRAW.value, 3)

    def test_game_result_distinct(self) -> None:
        """
        @brief Verify GameResult values are distinct.
        """
        self.assertNotEqual(GameResult.PLAYER1_WIN, GameResult.PLAYER2_WIN)
        self.assertNotEqual(GameResult.PLAYER1_WIN, GameResult.DRAW)
        self.assertNotEqual(GameResult.PLAYER2_WIN, GameResult.DRAW)


if __name__ == "__main__":
    unittest.main()
