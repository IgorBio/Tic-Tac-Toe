"""Mapper between domain and web GameBoard models."""

from domain.model.game_board import GameBoard as DomainGameBoard
from web.model.game_board import GameBoard as WebGameBoard


class GameBoardMapper:
    """
    Maps between domain and web GameBoard representations.
    
    This mapper handles the conversion between the domain layer's GameBoard
    and the web layer's GameBoard.
    """
    
    @staticmethod
    def to_web(domain_board: DomainGameBoard) -> WebGameBoard:
        """
        Convert domain GameBoard to web GameBoard.
        
        Args:
            domain_board: Domain layer GameBoard
            
        Returns:
            Web layer GameBoard
        """
        return WebGameBoard(domain_board.board)
    
    @staticmethod
    def to_domain(web_board: WebGameBoard) -> DomainGameBoard:
        """
        Convert web GameBoard to domain GameBoard.
        
        Args:
            web_board: Web layer GameBoard
            
        Returns:
            Domain layer GameBoard
        """
        return DomainGameBoard(web_board.board)
