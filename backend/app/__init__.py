# import os
# from flask import Flask
# from flask_cors import CORS
# from dotenv import load_dotenv

# from .config import DevelopmentConfig, ProductionConfig

# load_dotenv()

# from .extensions import db


# def create_app():
#     app = Flask(__name__)

#     # Choose the config based on the environment
#     env = os.getenv("FLASK_ENV", "production")
#     if env == "production":
#         app.config.from_object(ProductionConfig)
#     else:
#         app.config.from_object(DevelopmentConfig)

#     CORS(app)

#     db.init_app(app)

#     with app.app_context():
#         db.create_all()

#     from .main.routes import main

#     app.register_blueprint(main)

#     return app


import os
import logging
from flask import Flask
from flask_cors import CORS
from .extensions import db
from .main.routes import main as main_bp

# from .auth.routes import auth
from .config import DevelopmentConfig, ProductionConfig, TestingConfig


def create_app(config_class=None):
    app = Flask(__name__)

    CORS(app)

    config_class = os.getenv("FLASK_ENV", config_class)

    if config_class == "DevelopmentConfig":
        app.config.from_object(DevelopmentConfig())
    elif config_class == "ProductionConfig":
        app.config.from_object(ProductionConfig())
    elif config_class == "TestingConfig":
        app.config.from_object(TestingConfig())
    else:
        app.config.from_object(DevelopmentConfig())

    # Initialize extensions
    db.init_app(app)

    # Create all tables
    with app.app_context():
        db.create_all()

    # Register Blueprints
    app.register_blueprint(main_bp)
    # app.register_blueprint(auth_bp)

    logging.warning(f"Using database: {app.config['SQLALCHEMY_DATABASE_URI']}")

    return app
