from flask import Flask, render_template, url_for

from controllers.users import login_manager
from models import db
from routes.chess_game_bp import chess_game_bp
from routes.users_bp import users_bp

app = Flask(__name__)
app.config.from_object('config')
app.register_blueprint(chess_game_bp)
app.register_blueprint(users_bp)
login_manager.init_app(app)
db.create_tables()


@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(port=8000, debug=True)


