# Datasource Layer

The datasource layer provides data persistence and storage capabilities for the Tic-Tac-Toe game.

## Quick Start

```python
from uuid import uuid4
from domain.model.game import Game
from domain.model.game_board import GameBoard
from datasource.repository.game_storage import GameStorage
from datasource.repository.game_repository_impl import GameRepositoryImpl

# Initialize storage and repository
storage = GameStorage()
repository = GameRepositoryImpl(storage)

# Create and save a game
game_id = uuid4()
board = GameBoard([[1, 0, 0], [0, 0, 0], [0, 0, 0]])
game = Game(game_id, board)
repository.save(game)

# Retrieve the game
retrieved = repository.get(game_id)
print(f"Retrieved: {retrieved}")
```

## Components

### Models
- **GameBoard**: Persistence representation of game board
- **Game**: Persistence representation of game with UUID

### Mappers
- **GameBoardMapper**: Converts between domain and datasource GameBoard
- **GameMapper**: Converts between domain and datasource Game

### Repository
- **GameStorage**: Thread-safe in-memory storage
- **GameRepository**: Repository interface
- **GameRepositoryImpl**: Repository implementation

## Features

✓ **Thread-Safe**: Uses locks for concurrent access  
✓ **Clean Separation**: Domain-independent models  
✓ **Type-Safe**: Full type hints throughout  
✓ **Testable**: Easy to mock for testing  
✓ **Zero Dependencies**: Pure Python implementation  

## Testing

Run the test suite:

```bash
python tests/test_datasource.py
```

## Documentation

See [DATASOURCE_LAYER.md](DATASOURCE_LAYER.md) for comprehensive documentation.

## Architecture

The datasource layer follows the Repository pattern:

```
Domain Layer
     ↓
GameRepository (interface)
     ↓
GameRepositoryImpl
     ↓
GameMapper
     ↓
GameStorage (thread-safe)
```

## Thread Safety

All storage operations are thread-safe using Python's `threading.Lock`:

```python
# Multiple threads can safely access storage
def play_game():
    game = repository.get(game_id)
    # ... make moves ...
    repository.save(game)

threads = [Thread(target=play_game) for _ in range(10)]
```

## License

MIT
