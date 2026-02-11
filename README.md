# Tic-Tac-Toe Game API

A RESTful API for playing Tic-Tac-Toe against an AI opponent using the Minimax algorithm.

## Features

- **Minimax Algorithm**: Optimal AI opponent that never loses
- **Concurrent Games**: Support for multiple simultaneous games
- **Thread-Safe**: Designed for concurrent access
- **Layered Architecture**: Clean separation of concerns
- **REST API**: Simple HTTP interface

## Quick Start

### Installation

```bash
pip install flask
```

### Running the Application

```bash
python -m web.module.app
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Create/Update Game

**Endpoint**: `POST /game/{uuid}`

**Description**: Submit a move and receive the computer's response

**Request Body**:
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

**Response Body**:
```json
{
  "uuid": "123e4567-e89b-12d3-a456-426614174000",
  "board": [
    [0, 0, 0],
    [0, 1, 0],
    [2, 0, 0]
  ]
}
```

**Board Values**:
- `0`: Empty cell
- `1`: X (human player)
- `2`: O (computer player)

## Architecture

This project follows a **layered architecture** pattern:

- **Web Layer**: HTTP handling and routing
- **Domain Layer**: Business logic and game rules
- **Datasource Layer**: Data persistence and storage
- **DI Layer**: Dependency injection and configuration

For detailed architecture documentation, see [project_structure.md](project_structure.md)

## Project Structure

```
tic-tac-toe/
├── web/              # Presentation layer
├── domain/           # Business logic layer
├── datasource/       # Data access layer
└── di/               # Dependency injection
```

## License

MIT
