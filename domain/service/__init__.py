"""Domain services package."""

from domain.service.game_service import GameService
from domain.service.game_service_impl import GameServiceImpl

__all__ = ['GameService', 'GameServiceImpl']
