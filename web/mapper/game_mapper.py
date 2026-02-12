"""Mapper between domain and web Game models."""

from domain.model.game import Game as DomainGame
from web.model.game import Game as WebGame
from web.mapper.game_board_mapper import GameBoardMapper


class GameMapper:
    """
    Maps between domain and web Game representations.
    
    This mapper handles the conversion between the domain layer's Game
    and the web layer's Game.
    """
    
    @staticmethod
    def to_web(domain_game: DomainGame) -> WebGame:
        """
        Convert domain Game to web Game.
        
        Args:
            domain_game: Domain layer Game
            
        Returns:
            Web layer Game
        """
        web_board = GameBoardMapper.to_web(domain_game.board)
        return WebGame(domain_game.game_id, web_board)
    
    @staticmethod
    def to_domain(web_game: WebGame) -> DomainGame:
        """
        Convert web Game to domain Game.
        
        Args:
            web_game: Web layer Game
            
        Returns:
            Domain layer Game
        """
        domain_board = GameBoardMapper.to_domain(web_game.board)
        return DomainGame(web_game.uuid, domain_board)
