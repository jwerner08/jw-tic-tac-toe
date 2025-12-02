# Tic-Tac-Toe Game

A Python-based tic-tac-toe game with PostgreSQL database backend.

## Prerequisites

- Python 3.14+
- Docker and Docker Compose
- [uv](https://github.com/astral-sh/uv) package manager

## Setup

### 1. Install Dependencies

```bash
uv sync
```

### 2. Start PostgreSQL Database

```bash
docker-compose up -d
```

The database will be available at `localhost:54321`.

### 3. Start the Game

```bash
uv run python main.py
```

This will launch the interactive CLI menu where you can:

- Start a new game
- Load a saved game
- List all games
- Play tic-tac-toe!

## Usage

### Playing the Game

When you start a new game, you'll see:

- The board with position numbers (0-8)
- Current player's turn (X or O)
- Prompt to enter a position

**Enter a position (0-8)** to place your mark, or **'q'** to save and quit.

### Example Game

```text
Position numbers:
 0 │ 1 │ 2
───┼───┼───
 3 │ 4 │ 5
───┼───┼───
 6 │ 7 │ 8

Player X, enter position (0-8) or 'q' to quit: 4

 - │ - │ -
───┼───┼───
 - │ x │ -
───┼───┼───
 - │ - │ -
```

### Features

- **Save/Resume Games**: Quit anytime with 'q' and resume later
- **Game History**: View all moves made in a game
- **Multiple Games**: Manage multiple games simultaneously

## Testing

### Test Game Logic

```bash
uv run python test_game_logic.py
```

Tests all core game functions (move validation, winner detection, etc.)

### Test Board Serialization

```bash
uv run python test_board.py
```

Demonstrates the database board serialization with a sample game.

## Project Structure

```text
├── main.py              # Main application entry point
├── models.py            # SQLAlchemy models (Game, Move)
├── db.py                # Database configuration and session management
├── test_board.py        # Demo script showing board serialization
├── docker-compose.yml   # PostgreSQL container setup
├── pyproject.toml       # Project dependencies
├── ruff.toml            # Linting and formatting configuration
└── .env.example         # Example environment configuration
```

## Database Schema

### Game Table

- `id`: Primary key
- `board_state`: 9-character string representing the board (positions 0-8)
  - **Initial state**: `---------` (9 dashes)
  - **After moves**: positions replaced with `x` or `o`
  - **Example**: `xxo-o---x` means:
    - X at positions 0, 1, 8
    - O at positions 2, 4
    - Empty at positions 3, 5, 6, 7
- `current_player`: Current player's turn (x or o)
- `winner`: Winner of the game (x, o, or NULL)
- `status`: Game status (in_progress, completed, draw)
- `created_at`: Timestamp when game was created
- `updated_at`: Timestamp when game was last updated

### Move Table

- `id`: Primary key
- `game_id`: Foreign key to Game
- `player`: Player who made the move (x or o)
- `position`: Board position (0-8)
- `move_number`: Sequential move number in the game
- `created_at`: Timestamp when move was made

## Development

### Linting and Formatting

```bash
# Run linter
uv run ruff check .

# Format code
uv run ruff format .
```

### Database Management

```bash
# Stop database
docker-compose down

# Stop and remove volumes (fresh start)
docker-compose down -v
```

## Game Rules

Tic-tac-toe is played on a 3×3 grid by two players who alternately place marks (X and O) in one of the nine spaces. A player wins by marking all three spaces in a row, column, or diagonal.

### Board Positions

```text
0 | 1 | 2
---------
3 | 4 | 5
---------
6 | 7 | 8
```

### Board Serialization

The board is stored as a 9-character string where each character represents a position:

- `-` = empty space
- `x` = X player's mark
- `o` = O player's mark

**Example game progression:**

```text
Initial:    ---------  (empty board)
After X(0): x--------  (X plays top-left)
After O(4): x---o----  (O plays center)
After X(1): xx--o----  (X plays top-center)
After O(2): xxo-o----  (O plays top-right)
After X(8): xxo-o---x  (X plays bottom-right, wins diagonal!)
```
