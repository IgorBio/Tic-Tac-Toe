"""Domain model for game board."""

from typing import List


class GameBoard:
    """
    Represents a Tic-Tac-Toe game board as an integer matrix.
    
    Cell values:
    - 0: Empty cell
    - 1: X (human player)
    - 2: O (computer player)
    """
    
    def __init__(self, board: List[List[int]]):
        """
        Initialize game board.
        
        Args:
            board: 3x3 integer matrix representing the game state
            
        Raises:
            ValueError: If board dimensions are invalid or values are out of range
        """
        if len(board) != 3:
            raise ValueError("Board must have exactly 3 rows")
        
        for row in board:
            if len(row) != 3:
                raise ValueError("Each row must have exactly 3 columns")
            for cell in row:
                if cell not in [0, 1, 2]:
                    raise ValueError("Cell values must be 0 (empty), 1 (X), or 2 (O)")
        
        self._board = [row[:] for row in board]  # Deep copy to prevent external modifications
    
    @property
    def board(self) -> List[List[int]]:
        """Get a copy of the board matrix."""
        return [row[:] for row in self._board]
    
    def get_cell(self, row: int, col: int) -> int:
        """
        Get value of a specific cell.
        
        Args:
            row: Row index (0-2)
            col: Column index (0-2)
            
        Returns:
            Cell value (0, 1, or 2)
        """
        return self._board[row][col]
    
    def set_cell(self, row: int, col: int, value: int) -> None:
        """
        Set value of a specific cell.
        
        Args:
            row: Row index (0-2)
            col: Column index (0-2)
            value: Cell value (0, 1, or 2)
        """
        if value not in [0, 1, 2]:
            raise ValueError("Cell value must be 0, 1, or 2")
        self._board[row][col] = value
    
    def __eq__(self, other) -> bool:
        """Check equality of two game boards."""
        if not isinstance(other, GameBoard):
            return False
        return self._board == other._board
    
    def __repr__(self) -> str:
        """String representation of the game board."""
        return f"GameBoard({self._board})"
