"""Main entry point for the Tic-Tac-Toe application."""

import sys
sys.path.insert(0, '.')

from datasource.repository.game_storage import GameStorage
from datasource.repository.game_repository_impl import GameRepositoryImpl
from domain.service.game_service_impl import GameServiceImpl
from web.module.app import run_app


def main():
    """
    Initialize dependencies and start the Flask application.
    
    This is a temporary implementation until the DI layer is complete.
    """
    # Create singleton storage
    storage = GameStorage()
    
    # Create repository with storage
    repository = GameRepositoryImpl(storage)
    
    # Create service with repository
    game_service = GameServiceImpl(repository)
    
    # Run Flask app
    print("Starting Tic-Tac-Toe API server...")
    print("Server running at http://localhost:5000")
    print("\nEndpoints:")
    print("  POST /game/{uuid} - Submit move and get computer response")
    print("  GET  /health      - Health check")
    print("\nPress Ctrl+C to stop")
    
    run_app(game_service, host='0.0.0.0', port=5000, debug=True)


if __name__ == '__main__':
    main()
