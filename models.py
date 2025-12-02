import enum
from datetime import UTC, datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base


class GameStatus(enum.Enum):
    """Enum representing the current status of a game."""

    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    DRAW = "draw"


class Player(enum.Enum):
    """Enum representing a player's mark (X or O)."""

    X = "x"
    O = "o"  # noqa: E741


class Game(Base):
    """
    Game model representing a tic-tac-toe game.

    Board positions (0-8):
        0 | 1 | 2
        ---------
        3 | 4 | 5
        ---------
        6 | 7 | 8

    board_state format: 9-character string
        - Initial state: "---------" (9 dashes)
        - After moves: positions replaced with 'x' or 'o'
        - Example: "x-o---x--" means X at position 0, O at position 2, X at position 6
    """

    __tablename__ = "games"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    board_state: Mapped[str] = mapped_column(String(9), default="---------")
    current_player: Mapped[Player] = mapped_column(Enum(Player), default=Player.X)
    winner: Mapped[Player | None] = mapped_column(Enum(Player), nullable=True)
    status: Mapped[GameStatus] = mapped_column(
        Enum(GameStatus), default=GameStatus.IN_PROGRESS
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(UTC)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

    moves: Mapped[list[Move]] = relationship(
        back_populates="game", cascade="all, delete-orphan"
    )


class Move(Base):
    """
    Move model representing a single move in a tic-tac-toe game.

    Tracks the complete history of moves for each game, enabling:
    - Game replay
    - Move validation
    - Audit trail
    """

    __tablename__ = "moves"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    game_id: Mapped[int] = mapped_column(Integer, ForeignKey("games.id"))
    player: Mapped[Player] = mapped_column(Enum(Player))
    position: Mapped[int] = mapped_column(Integer)
    move_number: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(UTC)
    )

    game: Mapped[Game] = relationship(back_populates="moves")
