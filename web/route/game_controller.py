"""Game controller for REST API endpoints."""

from flask import Blueprint, request, jsonify
from uuid import UUID
from typing import Dict, Any

from web.model.game import Game as WebGame
from web.mapper.game_mapper import GameMapper
from domain.service.game_service import GameService


class GameController:
    """
    Controller for game-related HTTP endpoints.
    
    Handles requests for creating and updating Tic-Tac-Toe games.
    """
    
    def __init__(self, game_service: GameService):
        """
        Initialize game controller.
        
        Args:
            game_service: Domain service for game business logic
        """
        self._game_service = game_service
        self._blueprint = Blueprint('game', __name__)
        self._register_routes()
    
    def _register_routes(self):
        """Register all routes for this controller."""
        self._blueprint.add_url_rule(
            '/game/<uuid:game_id>',
            'update_game',
            self._update_game,
            methods=['POST']
        )
    
    @property
    def blueprint(self) -> Blueprint:
        """Get the Flask blueprint for this controller."""
        return self._blueprint
    
    def _update_game(self, game_id: UUID) -> tuple[Dict[str, Any], int]:
        """
        Handle POST /game/{uuid} endpoint.
        
        Receives a game with the human player's move and returns
        the game with the computer's response move.
        
        Args:
            game_id: UUID of the game from URL path
            
        Returns:
            Tuple of (response_dict, status_code)
        """
        try:
            # Parse request JSON
            data = request.get_json()
            if data is None:
                return {
                    'error': 'Invalid request',
                    'message': 'Request body must be valid JSON'
                }, 400
            
            # Validate that UUID in body matches URL
            if 'uuid' in data:
                try:
                    body_uuid = UUID(data['uuid'])
                    if body_uuid != game_id:
                        return {
                            'error': 'UUID mismatch',
                            'message': f'UUID in URL ({game_id}) does not match UUID in body ({body_uuid})'
                        }, 400
                except (ValueError, TypeError):
                    return {
                        'error': 'Invalid UUID',
                        'message': 'UUID in request body is not valid'
                    }, 400
            else:
                # If UUID not in body, add it
                data['uuid'] = str(game_id)
            
            # Parse web model
            try:
                web_game = WebGame.from_dict(data)
            except ValueError as e:
                return {
                    'error': 'Invalid request',
                    'message': str(e)
                }, 400
            
            # Convert to domain model
            current_domain_game = GameMapper.to_domain(web_game)
            
            # Get previous game state (if exists)
            previous_domain_game = self._game_service._repository.get(game_id)
            
            # Validate the game board
            try:
                self._game_service.validate_game_board(
                    game_id, 
                    current_domain_game, 
                    previous_domain_game
                )
            except ValueError as e:
                return {
                    'error': 'Invalid move',
                    'message': str(e)
                }, 400
            
            # Check if game is already over before human's move
            if previous_domain_game is not None:
                is_over, winner = self._game_service.check_game_over(previous_domain_game)
                if is_over:
                    return {
                        'error': 'Game already over',
                        'message': self._format_game_over_message(winner)
                    }, 400
            
            # Save the current state (with human's move)
            self._game_service._repository.save(current_domain_game)
            
            # Check if game is over after human's move
            is_over, winner = self._game_service.check_game_over(current_domain_game)
            if is_over:
                # Game ended with human's move, return current state
                response_web_game = GameMapper.to_web(current_domain_game)
                response = response_web_game.to_dict()
                response['game_over'] = True
                response['winner'] = self._format_game_over_message(winner)
                return response, 200
            
            # Get computer's move
            try:
                row, col = self._game_service.get_next_move(current_domain_game)
            except ValueError as e:
                return {
                    'error': 'Cannot compute move',
                    'message': str(e)
                }, 500
            
            # Apply computer's move
            current_domain_game.board.set_cell(row, col, 2)
            
            # Save updated state
            self._game_service._repository.save(current_domain_game)
            
            # Check if game is over after computer's move
            is_over, winner = self._game_service.check_game_over(current_domain_game)
            
            # Convert back to web model and return
            response_web_game = GameMapper.to_web(current_domain_game)
            response = response_web_game.to_dict()
            
            if is_over:
                response['game_over'] = True
                response['winner'] = self._format_game_over_message(winner)
            
            return response, 200
            
        except Exception as e:
            # Catch unexpected errors
            return {
                'error': 'Internal server error',
                'message': str(e)
            }, 500
    
    def _format_game_over_message(self, winner: int) -> str:
        """
        Format game over message based on winner.
        
        Args:
            winner: 0 for draw, 1 for human, 2 for computer
            
        Returns:
            Formatted message
        """
        if winner == 0:
            return 'Draw'
        elif winner == 1:
            return 'Human wins (X)'
        elif winner == 2:
            return 'Computer wins (O)'
        else:
            return 'Unknown'
