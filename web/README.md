# Web Layer

The web layer provides the REST API interface for the Tic-Tac-Toe game.

## Quick Start

### Installation

```bash
pip install flask
```

### Running the API

```bash
python main.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### POST /game/{uuid}

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

### GET /health

Health check endpoint.

**Response**:
```json
{
  "status": "ok"
}
```

## Board Values

- `0`: Empty cell
- `1`: X (human player)
- `2`: O (computer player)

## Components

### Models
- **GameBoard**: Web representation of game board with JSON serialization
- **Game**: Web representation of game with UUID and board

### Mappers
- **GameBoardMapper**: Converts between domain and web GameBoard
- **GameMapper**: Converts between domain and web Game

### Controllers
- **GameController**: REST API endpoints for game operations

### Module
- **app.py**: Flask application setup and configuration

## Features

✓ **REST API**: Clean HTTP interface  
✓ **JSON Support**: Easy serialization/deserialization  
✓ **Validation**: Comprehensive input validation  
✓ **Error Handling**: Detailed error messages  
✓ **Concurrent Games**: Support for multiple simultaneous games  
✓ **Type-Safe**: Full type hints throughout  

## Testing

Run the test suite:

```bash
python tests/web/test_web.py
```

## Documentation

See [WEB_LAYER.md](WEB_LAYER.md) for comprehensive documentation.

## Example Usage

### Using curl

Start a new game:
```bash
curl -X POST http://localhost:5000/game/123e4567-e89b-12d3-a456-426614174000 \
  -H "Content-Type: application/json" \
  -d '{
    "uuid": "123e4567-e89b-12d3-a456-426614174000",
    "board": [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
  }'
```

### Using Python requests

```python
import requests
from uuid import uuid4

game_id = uuid4()

response = requests.post(
    f'http://localhost:5000/game/{game_id}',
    json={
        'uuid': str(game_id),
        'board': [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    }
)

print(response.json())
```

## Architecture

The web layer follows a clean architecture pattern:

```
Client Request
     ↓
GameController (validates, coordinates)
     ↓
GameMapper (domain ↔ web conversion)
     ↓
GameService (domain layer - business logic)
     ↓
GameRepository (datasource layer - persistence)
     ↓
Response to Client
```

## Error Responses

The API provides detailed error messages:

**Invalid Move**:
```json
{
  "error": "Invalid move",
  "message": "Multiple cells changed: 2. Only one move allowed per turn."
}
```

**UUID Mismatch**:
```json
{
  "error": "UUID mismatch",
  "message": "UUID in URL (...) does not match UUID in body (...)"
}
```

**Game Over**:
```json
{
  "error": "Game already over",
  "message": "Human wins (X)"
}
```

## Compliance with Requirements

✅ Models for game board and game in separate files  
✅ Mappers for domain ↔ web conversion  
✅ Flask controller with POST /game/{uuid} endpoint  
✅ Error responses with descriptions  
✅ Support for multiple concurrent games  
✅ All models, interfaces, implementations in separate files  

## License

MIT
