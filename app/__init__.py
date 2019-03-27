from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_login import LoginManager
from flask_pagedown import PageDown
from flask_ckeditor import CKEditor


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
mail = Mail()
pagedown = PageDown()
ckeditor = CKEditor()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    login.login_view = "auth.login"
    pagedown.init_app(app)
    ckeditor.init_app(app)

    from app.admin import admin

    app.register_blueprint(admin, url_prefix="/admin")

    from app.users import users

    app.register_blueprint(users)

    from app.auth import auth

    app.register_blueprint(auth, url_prefix="/auth")

    return app
