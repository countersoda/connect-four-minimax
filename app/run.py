from typing import Dict
from flask import Flask, jsonify, request
from flask_cors import CORS
from uuid import uuid4, UUID
import numpy as np

from connect_four import ConnectFour

app = Flask(__name__)
CORS(app)
# A simple in-memory structure to store game state
games: Dict[str, ConnectFour] = {}

@app.route('/create_game', methods=['POST'])
def create_game():
    game_id = uuid4()
    game = ConnectFour()
    games[game_id] = game
    return jsonify({'game_id': game_id, 'board': np.flip(game.board, 0).tolist(), 'is_game_over': game.game_over})

@app.route('/take_turn/<game_id>', methods=['POST'])
def take_turn(game_id):
    print(games)
    if not games.get(UUID(game_id)):
        return jsonify({'error': 'Game not found'}), 404

    data = request.json
    column = data.get('column')
    game = games.get(UUID(game_id))
    valid = game.make_move(column)
    if not valid:
        return jsonify({'status': False, 'is_game_over': game.is_terminal_node(game.board)})

    return jsonify({'status': True, 'board': np.flip(game.board, 0).tolist(), 'is_game_over': game.game_over, 'winner': game.winner})

@app.route('/check_ai_move/<game_id>', methods=['GET'])
def check_ai_move(game_id):
    game = games.get(UUID(game_id))
    if not game:
        return jsonify({'error': 'Game not found'}), 404

    if game.turn != 1:  
        return jsonify({'status': False, 'board': np.flip(game.board, 0).tolist(), 'is_game_over': game.is_terminal_node(game.board)})

    ai_move = game.ai_move()
    return jsonify({'status': True, 'column': ai_move, 'board': np.flip(game.board, 0).tolist(), 'is_game_over': game.game_over, 'winner': game.winner})


if __name__ == '__main__':
    app.run(debug=True)
