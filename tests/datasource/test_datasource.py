"""Test script for datasource layer."""

import sys
from uuid import uuid4, UUID
from threading import Thread
from time import sleep

# Add parent directory to path
sys.path.insert(0, '/home/claude')

from domain.model.game_board import GameBoard as DomainGameBoard
from domain.model.game import Game as DomainGame
from datasource.model.game_board import GameBoard as DataGameBoard
from datasource.model.game import Game as DataGame
from datasource.mapper.game_board_mapper import GameBoardMapper
from datasource.mapper.game_mapper import GameMapper
from datasource.repository.game_storage import GameStorage
from datasource.repository.game_repository_impl import GameRepositoryImpl


def test_datasource_models():
    """Test datasource models."""
    print("Testing Datasource Models...")
    
    # Test GameBoard
    board = DataGameBoard([[0, 0, 0], [0, 1, 0], [0, 0, 0]])
    print(f"✓ DataGameBoard created: {board}")
    
    # Test Game
    game_id = uuid4()
    game = DataGame(game_id, board)
    print(f"✓ DataGame created: {game}")
    print(f"  Game ID: {game.game_id}")
    print(f"  Board: {game.board}")
    
    print()


def test_mappers():
    """Test domain-datasource mappers."""
    print("Testing Mappers...")
    
    # Test GameBoard mapper
    domain_board = DomainGameBoard([[1, 0, 0], [0, 2, 0], [0, 0, 1]])
    print(f"Domain board: {domain_board}")
    
    # Domain -> Datasource
    data_board = GameBoardMapper.to_datasource(domain_board)
    print(f"✓ Mapped to datasource: {data_board}")
    
    # Datasource -> Domain
    mapped_domain_board = GameBoardMapper.to_domain(data_board)
    print(f"✓ Mapped back to domain: {mapped_domain_board}")
    
    assert domain_board == mapped_domain_board, "Board mapping failed!"
    print("✓ GameBoard mapping is correct")
    
    # Test Game mapper
    game_id = uuid4()
    domain_game = DomainGame(game_id, domain_board)
    print(f"\nDomain game: {domain_game}")
    
    # Domain -> Datasource
    data_game = GameMapper.to_datasource(domain_game)
    print(f"✓ Mapped to datasource: {data_game}")
    
    # Datasource -> Domain
    mapped_domain_game = GameMapper.to_domain(data_game)
    print(f"✓ Mapped back to domain: {mapped_domain_game}")
    
    assert domain_game == mapped_domain_game, "Game mapping failed!"
    print("✓ Game mapping is correct")
    
    print()


def test_storage():
    """Test thread-safe storage."""
    print("Testing GameStorage...")
    
    storage = GameStorage()
    
    # Create test games
    game_id_1 = uuid4()
    board_1 = DataGameBoard([[1, 0, 0], [0, 0, 0], [0, 0, 0]])
    game_1 = DataGame(game_id_1, board_1)
    
    game_id_2 = uuid4()
    board_2 = DataGameBoard([[0, 0, 0], [0, 2, 0], [0, 0, 0]])
    game_2 = DataGame(game_id_2, board_2)
    
    # Test save
    storage.save(game_1)
    print(f"✓ Saved game 1: {game_id_1}")
    
    storage.save(game_2)
    print(f"✓ Saved game 2: {game_id_2}")
    
    # Test count
    assert storage.count() == 2, "Storage count incorrect!"
    print(f"✓ Storage count: {storage.count()}")
    
    # Test exists
    assert storage.exists(game_id_1), "Game 1 should exist!"
    assert storage.exists(game_id_2), "Game 2 should exist!"
    print("✓ Exists check works")
    
    # Test get
    retrieved_1 = storage.get(game_id_1)
    assert retrieved_1 is not None, "Failed to retrieve game 1!"
    assert retrieved_1.game_id == game_id_1, "Retrieved wrong game!"
    print(f"✓ Retrieved game 1: {retrieved_1}")
    
    # Test get non-existent
    non_existent = storage.get(uuid4())
    assert non_existent is None, "Should return None for non-existent game!"
    print("✓ Returns None for non-existent game")
    
    # Test delete
    deleted = storage.delete(game_id_1)
    assert deleted, "Failed to delete game 1!"
    assert not storage.exists(game_id_1), "Game 1 should not exist after deletion!"
    assert storage.count() == 1, "Count should be 1 after deletion!"
    print("✓ Delete works")
    
    # Test clear
    storage.clear()
    assert storage.count() == 0, "Storage should be empty after clear!"
    print("✓ Clear works")
    
    print()


def test_repository():
    """Test repository implementation."""
    print("Testing GameRepository...")
    
    storage = GameStorage()
    repository = GameRepositoryImpl(storage)
    
    # Create test domain games
    game_id_1 = uuid4()
    board_1 = DomainGameBoard([[1, 0, 0], [0, 0, 0], [0, 0, 0]])
    domain_game_1 = DomainGame(game_id_1, board_1)
    
    game_id_2 = uuid4()
    board_2 = DomainGameBoard([[0, 0, 0], [0, 2, 0], [0, 0, 0]])
    domain_game_2 = DomainGame(game_id_2, board_2)
    
    # Test save
    repository.save(domain_game_1)
    print(f"✓ Saved domain game 1 via repository: {game_id_1}")
    
    repository.save(domain_game_2)
    print(f"✓ Saved domain game 2 via repository: {game_id_2}")
    
    # Test exists
    assert repository.exists(game_id_1), "Game 1 should exist!"
    assert repository.exists(game_id_2), "Game 2 should exist!"
    print("✓ Exists check works")
    
    # Test get
    retrieved_1 = repository.get(game_id_1)
    assert retrieved_1 is not None, "Failed to retrieve game 1!"
    assert isinstance(retrieved_1, DomainGame), "Should return domain game!"
    assert retrieved_1.game_id == game_id_1, "Retrieved wrong game!"
    assert retrieved_1.board == board_1, "Board doesn't match!"
    print(f"✓ Retrieved domain game 1: {retrieved_1}")
    
    # Test get non-existent
    non_existent = repository.get(uuid4())
    assert non_existent is None, "Should return None for non-existent game!"
    print("✓ Returns None for non-existent game")
    
    # Test delete
    deleted = repository.delete(game_id_1)
    assert deleted, "Failed to delete game 1!"
    assert not repository.exists(game_id_1), "Game 1 should not exist after deletion!"
    print("✓ Delete works")
    
    print()


def test_thread_safety():
    """Test thread-safe concurrent access."""
    print("Testing Thread Safety...")
    
    storage = GameStorage()
    repository = GameRepositoryImpl(storage)
    
    results = []
    
    def save_games(thread_id: int, count: int):
        """Save multiple games in a thread."""
        for i in range(count):
            game_id = uuid4()
            board = DomainGameBoard([[thread_id % 3, i % 3, 0], [0, 0, 0], [0, 0, 0]])
            game = DomainGame(game_id, board)
            repository.save(game)
            results.append((thread_id, game_id))
    
    # Create multiple threads
    threads = []
    games_per_thread = 5
    num_threads = 4
    
    print(f"Starting {num_threads} threads, each saving {games_per_thread} games...")
    
    for i in range(num_threads):
        thread = Thread(target=save_games, args=(i, games_per_thread))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    # Verify results
    total_games = num_threads * games_per_thread
    assert len(results) == total_games, f"Expected {total_games} results, got {len(results)}"
    print(f"✓ All {total_games} games saved successfully")
    
    # Verify all games can be retrieved
    for thread_id, game_id in results:
        game = repository.get(game_id)
        assert game is not None, f"Failed to retrieve game {game_id}"
        assert game.game_id == game_id, "Game ID mismatch!"
    
    print(f"✓ All {total_games} games retrieved successfully")
    print("✓ Thread safety verified")
    
    print()


def test_update_scenario():
    """Test a realistic game update scenario."""
    print("Testing Realistic Game Update Scenario...")
    
    storage = GameStorage()
    repository = GameRepositoryImpl(storage)
    
    # Start a new game
    game_id = uuid4()
    print(f"New game started: {game_id}")
    
    # Human makes first move
    board = DomainGameBoard([[0, 0, 0], [0, 1, 0], [0, 0, 0]])
    game = DomainGame(game_id, board)
    repository.save(game)
    print(f"✓ Human's first move saved: center")
    print(f"  Board:\n  {board.board[0]}\n  {board.board[1]}\n  {board.board[2]}")
    
    # Computer makes move
    board_2 = DomainGameBoard([[2, 0, 0], [0, 1, 0], [0, 0, 0]])
    game_2 = DomainGame(game_id, board_2)
    repository.save(game_2)
    print(f"✓ Computer's move saved: top-left corner")
    print(f"  Board:\n  {board_2.board[0]}\n  {board_2.board[1]}\n  {board_2.board[2]}")
    
    # Retrieve and verify
    retrieved = repository.get(game_id)
    assert retrieved is not None, "Failed to retrieve game!"
    assert retrieved.board == board_2, "Board doesn't match latest state!"
    print(f"✓ Game state updated correctly")
    
    print()


if __name__ == "__main__":
    print("=" * 70)
    print("DATASOURCE LAYER TESTS")
    print("=" * 70)
    print()
    
    test_datasource_models()
    test_mappers()
    test_storage()
    test_repository()
    test_thread_safety()
    test_update_scenario()
    
    print("=" * 70)
    print("ALL DATASOURCE LAYER TESTS PASSED! ✓")
    print("=" * 70)
