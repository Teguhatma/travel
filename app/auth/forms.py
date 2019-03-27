from flask_wtf import FlaskForm
from app.models import User
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp
from wtforms import (
    StringField,
    BooleanField,
    PasswordField,
    SubmitField,
    ValidationError,
)


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField()
    submit = SubmitField("Login")


class PasswordResetRequestForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Length(1, 64), Email()])
    submit = SubmitField("Reset Password")


class PasswordResetForm(FlaskForm):
    password = PasswordField(
        "New Password",
        validators=[
            DataRequired(),
            EqualTo("password2", message="Password must match"),
        ],
    )
    password2 = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Reset Password")


class RegistrationForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(1, 64),
            Regexp(
                "^[A-Za-z][A-Za-z0-9_.]*$",
                0,
                "Usernames mush have only letters, numbers, dots or underscores",
            ),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            EqualTo("password2", message="Password must match."),
        ],
    )
    password2 = PasswordField("Confirm password", validators=[DataRequired()])
    submit = SubmitField("Register")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Email already registered.")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Username already in use.")


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField("Old password", validators=[DataRequired()])
    password = PasswordField(
        "New password",
        validators=[
            DataRequired(),
            EqualTo("password2", message="Password must be match."),
        ],
    )
    password2 = PasswordField("Confirm new password", validators=[DataRequired()])
    submit = SubmitField("Update Password")


class ChangeEmailForm(FlaskForm):
    email = StringField(
        "New Email", validators=[DataRequired(), Length(1, 64), Email()]
    )
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Update Email Address")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Email already registered")
