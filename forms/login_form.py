from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, EmailField


class LoginForm(FlaskForm):
    username = StringField(label='Username', validators=[validators.DataRequired('Enter your email or username')])
    password = StringField(label='Password', validators=[validators.DataRequired('Enter your password')])
    submit = SubmitField('Submit')

