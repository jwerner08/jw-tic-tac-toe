"""Command-line interface for tic-tac-toe game."""

from sqlalchemy.orm import Session

from db import SessionLocal, init_db
from game_logic import (
    check_draw,
    check_winner,
    get_move_count,
    get_next_player,
    is_valid_move,
    make_move,
)
from models import Game, GameStatus, Move, Player


def display_board(board_state: str):
    """Display the board in a readable format."""
    print("\n")
    print(f" {board_state[0]} │ {board_state[1]} │ {board_state[2]} ")
    print("───┼───┼───")
    print(f" {board_state[3]} │ {board_state[4]} │ {board_state[5]} ")
    print("───┼───┼───")
    print(f" {board_state[6]} │ {board_state[7]} │ {board_state[8]} ")
    print()


def display_positions():
    """Display the position numbers for reference."""
    print("\nPosition numbers:")
    print(" 0 │ 1 │ 2 ")
    print("───┼───┼───")
    print(" 3 │ 4 │ 5 ")
    print("───┼───┼───")
    print(" 6 │ 7 │ 8 ")
    print()


def get_player_move(board_state: str, player: Player) -> int:
    """
    Get a valid move from the player.

    Args:
        board_state: Current board state
        player: Current player

    Returns:
        Valid position (0-8)
    """
    while True:
        try:
            move = input(
                f"\nPlayer {player.value.upper()}, enter position (0-8) or 'q' to quit: "
            ).strip()

            if move.lower() == "q":
                return -1

            position = int(move)

            if not is_valid_move(board_state, position):
                print("❌ Invalid move! Position must be 0-8 and empty.")
                continue

            return position

        except ValueError:
            print("❌ Invalid input! Please enter a number between 0 and 8.")
        except KeyboardInterrupt:
            print("\n\nGame interrupted.")
            return -1


def save_move_to_db(db: Session, game: Game, position: int, player: Player) -> None:
    """
    Save a move to the database.

    Args:
        db: Database session
        game: Game instance
        position: Move position
        player: Player who made the move
    """
    move_number = get_move_count(game.board_state)
    move = Move(
        game_id=game.id,
        player=player,
        position=position,
        move_number=move_number,
    )
    db.add(move)
    db.commit()


def play_game(db: Session, game: Game) -> None:
    """
    Main game loop.

    Args:
        db: Database session
        game: Game instance to play
    """
    print("\n" + "=" * 50)
    print(f"🎮 TIC-TAC-TOE - Game #{game.id}")
    print("=" * 50)
    display_positions()

    while game.status == GameStatus.IN_PROGRESS:
        display_board(game.board_state)
        print(f"Current player: {game.current_player.value.upper()}")

        position = get_player_move(game.board_state, game.current_player)

        if position == -1:
            print("\n👋 Game saved! You can resume later.")
            return

        game.board_state = make_move(game.board_state, position, game.current_player)
        save_move_to_db(db, game, position, game.current_player)

        winner = check_winner(game.board_state)
        if winner:
            game.winner = winner
            game.status = GameStatus.COMPLETED
            db.commit()
            display_board(game.board_state)
            print("=" * 50)
            print(f"🎉 GAME OVER! Player {winner.value.upper()} wins!")
            print("=" * 50)
            display_game_history(db, game)
            return

        if check_draw(game.board_state):
            game.status = GameStatus.DRAW
            db.commit()
            display_board(game.board_state)
            print("=" * 50)
            print("🤝 GAME OVER! It's a draw!")
            print("=" * 50)
            display_game_history(db, game)
            return

        game.current_player = get_next_player(game.current_player)
        db.commit()


def display_game_history(db: Session, game: Game) -> None:
    """
    Display the move history for a game.

    Args:
        db: Database session
        game: Game instance
    """
    db.refresh(game)
    if not game.moves:
        return

    print("\n📜 Game History:")
    for move in game.moves:
        print(
            f"  Move {move.move_number}: {move.player.value.upper()} → position {move.position}"
        )
    print()


def list_saved_games(db: Session) -> list[Game]:
    """
    List all saved games.

    Args:
        db: Database session

    Returns:
        List of Game instances
    """
    return db.query(Game).order_by(Game.created_at.desc()).all()


def display_saved_games(games: list[Game]) -> None:
    """
    Display a list of saved games.

    Args:
        games: List of Game instances
    """
    if not games:
        print("\n📂 No saved games found.")
        return

    print("\n📂 Saved Games:")
    print("-" * 70)
    for game in games:
        status_emoji = {
            GameStatus.IN_PROGRESS: "⏸️ ",
            GameStatus.COMPLETED: "🏆",
            GameStatus.DRAW: "🤝",
        }
        status_text = status_emoji.get(game.status, "")

        if game.status == GameStatus.COMPLETED:
            info = f"Winner: {game.winner.value.upper()}"
        elif game.status == GameStatus.DRAW:
            info = "Draw"
        else:
            info = f"Turn: {game.current_player.value.upper()}"

        move_count = get_move_count(game.board_state)
        print(
            f"  {status_text} Game #{game.id} | {info} | "
            f"Moves: {move_count} | {game.created_at.strftime('%Y-%m-%d %H:%M')}"
        )
    print("-" * 70)


def load_game(db: Session, game_id: int) -> Game | None:
    """
    Load a game by ID.

    Args:
        db: Database session
        game_id: Game ID to load

    Returns:
        Game instance or None if not found
    """
    return db.query(Game).filter(Game.id == game_id).first()


def new_game(db: Session) -> Game:
    """
    Create a new game.

    Args:
        db: Database session

    Returns:
        New Game instance
    """
    game = Game()
    db.add(game)
    db.commit()
    db.refresh(game)
    return game


def handle_load_game(db: Session) -> None:
    """
    Handle loading a saved game.

    Args:
        db: Database session
    """
    games = list_saved_games(db)
    display_saved_games(games)

    if not games:
        return

    try:
        game_id = int(input("\nEnter game ID to load (or 0 to cancel): "))
        if game_id == 0:
            return

        game = load_game(db, game_id)
        if game:
            if game.status != GameStatus.IN_PROGRESS:
                print("\n⚠️  This game is already finished. Showing final state...")
                display_board(game.board_state)
                if game.status == GameStatus.COMPLETED:
                    print(f"Winner: {game.winner.value.upper()}")
                else:
                    print("Result: Draw")
                display_game_history(db, game)
            else:
                play_game(db, game)
        else:
            print(f"\n❌ Game #{game_id} not found.")
    except ValueError:
        print("\n❌ Invalid game ID.")


def handle_list_games(db: Session) -> None:
    """
    Handle listing all games.

    Args:
        db: Database session
    """
    games = list_saved_games(db)
    display_saved_games(games)
    input("\nPress Enter to continue...")


def main_menu():
    """Display and handle the main menu."""
    init_db()
    db = SessionLocal()

    try:
        while True:
            print("\n" + "=" * 50)
            print("🎮 TIC-TAC-TOE")
            print("=" * 50)
            print("\n1. New Game")
            print("2. Load Game")
            print("3. List All Games")
            print("4. Quit")

            choice = input("\nEnter your choice (1-4): ").strip()

            if choice == "1":
                game = new_game(db)
                play_game(db, game)
            elif choice == "2":
                handle_load_game(db)
            elif choice == "3":
                handle_list_games(db)
            elif choice == "4" or choice.lower() == "q":
                print("\n👋 Thanks for playing! Goodbye!")
                break
            else:
                print("\n❌ Invalid choice. Please enter 1-4.")

    except KeyboardInterrupt:
        print("\n\n👋 Thanks for playing! Goodbye!")
    finally:
        db.close()


if __name__ == "__main__":
    main_menu()
