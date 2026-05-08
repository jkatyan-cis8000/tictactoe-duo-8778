"""Service layer for Tic-Tac-Toe game logic."""

from src.types_layer import Board, Game, GameState, Move, Player


def apply_move(game: Game, row: int, col: int) -> Game:
    """Apply a move to a game and return the new game state."""
    return game.with_move(row, col)


def is_valid_move(game: Game, row: int, col: int) -> bool:
    """Check if a move is valid for the current game state."""
    if game.state != GameState.ONGOING:
        return False
    if game.board.at(row, col) is not None:
        return False
    return True


def format_board(board: Board) -> str:
    """Format the board as a string for display."""
    lines = []
    for row in range(3):
        cells = []
        for col in range(3):
            cell_value = board.at(row, col)
            if cell_value is None:
                cells.append(f" {row}{col} ")
            else:
                cells.append(f" {cell_value.value} ")
        lines.append("|".join(cells))
    return "\n-----\n".join(lines)


def format_game(game: Game) -> str:
    """Format the entire game state for display."""
    output = [format_board(game.board)]
    output.append(f"\nCurrent player: {game.current_player.value}")
    output.append(f"State: {game.state.value}")
    if game.moves:
        output.append(f"\nMoves made: {len(game.moves)}")
        for i, move in enumerate(game.moves):
            player = move.player.value
            output.append(f"  {i+1}. Player {player}: ({move.row},{move.col})")
    return "\n".join(output)
