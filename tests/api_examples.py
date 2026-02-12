"""
API Usage Examples for Tic-Tac-Toe Game

This file demonstrates how to interact with the Tic-Tac-Toe API
using Python requests library.
"""

import requests
from uuid import uuid4
import json


# API base URL
BASE_URL = "http://localhost:5000"


def print_board(board):
    """Pretty print the game board."""
    symbols = {0: '.', 1: 'X', 2: 'O'}
    print("\nCurrent Board:")
    for row in board:
        print(' '.join(symbols[cell] for cell in row))
    print()


def example_1_new_game():
    """Example 1: Start a new game."""
    print("=" * 60)
    print("EXAMPLE 1: Start a New Game")
    print("=" * 60)
    
    game_id = uuid4()
    print(f"Game ID: {game_id}\n")
    
    # Human plays center
    request_data = {
        "uuid": str(game_id),
        "board": [
            [0, 0, 0],
            [0, 1, 0],
            [0, 0, 0]
        ]
    }
    
    print("Human plays center (X):")
    print_board(request_data['board'])
    
    response = requests.post(
        f"{BASE_URL}/game/{game_id}",
        json=request_data
    )
    
    print(f"Response Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("Computer's response:")
        print_board(data['board'])
        
        if 'game_over' in data:
            print(f"Game Over! {data['winner']}")
    else:
        print(f"Error: {response.json()}")
    
    print()


def example_2_continue_game():
    """Example 2: Continue an existing game."""
    print("=" * 60)
    print("EXAMPLE 2: Continue Existing Game")
    print("=" * 60)
    
    game_id = uuid4()
    
    # Move 1: Human plays center
    response = requests.post(
        f"{BASE_URL}/game/{game_id}",
        json={
            "uuid": str(game_id),
            "board": [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
        }
    )
    data = response.json()
    print("After Move 1:")
    print_board(data['board'])
    
    # Move 2: Human plays bottom-left
    response = requests.post(
        f"{BASE_URL}/game/{game_id}",
        json={
            "uuid": str(game_id),
            "board": [
                [data['board'][0][0], data['board'][0][1], data['board'][0][2]],
                [data['board'][1][0], data['board'][1][1], data['board'][1][2]],
                [1, data['board'][2][1], data['board'][2][2]]
            ]
        }
    )
    data = response.json()
    print("After Move 2:")
    print_board(data['board'])
    
    if 'game_over' in data:
        print(f"Game Over! {data['winner']}")
    
    print()


def example_3_invalid_move_multiple_cells():
    """Example 3: Invalid move - multiple cells changed."""
    print("=" * 60)
    print("EXAMPLE 3: Invalid Move - Multiple Cells")
    print("=" * 60)
    
    game_id = uuid4()
    
    # Try to change multiple cells at once
    request_data = {
        "uuid": str(game_id),
        "board": [
            [1, 1, 0],  # Two moves at once!
            [0, 0, 0],
            [0, 0, 0]
        ]
    }
    
    print("Attempting to play two moves at once:")
    print_board(request_data['board'])
    
    response = requests.post(
        f"{BASE_URL}/game/{game_id}",
        json=request_data
    )
    
    print(f"Response Status: {response.status_code}")
    print(f"Error: {response.json()}")
    print()


def example_4_invalid_move_modify_previous():
    """Example 4: Invalid move - modifying previous moves."""
    print("=" * 60)
    print("EXAMPLE 4: Invalid Move - Modify Previous Move")
    print("=" * 60)
    
    game_id = uuid4()
    
    # First move
    response = requests.post(
        f"{BASE_URL}/game/{game_id}",
        json={
            "uuid": str(game_id),
            "board": [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
        }
    )
    data = response.json()
    print("After first move:")
    print_board(data['board'])
    
    # Try to modify previous move
    cheating_board = [
        [0, 0, 0],
        [1, 1, 1],  # Changed computer's move!
        [0, 0, 0]
    ]
    
    print("Attempting to modify computer's move:")
    print_board(cheating_board)
    
    response = requests.post(
        f"{BASE_URL}/game/{game_id}",
        json={
            "uuid": str(game_id),
            "board": cheating_board
        }
    )
    
    print(f"Response Status: {response.status_code}")
    print(f"Error: {response.json()}")
    print()


def example_5_uuid_mismatch():
    """Example 5: UUID mismatch between URL and body."""
    print("=" * 60)
    print("EXAMPLE 5: UUID Mismatch")
    print("=" * 60)
    
    game_id_url = uuid4()
    game_id_body = uuid4()
    
    print(f"UUID in URL:  {game_id_url}")
    print(f"UUID in body: {game_id_body}")
    
    response = requests.post(
        f"{BASE_URL}/game/{game_id_url}",
        json={
            "uuid": str(game_id_body),
            "board": [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
        }
    )
    
    print(f"\nResponse Status: {response.status_code}")
    print(f"Error: {response.json()}")
    print()


def example_6_complete_game():
    """Example 6: Play a complete game."""
    print("=" * 60)
    print("EXAMPLE 6: Complete Game")
    print("=" * 60)
    
    game_id = uuid4()
    current_board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    
    moves = [
        (1, 1),  # Human: center
        (0, 1),  # Human: top-center
        (2, 1),  # Human: bottom-center
    ]
    
    for i, (row, col) in enumerate(moves, 1):
        print(f"\n--- Move {i} ---")
        
        # Make human move
        current_board[row][col] = 1
        
        response = requests.post(
            f"{BASE_URL}/game/{game_id}",
            json={
                "uuid": str(game_id),
                "board": current_board
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            current_board = data['board']
            print_board(current_board)
            
            if 'game_over' in data:
                print(f"🎉 Game Over! {data['winner']}")
                break
        else:
            print(f"Error: {response.json()}")
            break
    
    print()


def example_7_health_check():
    """Example 7: Health check endpoint."""
    print("=" * 60)
    print("EXAMPLE 7: Health Check")
    print("=" * 60)
    
    response = requests.get(f"{BASE_URL}/health")
    
    print(f"Response Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()


def example_8_concurrent_games():
    """Example 8: Multiple concurrent games."""
    print("=" * 60)
    print("EXAMPLE 8: Concurrent Games")
    print("=" * 60)
    
    # Start three different games
    games = []
    
    for i in range(3):
        game_id = uuid4()
        games.append(game_id)
        
        # Different starting positions
        positions = [
            [[0, 0, 0], [0, 1, 0], [0, 0, 0]],  # Center
            [[1, 0, 0], [0, 0, 0], [0, 0, 0]],  # Top-left
            [[0, 0, 0], [0, 0, 0], [0, 0, 1]],  # Bottom-right
        ]
        
        response = requests.post(
            f"{BASE_URL}/game/{game_id}",
            json={
                "uuid": str(game_id),
                "board": positions[i]
            }
        )
        
        print(f"\nGame {i+1} (ID: {game_id}):")
        print_board(response.json()['board'])
    
    print(f"\n✓ Successfully running {len(games)} concurrent games!")
    print()


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("TIC-TAC-TOE API USAGE EXAMPLES")
    print("=" * 60)
    print(f"\nAPI Base URL: {BASE_URL}")
    print("\nMake sure the server is running:")
    print("  python main.py")
    print("\n" + "=" * 60 + "\n")
    
    try:
        # Run all examples
        example_7_health_check()
        example_1_new_game()
        example_2_continue_game()
        example_3_invalid_move_multiple_cells()
        example_4_invalid_move_modify_previous()
        example_5_uuid_mismatch()
        example_6_complete_game()
        example_8_concurrent_games()
        
        print("=" * 60)
        print("ALL EXAMPLES COMPLETED!")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to API server")
        print("Make sure the server is running:")
        print("  python main.py")
        print()
