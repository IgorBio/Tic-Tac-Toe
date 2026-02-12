# Tic-Tac-Toe (Flask + Minimax)

A layered Tic-Tac-Toe project with:

- a Flask backend API,
- a simple browser UI,
- a Minimax-based computer opponent.

## What You Can Run

- Web UI: `GET /`
- Health check: `GET /health`
- Game move API: `POST /game/<uuid>`

## Requirements

- Python 3.10+
- `flask`

Install dependency:

```bash
pip install flask
```

## Run

From the project root:

```bash
python main.py
```

Server starts on:

- `http://localhost:5000/`

## Play in Browser

1. Open `http://localhost:5000/`.
2. Click a cell to place `X`.
3. The server responds with the AI move (`O`).
4. Click **New game** to reset.

## API

### `POST /game/<uuid>`

Submit the current board after the human move and receive the updated board after the AI move.

Request example:

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

Successful response example:

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

Possible extra fields when a game finishes:

```json
{
  "game_over": true,
  "winner": "Human wins (X)"
}
```

### `GET /health`

Response:

```json
{
  "status": "ok"
}
```

## Board Encoding

- `0` = empty
- `1` = human (`X`)
- `2` = computer (`O`)

## Architecture

The project uses a layered structure:

- `web/` - HTTP layer (routes, app module, web models/mappers)
- `domain/` - game rules and core services
- `datasource/` - persistence abstractions and implementations
- `di/` - dependency wiring

## License

MIT
