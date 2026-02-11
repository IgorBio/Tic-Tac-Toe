"""Implementation of game service with Minimax algorithm."""

from typing import Tuple, Optional, List
from uuid import UUID
from domain.model.game import Game
from domain.model.game_board import GameBoard
from domain.service.game_service import GameService


class GameServiceImpl(GameService):
    """
    Implementation of GameService interface.
    
    Provides game logic including Minimax algorithm for AI moves,
    board validation, and game state checking.
    """
    
    def __init__(self, repository):
        """
        Initialize game service with repository dependency.
        
        Args:
            repository: Repository for game data access
        """
        self._repository = repository
    
    def get_next_move(self, game: Game) -> Tuple[int, int]:
        """
        Calculate the next move using Minimax algorithm.
        
        The computer plays as O (player 2) and tries to maximize its score.
        
        Args:
            game: Current game state
            
        Returns:
            Tuple of (row, col) for the best move
            
        Raises:
            ValueError: If game is over or board is full
        """
        is_over, _ = self.check_game_over(game)
        if is_over:
            raise ValueError("Game is already over")
        
        board_matrix = game.board.board
        best_score = float('-inf')
        best_move = None
        
        # Try all possible moves
        for row in range(3):
            for col in range(3):
                if board_matrix[row][col] == 0:
                    # Make move
                    board_matrix[row][col] = 2  # Computer is player 2 (O)
                    score = self._minimax(board_matrix, 0, False)
                    # Undo move
                    board_matrix[row][col] = 0
                    
                    if score > best_score:
                        best_score = score
                        best_move = (row, col)
        
        if best_move is None:
            raise ValueError("No valid moves available")
        
        return best_move
    
    def _minimax(self, board: List[List[int]], depth: int, is_maximizing: bool) -> int:
        """
        Minimax algorithm implementation.
        
        Args:
            board: Current board state
            depth: Current depth in game tree
            is_maximizing: True if maximizing player (computer), False if minimizing (human)
            
        Returns:
            Score of the position
        """
        # Check terminal states
        winner = self._check_winner(board)
        if winner == 2:  # Computer wins
            return 10 - depth
        elif winner == 1:  # Human wins
            return depth - 10
        elif self._is_board_full(board):  # Draw
            return 0
        
        if is_maximizing:
            # Computer's turn (maximize)
            max_score = float('-inf')
            for row in range(3):
                for col in range(3):
                    if board[row][col] == 0:
                        board[row][col] = 2
                        score = self._minimax(board, depth + 1, False)
                        board[row][col] = 0
                        max_score = max(max_score, score)
            return max_score
        else:
            # Human's turn (minimize)
            min_score = float('inf')
            for row in range(3):
                for col in range(3):
                    if board[row][col] == 0:
                        board[row][col] = 1
                        score = self._minimax(board, depth + 1, True)
                        board[row][col] = 0
                        min_score = min(min_score, score)
            return min_score
    
    def validate_game_board(self, game_id: UUID, current_game: Game, previous_game: Optional[Game]) -> bool:
        """
        Validate that the game board follows the rules.
        
        Checks:
        1. Exactly one new move was made by the human player
        2. No previous moves were modified
        3. The new move was placed in an empty cell
        
        Args:
            game_id: UUID of the game
            current_game: Current game state
            previous_game: Previous game state (None for new games)
            
        Returns:
            True if valid
            
        Raises:
            ValueError: If validation fails
        """
        current_board = current_game.board.board
        
        # For new games, validate that at most one cell is filled
        if previous_game is None:
            filled_cells = sum(1 for row in current_board for cell in row if cell != 0)
            if filled_cells == 0:
                raise ValueError("No move made")
            if filled_cells > 1:
                raise ValueError("New game can only have one move")
            
            # Check that the move is by human player (1)
            human_moves = sum(1 for row in current_board for cell in row if cell == 1)
            computer_moves = sum(1 for row in current_board for cell in row if cell == 2)
            
            if human_moves != 1:
                raise ValueError("First move must be by human player (value 1)")
            if computer_moves != 0:
                raise ValueError("Computer hasn't moved yet in new game")
            
            return True
        
        # For existing games, check that exactly one cell changed
        previous_board = previous_game.board.board
        changes = []
        
        for row in range(3):
            for col in range(3):
                prev_val = previous_board[row][col]
                curr_val = current_board[row][col]
                
                if prev_val != curr_val:
                    if prev_val != 0:
                        raise ValueError(
                            f"Previous move at ({row}, {col}) was modified. "
                            f"Previous moves cannot be changed."
                        )
                    changes.append((row, col, curr_val))
        
        if len(changes) == 0:
            raise ValueError("No new move detected")
        
        if len(changes) > 1:
            raise ValueError(
                f"Multiple cells changed: {len(changes)}. Only one move allowed per turn."
            )
        
        # Validate that the new move is by the human player
        _, _, new_value = changes[0]
        if new_value != 1:
            raise ValueError("New move must be by human player (value 1)")
        
        return True
    
    def check_game_over(self, game: Game) -> Tuple[bool, Optional[int]]:
        """
        Check if the game has ended.
        
        Args:
            game: Current game state
            
        Returns:
            (is_over, winner) where winner is 0 for draw, 1 for X, 2 for O, None if continuing
        """
        board = game.board.board
        winner = self._check_winner(board)
        
        if winner is not None:
            return (True, winner)
        
        if self._is_board_full(board):
            return (True, 0)  # Draw
        
        return (False, None)  # Game continues
    
    def _check_winner(self, board: List[List[int]]) -> Optional[int]:
        """
        Check if there is a winner on the board.
        
        Args:
            board: Current board state
            
        Returns:
            1 if X wins, 2 if O wins, None if no winner
        """
        # Check rows
        for row in range(3):
            if board[row][0] == board[row][1] == board[row][2] != 0:
                return board[row][0]
        
        # Check columns
        for col in range(3):
            if board[0][col] == board[1][col] == board[2][col] != 0:
                return board[0][col]
        
        # Check diagonals
        if board[0][0] == board[1][1] == board[2][2] != 0:
            return board[0][0]
        
        if board[0][2] == board[1][1] == board[2][0] != 0:
            return board[0][2]
        
        return None
    
    def _is_board_full(self, board: List[List[int]]) -> bool:
        """
        Check if the board is full.
        
        Args:
            board: Current board state
            
        Returns:
            True if no empty cells remain
        """
        return all(board[row][col] != 0 for row in range(3) for col in range(3))
