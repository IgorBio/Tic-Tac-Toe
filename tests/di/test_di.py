"""Test script for DI layer."""

import sys
sys.path.insert(0, '/home/claude')

from uuid import uuid4
from di.container import Container
from domain.model.game_board import GameBoard
from domain.model.game import Game
from datasource.repository.game_storage import GameStorage
from datasource.repository.game_repository import GameRepository
from domain.service.game_service import GameService


def test_container_creation():
    """Test container creation."""
    print("Testing Container Creation...")
    
    container = Container()
    print(f"✓ Container created: {container}")
    
    # Verify all components exist
    assert container.storage is not None
    assert container.repository is not None
    assert container.service is not None
    print("✓ All components initialized")
    
    print()


def test_singleton_storage():
    """Test that storage is a singleton."""
    print("Testing Singleton Storage...")
    
    container = Container()
    
    # Get storage multiple times
    storage1 = container.storage
    storage2 = container.get_storage()
    storage3 = container.storage
    
    # All should be the same instance
    assert storage1 is storage2
    assert storage2 is storage3
    assert storage1 is storage3
    print("✓ Storage is singleton (same instance)")
    
    # Verify it's a GameStorage instance
    assert isinstance(storage1, GameStorage)
    print(f"✓ Storage is GameStorage instance: {type(storage1).__name__}")
    
    print()


def test_repository_has_storage():
    """Test that repository is configured with storage."""
    print("Testing Repository Configuration...")
    
    container = Container()
    
    repository = container.repository
    
    # Verify it's a GameRepository
    assert isinstance(repository, GameRepository)
    print(f"✓ Repository is GameRepository instance")
    
    # Verify repository uses the singleton storage
    # (by checking it can access storage through the repository)
    game_id = uuid4()
    board = GameBoard([[0, 0, 0], [0, 1, 0], [0, 0, 0]])
    game = Game(game_id, board)
    
    repository.save(game)
    print(f"✓ Saved game through repository")
    
    # Verify it's in the singleton storage
    assert container.storage.exists(game_id)
    print(f"✓ Game exists in singleton storage")
    
    # Retrieve through repository
    retrieved = repository.get(game_id)
    assert retrieved is not None
    assert retrieved.game_id == game_id
    print(f"✓ Retrieved game through repository")
    
    print()


def test_service_has_repository():
    """Test that service is configured with repository."""
    print("Testing Service Configuration...")
    
    container = Container()
    
    service = container.service
    
    # Verify it's a GameService
    assert isinstance(service, GameService)
    print(f"✓ Service is GameService instance")
    
    # Verify service can use repository (indirectly)
    game_id = uuid4()
    board = GameBoard([[0, 0, 0], [0, 1, 0], [0, 0, 0]])
    game = Game(game_id, board)
    
    # Validate board (service uses repository internally)
    is_valid = service.validate_game_board(game_id, game, None)
    assert is_valid == True
    print(f"✓ Service validated board")
    
    # Get next move (service uses its full functionality)
    row, col = service.get_next_move(game)
    assert 0 <= row < 3
    assert 0 <= col < 3
    print(f"✓ Service computed next move: ({row}, {col})")
    
    print()


def test_full_integration():
    """Test full integration through container."""
    print("Testing Full Integration...")
    
    container = Container()
    
    # Use service to play a game
    game_id = uuid4()
    print(f"Game ID: {game_id}")
    
    # Human plays center
    board = GameBoard([[0, 0, 0], [0, 1, 0], [0, 0, 0]])
    game = Game(game_id, board)
    
    # Validate move
    is_valid = container.service.validate_game_board(game_id, game, None)
    assert is_valid
    print(f"✓ Move validated")
    
    # Get computer's response
    row, col = container.service.get_next_move(game)
    print(f"✓ Computer plays at ({row}, {col})")
    
    # Apply computer's move
    game.board.set_cell(row, col, 2)
    
    # Save game
    container.service._repository.save(game)
    print(f"✓ Game saved")
    
    # Verify game is in storage
    assert container.storage.exists(game_id)
    print(f"✓ Game exists in storage")
    
    # Retrieve game
    retrieved = container.service._repository.get(game_id)
    assert retrieved is not None
    assert retrieved.board.get_cell(row, col) == 2
    print(f"✓ Game retrieved with computer's move")
    
    print()


def test_multiple_containers():
    """Test that multiple containers have separate storages."""
    print("Testing Multiple Containers...")
    
    # Create two containers
    container1 = Container()
    container2 = Container()
    
    # Each should have its own storage
    assert container1.storage is not container2.storage
    print("✓ Each container has separate storage")
    
    # Save game in container1
    game_id = uuid4()
    board = GameBoard([[0, 0, 0], [0, 1, 0], [0, 0, 0]])
    game = Game(game_id, board)
    
    container1.repository.save(game)
    print(f"✓ Game saved in container1")
    
    # Game should exist in container1
    assert container1.storage.exists(game_id)
    print(f"✓ Game exists in container1 storage")
    
    # Game should NOT exist in container2
    assert not container2.storage.exists(game_id)
    print(f"✓ Game does NOT exist in container2 storage")
    
    print()


def test_getter_methods():
    """Test alternative getter methods."""
    print("Testing Getter Methods...")
    
    container = Container()
    
    # Test that property and getter return same instance
    assert container.storage is container.get_storage()
    print("✓ storage == get_storage()")
    
    assert container.repository is container.get_repository()
    print("✓ repository == get_repository()")
    
    assert container.service is container.get_service()
    print("✓ service == get_service()")
    
    print()


def test_complete_game_scenario():
    """Test a complete game scenario using container."""
    print("Testing Complete Game Scenario...")
    
    container = Container()
    service = container.service
    
    game_id = uuid4()
    print(f"\nGame ID: {game_id}")
    
    moves = [
        ((1, 1), "Human plays center"),
        ((0, 1), "Human plays top-center"),
    ]
    
    previous_game = None
    
    for i, ((row, col), description) in enumerate(moves, 1):
        print(f"\n--- Move {i}: {description} ---")
        
        # Get current board
        if previous_game is None:
            board = GameBoard([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        else:
            board = GameBoard(previous_game.board.board)
        
        # Make human move
        board.set_cell(row, col, 1)
        current_game = Game(game_id, board)
        
        # Validate
        is_valid = service.validate_game_board(game_id, current_game, previous_game)
        assert is_valid
        print(f"✓ Human move validated")
        
        # Check if game over
        is_over, winner = service.check_game_over(current_game)
        if is_over:
            print(f"✓ Game over! Winner: {winner}")
            break
        
        # Get computer move
        comp_row, comp_col = service.get_next_move(current_game)
        print(f"✓ Computer plays at ({comp_row}, {comp_col})")
        
        # Apply computer move
        current_game.board.set_cell(comp_row, comp_col, 2)
        
        # Save game
        service._repository.save(current_game)
        print(f"✓ Game saved")
        
        # Check if game over
        is_over, winner = service.check_game_over(current_game)
        if is_over:
            print(f"✓ Game over! Winner: {winner}")
            break
        
        previous_game = current_game
    
    print()


if __name__ == "__main__":
    print("=" * 70)
    print("DI LAYER TESTS")
    print("=" * 70)
    print()
    
    test_container_creation()
    test_singleton_storage()
    test_repository_has_storage()
    test_service_has_repository()
    test_full_integration()
    test_multiple_containers()
    test_getter_methods()
    test_complete_game_scenario()
    
    print("=" * 70)
    print("ALL DI LAYER TESTS PASSED! ✓")
    print("=" * 70)
