"""Flask application module."""

from flask import Flask
from web.route.game_controller import GameController
from domain.service.game_service import GameService


def create_app(game_service: GameService) -> Flask:
    """
    Create and configure Flask application.
    
    Args:
        game_service: Domain service for game business logic
        
    Returns:
        Configured Flask application
    """
    app = Flask(__name__)
    
    # Configure app
    app.config['JSON_SORT_KEYS'] = False
    
    # Register game controller
    game_controller = GameController(game_service)
    app.register_blueprint(game_controller.blueprint)
    
    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        """Health check endpoint."""
        return {'status': 'ok'}, 200
    
    return app


def run_app(game_service: GameService, host: str = '0.0.0.0', port: int = 5000, debug: bool = False):
    """
    Create and run Flask application.
    
    Args:
        game_service: Domain service for game business logic
        host: Host to bind to (default: 0.0.0.0)
        port: Port to bind to (default: 5000)
        debug: Enable debug mode (default: False)
    """
    app = create_app(game_service)
    app.run(host=host, port=port, debug=debug)
