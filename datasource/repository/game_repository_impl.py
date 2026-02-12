"""Implementation of game repository."""

from typing import Optional
from uuid import UUID
from domain.model.game import Game as DomainGame
from datasource.repository.game_repository import GameRepository
from datasource.repository.game_storage import GameStorage
from datasource.mapper.game_mapper import GameMapper


class GameRepositoryImpl(GameRepository):
    """
    Implementation of GameRepository interface.
    
    Uses GameStorage for persistence and GameMapper for domain-datasource conversion.
    """
    
    def __init__(self, storage: GameStorage):
        """
        Initialize repository with storage.
        
        Args:
            storage: GameStorage instance for data persistence
        """
        self._storage = storage
    
    def save(self, game: DomainGame) -> None:
        """
        Save a domain game to storage.
        
        Args:
            game: Domain Game to save
        """
        data_game = GameMapper.to_datasource(game)
        self._storage.save(data_game)
    
    def get(self, game_id: UUID) -> Optional[DomainGame]:
        """
        Retrieve a domain game by its UUID.
        
        Args:
            game_id: UUID of the game to retrieve
            
        Returns:
            Domain Game if found, None otherwise
        """
        data_game = self._storage.get(game_id)
        if data_game is None:
            return None
        return GameMapper.to_domain(data_game)
    
    def delete(self, game_id: UUID) -> bool:
        """
        Delete a game by its UUID.
        
        Args:
            game_id: UUID of the game to delete
            
        Returns:
            True if game was deleted, False if not found
        """
        return self._storage.delete(game_id)
    
    def exists(self, game_id: UUID) -> bool:
        """
        Check if a game exists.
        
        Args:
            game_id: UUID of the game to check
            
        Returns:
            True if game exists, False otherwise
        """
        return self._storage.exists(game_id)
