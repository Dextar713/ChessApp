from flask import Blueprint
from controllers.users import login, register, logout

users_bp = Blueprint('users_bp', __name__)
users_bp.route('/login', methods=['GET', 'POST'])(login)
users_bp.route('/register', methods=['GET', 'POST'])(register)
users_bp.route('/logout', methods=['GET'])(logout)
