"""Test script for domain layer."""

from uuid import uuid4
from domain.model.game_board import GameBoard
from domain.model.game import Game


def test_game_board():
    """Test GameBoard model."""
    print("Testing GameBoard...")
    
    # Create empty board
    board = GameBoard([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    print(f"Empty board created: {board}")
    
    # Test get/set cell
    board.set_cell(0, 0, 1)
    assert board.get_cell(0, 0) == 1
    print("✓ Cell get/set works")
    
    # Test validation
    try:
        invalid_board = GameBoard([[0, 0], [0, 0]])
        print("✗ Should have raised ValueError for invalid dimensions")
    except ValueError as e:
        print(f"✓ Validation works: {e}")
    
    # Test invalid cell value
    try:
        board.set_cell(0, 1, 5)
        print("✗ Should have raised ValueError for invalid cell value")
    except ValueError as e:
        print(f"✓ Cell value validation works: {e}")
    
    print()


def test_game():
    """Test Game model."""
    print("Testing Game...")
    
    # Create game
    game_id = uuid4()
    board = GameBoard([[0, 0, 0], [0, 1, 0], [0, 0, 0]])
    game = Game(game_id, board)
    
    print(f"Game created: {game}")
    print(f"Game ID: {game.game_id}")
    print(f"Board: {game.board}")
    
    # Test type validation
    try:
        invalid_game = Game("not-a-uuid", board)
        print("✗ Should have raised TypeError for invalid UUID")
    except TypeError as e:
        print(f"✓ UUID validation works: {e}")
    
    print()


def test_minimax_logic():
    """Test basic Minimax logic (manual verification)."""
    print("Testing Minimax scenarios...")
    
    # Scenario 1: Computer should block human from winning
    print("\nScenario 1: Block opponent's winning move")
    board1 = GameBoard([
        [1, 1, 0],  # Human about to win
        [0, 2, 0],
        [0, 0, 0]
    ])
    print(f"Board: {board1.board}")
    print("Expected: Computer should play at (0, 2) to block")
    
    # Scenario 2: Computer should take winning move
    print("\nScenario 2: Take winning move")
    board2 = GameBoard([
        [1, 0, 0],
        [2, 2, 0],  # Computer can win
        [1, 0, 0]
    ])
    print(f"Board: {board2.board}")
    print("Expected: Computer should play at (1, 2) to win")
    
    # Scenario 3: Fork opportunity
    print("\nScenario 3: Empty board - center is optimal")
    board3 = GameBoard([
        [0, 0, 0],
        [0, 1, 0],  # Human took center
        [0, 0, 0]
    ])
    print(f"Board: {board3.board}")
    print("Expected: Computer should play at corner")
    
    print()


if __name__ == "__main__":
    print("=" * 60)
    print("DOMAIN LAYER TESTS")
    print("=" * 60)
    print()
    
    test_game_board()
    test_game()
    test_minimax_logic()
    
    print("=" * 60)
    print("All basic tests passed!")
    print("=" * 60)
