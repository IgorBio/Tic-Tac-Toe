"""Web model for game board."""

from typing import List


class GameBoard:
    """
    Web representation of a Tic-Tac-Toe game board.
    
    This model is used for API requests/responses and can be easily 
    serialized to/from JSON.
    
    Cell values:
    - 0: Empty cell
    - 1: X (human player)
    - 2: O (computer player)
    """
    
    def __init__(self, board: List[List[int]]):
        """
        Initialize game board for web layer.
        
        Args:
            board: 3x3 integer matrix representing the game state
        """
        self._board = [row[:] for row in board]  # Deep copy
    
    @property
    def board(self) -> List[List[int]]:
        """Get a copy of the board matrix."""
        return [row[:] for row in self._board]
    
    def to_dict(self) -> List[List[int]]:
        """
        Convert to dictionary format for JSON serialization.
        
        Returns:
            Board as nested list
        """
        return self.board
    
    @classmethod
    def from_dict(cls, data: List[List[int]]) -> 'GameBoard':
        """
        Create GameBoard from dictionary data.
        
        Args:
            data: Board as nested list
            
        Returns:
            GameBoard instance
        """
        return cls(data)
    
    def __eq__(self, other) -> bool:
        """Check equality of two game boards."""
        if not isinstance(other, GameBoard):
            return False
        return self._board == other._board
    
    def __repr__(self) -> str:
        """String representation of the game board."""
        return f"GameBoard({self._board})"
