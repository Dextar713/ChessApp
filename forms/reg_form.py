from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, EmailField, PasswordField


class RegForm(FlaskForm):
    email = EmailField(label='Email', validators=[validators.DataRequired('Enter your email'),
                                                  validators.Email()])
    username = StringField(label='Username', validators=[validators.Length(max=30),
                                                         validators.DataRequired('Enter your username')])
    password = PasswordField(label='Password', validators=[validators.Length(min=5),
                                                         validators.DataRequired('Enter your password')])
    submit = SubmitField('Submit')
