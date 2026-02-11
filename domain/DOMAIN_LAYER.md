# Domain Layer Documentation

## Overview

The domain layer contains the core business logic and entities for the Tic-Tac-Toe game. This layer is independent of frameworks and external dependencies, following Clean Architecture principles.

## Structure

```
domain/
├── __init__.py
├── model/
│   ├── __init__.py
│   ├── game_board.py      # Game board entity (integer matrix)
│   └── game.py            # Current game entity (UUID + board)
└── service/
    ├── __init__.py
    ├── game_service.py     # Service interface (abstract)
    └── game_service_impl.py # Service implementation (Minimax algorithm)
```

## Models

### GameBoard

**File**: `domain/model/game_board.py`

Represents the Tic-Tac-Toe board as a 3x3 integer matrix.

**Cell Values**:
- `0`: Empty cell
- `1`: X (human player)
- `2`: O (computer player)

**Key Methods**:
- `__init__(board: List[List[int]])`: Initialize with validation
- `get_cell(row: int, col: int) -> int`: Get cell value
- `set_cell(row: int, col: int, value: int)`: Set cell value
- `board` (property): Get a copy of the board matrix

**Validation**:
- Board must be exactly 3x3
- Cell values must be 0, 1, or 2
- Raises `ValueError` for invalid input

**Example**:
```python
from domain.model.game_board import GameBoard

# Create empty board
board = GameBoard([[0, 0, 0], [0, 0, 0], [0, 0, 0]])

# Make a move
board.set_cell(1, 1, 1)  # Human plays center

# Get cell value
value = board.get_cell(1, 1)  # Returns 1
```

---

### Game

**File**: `domain/model/game.py`

Represents a current game with unique identifier and board state.

**Properties**:
- `game_id` (UUID): Unique identifier for the game
- `board` (GameBoard): Current state of the game board

**Key Methods**:
- `__init__(game_id: UUID, board: GameBoard)`: Initialize game
- `game_id` (property): Get game UUID
- `board` (property): Get game board

**Validation**:
- `game_id` must be a UUID instance
- `board` must be a GameBoard instance
- Raises `TypeError` for invalid types

**Example**:
```python
from uuid import uuid4
from domain.model.game import Game
from domain.model.game_board import GameBoard

# Create game
game_id = uuid4()
board = GameBoard([[0, 0, 0], [0, 1, 0], [0, 0, 0]])
game = Game(game_id, board)

# Access properties
print(game.game_id)  # UUID
print(game.board)    # GameBoard instance
```

---

## Services

### GameService (Interface)

**File**: `domain/service/game_service.py`

Abstract base class defining the contract for game business logic.

**Methods**:

#### 1. `get_next_move(game: Game) -> Tuple[int, int]`

Calculate the computer's next move using the Minimax algorithm.

- **Parameters**: `game` - Current game state
- **Returns**: Tuple of `(row, col)` for the best move
- **Raises**: `ValueError` if game is over or board is full

#### 2. `validate_game_board(game_id: UUID, current_game: Game, previous_game: Optional[Game]) -> bool`

Validate that the game board follows all rules:
- Only one new move was made
- No previous moves were modified
- The new move is in an empty cell

- **Parameters**: 
  - `game_id` - Game UUID
  - `current_game` - Current game state
  - `previous_game` - Previous state (None for new games)
- **Returns**: `True` if valid
- **Raises**: `ValueError` with detailed message if invalid

#### 3. `check_game_over(game: Game) -> Tuple[bool, Optional[int]]`

Check if the game has ended.

- **Parameters**: `game` - Current game state
- **Returns**: Tuple of `(is_over, winner)` where:
  - `is_over`: True if game ended
  - `winner`: `0` for draw, `1` for X, `2` for O, `None` if continuing

---

### GameServiceImpl (Implementation)

**File**: `domain/service/game_service_impl.py`

Concrete implementation of GameService with Minimax algorithm.

**Constructor**:
```python
def __init__(self, repository):
    """
    Args:
        repository: Repository for game data access
    """
```

**Minimax Algorithm**:

The implementation uses the classic Minimax algorithm with depth-based scoring:

1. **Maximizing Player** (Computer, O, player 2):
   - Tries to maximize score
   - Winning position: `10 - depth` (prefer faster wins)

2. **Minimizing Player** (Human, X, player 1):
   - Tries to minimize score
   - Winning position: `depth - 10` (prefer slower losses)

3. **Terminal States**:
   - Computer wins: `+10 - depth`
   - Human wins: `depth - 10`
   - Draw: `0`

**Algorithm Characteristics**:
- **Complete**: Explores entire game tree
- **Optimal**: Always finds the best move
- **Time Complexity**: O(b^d) where b=branching factor, d=depth
- **Perfect Play**: Computer never loses when playing optimally

**Validation Logic**:

For new games:
- At most one cell filled
- Must be human player (value 1)
- No computer moves yet

For existing games:
- Exactly one cell changed
- Changed cell was previously empty
- New move is by human player
- No previous moves modified

**Game Over Detection**:

Checks for:
1. Three in a row (horizontal)
2. Three in a column (vertical)
3. Three in a diagonal
4. Board full (draw)

**Example Usage**:
```python
from domain.service.game_service_impl import GameServiceImpl

# Initialize (repository injected)
service = GameServiceImpl(repository)

# Get computer's move
row, col = service.get_next_move(game)

# Validate board
is_valid = service.validate_game_board(game_id, current_game, previous_game)

# Check if game ended
is_over, winner = service.check_game_over(game)
if is_over:
    if winner == 0:
        print("Draw!")
    elif winner == 1:
        print("Human wins!")
    elif winner == 2:
        print("Computer wins!")
```

---

## Design Patterns

### 1. Entity Pattern
- `GameBoard` and `Game` are domain entities
- Encapsulate business rules and validation
- Immutable from external perspective (return copies)

### 2. Service Pattern
- Business logic encapsulated in services
- Clear separation from data access
- Testable with mock repositories

### 3. Interface Segregation
- Abstract `GameService` interface
- Concrete `GameServiceImpl` implementation
- Enables dependency injection and testing

---

## Dependencies

### Internal Dependencies
- `domain.model.game_board` → No dependencies
- `domain.model.game` → Depends on `GameBoard`
- `domain.service.game_service` → Depends on domain models
- `domain.service.game_service_impl` → Depends on interface and models

### External Dependencies
- Python standard library only:
  - `abc` (Abstract Base Classes)
  - `typing` (Type hints)
  - `uuid` (UUID support)

**No framework dependencies** - Pure business logic!

---

## Testing

The domain layer can be tested independently:

```python
# Test models
board = GameBoard([[0, 0, 0], [0, 1, 0], [0, 0, 0]])
game = Game(uuid4(), board)

# Test service with mock repository
mock_repo = MockRepository()
service = GameServiceImpl(mock_repo)

# Test Minimax
move = service.get_next_move(game)
assert move == (0, 0)  # Expected optimal move

# Test validation
is_valid = service.validate_game_board(game_id, current, previous)
assert is_valid == True

# Test game over
is_over, winner = service.check_game_over(game)
assert is_over == False
```

---

## Validation Rules Summary

### Board Validation
1. ✓ Board is 3x3 matrix
2. ✓ Cell values are 0, 1, or 2
3. ✓ Exactly one new move per turn
4. ✓ New move in empty cell
5. ✓ Previous moves unchanged
6. ✓ Human player makes moves

### Game State Validation
1. ✓ Valid UUID
2. ✓ Valid GameBoard
3. ✓ Legal move sequence

---

## Error Handling

**ValueError**:
- Invalid board dimensions
- Invalid cell values
- Invalid moves
- Game already over
- Multiple moves in one turn
- Modified previous moves

**TypeError**:
- Invalid UUID type
- Invalid GameBoard type

All errors include descriptive messages for debugging.

---

## Thread Safety

The domain layer is **stateless** and **thread-safe**:
- Models are value objects
- Services don't maintain state
- All operations are pure functions (given same input → same output)

Thread safety is handled at the repository/storage layer.
