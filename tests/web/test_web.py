"""Test script for web layer."""

import sys
sys.path.insert(0, '/home/claude')

from uuid import uuid4
from web.model.game_board import GameBoard as WebGameBoard
from web.model.game import Game as WebGame
from domain.model.game_board import GameBoard as DomainGameBoard
from domain.model.game import Game as DomainGame
from web.mapper.game_board_mapper import GameBoardMapper
from web.mapper.game_mapper import GameMapper


def test_web_models():
    """Test web models."""
    print("Testing Web Models...")
    
    # Test WebGameBoard
    board = WebGameBoard([[0, 0, 0], [0, 1, 0], [0, 0, 0]])
    print(f"✓ WebGameBoard created: {board}")
    
    # Test to_dict
    board_dict = board.to_dict()
    print(f"✓ Board to_dict: {board_dict}")
    
    # Test from_dict
    board_from_dict = WebGameBoard.from_dict(board_dict)
    assert board == board_from_dict, "Board from_dict failed!"
    print(f"✓ Board from_dict works")
    
    # Test WebGame
    game_id = uuid4()
    game = WebGame(game_id, board)
    print(f"✓ WebGame created: {game}")
    
    # Test to_dict
    game_dict = game.to_dict()
    print(f"✓ Game to_dict: {game_dict}")
    assert 'uuid' in game_dict
    assert 'board' in game_dict
    print(f"✓ Game dict has required fields")
    
    # Test from_dict
    game_from_dict = WebGame.from_dict(game_dict)
    assert game == game_from_dict, "Game from_dict failed!"
    print(f"✓ Game from_dict works")
    
    # Test invalid from_dict
    try:
        WebGame.from_dict({'uuid': 'invalid-uuid', 'board': [[0, 0, 0], [0, 0, 0], [0, 0, 0]]})
        print("✗ Should have raised ValueError for invalid UUID")
    except ValueError as e:
        print(f"✓ UUID validation works: {e}")
    
    try:
        WebGame.from_dict({'board': [[0, 0, 0], [0, 0, 0], [0, 0, 0]]})
        print("✗ Should have raised ValueError for missing UUID")
    except ValueError as e:
        print(f"✓ Missing UUID validation works: {e}")
    
    print()


def test_web_mappers():
    """Test web mappers."""
    print("Testing Web Mappers...")
    
    # Test GameBoard mapper
    domain_board = DomainGameBoard([[1, 0, 0], [0, 2, 0], [0, 0, 1]])
    print(f"Domain board: {domain_board}")
    
    # Domain -> Web
    web_board = GameBoardMapper.to_web(domain_board)
    print(f"✓ Mapped to web: {web_board}")
    
    # Web -> Domain
    mapped_domain_board = GameBoardMapper.to_domain(web_board)
    print(f"✓ Mapped back to domain: {mapped_domain_board}")
    
    assert domain_board == mapped_domain_board, "Board mapping failed!"
    print("✓ GameBoard mapping is correct")
    
    # Test Game mapper
    game_id = uuid4()
    domain_game = DomainGame(game_id, domain_board)
    print(f"\nDomain game: {domain_game}")
    
    # Domain -> Web
    web_game = GameMapper.to_web(domain_game)
    print(f"✓ Mapped to web: {web_game}")
    assert web_game.uuid == game_id, "UUID not preserved!"
    
    # Web -> Domain
    mapped_domain_game = GameMapper.to_domain(web_game)
    print(f"✓ Mapped back to domain: {mapped_domain_game}")
    
    assert domain_game == mapped_domain_game, "Game mapping failed!"
    print("✓ Game mapping is correct")
    
    print()


def test_json_serialization():
    """Test JSON serialization/deserialization."""
    print("Testing JSON Serialization...")
    
    import json
    
    # Create a game
    game_id = uuid4()
    board = WebGameBoard([[1, 0, 0], [0, 2, 0], [0, 0, 1]])
    game = WebGame(game_id, board)
    
    # Serialize to JSON
    game_dict = game.to_dict()
    json_str = json.dumps(game_dict)
    print(f"✓ Serialized to JSON: {json_str}")
    
    # Deserialize from JSON
    parsed_dict = json.loads(json_str)
    restored_game = WebGame.from_dict(parsed_dict)
    print(f"✓ Deserialized from JSON: {restored_game}")
    
    assert game == restored_game, "JSON round-trip failed!"
    print("✓ JSON serialization works correctly")
    
    print()


if __name__ == "__main__":
    print("=" * 70)
    print("WEB LAYER TESTS")
    print("=" * 70)
    print()
    
    test_web_models()
    test_web_mappers()
    test_json_serialization()
    
    print("=" * 70)
    print("ALL WEB LAYER TESTS PASSED! ✓")
    print("=" * 70)
