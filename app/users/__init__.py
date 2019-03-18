from flask import Blueprint

users = Blueprint('users', __name__, static_folder='static', template_folder='templates')

from app.users import routes