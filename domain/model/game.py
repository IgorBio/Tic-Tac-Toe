"""Domain model for current game."""

from uuid import UUID
from domain.model.game_board import GameBoard


class Game:
    """
    Represents a current game of Tic-Tac-Toe.
    
    Contains a unique identifier and the current state of the game board.
    """
    
    def __init__(self, game_id: UUID, board: GameBoard):
        """
        Initialize a game.
        
        Args:
            game_id: Unique identifier for the game
            board: Current state of the game board
        """
        if not isinstance(game_id, UUID):
            raise TypeError("game_id must be a UUID instance")
        if not isinstance(board, GameBoard):
            raise TypeError("board must be a GameBoard instance")
        
        self._game_id = game_id
        self._board = board
    
    @property
    def game_id(self) -> UUID:
        """Get the game's unique identifier."""
        return self._game_id
    
    @property
    def board(self) -> GameBoard:
        """Get the game board."""
        return self._board
    
    def __eq__(self, other) -> bool:
        """Check equality of two games."""
        if not isinstance(other, Game):
            return False
        return self._game_id == other._game_id and self._board == other._board
    
    def __repr__(self) -> str:
        """String representation of the game."""
        return f"Game(game_id={self._game_id}, board={self._board})"
