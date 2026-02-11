"""Interface for game service."""

from abc import ABC, abstractmethod
from typing import Tuple, Optional
from uuid import UUID
from domain.model.game import Game


class GameService(ABC):
    """
    Interface for game service that handles Tic-Tac-Toe business logic.
    """
    
    @abstractmethod
    def get_next_move(self, game: Game) -> Tuple[int, int]:
        """
        Calculate the next move for the computer using the Minimax algorithm.
        
        Args:
            game: Current game state
            
        Returns:
            Tuple of (row, col) representing the best move for the computer
            
        Raises:
            ValueError: If the game is already over or the board is full
        """
        pass
    
    @abstractmethod
    def validate_game_board(self, game_id: UUID, current_board: Game, previous_board: Optional[Game]) -> bool:
        """
        Validate that the game board is legal by checking:
        1. Only one new move was made (exactly one cell changed from 0 to 1)
        2. No previous moves were modified
        3. The new move is valid (placed in an empty cell)
        
        Args:
            game_id: UUID of the game being validated
            current_board: Current game state submitted by the user
            previous_board: Previous game state (None for new games)
            
        Returns:
            True if the board is valid, False otherwise
            
        Raises:
            ValueError: If validation fails with detailed error message
        """
        pass
    
    @abstractmethod
    def check_game_over(self, game: Game) -> Tuple[bool, Optional[int]]:
        """
        Check if the game has ended.
        
        Args:
            game: Current game state
            
        Returns:
            Tuple of (is_over, winner) where:
            - is_over: True if game has ended, False otherwise
            - winner: 0 for draw, 1 for X (human), 2 for O (computer), None if game continues
        """
        pass
