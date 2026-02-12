"""Mapper between domain and datasource Game models."""

from domain.model.game import Game as DomainGame
from datasource.model.game import Game as DataGame
from datasource.mapper.game_board_mapper import GameBoardMapper


class GameMapper:
    """
    Maps between domain and datasource Game representations.
    
    This mapper handles the conversion between the domain layer's Game
    and the datasource layer's Game.
    """
    
    @staticmethod
    def to_datasource(domain_game: DomainGame) -> DataGame:
        """
        Convert domain Game to datasource Game.
        
        Args:
            domain_game: Domain layer Game
            
        Returns:
            Datasource layer Game
        """
        data_board = GameBoardMapper.to_datasource(domain_game.board)
        return DataGame(domain_game.game_id, data_board)
    
    @staticmethod
    def to_domain(data_game: DataGame) -> DomainGame:
        """
        Convert datasource Game to domain Game.
        
        Args:
            data_game: Datasource layer Game
            
        Returns:
            Domain layer Game
        """
        domain_board = GameBoardMapper.to_domain(data_game.board)
        return DomainGame(data_game.game_id, domain_board)
