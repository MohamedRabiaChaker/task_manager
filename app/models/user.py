from datetime import datetime
from . import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __repr__(self):
        return f"<User {self.username}>"

    def set_password(self, password):
        """This function will hash the password (you can use Werkzeug's generate_password_hash)"""
        from werkzeug.security import generate_password_hash

        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """This function checks the hashed password against the user-provided password"""
        from werkzeug.security import check_password_hash

        return check_password_hash(self.password_hash, password)
