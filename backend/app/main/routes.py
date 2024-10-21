import os
import boto3
import certifi
from botocore.exceptions import NoCredentialsError
from app.extensions import db
from flask import request, jsonify, Blueprint
from .models import Friend
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from sqlalchemy import or_

load_dotenv()

# AWS S3 configuration
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME", default=None)
AWS_LOCATION = os.getenv("AWS_LOCATION", default=None)
AWS_S3_ACCESS_KEY_ID = os.getenv("AWS_S3_ACCESS_KEY_ID", default=None)
AWS_S3_SECRET_ACCESS_KEY = os.getenv("AWS_S3_SECRET_ACCESS_KEY", default=None)
AWS_S3_CUSTOM_DOMAIN = os.getenv("AWS_S3_CUSTOM_DOMAIN", default=None)
AWS_S3_ENDPOINT_URL = os.getenv("AWS_S3_ENDPOINT_URL", default=None)
AWS_S3_FILE_OVERWRITE = os.getenv("AWS_S3_FILE_OVERWRITE", default=None)

# Ensure all required environment variables are set
if not all(
    [
        AWS_STORAGE_BUCKET_NAME,
        AWS_S3_ACCESS_KEY_ID,
        AWS_S3_SECRET_ACCESS_KEY,
        AWS_S3_CUSTOM_DOMAIN,
        AWS_S3_ENDPOINT_URL,
    ]
):
    raise ValueError("One or more required environment variables are missing.")


s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_S3_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_S3_SECRET_ACCESS_KEY,
    endpoint_url=AWS_S3_ENDPOINT_URL,
    verify=certifi.where(),
)


main = Blueprint("main", __name__)


@main.route("/")
def home():
    api_url = (
        os.getenv("API_URL_PROD")
        if os.getenv("FLASK_ENV") == "production"
        else os.getenv("API_URL_DEV")
    )
    return f"""
    <div style="text-align: center; width:100%;">
        <h1>🚀</h1>
        <h1>DevFriendsHub</h1>
        <br>
        <p>Backend Flask Server</p>
        <br>
        <a href="{api_url}">Go to API Endpoint</a>
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
            file_path = f"{AWS_LOCATION}/{UPLOAD_FOLDER}/{filename}"
            try:
                s3_client.upload_fileobj(
                    file,
                    AWS_STORAGE_BUCKET_NAME,
                    file_path,
                    ExtraArgs={"ACL": "public-read"},
                )
                image_upload = f"https://{AWS_S3_CUSTOM_DOMAIN}/{file_path}"
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

        # Handle image upload and replace old image
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = f"{AWS_LOCATION}/{UPLOAD_FOLDER}/{filename}"

            # Delete old image if it exists
            if friend.image_upload:
                old_image_key = friend.image_upload.replace(
                    f"https://{AWS_S3_CUSTOM_DOMAIN}/", ""
                )
                try:
                    s3_client.delete_object(
                        Bucket=AWS_STORAGE_BUCKET_NAME, Key=old_image_key
                    )
                except NoCredentialsError:
                    return jsonify({"error": "AWS credentials not available"}), 500

            try:
                # Upload the new image
                s3_client.upload_fileobj(
                    file,
                    AWS_STORAGE_BUCKET_NAME,
                    file_path,
                    ExtraArgs={"ACL": "public-read"},
                )
                friend.image_upload = f"https://{AWS_S3_CUSTOM_DOMAIN}/{file_path}"
            except NoCredentialsError:
                return jsonify({"error": "AWS credentials not available"}), 500

        db.session.commit()
        return jsonify(friend.to_json()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@main.route("/api/friends/search", methods=["GET"])
def search_friend():
    try:
        query_param = request.args.get("query")

        # Build the query
        query = Friend.query
        if query_param:
            # Use or_ to search both name and role fields
            query = query.filter(
                or_(
                    Friend.name.ilike(f"%{query_param}%"),
                    Friend.role.ilike(f"%{query_param}%"),
                )
            )

        friends = query.all()
        result = [friend.to_json() for friend in friends]
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
