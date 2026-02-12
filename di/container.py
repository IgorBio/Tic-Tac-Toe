"""Dependency Injection Container for the Tic-Tac-Toe application."""

from datasource.repository.game_storage import GameStorage
from datasource.repository.game_repository_impl import GameRepositoryImpl
from datasource.repository.game_repository import GameRepository
from domain.service.game_service_impl import GameServiceImpl
from domain.service.game_service import GameService


class Container:
    """
    Dependency Injection Container.
    
    This class manages the dependency graph for the application,
    providing singleton instances where needed and creating
    transient instances for services and repositories.
    
    Components:
    - GameStorage: Singleton - shared across entire application
    - GameRepository: Created with singleton storage
    - GameService: Created with repository
    """
    
    def __init__(self):
        """
        Initialize the container.
        
        Creates the singleton storage instance and sets up
        the dependency graph.
        """
        # Singleton: One storage instance for entire application
        self._storage = GameStorage()
        
        # Repository: Uses singleton storage
        self._repository = GameRepositoryImpl(self._storage)
        
        # Service: Uses repository
        self._service = GameServiceImpl(self._repository)
    
    @property
    def storage(self) -> GameStorage:
        """
        Get the singleton storage instance.
        
        Returns:
            GameStorage singleton instance
        """
        return self._storage
    
    @property
    def repository(self) -> GameRepository:
        """
        Get the repository instance.
        
        Returns:
            GameRepository instance configured with storage
        """
        return self._repository
    
    @property
    def service(self) -> GameService:
        """
        Get the game service instance.
        
        Returns:
            GameService instance configured with repository
        """
        return self._service
    
    def get_storage(self) -> GameStorage:
        """
        Get the singleton storage instance.
        
        Alternative getter method for storage.
        
        Returns:
            GameStorage singleton instance
        """
        return self._storage
    
    def get_repository(self) -> GameRepository:
        """
        Get the repository instance.
        
        Alternative getter method for repository.
        
        Returns:
            GameRepository instance configured with storage
        """
        return self._repository
    
    def get_service(self) -> GameService:
        """
        Get the game service instance.
        
        Alternative getter method for service.
        
        Returns:
            GameService instance configured with repository
        """
        return self._service
