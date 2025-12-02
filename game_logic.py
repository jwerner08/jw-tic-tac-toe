"""Core game logic for tic-tac-toe."""

from models import GameStatus, Player


def is_valid_move(board_state: str, position: int) -> bool:
    """
    Check if a move is valid.

    Args:
        board_state: Current board state (9-character string)
        position: Position to check (0-8)

    Returns:
        True if the move is valid, False otherwise
    """
    if position < 0 or position > 8:
        return False
    return board_state[position] == "-"


def make_move(board_state: str, position: int, player: Player) -> str:
    """
    Make a move on the board.

    Args:
        board_state: Current board state
        position: Position to place the mark (0-8)
        player: Player making the move

    Returns:
        New board state after the move
    """
    board_list = list(board_state)
    board_list[position] = player.value
    return "".join(board_list)


def check_winner(board_state: str) -> Player | None:
    """
    Check if there's a winner on the board.

    Args:
        board_state: Current board state

    Returns:
        Player enum if there's a winner, None otherwise
    """
    winning_combinations = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6],
    ]

    for combo in winning_combinations:
        positions = [board_state[i] for i in combo]
        if positions[0] != "-" and positions[0] == positions[1] == positions[2]:
            return Player.X if positions[0] == "x" else Player.O

    return None


def check_draw(board_state: str) -> bool:
    """
    Check if the game is a draw (board full with no winner).

    Args:
        board_state: Current board state

    Returns:
        True if the game is a draw, False otherwise
    """
    return "-" not in board_state and check_winner(board_state) is None


def get_game_status(board_state: str) -> tuple[GameStatus, Player | None]:
    """
    Get the current game status and winner (if any).

    Args:
        board_state: Current board state

    Returns:
        Tuple of (GameStatus, winner or None)
    """
    winner = check_winner(board_state)
    if winner:
        return GameStatus.COMPLETED, winner

    if check_draw(board_state):
        return GameStatus.DRAW, None

    return GameStatus.IN_PROGRESS, None


def get_next_player(current_player: Player) -> Player:
    """
    Get the next player to move.

    Args:
        current_player: Current player

    Returns:
        Next player
    """
    return Player.O if current_player == Player.X else Player.X


def get_move_count(board_state: str) -> int:
    """
    Count the number of moves made on the board.

    Args:
        board_state: Current board state

    Returns:
        Number of moves made
    """
    return sum(1 for pos in board_state if pos != "-")
