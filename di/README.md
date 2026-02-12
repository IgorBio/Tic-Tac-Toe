# Dependency Injection Layer

The DI (Dependency Injection) layer manages the dependency graph for the Tic-Tac-Toe application.

## Quick Start

```python
from di.container import Container

# Create container
container = Container()

# Get service (ready to use)
game_service = container.service

# Use in your application
from web.module.app import run_app
run_app(game_service, host='0.0.0.0', port=5000)
```

## Components

### Container

The `Container` class manages all dependencies and their lifecycle.

**Managed Components**:
- **GameStorage** (Singleton) - Thread-safe storage for games
- **GameRepository** - Data access layer
- **GameService** - Business logic layer

## Dependency Graph

```
Container
    │
    ├─> GameStorage (singleton)
    │        │
    │        ↓
    ├─> GameRepository (uses storage)
    │        │
    │        ↓
    └─> GameService (uses repository)
```

## Usage

### Basic Usage

```python
from di.container import Container

# Initialize container
container = Container()

# Get service
service = container.service

# Service is ready to use with all dependencies injected
```

### With Flask Application

```python
from di.container import Container
from web.module.app import create_app

# Create container
container = Container()

# Get service
game_service = container.service

# Create Flask app with injected service
app = create_app(game_service)

# Run app
app.run(host='0.0.0.0', port=5000)
```

### Accessing Components

```python
from di.container import Container

container = Container()

# Get storage (singleton)
storage = container.storage
# or
storage = container.get_storage()

# Get repository
repository = container.repository
# or
repository = container.get_repository()

# Get service
service = container.service
# or
service = container.get_service()
```

## Component Lifecycle

### Singleton Components

**GameStorage**:
- Created once per container
- Shared across all requests
- Thread-safe for concurrent access
- Maintains state for all games

### Transient Components

**GameRepository**:
- Created with singleton storage
- Can be recreated if needed
- Stateless operations

**GameService**:
- Created with repository
- Can be recreated if needed
- Stateless operations

## Features

✓ **Singleton Pattern**: Single storage instance  
✓ **Dependency Graph**: Automatic dependency resolution  
✓ **Type Safety**: Full type hints  
✓ **Clean Separation**: Each component in separate file  
✓ **Easy Testing**: Simple to mock dependencies  

## Benefits

1. **Centralized Configuration**: All dependencies configured in one place
2. **Loose Coupling**: Components depend on interfaces, not implementations
3. **Easy Testing**: Mock dependencies by replacing container properties
4. **Single Responsibility**: Container only manages dependencies
5. **Scalability**: Easy to add new dependencies

## Testing

### Unit Testing with Mocked Dependencies

```python
from di.container import Container
from unittest.mock import Mock

# Create container
container = Container()

# Replace service with mock for testing
mock_service = Mock()
container._service = mock_service

# Now container.service returns the mock
assert container.service == mock_service
```

### Integration Testing

```python
from di.container import Container

# Use real container for integration tests
container = Container()
service = container.service

# Test with real dependencies
# ...
```

## Example: Complete Application

```python
#!/usr/bin/env python
"""Main entry point for Tic-Tac-Toe application."""

from di.container import Container
from web.module.app import run_app


def main():
    """Initialize and run the application."""
    # Create DI container
    container = Container()
    
    # Get game service (with all dependencies injected)
    game_service = container.service
    
    # Run Flask application
    print("Starting Tic-Tac-Toe API server...")
    run_app(game_service, host='0.0.0.0', port=5000, debug=True)


if __name__ == '__main__':
    main()
```

## Architecture

The DI layer follows these principles:

1. **Dependency Inversion**: High-level modules depend on abstractions
2. **Single Responsibility**: Container only manages dependencies
3. **Open/Closed**: Easy to extend without modifying existing code
4. **Interface Segregation**: Each component gets exactly what it needs

## Thread Safety

The container itself is thread-safe:
- Singleton storage uses locks internally
- Container properties are immutable after initialization
- Safe for multi-threaded web servers

## Future Enhancements

Potential improvements:

1. **Configuration Files**: Load dependencies from config
2. **Multiple Containers**: Support different configurations
3. **Lazy Loading**: Create components only when needed
4. **Scoped Lifetimes**: Request-scoped instances
5. **Auto-wiring**: Automatic dependency resolution

## Compliance with Requirements

✅ Class Container with dependency graph  
✅ GameStorage as singleton  
✅ Repository with storage dependency  
✅ Service with repository dependency  
✅ All components in separate files  

## License

MIT
