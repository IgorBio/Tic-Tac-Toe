"""Web model for current game."""

from uuid import UUID
from typing import Dict, Any
from web.model.game_board import GameBoard


class Game:
    """
    Web representation of a current game of Tic-Tac-Toe.
    
    This model is used for API requests/responses and can be easily 
    serialized to/from JSON.
    
    Contains a unique identifier and the current state of the game board.
    """
    
    def __init__(self, uuid: UUID, board: GameBoard):
        """
        Initialize a game for web layer.
        
        Args:
            uuid: Unique identifier for the game
            board: Current state of the game board
        """
        self._uuid = uuid
        self._board = board
    
    @property
    def uuid(self) -> UUID:
        """Get the game's unique identifier."""
        return self._uuid
    
    @property
    def board(self) -> GameBoard:
        """Get the game board."""
        return self._board
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to dictionary format for JSON serialization.
        
        Returns:
            Dictionary with 'uuid' and 'board' keys
        """
        return {
            'uuid': str(self._uuid),
            'board': self._board.to_dict()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Game':
        """
        Create Game from dictionary data.
        
        Args:
            data: Dictionary with 'uuid' and 'board' keys
            
        Returns:
            Game instance
            
        Raises:
            ValueError: If required fields are missing or invalid
        """
        if 'uuid' not in data:
            raise ValueError("Missing required field: 'uuid'")
        if 'board' not in data:
            raise ValueError("Missing required field: 'board'")
        
        try:
            uuid = UUID(data['uuid'])
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid UUID format: {e}")
        
        board = GameBoard.from_dict(data['board'])
        return cls(uuid, board)
    
    def __eq__(self, other) -> bool:
        """Check equality of two games."""
        if not isinstance(other, Game):
            return False
        return self._uuid == other._uuid and self._board == other._board
    
    def __repr__(self) -> str:
        """String representation of the game."""
        return f"Game(uuid={self._uuid}, board={self._board})"
