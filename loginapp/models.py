from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from loginapp import db


# create 'users' table
class Users(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    registration_datetime = db.Column(db.DateTime, nullable=False, default=datetime.now())
    account_confirmed = db.Column(db.Boolean, nullable=False, default=False)

    # foreign key linking
    access_instances = db.relationship("UserAccess", backref="user")

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, pw):
        self.password_hash = generate_password_hash(pw)

    def verify_password(self, pw):
        return check_password_hash(self.password_hash, pw)

    def __repr__(self):
        return f"user_id={self.user_id}; email={self.email}; Name={self.last_name}, {self.first_name}"


# create 'user_access table
class UserAccess(db.Model):
    __tablename__ = "user_access"
    record_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    access_datetime = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __repr__(self):
        return f"user_id={self.user_id}; Name={self.user.last_name}, {self.user.first_name}"
