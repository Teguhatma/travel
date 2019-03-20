from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, BooleanField, PasswordField, SubmitField


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField()
    submit = SubmitField()