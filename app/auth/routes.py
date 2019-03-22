from flask import url_for, render_template, redirect, request, flash
from app.auth import auth
from .forms import LoginForm
from flask_login import current_user, login_user, logout_user
from app.models import User
from app.admin import admin
from werkzeug.urls import url_parse


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if User is None or not user.check_password(form.password.data):
            flash('Invalid username and password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('admin.dashboard')
        return redirect(next_page)
    return render_template('login.html', title='Login', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
