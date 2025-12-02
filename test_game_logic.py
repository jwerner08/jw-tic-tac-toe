"""Test script for game logic functions."""

from game_logic import (
    check_draw,
    check_winner,
    get_move_count,
    get_next_player,
    is_valid_move,
    make_move,
)
from models import Player


def test_is_valid_move():
    """Test move validation."""
    print("Testing is_valid_move()...")
    board = "---------"
    assert is_valid_move(board, 0) is True
    assert is_valid_move(board, 8) is True
    assert is_valid_move(board, 9) is False
    assert is_valid_move(board, -1) is False

    board = "x--------"
    assert is_valid_move(board, 0) is False
    assert is_valid_move(board, 1) is True
    print("✓ is_valid_move() passed")


def test_make_move():
    """Test making moves."""
    print("\nTesting make_move()...")
    board = "---------"
    board = make_move(board, 0, Player.X)
    assert board == "x--------"

    board = make_move(board, 4, Player.O)
    assert board == "x---o----"
    print("✓ make_move() passed")


def test_check_winner():
    """Test winner detection."""
    print("\nTesting check_winner()...")

    # Test horizontal win
    board = "xxx------"
    assert check_winner(board) == Player.X

    # Test vertical win
    board = "x--x--x--"
    assert check_winner(board) == Player.X

    # Test diagonal win (0, 4, 8)
    board = "x---x---x"
    assert check_winner(board) == Player.X

    # Test no winner
    board = "x-o------"
    assert check_winner(board) is None

    # Test O wins
    board = "ooo------"
    assert check_winner(board) == Player.O

    print("✓ check_winner() passed")


def test_check_draw():
    """Test draw detection."""
    print("\nTesting check_draw()...")

    # Full board with no winner = draw
    board = "xoxoxooxo"
    assert check_draw(board) is True

    # Incomplete board = not draw
    board = "x--------"
    assert check_draw(board) is False

    # Winner = not draw
    board = "xxxooox-o"
    assert check_draw(board) is False

    print("✓ check_draw() passed")


def test_get_next_player():
    """Test player switching."""
    print("\nTesting get_next_player()...")
    assert get_next_player(Player.X) == Player.O
    assert get_next_player(Player.O) == Player.X
    print("✓ get_next_player() passed")


def test_get_move_count():
    """Test move counting."""
    print("\nTesting get_move_count()...")
    assert get_move_count("---------") == 0
    assert get_move_count("x--------") == 1
    assert get_move_count("x-o------") == 2
    assert get_move_count("xoxoxoxox") == 9
    print("✓ get_move_count() passed")


def test_game_scenario():
    """Test a complete game scenario."""
    print("\nTesting complete game scenario...")

    board = "---------"
    print(f"Initial: {board}")

    # X plays center
    board = make_move(board, 4, Player.X)
    print(f"X plays 4: {board}")
    assert board == "----x----"
    assert check_winner(board) is None

    # O plays corner
    board = make_move(board, 0, Player.O)
    print(f"O plays 0: {board}")
    assert board == "o---x----"

    # X plays top-right
    board = make_move(board, 2, Player.X)
    print(f"X plays 2: {board}")
    assert board == "o-x-x----"

    # O plays bottom-left
    board = make_move(board, 6, Player.O)
    print(f"O plays 6: {board}")
    assert board == "o-x-x-o--"

    # X plays top-left (X wins diagonal 2-4-6)
    board = make_move(board, 6, Player.X)
    print(f"X plays 6: {board}")

    # Actually let's do a proper winning scenario
    board = "---------"
    board = make_move(board, 0, Player.X)
    board = make_move(board, 3, Player.O)
    board = make_move(board, 1, Player.X)
    board = make_move(board, 4, Player.O)
    board = make_move(board, 2, Player.X)  # X wins top row

    print(f"Final board: {board}")
    assert check_winner(board) == Player.X
    print("✓ Game scenario passed - X wins!")


if __name__ == "__main__":
    print("=" * 50)
    print("Running Game Logic Tests")
    print("=" * 50)

    test_is_valid_move()
    test_make_move()
    test_check_winner()
    test_check_draw()
    test_get_next_player()
    test_get_move_count()
    test_game_scenario()

    print("\n" + "=" * 50)
    print("✓ All tests passed!")
    print("=" * 50)
