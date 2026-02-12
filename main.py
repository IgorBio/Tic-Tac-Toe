"""Main entry point for the Tic-Tac-Toe application."""

import sys
sys.path.insert(0, '.')

from di.container import Container
from web.module.app import run_app


def main():
    """
    Initialize dependencies and start the Flask application.
    
    Uses the DI container to manage all dependencies.
    """
    # Create DI container
    container = Container()
    
    # Get game service (with all dependencies injected)
    game_service = container.service
    
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
