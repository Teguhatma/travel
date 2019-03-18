from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail


db = SQLAlchemy()
migrate = Migrate()
mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    from app.admin import admin
    app.register_blueprint(admin, url_prefix='/admin')
    from app.users import users
    app.register_blueprint(users)

    return app