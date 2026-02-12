# Datasource Layer Documentation

## Overview

The datasource layer handles data persistence and storage for the Tic-Tac-Toe game. This layer is responsible for storing and retrieving game data, implementing thread-safe operations for concurrent access, and providing a clean abstraction between the domain layer and the actual storage mechanism.

## Structure

```
datasource/
├── __init__.py
├── model/
│   ├── __init__.py
│   ├── game_board.py      # Persistence model for game board
│   └── game.py            # Persistence model for game
├── mapper/
│   ├── __init__.py
│   ├── game_board_mapper.py  # Domain ↔ Datasource GameBoard mapper
│   └── game_mapper.py        # Domain ↔ Datasource Game mapper
└── repository/
    ├── __init__.py
    ├── game_storage.py          # Thread-safe in-memory storage
    ├── game_repository.py       # Repository interface
    └── game_repository_impl.py  # Repository implementation
```

## Models

### GameBoard (Datasource)

**File**: `datasource/model/game_board.py`

Datasource representation of the Tic-Tac-Toe board, optimized for persistence.

**Properties**:
- `board` (property): Returns a copy of the 3x3 integer matrix

**Cell Values**:
- `0`: Empty cell
- `1`: X (human player)
- `2`: O (computer player)

**Example**:
```python
from datasource.model.game_board import GameBoard

board = GameBoard([[1, 0, 0], [0, 2, 0], [0, 0, 0]])
matrix = board.board  # Get copy of board
```

**Design Notes**:
- Simplified compared to domain model
- Focused on serialization/deserialization
- No validation (handled by domain layer)

---

### Game (Datasource)

**File**: `datasource/model/game.py`

Datasource representation of a game, containing UUID and board state.

**Properties**:
- `game_id` (UUID): Unique game identifier
- `board` (GameBoard): Game board state

**Example**:
```python
from uuid import uuid4
from datasource.model.game import Game
from datasource.model.game_board import GameBoard

game_id = uuid4()
board = GameBoard([[0, 0, 0], [0, 1, 0], [0, 0, 0]])
game = Game(game_id, board)
```

---

## Mappers

Mappers convert between domain and datasource representations, enabling clean separation of concerns.

### GameBoardMapper

**File**: `datasource/mapper/game_board_mapper.py`

Maps between domain and datasource GameBoard models.

**Methods**:

#### `to_datasource(domain_board: DomainGameBoard) -> DataGameBoard`
Convert domain GameBoard to datasource GameBoard.

```python
from domain.model.game_board import GameBoard as DomainGameBoard
from datasource.mapper.game_board_mapper import GameBoardMapper

domain_board = DomainGameBoard([[1, 0, 0], [0, 2, 0], [0, 0, 1]])
data_board = GameBoardMapper.to_datasource(domain_board)
```

#### `to_domain(data_board: DataGameBoard) -> DomainGameBoard`
Convert datasource GameBoard to domain GameBoard.

```python
from datasource.mapper.game_board_mapper import GameBoardMapper

domain_board = GameBoardMapper.to_domain(data_board)
```

---

### GameMapper

**File**: `datasource/mapper/game_mapper.py`

Maps between domain and datasource Game models.

**Methods**:

#### `to_datasource(domain_game: DomainGame) -> DataGame`
Convert domain Game to datasource Game.

```python
from domain.model.game import Game as DomainGame
from datasource.mapper.game_mapper import GameMapper

domain_game = DomainGame(game_id, domain_board)
data_game = GameMapper.to_datasource(domain_game)
```

#### `to_domain(data_game: DataGame) -> DomainGame`
Convert datasource Game to domain Game.

```python
from datasource.mapper.game_mapper import GameMapper

domain_game = GameMapper.to_domain(data_game)
```

---

## Storage

### GameStorage

**File**: `datasource/repository/game_storage.py`

Thread-safe in-memory storage for games using Python's threading lock mechanism.

**Thread Safety**:
- Uses `threading.Lock` for synchronization
- All operations are atomic
- Safe for concurrent access from multiple threads
- Supports multiple simultaneous games

**Methods**:

#### `save(game: Game) -> None`
Save a game to storage (creates or updates).

```python
from datasource.repository.game_storage import GameStorage

storage = GameStorage()
storage.save(game)
```

#### `get(game_id: UUID) -> Optional[Game]`
Retrieve a game by UUID.

```python
game = storage.get(game_id)
if game is not None:
    print(f"Found game: {game}")
```

#### `delete(game_id: UUID) -> bool`
Delete a game by UUID.

```python
deleted = storage.delete(game_id)
if deleted:
    print("Game deleted successfully")
```

#### `exists(game_id: UUID) -> bool`
Check if a game exists.

```python
if storage.exists(game_id):
    print("Game exists")
```

#### `clear() -> None`
Clear all games from storage.

```python
storage.clear()
```

#### `count() -> int`
Get the number of stored games.

```python
num_games = storage.count()
print(f"Total games: {num_games}")
```

**Implementation Details**:
- Uses `Dict[UUID, Game]` internally
- Lock acquired for all operations
- No external dependencies (pure Python)

---

## Repository

### GameRepository (Interface)

**File**: `datasource/repository/game_repository.py`

Abstract interface defining repository contract.

**Methods**:

#### `save(game: Game) -> None`
Save a domain game.

#### `get(game_id: UUID) -> Optional[Game]`
Retrieve a domain game by UUID.

#### `delete(game_id: UUID) -> bool`
Delete a game by UUID.

#### `exists(game_id: UUID) -> bool`
Check if a game exists.

---

### GameRepositoryImpl

**File**: `datasource/repository/game_repository_impl.py`

Concrete implementation of GameRepository using GameStorage.

**Constructor**:
```python
def __init__(self, storage: GameStorage):
    """
    Args:
        storage: GameStorage instance for persistence
    """
```

**Key Responsibilities**:
1. Convert domain models to datasource models (using mappers)
2. Delegate storage operations to GameStorage
3. Convert datasource models back to domain models
4. Provide clean abstraction for domain layer

**Example Usage**:
```python
from datasource.repository.game_storage import GameStorage
from datasource.repository.game_repository_impl import GameRepositoryImpl
from domain.model.game import Game
from domain.model.game_board import GameBoard
from uuid import uuid4

# Initialize
storage = GameStorage()
repository = GameRepositoryImpl(storage)

# Save a game
game_id = uuid4()
board = GameBoard([[1, 0, 0], [0, 0, 0], [0, 0, 0]])
game = Game(game_id, board)
repository.save(game)

# Retrieve a game
retrieved_game = repository.get(game_id)
if retrieved_game:
    print(f"Found: {retrieved_game}")

# Check existence
if repository.exists(game_id):
    print("Game exists")

# Delete a game
if repository.delete(game_id):
    print("Game deleted")
```

---

## Design Patterns

### 1. Repository Pattern
- Abstracts data access logic
- Provides collection-like interface
- Decouples domain from storage details

### 2. Data Mapper Pattern
- Separates domain and persistence models
- Enables independent evolution of layers
- Handles conversion between representations

### 3. Singleton Pattern (for Storage)
- Single GameStorage instance shared across application
- Managed by DI container
- Ensures consistent state

### 4. Dependency Injection
- Repository depends on Storage (injected)
- Enables testing with mock storage
- Loose coupling between components

---

## Thread Safety

### Concurrency Support

The datasource layer is designed for concurrent access:

**Storage Level**:
- All GameStorage methods use `threading.Lock`
- Operations are atomic
- Safe for multi-threaded web servers

**Repository Level**:
- Stateless operations
- Safe for concurrent calls
- Each request gets consistent view

**Mappers**:
- Pure functions (stateless)
- Thread-safe by design
- No shared state

### Concurrent Game Scenario

```python
from threading import Thread

def play_game(game_id):
    # Each thread works with its own game
    game = repository.get(game_id)
    # ... make moves ...
    repository.save(game)

# Multiple concurrent games
threads = [Thread(target=play_game, args=(uuid4(),)) for _ in range(10)]
for t in threads:
    t.start()
for t in threads:
    t.join()
```

---

## Data Flow

### Save Operation

```
1. Domain Layer creates Game object
   ↓
2. Repository.save(domain_game) called
   ↓
3. GameMapper converts to datasource Game
   ↓
4. Storage.save(data_game) called
   ↓
5. Lock acquired
   ↓
6. Game stored in dictionary
   ↓
7. Lock released
```

### Retrieve Operation

```
1. Domain Layer requests game by UUID
   ↓
2. Repository.get(game_id) called
   ↓
3. Storage.get(game_id) called
   ↓
4. Lock acquired
   ↓
5. Game retrieved from dictionary
   ↓
6. Lock released
   ↓
7. GameMapper converts to domain Game
   ↓
8. Domain Game returned
```

---

## Error Handling

The datasource layer is designed for robustness:

**Storage Operations**:
- Return `None` for missing games (not exceptions)
- Return `False` for failed deletions
- Atomic operations prevent partial updates

**Thread Safety**:
- Lock ensures data consistency
- No race conditions
- No deadlocks (single lock design)

**Mapper Operations**:
- Assume valid input from domain layer
- Domain layer handles validation
- Simple conversion logic

---

## Testing

### Unit Tests

Test individual components:

```python
# Test Storage
storage = GameStorage()
storage.save(game)
assert storage.exists(game_id)

# Test Mappers
data_board = GameBoardMapper.to_datasource(domain_board)
assert data_board.board == domain_board.board

# Test Repository
repository = GameRepositoryImpl(storage)
repository.save(domain_game)
assert repository.get(game_id) == domain_game
```

### Thread Safety Tests

Test concurrent access:

```python
def test_concurrent_saves():
    storage = GameStorage()
    repository = GameRepositoryImpl(storage)
    
    def save_game(thread_id):
        for i in range(100):
            game_id = uuid4()
            game = create_game(game_id)
            repository.save(game)
    
    threads = [Thread(target=save_game, args=(i,)) for i in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    # Verify all saves succeeded
    assert storage.count() == 1000
```

---

## Dependencies

### Internal Dependencies
- `domain.model.game_board` → Used by mappers
- `domain.model.game` → Used by mappers and repository
- `datasource.model.*` → Used internally
- `datasource.mapper.*` → Used by repository

### External Dependencies
- `threading` → For thread-safe operations
- `typing` → For type hints
- `uuid` → For game identifiers

**No third-party dependencies required!**

---

## Future Enhancements

### Potential Improvements

1. **Database Integration**:
   - Replace in-memory storage with database
   - Implement `GameRepositoryImpl` for SQL/NoSQL
   - No changes needed to domain layer

2. **Caching**:
   - Add caching layer above repository
   - Reduce storage access
   - Improve performance

3. **Serialization**:
   - Add JSON serialization for games
   - Enable API responses
   - File-based storage

4. **Metrics**:
   - Track repository operation counts
   - Monitor storage size
   - Performance analytics

### Extensibility Points

The architecture supports easy extensions:

**New Storage Backend**:
```python
class DatabaseStorage:
    def save(self, game): ...
    def get(self, game_id): ...

# Just inject different storage
repository = GameRepositoryImpl(DatabaseStorage())
```

**Multiple Repositories**:
```python
class GameArchiveRepository:
    """Repository for completed games."""
    pass

class ActiveGameRepository:
    """Repository for ongoing games."""
    pass
```

---

## Performance Considerations

### Storage Performance

- **Save**: O(1) - Hash table insert
- **Get**: O(1) - Hash table lookup
- **Delete**: O(1) - Hash table deletion
- **Exists**: O(1) - Hash table membership test

### Memory Usage

- Each game: ~100 bytes (UUID + board)
- 1000 games: ~100 KB
- Scales linearly with game count

### Lock Contention

- Single lock design is simple but may bottleneck
- For high-concurrency scenarios, consider:
  - Read-write locks
  - Lock-free data structures
  - Sharding by game ID

---

## Integration with Other Layers

### Domain Layer Integration

```python
# Domain service uses repository
class GameServiceImpl(GameService):
    def __init__(self, repository: GameRepository):
        self._repository = repository
    
    def process_move(self, game_id, move):
        game = self._repository.get(game_id)
        # ... game logic ...
        self._repository.save(game)
```

### DI Layer Integration

```python
# DI container wires everything together
class Container:
    def __init__(self):
        self.storage = GameStorage()  # Singleton
        self.repository = GameRepositoryImpl(self.storage)
        self.service = GameServiceImpl(self.repository)
```

---

## Best Practices

### Do's ✓

- Always inject Storage into Repository
- Use mappers for all conversions
- Keep models simple (no business logic)
- Test thread safety
- Return `None` for missing data

### Don'ts ✗

- Don't add business logic to models
- Don't skip mapper conversions
- Don't access storage directly from domain
- Don't ignore thread safety
- Don't return exceptions for missing data

---

## Summary

The datasource layer provides:

1. **Clean Abstraction**: Repository pattern hides storage details
2. **Thread Safety**: Lock-based synchronization for concurrent access
3. **Separation of Concerns**: Different models for domain and persistence
4. **Testability**: Mock storage for unit tests
5. **Extensibility**: Easy to swap storage implementations
6. **Performance**: O(1) operations for all key methods

The layer successfully bridges the gap between domain business logic and data persistence while maintaining clean architecture principles.
