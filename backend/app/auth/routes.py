from app.extensions import db, bcrypt
from flask import request, jsonify, Blueprint
from .models import User
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, unset_jwt_cookies


main = Blueprint("main", __name__)

bcrypt = bcrypt(main)


@main.route("/api/auth/register", methods=["POST"])
def register():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
    new_user = User(
        username=data["username"],
        email=data["email"],
        password=hashed_password,
        role=data["role"],
    )
    db.session.add(new_user)
    db.session.commit()
    access_token = create_access_token(
        identity={
            "id": new_user.id,
            "username": new_user.username,
            "role": new_user.role,
        }
    )
    return jsonify(
        {"message": "User registered successfully", "access_token": access_token}
    )


@main.route("/api/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data["username"]).first()
    if user and bcrypt.check_password_hash(user.password, data["password"]):
        access_token = create_access_token(
            identity={"id": user.id, "username": user.username, "role": user.role}
        )
        return jsonify(
            access_token=access_token,
            user={"username": user.username, "role": user.role},
        )
    return jsonify({"message": "Invalid credentials"}), 401


@main.route("/api/auth/logout", methods=["POST"])
@jwt_required()
def logout():
    response = jsonify({"message": "Logout successful"})
    unset_jwt_cookies(response)
    return response
