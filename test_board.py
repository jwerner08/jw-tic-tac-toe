"""Test script to demonstrate board serialization."""

from db import SessionLocal, init_db
from models import Game, GameStatus, Move, Player


def display_board(board_state: str):
    """Display the board in a readable format."""
    print(f"\n{board_state[0]} | {board_state[1]} | {board_state[2]}")
    print("---------")
    print(f"{board_state[3]} | {board_state[4]} | {board_state[5]}")
    print("---------")
    print(f"{board_state[6]} | {board_state[7]} | {board_state[8]}")


def test_board_serialization():
    """Test creating a game and making moves with board serialization."""
    init_db()

    db = SessionLocal()

    try:
        print("\n=== Creating a new game ===")
        game = Game()
        db.add(game)
        db.commit()
        db.refresh(game)

        print(f"Game ID: {game.id}")
        print(f"Initial board_state: '{game.board_state}'")
        display_board(game.board_state)

        print("\n=== Making moves ===")

        # Move 1: X plays position 0 (top-left)
        print("\nMove 1: X plays position 0")
        board_list = list(game.board_state)
        board_list[0] = Player.X.value
        game.board_state = "".join(board_list)
        game.current_player = Player.O
        move1 = Move(game_id=game.id, player=Player.X, position=0, move_number=1)
        db.add(move1)
        db.commit()
        db.refresh(game)
        print(f"Board state: '{game.board_state}'")
        display_board(game.board_state)

        # Move 2: O plays position 4 (center)
        print("\nMove 2: O plays position 4")
        board_list = list(game.board_state)
        board_list[4] = Player.O.value
        game.board_state = "".join(board_list)
        game.current_player = Player.X
        move2 = Move(game_id=game.id, player=Player.O, position=4, move_number=2)
        db.add(move2)
        db.commit()
        db.refresh(game)
        print(f"Board state: '{game.board_state}'")
        display_board(game.board_state)

        # Move 3: X plays position 1 (top-center)
        print("\nMove 3: X plays position 1")
        board_list = list(game.board_state)
        board_list[1] = Player.X.value
        game.board_state = "".join(board_list)
        game.current_player = Player.O
        move3 = Move(game_id=game.id, player=Player.X, position=1, move_number=3)
        db.add(move3)
        db.commit()
        db.refresh(game)
        print(f"Board state: '{game.board_state}'")
        display_board(game.board_state)

        # Move 4: O plays position 2 (top-right)
        print("\nMove 4: O plays position 2")
        board_list = list(game.board_state)
        board_list[2] = Player.O.value
        game.board_state = "".join(board_list)
        game.current_player = Player.X
        move4 = Move(game_id=game.id, player=Player.O, position=2, move_number=4)
        db.add(move4)
        db.commit()
        db.refresh(game)
        print(f"Board state: '{game.board_state}'")
        display_board(game.board_state)

        # Move 5: X plays position 8 (bottom-right) - X wins diagonal!
        print("\nMove 5: X plays position 8 (bottom-right)")
        board_list = list(game.board_state)
        board_list[8] = Player.X.value
        game.board_state = "".join(board_list)
        game.winner = Player.X
        game.status = GameStatus.COMPLETED
        move5 = Move(game_id=game.id, player=Player.X, position=8, move_number=5)
        db.add(move5)
        db.commit()
        db.refresh(game)
        print(f"Board state: '{game.board_state}'")
        display_board(game.board_state)
        print(f"\n🎉 Winner: {game.winner.value.upper()}!")
        print(f"Game status: {game.status.value}")

        print("\n=== Game History ===")
        for move in game.moves:
            print(
                f"Move {move.move_number}: {move.player.value.upper()} → position {move.position}"
            )

        print(f"\nFinal board_state in database: '{game.board_state}'")

    finally:
        db.close()


if __name__ == "__main__":
    test_board_serialization()
