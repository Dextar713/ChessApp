from flask import render_template, request, jsonify, flash
from flask_login import login_required

from chess import Chess

game_modes = [(1, 0), (2, 1), (3, 0), (3, 2), (5, 0), (5, 3), (10, 0), (10, 5), (15, 10), (30, 0), (30, 20)]
game = Chess()


@login_required
def play():
    return render_template('game_modes.html', modes=game_modes)


@login_required
def start_game():
    global game
    if request.method == 'GET':
        game = Chess()
        minutes = request.args.get('minutes')
        extra = request.args.get('extra')
        game.board.start_game()
        return render_template('board.html', game=game, mins=minutes, extra=extra)
    move_data = request.get_json()
    try:
        time_expired = move_data['time_expired']
    except KeyError:
        pass
    else:
        game.game_over = True
        if time_expired == 'White':
            game.winner = 'Black'
        else:
            game.winner = 'White'
        return jsonify({'success': False, 'game_over': game.game_over, 'winner': game.winner}), 200
    fig = game.board.get_fig(move_data['prevx'], move_data['prevy'])
    if fig is not None:
        fig = fig.my_copy()
    if game.game_over:
        res: bool = False
    else:
        res: bool = game.make_move(fig, move_data['curx'], move_data['cury'])
    return jsonify({'success': res, 'img': fig.image, 'game_over': game.game_over, 'winner': game.winner}), 200
