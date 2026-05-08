"""Tic-Tac-Toe CLI entry point."""

import sys

from src.ui.cli import run_cli


def main() -> int:
    """Run the application."""
    try:
        run_cli()
        return 0
    except KeyboardInterrupt:
        print("\nGame interrupted.")
        return 130


if __name__ == "__main__":
    sys.exit(main())
