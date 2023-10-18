from flask import request, render_template, redirect, url_for, flash
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from sqlalchemy import or_
from werkzeug.security import generate_password_hash, check_password_hash

from forms.login_form import LoginForm
from forms.reg_form import RegForm
from models import db
from models.user import User

login_manager = LoginManager()
login_manager.login_view = '/login'
login_manager.login_message = 'Please log in to access this page!'


@login_manager.user_loader
def load_user(user_id):
    user = db.session.query(User).filter(User.id == int(user_id)).first()
    if user:
        return user
    return None


def login():
    login_form = LoginForm()
    if request.method == 'GET':
        return render_template('login.html', login_form=login_form)
    if login_form.validate_on_submit():
        email_or_name = login_form.username.data
        password = login_form.password.data
        if '@' in email_or_name:
            cur_user = db.session.query(User).filter(User.email == email_or_name).first()
        else:
            cur_user = db.session.query(User).filter(User.name == email_or_name).first()
        if cur_user is None:
            flash('No such user!')
            return render_template('login.html', login_form=login_form)
        if check_password_hash(cur_user.password, password):
            login_user(cur_user)
            return redirect(url_for('home'))
        else:
            flash('Wrong password!')
            return render_template('login.html', login_form=login_form)


def register():
    reg_form = RegForm()
    if request.method == 'GET':
        return render_template('register.html', reg_form=reg_form)
    if reg_form.validate_on_submit():
        name = reg_form.username.data
        password = reg_form.password.data
        email = reg_form.email.data
        prev_user = db.session.query(User).filter(or_(User.email == email, User.name == name)).first()
        if prev_user is not None:
            flash('This user already exists!')
            return render_template('register.html', reg_form=reg_form)
        hashed_password = generate_password_hash(
            method="pbkdf2:sha256",
            salt_length=7,
            password=password
        )
        new_user = User(
            name=name,
            password=hashed_password,
            email=email
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('home'))


@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
