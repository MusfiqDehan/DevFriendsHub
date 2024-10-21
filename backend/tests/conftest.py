import pytest
import logging
from app import create_app
from app.extensions import db
from app.main.models import Friend


@pytest.fixture
def app():
    app = create_app("TestingConfig")
    logging.warning(f"Using database: {app.config['SQLALCHEMY_DATABASE_URI']}")
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def init_db(app):
    with app.app_context():
        # Create some initial data if needed
        friend1 = Friend(
            name="Alice",
            role="Developer",
            description="Backend Developer",
            gender="Female",
            img_url="",
            image_upload="",
        )
        friend2 = Friend(
            name="Bob",
            role="Designer",
            description="UI/UX Designer",
            gender="Male",
            img_url="",
            image_upload="",
        )
        db.session.add(friend1)
        db.session.add(friend2)
        db.session.commit()
        yield db
        db.drop_all()
