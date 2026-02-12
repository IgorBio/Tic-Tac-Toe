"""Datasource model for current game."""

from uuid import UUID
from datasource.model.game_board import GameBoard


class Game:
    """
    Datasource representation of a current game of Tic-Tac-Toe.
    
    Contains a unique identifier and the current state of the game board.
    This model is used for persistence and can be easily serialized/deserialized.
    """
    
    def __init__(self, game_id: UUID, board: GameBoard):
        """
        Initialize a game for datasource.
        
        Args:
            game_id: Unique identifier for the game
            board: Current state of the game board
        """
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
