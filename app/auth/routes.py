import os

from . import blueprint
from .helpers import password_has_issue, validate_email, generate_uuid_integer
from ..models import User
from ..models import db

from flask import request, jsonify
import jwt


@blueprint.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username", None)
    password = data.get("password", None)
    email = data.get("email", None)
    if password is None or username is None or email is None:
        return (
            jsonify({"error": "Missing required fields"}),
            400,
        )

    if not validate_email(email):
        return (
            jsonify({"error": "invalid email format"}),
            400,
        )

    if User.query.filter_by(email=email).first() is not None:
        return jsonify({"error": "User with this email already exists"}), 400

    if password_has_issue(password):
        return (
            jsonify({"error": password_has_issue(password)}),
            400,
        )

    user = User(id=generate_uuid_integer(), username=username, email=email)
    user.set_password(password)
    try:
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "Successfully created user"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while registering the user"}), 500


@blueprint.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if "password" not in data or "email" not in data:
        return jsonify({"error": "Missing email or password"}), 400
    email = data["email"]
    password = data["password"]
    try:
        user: User = User.query.filter_by(email=email).first()
    except Exception as e:
        return jsonify({"error": "internal server error", "stack": str(e)}), 500

    if not user.check_password(password) or not user:
        return jsonify({"error": "passowrd and email combination is incorrect"}), 400

    SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    token = jwt.encode({"email": email, "id": user.id}, key=SECRET_KEY)
    return jsonify({"token": token, "message": "login successful"}), 200
