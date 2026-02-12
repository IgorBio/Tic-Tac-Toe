# Web Layer Documentation

## Overview

The web layer provides the REST API interface for the Tic-Tac-Toe game. This layer handles HTTP requests/responses, validates input, and coordinates with the domain layer for business logic.

## Structure

```
web/
├── __init__.py
├── model/
│   ├── __init__.py
│   ├── game_board.py      # Web model for game board
│   └── game.py            # Web model for game
├── mapper/
│   ├── __init__.py
│   ├── game_board_mapper.py  # Domain ↔ Web GameBoard mapper
│   └── game_mapper.py        # Domain ↔ Web Game mapper
├── route/
│   ├── __init__.py
│   └── game_controller.py    # REST API controller
└── module/
    ├── __init__.py
    └── app.py                # Flask application setup
```

## Models

### GameBoard (Web)

**File**: `web/model/game_board.py`

Web representation of the game board, optimized for JSON serialization.

**Properties**:
- `board` (property): Returns a copy of the 3x3 integer matrix

**Methods**:
- `to_dict() -> List[List[int]]`: Convert to dictionary for JSON
- `from_dict(data: List[List[int]]) -> GameBoard`: Create from dictionary

**Example**:
```python
from web.model.game_board import GameBoard

# Create board
board = GameBoard([[1, 0, 0], [0, 2, 0], [0, 0, 0]])

# Serialize to JSON
board_dict = board.to_dict()

# Deserialize from JSON
board = GameBoard.from_dict(board_dict)
```

---

### Game (Web)

**File**: `web/model/game.py`

Web representation of a game, with UUID and board state.

**Properties**:
- `uuid` (UUID): Unique game identifier
- `board` (GameBoard): Game board state

**Methods**:
- `to_dict() -> Dict[str, Any]`: Convert to dictionary for JSON
- `from_dict(data: Dict[str, Any]) -> Game`: Create from dictionary

**Example**:
```python
from uuid import uuid4
from web.model.game import Game
from web.model.game_board import GameBoard

# Create game
game = Game(uuid4(), GameBoard([[0, 0, 0], [0, 1, 0], [0, 0, 0]]))

# Serialize to JSON
game_dict = game.to_dict()
# {'uuid': '...', 'board': [[0, 0, 0], [0, 1, 0], [0, 0, 0]]}

# Deserialize from JSON
game = Game.from_dict(game_dict)
```

**Validation**:
- UUID must be valid
- Board must be present
- Raises `ValueError` for invalid data

---

## Mappers

### GameBoardMapper

**File**: `web/mapper/game_board_mapper.py`

Converts between domain and web GameBoard models.

**Methods**:

#### `to_web(domain_board: DomainGameBoard) -> WebGameBoard`
Convert domain GameBoard to web GameBoard.

```python
from web.mapper.game_board_mapper import GameBoardMapper

web_board = GameBoardMapper.to_web(domain_board)
```

#### `to_domain(web_board: WebGameBoard) -> DomainGameBoard`
Convert web GameBoard to domain GameBoard.

```python
domain_board = GameBoardMapper.to_domain(web_board)
```

---

### GameMapper

**File**: `web/mapper/game_mapper.py`

Converts between domain and web Game models.

**Methods**:

#### `to_web(domain_game: DomainGame) -> WebGame`
Convert domain Game to web Game.

```python
from web.mapper.game_mapper import GameMapper

web_game = GameMapper.to_web(domain_game)
```

#### `to_domain(web_game: WebGame) -> DomainGame`
Convert web Game to domain Game.

```python
domain_game = GameMapper.to_domain(web_game)
```

---

## Controllers

### GameController

**File**: `web/route/game_controller.py`

REST API controller for game operations.

**Constructor**:
```python
def __init__(self, game_service: GameService):
    """
    Args:
        game_service: Domain service for game business logic
    """
```

**Endpoints**:

#### POST /game/{uuid}

Submit a move and receive the computer's response.

**Request**:
```json
{
  "uuid": "123e4567-e89b-12d3-a456-426614174000",
  "board": [
    [0, 0, 0],
    [0, 1, 0],
    [0, 0, 0]
  ]
}
```

**Response (Success)**:
```json
{
  "uuid": "123e4567-e89b-12d3-a456-426614174000",
  "board": [
    [2, 0, 0],
    [0, 1, 0],
    [0, 0, 0]
  ]
}
```

**Response (Game Over)**:
```json
{
  "uuid": "123e4567-e89b-12d3-a456-426614174000",
  "board": [
    [1, 1, 1],
    [2, 2, 0],
    [0, 0, 0]
  ],
  "game_over": true,
  "winner": "Human wins (X)"
}
```

**Error Responses**:

**400 Bad Request** - Invalid move:
```json
{
  "error": "Invalid move",
  "message": "Multiple cells changed: 2. Only one move allowed per turn."
}
```

**400 Bad Request** - UUID mismatch:
```json
{
  "error": "UUID mismatch",
  "message": "UUID in URL (...) does not match UUID in body (...)"
}
```

**400 Bad Request** - Game already over:
```json
{
  "error": "Game already over",
  "message": "Human wins (X)"
}
```

**500 Internal Server Error**:
```json
{
  "error": "Internal server error",
  "message": "..."
}
```

---

## Flask Application

### create_app

**File**: `web/module/app.py`

Creates and configures the Flask application.

**Usage**:
```python
from web.module.app import create_app

app = create_app(game_service)
```

**Endpoints**:
- `POST /game/{uuid}` - Game operations
- `GET /health` - Health check

---

### run_app

Convenience function to create and run the application.

**Usage**:
```python
from web.module.app import run_app

run_app(game_service, host='0.0.0.0', port=5000, debug=False)
```

---

## Request/Response Flow

### Successful Game Flow

```
1. Client sends POST /game/{uuid}
   {
     "uuid": "...",
     "board": [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
   }
   ↓
2. GameController receives request
   - Validates JSON
   - Validates UUID match
   ↓
3. Parse web model from JSON
   - WebGame.from_dict(data)
   ↓
4. Convert to domain model
   - GameMapper.to_domain(web_game)
   ↓
5. Validate move
   - game_service.validate_game_board()
   - Checks: only one new move, no changes to previous moves
   ↓
6. Check if game over (after human move)
   - If yes, return current state with game_over flag
   ↓
7. Get computer's move
   - game_service.get_next_move()
   - Uses Minimax algorithm
   ↓
8. Apply computer's move
   - board.set_cell(row, col, 2)
   ↓
9. Save updated game
   - repository.save(game)
   ↓
10. Check if game over (after computer move)
    ↓
11. Convert to web model
    - GameMapper.to_web(domain_game)
    ↓
12. Serialize to JSON
    - web_game.to_dict()
    ↓
13. Return response
    {
      "uuid": "...",
      "board": [[2, 0, 0], [0, 1, 0], [0, 0, 0]]
    }
```

---

## Error Handling

The controller provides detailed error messages for various scenarios:

### Validation Errors (400)

1. **Invalid JSON**:
   - Missing request body
   - Malformed JSON

2. **UUID Errors**:
   - UUID in URL doesn't match body
   - Invalid UUID format
   - Missing UUID in body

3. **Invalid Moves**:
   - Multiple cells changed
   - Previous moves modified
   - No move detected
   - Wrong player (computer instead of human)

4. **Game State Errors**:
   - Game already over
   - Invalid board state

### Server Errors (500)

- Unexpected exceptions
- Service errors
- Internal failures

---

## Concurrent Game Support

The web layer supports multiple simultaneous games:

- Each game has unique UUID
- Games stored independently in repository
- Thread-safe storage (handled by datasource layer)
- No shared state between requests

**Example - Multiple Games**:
```python
# Game 1
POST /game/uuid-1
{
  "uuid": "uuid-1",
  "board": [[1, 0, 0], [0, 0, 0], [0, 0, 0]]
}

# Game 2 (different game, independent)
POST /game/uuid-2
{
  "uuid": "uuid-2",
  "board": [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
}
```

---

## Testing

### Unit Tests

Test web models and mappers:

```python
from web.model.game import Game
from web.mapper.game_mapper import GameMapper

# Test serialization
game_dict = game.to_dict()
assert 'uuid' in game_dict
assert 'board' in game_dict

# Test deserialization
game = Game.from_dict(game_dict)

# Test mapping
web_game = GameMapper.to_web(domain_game)
domain_game = GameMapper.to_domain(web_game)
```

### Integration Tests

Test API endpoints using Flask test client:

```python
from web.module.app import create_app

app = create_app(game_service)
client = app.test_client()

# Test POST /game/{uuid}
response = client.post(
    f'/game/{game_id}',
    json={
        'uuid': str(game_id),
        'board': [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    }
)

assert response.status_code == 200
data = response.get_json()
assert 'uuid' in data
assert 'board' in data
```

---

## API Examples

### Start New Game

```bash
curl -X POST http://localhost:5000/game/123e4567-e89b-12d3-a456-426614174000 \
  -H "Content-Type: application/json" \
  -d '{
    "uuid": "123e4567-e89b-12d3-a456-426614174000",
    "board": [
      [0, 0, 0],
      [0, 1, 0],
      [0, 0, 0]
    ]
  }'
```

**Response**:
```json
{
  "uuid": "123e4567-e89b-12d3-a456-426614174000",
  "board": [
    [2, 0, 0],
    [0, 1, 0],
    [0, 0, 0]
  ]
}
```

---

### Continue Existing Game

```bash
curl -X POST http://localhost:5000/game/123e4567-e89b-12d3-a456-426614174000 \
  -H "Content-Type: application/json" \
  -d '{
    "uuid": "123e4567-e89b-12d3-a456-426614174000",
    "board": [
      [2, 0, 0],
      [0, 1, 0],
      [1, 0, 0]
    ]
  }'
```

---

### Invalid Move Example

```bash
curl -X POST http://localhost:5000/game/123e4567-e89b-12d3-a456-426614174000 \
  -H "Content-Type: application/json" \
  -d '{
    "uuid": "123e4567-e89b-12d3-a456-426614174000",
    "board": [
      [1, 1, 0],
      [0, 1, 0],
      [0, 0, 0]
    ]
  }'
```

**Response** (400):
```json
{
  "error": "Invalid move",
  "message": "Multiple cells changed: 2. Only one move allowed per turn."
}
```

---

## Dependencies

### Internal Dependencies
- `domain.model.*` - Used by mappers
- `domain.service.game_service` - Used by controller
- `web.model.*` - Used internally
- `web.mapper.*` - Used by controller

### External Dependencies
- `Flask` - Web framework
- `uuid` - UUID support
- `typing` - Type hints

---

## Configuration

### Flask Configuration

The app can be configured with:

```python
app.config['JSON_SORT_KEYS'] = False  # Don't sort JSON keys
```

### Running the Application

**Development**:
```bash
python main.py
```

**Production**:
```python
from web.module.app import create_app

app = create_app(game_service)
# Use production WSGI server like Gunicorn
```

---

## Best Practices

### Do's ✓

- Always validate UUID in both URL and body
- Provide detailed error messages
- Use mappers for all conversions
- Return appropriate HTTP status codes
- Support JSON serialization
- Handle all exceptions gracefully

### Don'ts ✗

- Don't skip validation
- Don't expose internal errors to clients
- Don't modify domain models in web layer
- Don't add business logic to controllers
- Don't return 200 for errors

---

## Security Considerations

1. **Input Validation**:
   - Validate all JSON input
   - Check UUID format
   - Validate board dimensions

2. **Error Messages**:
   - Don't expose stack traces
   - Sanitize error messages
   - Log internal errors separately

3. **Rate Limiting**:
   - Consider adding rate limiting
   - Prevent abuse

4. **CORS**:
   - Configure CORS if needed
   - Restrict allowed origins

---

## Future Enhancements

1. **Authentication**:
   - Add user authentication
   - Track games per user

2. **Pagination**:
   - List user's games
   - Game history

3. **WebSockets**:
   - Real-time updates
   - Multiplayer support

4. **API Versioning**:
   - Version endpoints
   - Support multiple API versions

---

## Summary

The web layer provides:

1. **REST API**: Clean HTTP interface
2. **JSON Serialization**: Easy integration
3. **Validation**: Comprehensive error checking
4. **Error Handling**: Detailed error messages
5. **Concurrent Games**: Multiple simultaneous games
6. **Clean Architecture**: Separation from domain logic

All requirements for Task 4 have been implemented successfully.
