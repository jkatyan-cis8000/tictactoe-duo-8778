"""Pure type definitions for the Tic-Tac-Toe game."""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Player(Enum):
    """Player symbols."""

    X = "X"
    O = "O"


class GameState(Enum):
    """Possible game states."""

    ONGOING = "ongoing"
    WON_X = "won_x"
    WON_O = "won_o"
    DRAW = "draw"


@dataclass(frozen=True)
class Cell:
    """A single cell in the grid."""

    row: int
    col: int
    value: Optional[Player] = None


@dataclass(frozen=True)
class Board:
    """The 3x3 game board."""

    cells: tuple[tuple[Optional[Player], ...], ...]

    @classmethod
    def new(cls) -> "Board":
        """Create a new empty board."""
        return cls(cells=((None,) * 3,) * 3)

    def at(self, row: int, col: int) -> Optional[Player]:
        """Get the player at a cell."""
        return self.cells[row][col]

    def with_move(self, row: int, col: int, player: Player) -> "Board":
        """Return a new board with the move applied."""
        rows = list(list(r) for r in self.cells)
        rows[row][col] = player
        return Board(cells=tuple(tuple(r) for r in rows))


@dataclass(frozen=True)
class Move:
    """A player's move."""

    player: Player
    row: int
    col: int


@dataclass(frozen=True)
class Game:
    """Game state and history."""

    board: Board
    current_player: Player
    state: GameState
    moves: tuple[Move, ...]

    @classmethod
    def new(cls) -> "Game":
        """Create a new game."""
        return cls(
            board=Board.new(),
            current_player=Player.X,
            state=GameState.ONGOING,
            moves=(),
        )

    def with_move(self, row: int, col: int) -> "Game":
        """Return a new game with the move applied."""
        new_board = self.board.with_move(row, col, self.current_player)
        new_state = self._compute_state(new_board, row, col)
        new_moves = self.moves + (Move(player=self.current_player, row=row, col=col),)

        next_player = Player.O if self.current_player == Player.X else Player.X

        return Game(
            board=new_board,
            current_player=next_player,
            state=new_state,
            moves=new_moves,
        )

    def _compute_state(self, board: Board, row: int, col: int) -> GameState:
        """Compute the new game state after a move."""
        player = board.at(row, col)
        assert player is not None

        # Check for win
        if self._check_win(board, player):
            return GameState.WON_X if player == Player.X else GameState.WON_O

        # Check for draw
        if all(cell is not None for row in board.cells for cell in row):
            return GameState.DRAW

        return GameState.ONGOING

    def _check_win(self, board: Board, player: Player) -> bool:
        """Check if the player has won."""
        # Check rows
        for row in range(3):
            if all(board.at(row, col) == player for col in range(3)):
                return True

        # Check columns
        for col in range(3):
            if all(board.at(row, col) == player for row in range(3)):
                return True

        # Check diagonals
        if all(board.at(i, i) == player for i in range(3)):
            return True
        if all(board.at(i, 2 - i) == player for i in range(3)):
            return True

        return False
