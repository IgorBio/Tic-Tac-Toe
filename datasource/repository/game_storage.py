"""Thread-safe storage for game data."""

from threading import Lock
from typing import Optional, Dict
from uuid import UUID
from datasource.model.game import Game


class GameStorage:
    """
    Thread-safe in-memory storage for games.
    
    Uses a lock to ensure thread-safe operations when multiple
    games are being played simultaneously.
    """
    
    def __init__(self):
        """Initialize the game storage with an empty dictionary and a lock."""
        self._games: Dict[UUID, Game] = {}
        self._lock = Lock()
    
    def save(self, game: Game) -> None:
        """
        Save a game to storage.
        
        Args:
            game: Game to save
        """
        with self._lock:
            self._games[game.game_id] = game
    
    def get(self, game_id: UUID) -> Optional[Game]:
        """
        Retrieve a game from storage.
        
        Args:
            game_id: UUID of the game to retrieve
            
        Returns:
            Game if found, None otherwise
        """
        with self._lock:
            return self._games.get(game_id)
    
    def delete(self, game_id: UUID) -> bool:
        """
        Delete a game from storage.
        
        Args:
            game_id: UUID of the game to delete
            
        Returns:
            True if game was deleted, False if not found
        """
        with self._lock:
            if game_id in self._games:
                del self._games[game_id]
                return True
            return False
    
    def exists(self, game_id: UUID) -> bool:
        """
        Check if a game exists in storage.
        
        Args:
            game_id: UUID of the game to check
            
        Returns:
            True if game exists, False otherwise
        """
        with self._lock:
            return game_id in self._games
    
    def clear(self) -> None:
        """Clear all games from storage."""
        with self._lock:
            self._games.clear()
    
    def count(self) -> int:
        """
        Get the number of games in storage.
        
        Returns:
            Number of games stored
        """
        with self._lock:
            return len(self._games)
