# Tic-Tac-Toe Project Structure

## Overview

This project implements a Tic-Tac-Toe game using a layered architecture pattern. The application is divided into four main layers: **web**, **domain**, **datasource**, and **di** (dependency injection). Each layer is implemented as a separate module with specific responsibilities.

## Architecture Principles

The project follows **Clean Architecture** principles:
- **Separation of Concerns**: Each layer has a distinct responsibility
- **Dependency Rule**: Dependencies point inward (web → domain ← datasource)
- **Abstraction**: Layers communicate through interfaces
- **Testability**: Each layer can be tested independently

## Project Structure

```
tic-tac-toe/
│
├── web/                          # Web Layer (Presentation Layer)
│   ├── __init__.py
│   ├── model/                    # Web-specific models (DTOs)
│   │   ├── __init__.py
│   │   ├── game_board.py         # Web model for game board
│   │   └── game.py               # Web model for current game
│   ├── mapper/                   # Domain ↔ Web mappers
│   │   ├── __init__.py
│   │   ├── game_board_mapper.py  # Maps domain GameBoard to web GameBoard
│   │   └── game_mapper.py        # Maps domain Game to web Game
│   ├── route/                    # HTTP route handlers (controllers)
│   │   ├── __init__.py
│   │   └── game_controller.py    # REST API endpoints for game operations
│   └── module/                   # Flask application setup
│       ├── __init__.py
│       └── app.py                # Flask application initialization
│
├── domain/                       # Domain Layer (Business Logic Layer)
│   ├── __init__.py
│   ├── model/                    # Domain models (business entities)
│   │   ├── __init__.py
│   │   ├── game_board.py         # Domain model for game board (integer matrix)
│   │   └── game.py               # Domain model for current game (UUID + board)
│   └── service/                  # Business logic services
│       ├── __init__.py
│       ├── game_service.py       # Interface for game service
│       └── game_service_impl.py  # Implementation of game service
│
├── datasource/                   # Data Source Layer (Data Access Layer)
│   ├── __init__.py
│   ├── model/                    # Data models (persistence entities)
│   │   ├── __init__.py
│   │   ├── game_board.py         # Data model for game board
│   │   └── game.py               # Data model for current game
│   ├── mapper/                   # Domain ↔ Datasource mappers
│   │   ├── __init__.py
│   │   ├── game_board_mapper.py  # Maps domain GameBoard to data GameBoard
│   │   └── game_mapper.py        # Maps domain Game to data Game
│   └── repository/               # Data access repositories
│       ├── __init__.py
│       ├── game_repository.py    # Interface for game repository
│       ├── game_repository_impl.py # Implementation of game repository
│       └── game_storage.py       # Thread-safe in-memory storage
│
└── di/                           # Dependency Injection Layer
    ├── __init__.py
    └── container.py              # Dependency injection container (graph)
```

## Layer Descriptions

### 1. Web Layer (`web/`)

**Responsibility**: Handle HTTP requests and responses, present data to clients.

**Components**:
- **model/**: Data Transfer Objects (DTOs) for API communication
  - Contains JSON-serializable models for requests/responses
  - Independent from domain models to allow API versioning
  
- **mapper/**: Convert between domain models and web models
  - `game_board_mapper.py`: Transforms domain GameBoard ↔ web GameBoard
  - `game_mapper.py`: Transforms domain Game ↔ web Game
  
- **route/**: REST API controllers
  - `game_controller.py`: Handles `POST /game/{uuid}` endpoint
  - Validates requests, calls domain services, formats responses
  
- **module/**: Application initialization
  - `app.py`: Flask application setup and configuration

**Dependencies**: 
- Uses domain layer services (via interfaces)
- No direct dependency on datasource layer

---

### 2. Domain Layer (`domain/`)

**Responsibility**: Implement business logic and rules.

**Components**:
- **model/**: Core business entities
  - `game_board.py`: Game board represented as integer matrix
    - 0: empty cell
    - 1: X (human player)
    - 2: O (computer player)
  - `game.py`: Current game entity with UUID and game board
  
- **service/**: Business logic interfaces and implementations
  - `game_service.py`: Interface defining game operations
    - `get_next_move()`: Calculate computer move using Minimax algorithm
    - `validate_game_board()`: Ensure no previous moves were modified
    - `check_game_over()`: Determine if game has ended
  - `game_service_impl.py`: Concrete implementation of game service

**Dependencies**: 
- No dependencies on other layers (pure business logic)
- Repository interfaces are defined here but implemented in datasource

---

### 3. Datasource Layer (`datasource/`)

**Responsibility**: Manage data persistence and retrieval.

**Components**:
- **model/**: Data persistence entities
  - `game_board.py`: Persistence model for game board
  - `game.py`: Persistence model for current game
  
- **mapper/**: Convert between domain models and data models
  - `game_board_mapper.py`: Transforms domain GameBoard ↔ data GameBoard
  - `game_mapper.py`: Transforms domain Game ↔ data Game
  
- **repository/**: Data access layer
  - `game_repository.py`: Interface for game data operations
  - `game_repository_impl.py`: Implementation using storage
  - `game_storage.py`: Thread-safe in-memory storage using concurrent collections
    - Supports multiple simultaneous games
    - Thread-safe operations for concurrent access

**Dependencies**: 
- Implements interfaces defined in domain layer
- No dependency on web layer

---

### 4. Dependency Injection Layer (`di/`)

**Responsibility**: Wire up dependencies and manage object lifecycle.

**Components**:
- `container.py`: Dependency injection container
  - Defines the dependency graph
  - Manages singleton instances (e.g., storage)
  - Creates and injects repositories
  - Creates and injects services
  - Provides configured instances to web layer

**Singleton Components**:
- Game storage (shared across all requests)

**Transient Components**:
- Repositories (created per request)
- Services (created per request)

---

## Data Flow

### Example: POST /game/{uuid} Request

```
1. Client sends HTTP POST request
   ↓
2. Web Layer (route/game_controller.py)
   - Receives request
   - Deserializes JSON to web model
   ↓
3. Web Mapper (mapper/game_mapper.py)
   - Converts web model to domain model
   ↓
4. Domain Service (service/game_service_impl.py)
   - Validates game board
   - Checks if game is over
   - Calculates next move using Minimax
   ↓
5. Repository (datasource/repository/game_repository_impl.py)
   - Retrieves/saves game from storage
   ↓
6. Storage (datasource/repository/game_storage.py)
   - Thread-safe access to in-memory data
   ↓
7. Response flows back through layers
   - Data model → Domain model → Web model → HTTP response
```

---

## Design Patterns Used

1. **Layered Architecture**: Separation of concerns across layers
2. **Repository Pattern**: Abstraction of data access
3. **Dependency Injection**: Decoupling of components
4. **Data Mapper Pattern**: Conversion between layer models
5. **Service Layer Pattern**: Encapsulation of business logic
6. **Singleton Pattern**: Single instance of storage

---

## Technology Stack

- **Python 3.x**: Programming language
- **Flask**: Web framework for REST API
- **Threading**: Thread-safe collections for concurrent access
- **UUID**: Unique game identifiers

---

## Module Independence

Each layer is designed as a separate module:
- Can be developed independently
- Can be tested in isolation
- Can be replaced without affecting other layers
- Clear interfaces between layers

---

## Thread Safety

The application supports multiple concurrent games:
- Thread-safe storage implementation
- Concurrent collections for data storage
- Safe for multi-threaded web server environments

---

## Extensibility

The architecture allows for easy extensions:
- **Add new endpoints**: Extend web/route layer
- **Change storage**: Implement new repository (e.g., database)
- **Modify algorithms**: Update domain service implementations
- **Add features**: Extend models and services in domain layer

---

## Testing Strategy

Each layer can be tested independently:
- **Unit tests**: Test domain services with mock repositories
- **Integration tests**: Test repositories with actual storage
- **API tests**: Test web controllers with mock services
- **End-to-end tests**: Test complete flow through all layers

---

## Configuration

Dependency injection configuration in `di/container.py`:
```python
container = Container()
container.storage = Singleton(GameStorage)
container.repository = GameRepositoryImpl(container.storage)
container.service = GameServiceImpl(container.repository)
```

---

## Notes

- All models, interfaces, and implementations are in separate files
- Mappers handle conversions between layer boundaries
- Domain layer is pure business logic with no framework dependencies
- Web layer uses Flask for HTTP handling
- Datasource layer uses thread-safe collections for concurrency
