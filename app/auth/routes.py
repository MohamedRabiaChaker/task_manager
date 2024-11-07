import uuid

from . import blueprint
from ..models import User
from ..models import db

from flask import request, jsonify


def validate_email(email):
    import re

    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None


def password_has_issue(password):
    import re

    if len(password) < 8:
        return "Password must be at least 8 characters long."

    if not re.search(r"[A-Z]", password):
        return "Password must contain at least one uppercase letter."

    if not re.search(r"[a-z]", password):
        return "Password must contain at least one lowercase letter."

    if not re.search(r"\d", password):
        return "Password must contain at least one digit."

    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return "Password must contain at least one special character."

    return False


def generate_uuid_integer():
    uuid_as_int = uuid.uuid4().int

    sql_integer_range = (2**31) - 1
    limited_uuid_int = uuid_as_int % sql_integer_range

    return limited_uuid_int


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
