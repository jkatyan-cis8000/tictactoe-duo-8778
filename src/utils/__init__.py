"""Pure utility helpers."""

from src.types_layer import Player


def parse_player(value: str) -> Player:
    """Parse a string into a Player."""
    value = value.strip().upper()
    if value == "X":
        return Player.X
    if value == "O":
        return Player.O
    raise ValueError(f"Invalid player: {value}")


def parse_move(value: str) -> tuple[int, int]:
    """Parse 'row,col' into coordinates."""
    parts = value.strip().split(",")
    if len(parts) != 2:
        raise ValueError(f"Invalid move format: {value}")
    row, col = int(parts[0].strip()), int(parts[1].strip())
    if not (0 <= row <= 2 and 0 <= col <= 2):
        raise ValueError(f"Move out of bounds: {value}")
    return row, col
