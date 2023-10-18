from flask import Blueprint
from controllers.chess_game import play, start_game

chess_game_bp = Blueprint('chess_game_bp', __name__)
chess_game_bp.route('/play', methods=['GET', 'POST'])(play)
chess_game_bp.route('/game', methods=['GET', 'POST'])(start_game)
# chess_game_bp.route('/game', methods=['GET', 'POST'])(move)
