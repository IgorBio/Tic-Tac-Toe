"""Interface for game repository."""

from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID
from domain.model.game import Game


class GameRepository(ABC):
    """
    Interface for game repository.
    
    Defines methods for persisting and retrieving games.
    """
    
    @abstractmethod
    def save(self, game: Game) -> None:
        """
        Save a game.
        
        Args:
            game: Domain Game to save
        """
        pass
    
    @abstractmethod
    def get(self, game_id: UUID) -> Optional[Game]:
        """
        Retrieve a game by its UUID.
        
        Args:
            game_id: UUID of the game to retrieve
            
        Returns:
            Domain Game if found, None otherwise
        """
        pass
    
    @abstractmethod
    def delete(self, game_id: UUID) -> bool:
        """
        Delete a game by its UUID.
        
        Args:
            game_id: UUID of the game to delete
            
        Returns:
            True if game was deleted, False if not found
        """
        pass
    
    @abstractmethod
    def exists(self, game_id: UUID) -> bool:
        """
        Check if a game exists.
        
        Args:
            game_id: UUID of the game to check
            
        Returns:
            True if game exists, False otherwise
        """
        pass
