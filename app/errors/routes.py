from app.errors import errors
from flask import render_template
from app import db


@errors.app_errorhandler(404)
def not_found_error(e):
    return render_template("404.html"), 404


@errors.app_errorhandler(500)
def internal_error(e):
    db.session.rollback()
    return render_template("500.html"), 500
