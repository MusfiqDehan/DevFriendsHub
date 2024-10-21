import os
import boto3
import certifi
from botocore.exceptions import NoCredentialsError
from app.extensions import db
from flask import request, jsonify, Blueprint
from ..models import Friend
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

load_dotenv()

main = Blueprint("main", __name__)

# AWS S3 configuration
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME", default=None)
AWS_LOCATION = os.getenv("AWS_LOCATION", default=None)
AWS_S3_ACCESS_KEY_ID = os.getenv("AWS_S3_ACCESS_KEY_ID", default=None)
AWS_S3_SECRET_ACCESS_KEY = os.getenv("AWS_S3_SECRET_ACCESS_KEY", default=None)
AWS_S3_CUSTOM_DOMAIN = os.getenv("AWS_S3_CUSTOM_DOMAIN", default=None)
AWS_S3_ENDPOINT_URL = os.getenv("AWS_S3_ENDPOINT_URL", default=None)
AWS_S3_FILE_OVERWRITE = os.getenv("AWS_S3_FILE_OVERWRITE", default=None)


s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_S3_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_S3_SECRET_ACCESS_KEY,
    endpoint_url=AWS_S3_ENDPOINT_URL,
    verify=certifi.where(),
)


@main.route("/")
def home():
    return """
  <div style="text-align: center; width:100%;">
    <h1>🚀</h1>
    <h1>DevFriendsHub</h1>
    <br>
    <p>Backend Flask Server</p>
    <br>
    <a href="https://devfriendshub.up.railway.app/api/friends">Go to API Endpoint</a>
  </div>
  """


# Get all friends
@main.route("/api/friends", methods=["GET"])
def get_friends():
    friends = Friend.query.all()
    result = [friend.to_json() for friend in friends]
    return jsonify(result)


UPLOAD_FOLDER = "profile-images"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@main.route("/api/friends", methods=["POST"])
def create_friend():
    try:
        data = request.form.to_dict()
        file = request.files.get("image_upload")

        # Validations
        required_fields = ["name", "role", "description", "gender"]
        for field in required_fields:
            if field not in data or not data.get(field):
                return jsonify({"error": f"Missing required field: {field}"}), 400

        name = data.get("name")
        role = data.get("role")
        description = data.get("description")
        gender = data.get("gender")

        # Handle image upload
        image_upload = None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            try:
                s3_client.upload_fileobj(
                    file,
                    AWS_STORAGE_BUCKET_NAME,
                    ExtraArgs={"ACL": "public-read"},
                )
                image_upload = f"https://{AWS_S3_CUSTOM_DOMAIN}/{filename}"
            except NoCredentialsError:
                return jsonify({"error": "AWS credentials not available"}), 500

        # Fetch avatar image based on gender if no image is uploaded
        img_url = None
        if not image_upload:
            if gender == "male":
                img_url = f"https://avatar.iran.liara.run/public/boy?username={name}"
            elif gender == "female":
                img_url = f"https://avatar.iran.liara.run/public/girl?username={name}"

        new_friend = Friend(
            name=name,
            role=role,
            description=description,
            gender=gender,
            img_url=img_url,
            image_upload=image_upload,
        )

        db.session.add(new_friend)
        db.session.commit()

        return jsonify(new_friend.to_json()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# Delete a friend
@main.route("/api/friends/<int:id>", methods=["DELETE"])
def delete_friend(id):
    try:
        friend = Friend.query.get(id)
        if friend is None:
            return jsonify({"error": "Friend not found"}), 404

        db.session.delete(friend)
        db.session.commit()
        return jsonify({"msg": "Friend deleted"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# Update a friend profile
@main.route("/api/friends/<int:id>", methods=["PATCH"])
def update_friend(id):
    try:
        friend = Friend.query.get(id)
        if friend is None:
            return jsonify({"error": "Friend not found"}), 404

        data = request.form.to_dict()
        file = request.files.get("image_upload")

        # Update fields
        friend.name = data.get("name", friend.name)
        friend.role = data.get("role", friend.role)
        friend.description = data.get("description", friend.description)
        friend.gender = data.get("gender", friend.gender)

        # Handle image upload
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            try:
                s3_client.upload_fileobj(
                    file,
                    AWS_STORAGE_BUCKET_NAME,
                    ExtraArgs={"ACL": "public-read"},
                )
                image_upload = f"https://{AWS_S3_CUSTOM_DOMAIN}/{filename}"
            except NoCredentialsError:
                return jsonify({"error": "AWS credentials not available"}), 500

            friend.image_upload = image_upload

        db.session.commit()
        return jsonify(friend.to_json()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
