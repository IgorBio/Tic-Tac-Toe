"""Mapper between domain and datasource GameBoard models."""

from domain.model.game_board import GameBoard as DomainGameBoard
from datasource.model.game_board import GameBoard as DataGameBoard


class GameBoardMapper:
    """
    Maps between domain and datasource GameBoard representations.
    
    This mapper handles the conversion between the domain layer's GameBoard
    and the datasource layer's GameBoard.
    """
    
    @staticmethod
    def to_datasource(domain_board: DomainGameBoard) -> DataGameBoard:
        """
        Convert domain GameBoard to datasource GameBoard.
        
        Args:
            domain_board: Domain layer GameBoard
            
        Returns:
            Datasource layer GameBoard
        """
        return DataGameBoard(domain_board.board)
    
    @staticmethod
    def to_domain(data_board: DataGameBoard) -> DomainGameBoard:
        """
        Convert datasource GameBoard to domain GameBoard.
        
        Args:
            data_board: Datasource layer GameBoard
            
        Returns:
            Domain layer GameBoard
        """
        return DomainGameBoard(data_board.board)
