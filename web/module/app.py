"""Flask application module."""

from pathlib import Path
from flask import Flask, render_template
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
    project_root = Path(__file__).resolve().parents[2]
    app = Flask(
        __name__,
        template_folder=str(project_root / 'templates'),
        static_folder=str(project_root / 'static'),
    )

    # Configure app
    app.config['JSON_SORT_KEYS'] = False

    # Register game controller
    game_controller = GameController(game_service)
    app.register_blueprint(game_controller.blueprint)

    @app.route('/', methods=['GET'])
    def index():
        """Serve minimal Tic-Tac-Toe web client."""
        return render_template('index.html')

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
