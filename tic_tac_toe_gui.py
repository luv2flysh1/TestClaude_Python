"""
@file tic_tac_toe_gui.py
@brief Tkinter GUI for the Tic Tac Toe game.

This module provides a graphical user interface for the Tic Tac Toe game,
reusing the game logic from tic_tac_toe.py.

@author User
@date 2024
"""

import tkinter as tk
from typing import Optional

from tic_tac_toe import (
    Board,
    Difficulty,
    GameMode,
    GameResult,
    Scoreboard,
    check_winner,
    create_board,
    get_computer_move,
    is_board_full,
    is_valid_move,
    make_move,
    position_to_num,
)

# Color scheme
COLORS = {
    "background": "#1a1a2e",
    "primary": "#16213e",
    "accent": "#0f3460",
    "x_color": "#e94560",
    "o_color": "#00d9ff",
    "white": "#ffffff",
    "button_bg": "#0f3460",
    "button_hover": "#1a4a7a",
    "win_highlight": "#4ade80",
    "cell_bg": "#16213e",
}


class TicTacToeGUI:
    """
    @brief Main GUI class for the Tic Tac Toe game.

    Provides a graphical interface with mode selection, game board,
    scoreboard, and game controls.
    """

    def __init__(self) -> None:
        """
        @brief Initialize the GUI application.
        """
        self.root = tk.Tk()
        self.root.title("Tic Tac Toe")
        self.root.configure(bg=COLORS["background"])
        self.root.minsize(350, 500)

        # Configure root grid to expand
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Game state
        self.board: Board = create_board()
        self.current_player: str = "X"
        self.is_game_over: bool = False
        self.game_mode: Optional[GameMode] = None
        self.scoreboard = Scoreboard()
        self.waiting_for_computer: bool = False

        # UI components
        self.buttons: list[list[tk.Button]] = []
        self.status_label: Optional[tk.Label] = None
        self.score_label: Optional[tk.Label] = None
        self.games_label: Optional[tk.Label] = None
        self.header_label: Optional[tk.Label] = None
        self.new_game_btn: Optional[tk.Button] = None

        # Frames
        self.mode_frame: Optional[tk.Frame] = None
        self.game_frame: Optional[tk.Frame] = None

        # Build UI
        self._create_mode_frame()
        self._create_game_frame()
        self.show_mode_selection()

    def _create_mode_frame(self) -> None:
        """
        @brief Create the mode selection screen.
        """
        self.mode_frame = tk.Frame(self.root, bg=COLORS["background"])

        # Configure grid weights for centering
        self.mode_frame.grid_rowconfigure(0, weight=1)
        self.mode_frame.grid_rowconfigure(5, weight=1)
        self.mode_frame.grid_columnconfigure(0, weight=1)

        # Title
        title = tk.Label(
            self.mode_frame,
            text="TIC TAC TOE",
            font=("Helvetica", 28, "bold"),
            fg=COLORS["white"],
            bg=COLORS["background"],
        )
        title.grid(row=1, column=0, pady=(0, 10))

        # Subtitle
        subtitle = tk.Label(
            self.mode_frame,
            text="Select Game Mode",
            font=("Helvetica", 12),
            fg=COLORS["o_color"],
            bg=COLORS["background"],
        )
        subtitle.grid(row=2, column=0, pady=(0, 20))

        # Mode buttons container
        btn_frame = tk.Frame(self.mode_frame, bg=COLORS["background"])
        btn_frame.grid(row=3, column=0)

        modes = [
            ("Easy Mode", "Beatable AI (30% smart)", self._select_easy),
            ("Hard Mode", "Unbeatable AI (Minimax)", self._select_hard),
            ("Two Player", "Local Multiplayer", self._select_two_player),
        ]

        for text, desc, command in modes:
            frame = tk.Frame(btn_frame, bg=COLORS["background"])
            frame.pack(pady=8)

            btn = tk.Button(
                frame,
                text=text,
                font=("Helvetica", 11, "bold"),
                fg=COLORS["white"],
                bg=COLORS["button_bg"],
                activebackground=COLORS["button_hover"],
                activeforeground=COLORS["white"],
                width=18,
                height=1,
                relief=tk.FLAT,
                cursor="hand2",
                command=command,
            )
            btn.pack()

            desc_label = tk.Label(
                frame,
                text=desc,
                font=("Helvetica", 9),
                fg="#888888",
                bg=COLORS["background"],
            )
            desc_label.pack(pady=(2, 0))

    def _create_game_frame(self) -> None:
        """
        @brief Create the main game screen with board and controls.
        """
        self.game_frame = tk.Frame(self.root, bg=COLORS["background"])

        # Configure grid weights for responsive layout
        self.game_frame.grid_rowconfigure(2, weight=1)  # Board row expands
        self.game_frame.grid_columnconfigure(0, weight=1)

        # Header
        self.header_label = tk.Label(
            self.game_frame,
            text="",
            font=("Helvetica", 12),
            fg=COLORS["white"],
            bg=COLORS["background"],
        )
        self.header_label.grid(row=0, column=0, pady=(10, 5), sticky="ew")

        # Status
        self.status_label = tk.Label(
            self.game_frame,
            text="",
            font=("Helvetica", 11),
            fg=COLORS["o_color"],
            bg=COLORS["background"],
        )
        self.status_label.grid(row=1, column=0, pady=(0, 10), sticky="ew")

        # Board frame - this will expand
        board_container = tk.Frame(self.game_frame, bg=COLORS["background"])
        board_container.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)

        # Configure board container to center the board
        board_container.grid_rowconfigure(0, weight=1)
        board_container.grid_rowconfigure(2, weight=1)
        board_container.grid_columnconfigure(0, weight=1)
        board_container.grid_columnconfigure(2, weight=1)

        board_frame = tk.Frame(board_container, bg=COLORS["background"])
        board_frame.grid(row=1, column=1)

        self.buttons = []
        for row in range(3):
            button_row = []
            for col in range(3):
                btn = tk.Button(
                    board_frame,
                    text="",
                    font=("Helvetica", 32, "bold"),
                    width=3,
                    height=1,
                    fg=COLORS["white"],
                    bg=COLORS["cell_bg"],
                    activebackground=COLORS["button_hover"],
                    relief=tk.FLAT,
                    cursor="hand2",
                    command=lambda r=row, c=col: self._on_cell_click(r, c),
                )
                btn.grid(row=row, column=col, padx=2, pady=2)
                button_row.append(btn)
            self.buttons.append(button_row)

        # Scoreboard
        score_frame = tk.Frame(self.game_frame, bg=COLORS["primary"])
        score_frame.grid(row=3, column=0, sticky="ew", padx=15, pady=10)

        score_title = tk.Label(
            score_frame,
            text="SCOREBOARD",
            font=("Helvetica", 11, "bold"),
            fg=COLORS["o_color"],
            bg=COLORS["primary"],
        )
        score_title.pack(pady=(8, 2))

        self.score_label = tk.Label(
            score_frame,
            text="",
            font=("Helvetica", 13, "bold"),
            fg=COLORS["white"],
            bg=COLORS["primary"],
        )
        self.score_label.pack(pady=(2, 2))

        self.games_label = tk.Label(
            score_frame,
            text="",
            font=("Helvetica", 10),
            fg="#aaaaaa",
            bg=COLORS["primary"],
        )
        self.games_label.pack(pady=(0, 8))

        # Control buttons
        control_frame = tk.Frame(self.game_frame, bg=COLORS["background"])
        control_frame.grid(row=4, column=0, pady=(5, 15))

        # New Game button
        self.new_game_btn = tk.Button(
            control_frame,
            text="New Game",
            font=("Helvetica", 10, "bold"),
            fg=COLORS["white"],
            bg=COLORS["accent"],
            activebackground=COLORS["button_hover"],
            activeforeground=COLORS["white"],
            relief=tk.FLAT,
            cursor="hand2",
            padx=12,
            pady=4,
            command=self._new_game,
        )
        self.new_game_btn.pack(side=tk.LEFT, padx=4)

        # Other control buttons
        other_controls = [
            ("Change Mode", self._change_mode),
            ("Reset Scores", self._reset_scores),
        ]
        for text, command in other_controls:
            btn = tk.Button(
                control_frame,
                text=text,
                font=("Helvetica", 9),
                fg=COLORS["white"],
                bg=COLORS["accent"],
                activebackground=COLORS["button_hover"],
                activeforeground=COLORS["white"],
                relief=tk.FLAT,
                cursor="hand2",
                padx=8,
                pady=4,
                command=command,
            )
            btn.pack(side=tk.LEFT, padx=4)

    def show_mode_selection(self) -> None:
        """
        @brief Show the mode selection screen.
        """
        if self.game_frame:
            self.game_frame.grid_forget()
        if self.mode_frame:
            self.mode_frame.grid(row=0, column=0, sticky="nsew")

    def show_game_frame(self) -> None:
        """
        @brief Show the game board screen.
        """
        if self.mode_frame:
            self.mode_frame.grid_forget()
        if self.game_frame:
            self.game_frame.grid(row=0, column=0, sticky="nsew")

    def _select_easy(self) -> None:
        """
        @brief Handle Easy mode selection.
        """
        self.game_mode = GameMode.EASY
        self.scoreboard.player1_name = "You"
        self.scoreboard.player2_name = "Computer"
        self._start_game()

    def _select_hard(self) -> None:
        """
        @brief Handle Hard mode selection.
        """
        self.game_mode = GameMode.HARD
        self.scoreboard.player1_name = "You"
        self.scoreboard.player2_name = "Computer"
        self._start_game()

    def _select_two_player(self) -> None:
        """
        @brief Handle Two Player mode selection.
        """
        self.game_mode = GameMode.TWO_PLAYER
        self.scoreboard.player1_name = "Player 1"
        self.scoreboard.player2_name = "Player 2"
        self._start_game()

    def _start_game(self) -> None:
        """
        @brief Start a new game with the selected mode.
        """
        self._update_header()
        self.show_game_frame()
        self._new_game()

    def _new_game(self) -> None:
        """
        @brief Reset the board and start a new game.
        """
        self.board = create_board()
        self.current_player = "X"
        self.is_game_over = False
        self.waiting_for_computer = False
        self._update_board_display()
        self._update_status()
        self._update_scoreboard_display()
        self._set_board_enabled(True)
        self._reset_new_game_button()

    def _update_header(self) -> None:
        """
        @brief Update the header label based on game mode.
        """
        if self.header_label and self.game_mode:
            if self.game_mode == GameMode.EASY:
                text = "Easy Mode: You (X) vs Computer (O)"
            elif self.game_mode == GameMode.HARD:
                text = "Hard Mode: You (X) vs Computer (O)"
            else:
                text = "Two Player: Player 1 (X) vs Player 2 (O)"
            self.header_label.config(text=text)

    def _update_status(self, message: Optional[str] = None) -> None:
        """
        @brief Update the status label.

        @param message Optional custom message. If None, shows current turn.
        """
        if not self.status_label:
            return

        if message:
            self.status_label.config(text=message)
            return

        if self.is_game_over:
            return

        if self.game_mode == GameMode.TWO_PLAYER:
            if self.current_player == "X":
                player_name = "Player 1"
            else:
                player_name = "Player 2"
            turn_text = f"{player_name}'s turn ({self.current_player})"
            self.status_label.config(text=turn_text)
        else:
            if self.current_player == "X":
                self.status_label.config(text="Your turn (X)")
            else:
                self.status_label.config(text="Computer is thinking...")

    def _update_board_display(self) -> None:
        """
        @brief Update the visual display of the board.
        """
        for row in range(3):
            for col in range(3):
                cell = self.board[row][col]
                btn = self.buttons[row][col]

                btn.config(text=cell)

                if cell == "X":
                    btn.config(fg=COLORS["x_color"], bg=COLORS["cell_bg"])
                elif cell == "O":
                    btn.config(fg=COLORS["o_color"], bg=COLORS["cell_bg"])
                else:
                    btn.config(fg=COLORS["white"], bg=COLORS["cell_bg"])

    def _update_scoreboard_display(self) -> None:
        """
        @brief Update the scoreboard display.
        """
        if self.score_label:
            p1 = f"{self.scoreboard.player1_name}: {self.scoreboard.player1_wins}"
            p2 = f"{self.scoreboard.player2_name}: {self.scoreboard.player2_wins}"
            draws = f"Draws: {self.scoreboard.draws}"
            self.score_label.config(text=f"{p1}  |  {p2}  |  {draws}")
        if self.games_label:
            games_text = f"Games Played: {self.scoreboard.games_played}"
            self.games_label.config(text=games_text)

    def _on_cell_click(self, row: int, col: int) -> None:
        """
        @brief Handle a cell button click.

        @param row Row index of the clicked cell.
        @param col Column index of the clicked cell.
        """
        if self.is_game_over or self.waiting_for_computer:
            return

        position = position_to_num(row, col)

        if not is_valid_move(self.board, position):
            return

        # Make the move
        make_move(self.board, position, self.current_player)
        self._update_board_display()

        # Check for game over
        if self._check_game_over():
            return

        # Switch players
        self._switch_player()

        # If vs computer, schedule computer move
        is_vs_computer = self.game_mode in (GameMode.EASY, GameMode.HARD)
        if is_vs_computer and self.current_player == "O":
            self._schedule_computer_move()

    def _switch_player(self) -> None:
        """
        @brief Switch to the other player.
        """
        self.current_player = "O" if self.current_player == "X" else "X"
        self._update_status()

    def _schedule_computer_move(self) -> None:
        """
        @brief Schedule the computer's move with a short delay.
        """
        self.waiting_for_computer = True
        self._set_board_enabled(False)
        self._update_status("Computer is thinking...")
        self.root.after(500, self._computer_turn)

    def _computer_turn(self) -> None:
        """
        @brief Execute the computer's turn.
        """
        if self.is_game_over:
            self.waiting_for_computer = False
            return

        if self.game_mode == GameMode.EASY:
            difficulty = Difficulty.EASY
        else:
            difficulty = Difficulty.HARD
        move = get_computer_move(self.board, "O", "X", difficulty)
        make_move(self.board, move, "O")
        self._update_board_display()

        self.waiting_for_computer = False

        if self._check_game_over():
            return

        self._switch_player()
        self._set_board_enabled(True)

    def _check_game_over(self) -> bool:
        """
        @brief Check if the game has ended.

        @return True if game is over, False otherwise.
        """
        # Check for winner
        if check_winner(self.board, self.current_player):
            self._handle_win(self.current_player)
            return True

        # Check for draw
        if is_board_full(self.board):
            self._handle_draw()
            return True

        return False

    def _handle_win(self, player: str) -> None:
        """
        @brief Handle a win condition.

        @param player The winning player's mark ('X' or 'O').
        """
        self.is_game_over = True
        self._set_board_enabled(False)
        self._highlight_winning_cells(player)

        if self.game_mode == GameMode.TWO_PLAYER:
            if player == "X":
                msg = "Player 1 wins! Click 'New Game' to play again"
                self.scoreboard.record_result(GameResult.PLAYER1_WIN)
            else:
                msg = "Player 2 wins! Click 'New Game' to play again"
                self.scoreboard.record_result(GameResult.PLAYER2_WIN)
        else:
            if player == "X":
                msg = "You win! Click 'New Game' to play again"
                self.scoreboard.record_result(GameResult.PLAYER1_WIN)
            else:
                msg = "Computer wins! Click 'New Game' to play again"
                self.scoreboard.record_result(GameResult.PLAYER2_WIN)

        self._update_status(msg)
        self._update_scoreboard_display()
        self._highlight_new_game_button()

    def _handle_draw(self) -> None:
        """
        @brief Handle a draw condition.
        """
        self.is_game_over = True
        self._set_board_enabled(False)
        self._update_status("It's a draw! Click 'New Game' to play again")
        self.scoreboard.record_result(GameResult.DRAW)
        self._update_scoreboard_display()
        self._highlight_new_game_button()

    def _highlight_winning_cells(self, player: str) -> None:
        """
        @brief Highlight the winning cells.

        @param player The winning player's mark.
        """
        # Check rows
        for row in range(3):
            if all(self.board[row][col] == player for col in range(3)):
                for col in range(3):
                    self.buttons[row][col].config(bg=COLORS["win_highlight"])
                return

        # Check columns
        for col in range(3):
            if all(self.board[row][col] == player for row in range(3)):
                for row in range(3):
                    self.buttons[row][col].config(bg=COLORS["win_highlight"])
                return

        # Check main diagonal
        if all(self.board[i][i] == player for i in range(3)):
            for i in range(3):
                self.buttons[i][i].config(bg=COLORS["win_highlight"])
            return

        # Check anti-diagonal
        if all(self.board[i][2 - i] == player for i in range(3)):
            for i in range(3):
                self.buttons[i][2 - i].config(bg=COLORS["win_highlight"])
            return

    def _set_board_enabled(self, enabled: bool) -> None:
        """
        @brief Enable or disable all board buttons.

        @param enabled True to enable, False to disable.
        """
        state = tk.NORMAL if enabled else tk.DISABLED
        for row in self.buttons:
            for btn in row:
                btn.config(state=state)

    def _highlight_new_game_button(self) -> None:
        """
        @brief Highlight the New Game button to draw attention after game ends.
        """
        if self.new_game_btn:
            self.new_game_btn.config(bg=COLORS["win_highlight"], fg="#000000")

    def _reset_new_game_button(self) -> None:
        """
        @brief Reset the New Game button to normal styling.
        """
        if self.new_game_btn:
            self.new_game_btn.config(bg=COLORS["accent"], fg=COLORS["white"])

    def _change_mode(self) -> None:
        """
        @brief Return to mode selection screen.
        """
        self.show_mode_selection()

    def _reset_scores(self) -> None:
        """
        @brief Reset the scoreboard.
        """
        self.scoreboard.reset()
        self._update_scoreboard_display()

    def run(self) -> None:
        """
        @brief Start the main event loop.
        """
        # Set initial window size and center it
        width = 400
        height = 550
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

        self.root.mainloop()


def main() -> None:
    """
    @brief Main entry point for the GUI application.
    """
    app = TicTacToeGUI()
    app.run()


if __name__ == "__main__":
    main()
