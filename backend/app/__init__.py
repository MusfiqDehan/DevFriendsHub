import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv

from .config import DevelopmentConfig, ProductionConfig

load_dotenv()

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # Choose the config based on the environment
    env = os.getenv("FLASK_ENV", "production")
    if env == "production":
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    CORS(app)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    from .main.routes import main

    app.register_blueprint(main)

    return app
