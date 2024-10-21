import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")


class DevelopmentConfig(Config):
    def __init__(self):
        print("Using development config")

    SQLALCHEMY_DATABASE_URI = os.getenv("DEV_DATABASE_URL", default=None)
    DEBUG = True


class ProductionConfig(Config):
    def __init__(self):
        print("Using production config")

    SQLALCHEMY_DATABASE_URI = os.getenv("PROD_DATABASE_URL", default=None)
    DEBUG = False


class TestingConfig(Config):
    def __init__(self):
        print("Using testing config")

    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URL", default=None)
    TESTING = True
    DEBUG = True
