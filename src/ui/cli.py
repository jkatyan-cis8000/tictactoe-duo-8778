"""UI layer - CLI interface for Tic-Tac-Toe."""

from src.types_layer import Game, GameState, Player
from src.service import apply_move, format_game, is_valid_move
from src.utils import parse_move


def run_cli() -> None:
    """Run the CLI game loop."""
    game = Game.new()
    print("Tic-Tac-Toe! Players take turns. Enter moves as 'row,col' (0-2).")
    print(format_game(game))

    while game.state == GameState.ONGOING:
        current_player = game.current_player.value
        move_str = input(f"\nPlayer {current_player}, enter your move (row,col): ")

        try:
            row, col = parse_move(move_str)
        except ValueError as e:
            print(f"Invalid input: {e}")
            continue

        if not is_valid_move(game, row, col):
            print("Invalid move - cell occupied or game over.")
            continue

        game = apply_move(game, row, col)
        print("\n" + format_game(game))

    print("\nGame over!")
    if game.state == GameState.DRAW:
        print("It's a draw!")
    else:
        winner = "X" if game.state == GameState.WON_X else "O"
        print(f"Player {winner} wins!")
