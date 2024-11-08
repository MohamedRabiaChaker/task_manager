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
