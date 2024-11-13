import uuid
from functools import wraps

from ..models import User
import jwt
from flask import request, jsonify, current_app


def auth_protected(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = None

        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]

        if not token:
            return jsonify({"message": "Token not found"}), 401

        try:
            data = jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
            )

            user = User.query.filter_by(id=data["id"]).first()
            if not user:
                return jsonify({"message": "Invalid token"}), 401

        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Expired token, please refresh"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Provided token is not valid"}), 401

        return func(*args, **kwargs)

    return wrapper


def generate_uuid_integer():
    uuid_as_int = uuid.uuid4().int

    sql_integer_range = (2**31) - 1
    limited_uuid_int = uuid_as_int % sql_integer_range

    return limited_uuid_int


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


def extract_token_data():

    token = request.headers["Authorization"].split(" ")[1]
    data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])

    return data["id"], data["email"]
