from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'


def ingredient_emoji(type):
    emojis = {
        'vegetable': '🥦',
        'fruit':     '🍓',
        'legume':    '🥜',
        'fish':      '🐟',
        'meat':      '🥩',
        'dairy':     '🥛',
        'grain':     '🌾',
        'nut':       '🌰',
        'seed':      '🌱',
        'spice':     '🌿',
        'herb':      '🍃',
        'oil':       '🍶',
        'other':     '🍫',
        'protein':   '🥚',
    }
    return emojis.get(type, '🥗')

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app import models  # noqa: F401

    # Register template filter
    app.jinja_env.filters['ingredient_emoji'] = ingredient_emoji

    return app