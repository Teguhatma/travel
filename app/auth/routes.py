from flask import url_for, render_template, redirect, request, flash
from app.auth import auth
from .forms import (
    LoginForm,
    PasswordResetForm,
    PasswordResetRequestForm,
    RegistrationForm,
    ChangePasswordForm,
    ChangeEmailForm,
)
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from app.admin import admin
from app.email import send_email
from werkzeug.urls import url_parse
from app import db


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if current_user.is_authenticated:
        return redirect(url_for("admin.dashboard"))
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.verify_password(form.password.data):
            flash("Invalid username and password", "error")
            return redirect(url_for("auth.login"))
        login_user(user, remember=form.remember.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("admin.dashboard")
        return redirect(next_page)
    return render_template("login.html", title="Login", form=form)


@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/reset", methods=["GET", "POST"])
def password_reset_request():
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            send_email(
                user.email,
                "Reset Your Password",
                "email/reset_password",
                user=user,
                token=token,
            )
        flash("An email with instructions to reset your password has been sent to you.")
        return redirect(url_for("auth.login"))
    return render_template("reset_request_password.html", form=form)


@auth.route("/reset/<token>", methods=["GET", "POST"])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for("admin.dashboard"))
    form = PasswordResetForm()
    if form.validate_on_submit():
        if User.reset_password(token, form.password.data):
            db.session.commit()
            flash("Your password has been updated.")
            return redirect(url_for("auth.login"))
        else:
            return redirect(url_for("admin.dashboard"))
    return render_template("reset_password.html", form=form)


@auth.before_app_request
def before_request():
    if (
        current_user.is_authenticated
        and not current_user.confirmed
        and request.endpoint
        and request.blueprint != "auth"
        and request.endpoint != "static"
    ):
        return redirect(url_for("auth.unconfirmed"))


@auth.route("/unconfirmed")
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for("admin.index"))
    return render_template("unconfirmed.html")


@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            username=form.username.data,
            password=form.password.data,
        )
        db.session.add(user)
        db.session.commit()
        flash("You can now login.")
        token = user.generate_confirmation_token()
        send_email(
            user.email, "Confirm your account", "email/confirm", user=user, token=token
        )
        flash("A confirmation email has been sent to you by email.")
        return redirect(url_for("auth.login"))
    return render_template("register.html", form=form)


@auth.route("/confirm/<token>")
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for("admin.dashboard"))
    if current_user.confirm(token):
        db.session.commit()
        flash("You have confirmed your account. Thanks!")
    else:
        flash("The confirmation link is invalid or has expired.")
    return redirect(url_for("auth.login"))


@auth.route("/confirm")
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(
        current_user.email,
        "Confirm your account",
        "email/confirm",
        user=current_user,
        token=token,
    )
    flash("A new confirmation email has been sent to you by email.")
    return redirect(url_for("admin.dashboard"))


@auth.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash("Your password has been update.")
            return redirect(url_for("admin.dashboard"))
        else:
            flash("Invalid Password")
    return render_template("change_password.html", form=form)


@auth.route("/change-email", methods=["GET", "POST"])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data
            token = current_user.generate_email_change_token(new_email)
            send_email(
                new_email,
                "Confirm your email address",
                "email/change_email",
                user=current_user,
                token=token,
            )
            flash(
                "An email with instructions to confirm your new email address has been sent to you."
            )
            return redirect(url_for("admin.dashboard"))
        else:
            flash("Invalid email or password")
    return render_template("change_email.html", form=form)


@auth.route("/change-email/<token>")
@login_required
def change_email(token):
    if current_user.change_email(token):
        db.session.commit()
        flash("Your email address has been updated.")
    else:
        flash("Invalid request.")
    return redirect(url_for("admin.dashboard"))

