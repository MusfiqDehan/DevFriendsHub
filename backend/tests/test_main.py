from app.main.models import Friend
from app.extensions import db


def test_create_friend(init_db):
    # Create a new friend
    new_friend = Friend(
        name="Charlie",
        role="Tester",
        description="QA Tester",
        gender="Non-binary",
        img_url="",
        image_upload="",
    )
    db.session.add(new_friend)
    db.session.commit()

    # Verify the friend was created
    friend = Friend.query.filter_by(name="Charlie").first()
    assert friend is not None
    assert friend.name == "Charlie"
    assert friend.role == "Tester"
    assert friend.description == "QA Tester"
    assert friend.gender == "Non-binary"


def test_update_friend(init_db):
    # Update an existing friend
    friend = Friend.query.filter_by(name="Alice").first()
    friend.role = "Lead Developer"
    db.session.commit()

    # Verify the friend was updated
    updated_friend = Friend.query.filter_by(name="Alice").first()
    assert updated_friend.role == "Lead Developer"


def test_view_friend(init_db):
    # View an existing friend
    friend = Friend.query.filter_by(name="Bob").first()
    assert friend is not None
    assert friend.name == "Bob"
    assert friend.role == "Designer"
    assert friend.description == "UI/UX Designer"
    assert friend.gender == "Male"


def test_delete_friend(init_db):
    # Delete an existing friend
    friend = Friend.query.filter_by(name="Alice").first()
    db.session.delete(friend)
    db.session.commit()

    # Verify the friend was deleted
    deleted_friend = Friend.query.filter_by(name="Alice").first()
    assert deleted_friend is None
